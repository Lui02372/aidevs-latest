"""고정 System 지침, 대화 기록, 현재 질문을 서로 다른 영역으로 구성합니다."""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "여행 상담가입니다. 사용자가 말하지 않은 예약을 확정하지 마세요."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)


if __name__ == "__main__":
    history = [HumanMessage(content="부산에 갈 거예요."), AIMessage(content="기간을 알려주세요.")]
    value = prompt.invoke({"history": history, "question": "2박이면 충분할까요?"})
    for message in value.to_messages():
        print(f"{message.type}: {message.content}")
