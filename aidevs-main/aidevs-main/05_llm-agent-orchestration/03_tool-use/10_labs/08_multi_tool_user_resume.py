"""Lab 08 — Tool 두 개 실행 후 사용자에게 질문하고 세 번째 Tool을 실행합니다.

한 번의 함수 호출이 한 번의 사용자 대화를 나타냅니다.

첫 번째 Cycle:
    날씨 조회 → 관광지 검색 → 사용자 선택 질문 → waiting_user

두 번째 Cycle:
    사용자 답변 검증 → 일정 등록 Tool → completed

외부 API나 DB 대신 고정된 mock 데이터를 사용합니다. 실제 Agent에서는 LLM이
다음 행동과 arguments를 제안할 수 있지만, Tool 허용 여부와 사용자 선택값은
Backend가 다시 검증해야 합니다.
"""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class CityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    city: str = Field(min_length=1)


class AddItineraryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    city: str = Field(min_length=1)
    place: str = Field(min_length=1)


class AgentState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    city: str
    weather_result: dict[str, Any] | None = None
    attraction_result: dict[str, Any] | None = None
    selected_place: str | None = None
    itinerary_result: dict[str, Any] | None = None
    status: Literal["ready", "waiting_user", "completed", "stopped"] = "ready"
    trace: list[dict[str, Any]] = Field(default_factory=list)


# 외부 서비스 대신 언제 실행해도 같은 결과를 얻는 학습용 mock 데이터입니다.
WEATHER = {
    "서울": {"condition": "맑음", "temperature_c": 24},
    "제주": {"condition": "비", "temperature_c": 21},
}
ATTRACTIONS = {
    "서울": ["경복궁", "서울숲"],
    "제주": ["비자림", "제주현대미술관"],
}


def get_weather(arguments: dict[str, Any]) -> dict[str, Any]:
    """Tool 1: 도시의 mock 날씨를 조회합니다."""
    args = CityInput.model_validate(arguments)
    data = WEATHER.get(args.city)
    return {"found": data is not None, "city": args.city, **(data or {}), "source": "mock-weather"}


def search_attractions(arguments: dict[str, Any]) -> dict[str, Any]:
    """Tool 2: 도시의 mock 관광지를 검색합니다."""
    args = CityInput.model_validate(arguments)
    places = ATTRACTIONS.get(args.city, [])
    return {"found": bool(places), "city": args.city, "places": places, "source": "mock-attractions"}


def add_to_itinerary(arguments: dict[str, Any]) -> dict[str, Any]:
    """Tool 3: 검증된 장소를 mock 일정에 추가합니다."""
    args = AddItineraryInput.model_validate(arguments)
    return {
        "status": "added",
        "city": args.city,
        "place": args.place,
        "message": f"{args.place}을(를) 여행 일정에 추가했습니다.",
    }


TOOL_REGISTRY = {
    "get_weather": (CityInput, get_weather),
    "search_attractions": (CityInput, search_attractions),
    "add_to_itinerary": (AddItineraryInput, add_to_itinerary),
}


def execute_allowed_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """등록된 Tool과 올바른 arguments만 실행합니다."""
    tool_spec = TOOL_REGISTRY.get(tool_name)
    if tool_spec is None:
        return {"success": False, "error": {"code": "TOOL_NOT_ALLOWED"}}

    input_model, function = tool_spec
    try:
        validated = input_model.model_validate(arguments)
        return {"success": True, "data": function(validated.model_dump())}
    except ValidationError as error:
        return {"success": False, "error": {"code": "VALIDATION_ERROR", "details": error.errors()}}


def record_tool_result(state: AgentState, step: int, tool_name: str, result: dict[str, Any]) -> bool:
    state.trace.append({"step": step, "stage": "tool_result", "tool": tool_name, "data": result})
    if result["success"]:
        return True
    state.status = "stopped"
    return False


def collect_information(state: AgentState) -> dict[str, Any] | None:
    """첫 Cycle에서 두 조회 Tool을 순서대로 실행합니다."""
    weather = execute_allowed_tool("get_weather", {"city": state.city})
    if not record_tool_result(state, 1, "get_weather", weather):
        return {"status": "error", "error": weather["error"], "trace": state.trace.copy()}
    state.weather_result = weather["data"]

    attractions = execute_allowed_tool("search_attractions", {"city": state.city})
    if not record_tool_result(state, 2, "search_attractions", attractions):
        return {"status": "error", "error": attractions["error"], "trace": state.trace.copy()}
    state.attraction_result = attractions["data"]
    return None


def choose_place_from_message(message: str, candidates: list[str]) -> str | None:
    """실제 LLM의 선택값 추출을 단순한 문자열 규칙으로 흉내 냅니다."""
    return next((place for place in candidates if place in message), None)


def run_agent_cycle(state: AgentState, user_message: str) -> dict[str, Any]:
    """현재 State에 따라 조회, 사용자 대기 또는 일정 등록을 수행합니다."""
    state.trace.append({"stage": "user_message", "data": user_message})

    if state.weather_result is None or state.attraction_result is None:
        error = collect_information(state)
        if error is not None:
            return error

        candidates = state.attraction_result["places"]
        state.status = "waiting_user"
        state.trace.append({"step": 3, "stage": "ask_user", "candidates": candidates})
        return {
            "status": "waiting_user",
            "weather": state.weather_result,
            "candidates": candidates,
            "follow_up_question": f"추천 장소는 {', '.join(candidates)}입니다. 어디를 일정에 추가할까요?",
            "termination_reason": "needs_user_input",
            "trace": state.trace.copy(),
        }

    if state.status != "waiting_user":
        return {
            "status": state.status,
            "message": "이미 완료되었거나 중단된 실행입니다.",
            "termination_reason": "already_finished",
            "trace": state.trace.copy(),
        }

    candidates = state.attraction_result["places"]
    selected_place = choose_place_from_message(user_message, candidates)
    if selected_place is None:
        state.trace.append({"stage": "invalid_user_choice", "data": user_message})
        return {
            "status": "waiting_user",
            "candidates": candidates,
            "follow_up_question": f"{', '.join(candidates)} 중 하나를 선택해 주세요.",
            "termination_reason": "needs_valid_user_input",
            "trace": state.trace.copy(),
        }

    # 사용자가 선택한 값이 이전 Tool Result의 후보에 있는지 Backend가 다시 확인합니다.
    if selected_place not in candidates:
        state.status = "stopped"
        return {"status": "error", "error": {"code": "PLACE_NOT_ALLOWED"}, "trace": state.trace.copy()}

    state.selected_place = selected_place
    itinerary = execute_allowed_tool(
        "add_to_itinerary",
        {"city": state.city, "place": selected_place},
    )
    if not record_tool_result(state, 4, "add_to_itinerary", itinerary):
        return {"status": "error", "error": itinerary["error"], "trace": state.trace.copy()}

    state.itinerary_result = itinerary["data"]
    state.status = "completed"
    return {
        "status": "completed",
        "result": state.itinerary_result,
        "termination_reason": "completed",
        "trace": state.trace.copy(),
    }


if __name__ == "__main__":
    agent_state = AgentState(city="제주")

    print("\n사용자: 제주 여행 장소를 추천해 줘")
    first_cycle = run_agent_cycle(agent_state, "제주 여행 장소를 추천해 줘")
    print(first_cycle["follow_up_question"])

    print("\n사용자: 제주현대미술관을 추가해 줘")
    second_cycle = run_agent_cycle(agent_state, "제주현대미술관을 추가해 줘")
    print(second_cycle["result"]["message"])

    print("\n실행 Trace:")
    for item in second_cycle["trace"]:
        print("-", item)
