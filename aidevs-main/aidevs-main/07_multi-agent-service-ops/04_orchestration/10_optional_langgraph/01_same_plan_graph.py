"""
[시나리오]
앞의 일반 Python Orchestration에서 여행 정보를 조사하고, 세 전문 Agent의 결과를 모은 뒤,
최종 일정을 만드는 순차 Workflow를 살펴봤습니다. 이번에는 Agent 역할이나 실행 순서를
새로 설계하지 않고 이미 이해한 흐름을 LangGraph의 State, Node, Edge로 옮깁니다.

research Node는 날씨·장소·예산 조사 결과를 State에 기록합니다. join Node는 필요한 결과가
모두 준비됐는지 검사하고, itinerary Node는 최종 일정 생성 단계를 기록합니다. START와
END를 사용해 Workflow 시작과 종료를 명확히 표현합니다. 이 최소 예제는 조건 분기나 반복을
추가하기 전에 일반 Python 함수와 Graph 구성 요소의 대응 관계를 이해하는 것이 목표입니다.
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    trace: list[str]


def research(state: State) -> State:
    return {"trace": state["trace"] + ["weather", "place", "budget"]}


def join(state: State) -> State:
    required = {"weather", "place", "budget"}
    if not required.issubset(state["trace"]):
        raise RuntimeError("전문 Agent 결과가 모두 준비되지 않았습니다.")
    return {"trace": state["trace"] + ["joined"]}


def itinerary(state: State) -> State:
    return {"trace": state["trace"] + ["itinerary"]}


builder = StateGraph(State)
builder.add_node("research", research)
builder.add_node("join", join)
builder.add_node("itinerary", itinerary)
builder.add_edge(START, "research")
builder.add_edge("research", "join")
builder.add_edge("join", "itinerary")
builder.add_edge("itinerary", END)

print(builder.compile().invoke({"trace": []}))
