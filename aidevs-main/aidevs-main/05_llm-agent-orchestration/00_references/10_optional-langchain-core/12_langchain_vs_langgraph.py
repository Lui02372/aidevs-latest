"""같은 여행 분류 문제를 LCEL과 LangGraph로 구현해 역할 차이를 비교합니다."""

from typing import TypedDict

from langchain_core.runnables import RunnableBranch, RunnableLambda
from langgraph.graph import END, START, StateGraph


def classify(text: str) -> str:
    return "approval" if any(word in text for word in ("결제", "예약")) else "answer"


langchain_flow = RunnableLambda(classify) | RunnableBranch(
    (lambda route: route == "approval", RunnableLambda(lambda _: "사용자 승인이 필요합니다.")),
    RunnableLambda(lambda _: "정보 안내를 바로 생성합니다."),
)


class TravelState(TypedDict):
    request: str
    route: str
    result: str


def classify_node(state: TravelState) -> dict:
    return {"route": classify(state["request"])}


def approval_node(_: TravelState) -> dict:
    return {"result": "사용자 승인이 필요합니다."}


def answer_node(_: TravelState) -> dict:
    return {"result": "정보 안내를 바로 생성합니다."}


builder = StateGraph(TravelState)
builder.add_node("classify", classify_node)
builder.add_node("approval", approval_node)
builder.add_node("answer", answer_node)
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", lambda state: state["route"], {"approval": "approval", "answer": "answer"})
builder.add_edge("approval", END)
builder.add_edge("answer", END)
langgraph_flow = builder.compile()


if __name__ == "__main__":
    request = "부산 호텔을 예약하고 결제해 줘"
    print("LangChain:", langchain_flow.invoke(request))
    print("LangGraph:", langgraph_flow.invoke({"request": request, "route": "", "result": ""}))
