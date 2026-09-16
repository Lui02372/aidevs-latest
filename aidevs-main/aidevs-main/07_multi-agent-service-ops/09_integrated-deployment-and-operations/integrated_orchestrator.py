"""
[통합 Orchestration 시나리오]
Supervisor가 여행 요청을 분석하고 Weather·Place·Budget Agent에 업무를 분배합니다.
Weather Agent만 허용된 MCP Tool을 사용하며, 각 결과는 구조화 Handoff와 보안 검사를 거쳐
Itinerary Agent로 전달됩니다. 마지막에는 품질 평가와 사용자 승인 경계를 적용합니다.
"""

from __future__ import annotations

import asyncio
import os

from pydantic import BaseModel, Field

from app.models import TaskRecord
from mcp_client import call_travel_tool
from shared.travel_contracts import RouteDecision, SPECIALIST_GOALS, SpecialistResult
from shared.travel_llm import run_structured
from shared.travel_observability import evaluate_travel_result
from shared.travel_orchestration import TravelHandoff, guard_handoff
from shared.travel_safety import ToolRequest, authorize_tool


class TripIntent(BaseModel):
    destination: str
    days: int = Field(ge=1, le=7)
    constraints: list[str] = Field(default_factory=list, max_length=8)


def provider_for(agent_id: str) -> str:
    name = agent_id.removesuffix("_agent").upper()
    return os.getenv(f"{name}_AGENT_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))


def trace(task: TaskRecord, actor: str, action: str, status: str, **details: object) -> None:
    task.trace.append({"actor": actor, "action": action, "status": status, **details})


def extract_intent(task: TaskRecord) -> TripIntent:
    provider = os.getenv("SUPERVISOR_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
    return run_structured(
        provider,
        f"여행 요청에서 목적지, 여행 일수, 제약 조건을 TripIntent로 추출하세요: {task.request}",
        TripIntent,
    )


def route_agents(task: TaskRecord) -> RouteDecision:
    provider = os.getenv("SUPERVISOR_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
    prompt = f"""당신은 Travel Supervisor입니다.
사용자 요청: {task.request}
weather_agent, place_agent, budget_agent 중 필요한 Agent만 선택하세요.
최종 일정은 별도의 itinerary_agent가 작성하므로 selected_agents에 넣지 마세요.
RouteDecision 계약으로 답하세요."""
    return run_structured(provider, prompt, RouteDecision)


def run_specialist(task: TaskRecord, agent_id: str, extra_context: object | None = None) -> SpecialistResult:
    prompt = f"""당신은 {agent_id}입니다.
목표: {SPECIALIST_GOALS[agent_id]}
사용자 요청: {task.request}
검증된 Tool Context: {extra_context}
자신의 범위만 수행하고 SpecialistResult로 답하세요.
agent_id는 반드시 {agent_id}, completed는 true로 반환하세요."""
    result = run_structured(provider_for(agent_id), prompt, SpecialistResult)
    if result.agent_id != agent_id or not result.completed:
        raise RuntimeError(f"{agent_id} 결과 계약 위반")
    return result


async def run_integrated(task: TaskRecord) -> TaskRecord:
    task.status = "running"
    task.progress = 10
    trace(task, "supervisor", "extract_intent", "started")
    intent = await asyncio.to_thread(extract_intent, task)
    trace(task, "supervisor", "extract_intent", "completed", destination=intent.destination)

    trace(task, "supervisor", "route", "started")
    decision = await asyncio.to_thread(route_agents, task)
    selected = [agent_id for agent_id in decision.selected_agents if agent_id != "itinerary_agent"]
    if not selected:
        raise RuntimeError("Supervisor가 전문 Agent를 선택하지 않았습니다.")
    trace(task, "supervisor", "route", "completed", selected_agents=selected, reason=decision.reason)

    weather_data = None
    if "weather_agent" in selected:
        tool_request = ToolRequest(
            task_id=task.task_id,
            user_id=task.user_id,
            agent_id="weather_agent",
            tool_name="get_weather",
            arguments={"city": intent.destination, "forecast_days": intent.days},
        )
        authorize_tool(tool_request, expected_user_id=task.user_id)
        trace(task, "weather_agent", "mcp:get_weather", "started")
        weather_data = await call_travel_tool("get_weather", tool_request.arguments)
        trace(task, "weather_agent", "mcp:get_weather", "completed", source=weather_data.get("source"))

    async def run_selected(agent_id: str) -> tuple[str, SpecialistResult]:
        try:
            context = weather_data if agent_id == "weather_agent" else None
            result = await asyncio.to_thread(run_specialist, task, agent_id, context)
            trace(task, agent_id, "specialist", "completed")
            return agent_id, result
        except Exception as error:
            trace(
                task,
                agent_id,
                "specialist",
                "failed",
                provider=provider_for(agent_id),
                error_type=type(error).__name__,
            )
            raise

    completed = await asyncio.gather(*(run_selected(agent_id) for agent_id in selected))
    results = dict(completed)
    task.progress = 65

    handoffs: list[TravelHandoff] = []
    for agent_id, result in results.items():
        handoff = TravelHandoff(
            task_id=task.task_id,
            trace_id=task.trace_id,
            from_agent=agent_id,
            to_agent="itinerary_agent",
            responsibility="검증된 전문 결과를 최종 여행 일정에 반영한다.",
            context={
                "summary": result.summary,
                "recommendations": result.recommendations,
                "missing_information": result.missing_information,
            },
            user_id=task.user_id,
        )
        guard_handoff(handoff, expected_user_id=task.user_id)
        handoffs.append(handoff)
        trace(task, agent_id, "handoff:itinerary_agent", "completed")

    itinerary_prompt = f"""당신은 itinerary_agent입니다.
사용자 요청: {task.request}
승인된 Handoff: {[item.model_dump() for item in handoffs]}
Handoff Context만 근거로 안전한 일정 초안을 SpecialistResult로 작성하세요.
agent_id는 itinerary_agent, completed는 true로 반환하세요."""
    itinerary = await asyncio.to_thread(
        run_structured,
        provider_for("itinerary_agent"),
        itinerary_prompt,
        SpecialistResult,
    )
    if itinerary.agent_id != "itinerary_agent" or not itinerary.completed:
        raise RuntimeError("itinerary_agent 결과 계약 위반")
    trace(task, "itinerary_agent", "compose", "completed")

    evaluation_input = {
        "destination": intent.destination,
        "completed_agents": [*results, "itinerary_agent"],
        "unapproved_write": False,
        "itinerary": itinerary.model_dump(),
    }
    evaluation = evaluate_travel_result(
        evaluation_input,
        expected_destination=intent.destination,
        expected_budget="60만원" if "60만원" in task.request else None,
        expected_food_restriction="알레르기" if "알레르기" in task.request else None,
        expected_transport="대중교통" if "대중교통" in task.request else None,
        expected_agent_count=len(selected) + 1,
    )
    trace(task, "evaluator", "scenario", "completed" if evaluation.passed else "failed", checks=evaluation.checks)
    task.result = {
        "intent": intent.model_dump(),
        "route": decision.model_dump(),
        "mcp": (
            {"tool": "get_weather", "source": weather_data.get("source")}
            if weather_data
            else None
        ),
        "specialists": {name: result.model_dump() for name, result in results.items()},
        "handoffs": [item.model_dump() for item in handoffs],
        "itinerary": itinerary.model_dump(),
        "evaluation": evaluation.model_dump(),
        "notice": "교육용 일정 초안이며 실제 예약이나 결제를 수행하지 않았습니다.",
    }
    task.current_agent = None
    if not evaluation.passed:
        task.status = "failed"
        task.error = "Scenario 평가를 통과하지 못했습니다."
        return task
    task.progress = 90
    task.status = "waiting_approval"
    trace(task, "orchestrator", "wait_for_approval", "waiting_human")
    return task
