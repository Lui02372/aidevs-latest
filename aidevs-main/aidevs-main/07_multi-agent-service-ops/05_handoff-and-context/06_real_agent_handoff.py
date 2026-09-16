"""Lab 05-06: 실제 날씨와 두 LLM으로 Handoff 전체 흐름을 실행합니다.

Open-Meteo 예보를 Gemini Weather Agent가 해석해 Handoff를 제안하고, Python Guard를
통과한 최소 Context만 Gemma Itinerary Agent가 받아 일정을 작성합니다.
"""

import json

import httpx

from handoff_models import HandoffEnvelope, HandoffState, WeatherHandoffDecision
from handoff_registry import validate_handoff
from handoff_service import transfer_ownership_agent
from shared.travel_contracts import ItineraryResult
from shared.travel_llm import run_with_metadata


def get_live_weather() -> dict:
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 35.1796, "longitude": 129.0756,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "Asia/Seoul", "forecast_days": 3,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["daily"]


def weather_agent(weather: dict) -> dict:
    prompt = f"""당신은 weather_agent입니다.
Open-Meteo 실제 결과: {json.dumps(weather, ensure_ascii=False)}
부산 2박 3일 일정에 날씨 반영이 필요하면 itinerary_agent로 Handoff를 제안하세요.
handoff_context에는 destination, days, weather_summary, weather_cautions만 포함하세요.
WeatherHandoffDecision 계약으로 반환하세요."""
    return run_with_metadata("gemini", prompt, WeatherHandoffDecision)


def itinerary_agent(handoff: HandoffEnvelope) -> dict:
    prompt = f"""당신은 itinerary_agent입니다.
검증과 수락을 마친 Handoff의 책임만 수행하세요.
Handoff: {handoff.model_dump_json()}
ItineraryResult 계약으로 부산 3일 일정을 반환하세요."""
    return run_with_metadata("gemma", prompt, ItineraryResult)


if __name__ == "__main__":
    decision = weather_agent(get_live_weather())
    print("=== Gemini Weather Agent ===")
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    if decision["result"] is None or not decision["result"]["handoff_required"]:
        print("Handoff가 생성되지 않아 종료합니다.")
    else:
        data = decision["result"]
        proposal = HandoffEnvelope(
            handoff_id="handoff-live-001", task_id="travel-001", trace_id="trace-001",
            from_agent="weather_agent", to_agent=data["target_agent"],
            responsibility=data["responsibility"], context=data["handoff_context"],
            user_id="user-101",
        )
        state = HandoffState(task_id="travel-001", owner_agent="weather_agent")
        validated = validate_handoff(proposal, expected_user_id="user-101")
        result = itinerary_agent(validated)
        print("\n=== Gemma Itinerary Agent ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result["result"]:
            state, accepted = transfer_ownership_agent(state, proposal, target_accepted=True)
            accepted = accepted.model_copy(update={"status": "completed"})
            state.status = "completed"
            state.events.append({"event": "target_agent_completed", "owner": state.owner_agent})
        else:
            accepted = validated.model_copy(update={"status": "failed"})
            state.status = "failed"
            state.events.append({"event": "target_agent_failed", "owner": state.owner_agent})
            # 목표 Agent가 계약 결과를 반환하지 못했으므로 원래 책임자를 유지합니다.
            state.owner_agent = proposal.from_agent
        print("\n최종 Handoff 상태:", accepted.status)
        print("최종 책임 Agent:", state.owner_agent)
        print("Event:", state.events)
