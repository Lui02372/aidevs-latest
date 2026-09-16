"""요청 위험도에 따라 정보 안내와 승인용 Prompt를 선택합니다."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda


info_prompt = ChatPromptTemplate.from_messages(
    [("system", "읽기 전용 여행 정보를 간결하게 안내하세요."), ("human", "{request}")]
)
action_prompt = ChatPromptTemplate.from_messages(
    [("system", "예약·결제는 실행하지 말고 필요한 승인 정보와 예상 영향을 나열하세요."),
     ("human", "{request}")]
)

classify = RunnableLambda(
    lambda request: {"request": request, "requires_approval": any(word in request for word in ("예약", "결제", "취소"))}
)
route = RunnableBranch(
    (lambda data: data["requires_approval"], action_prompt),
    info_prompt,
)
chain = classify | route


if __name__ == "__main__":
    for request in ("부산 날씨를 알려줘", "부산 호텔을 예약해 줘"):
        print(f"\n요청: {request}")
        print(chain.invoke(request).to_string())
