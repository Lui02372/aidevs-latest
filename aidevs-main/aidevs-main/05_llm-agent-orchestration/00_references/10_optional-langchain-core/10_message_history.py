"""RunnableWithMessageHistory로 session별 대화 기록을 분리합니다."""

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory


stores: dict[str, InMemoryChatMessageHistory] = {}


def get_history(session_id: str) -> InMemoryChatMessageHistory:
    return stores.setdefault(session_id, InMemoryChatMessageHistory())


def mock_chat(messages):
    human_messages = [message.content for message in messages if message.type == "human"]
    return AIMessage(content=f"현재까지 사용자 질문은 {len(human_messages)}개입니다: {human_messages[-1]}")


chat = RunnableWithMessageHistory(RunnableLambda(mock_chat), get_history)


if __name__ == "__main__":
    config = {"configurable": {"session_id": "traveler-1"}}
    print(chat.invoke("부산에 가고 싶어요.", config=config).content)
    print(chat.invoke("며칠이 적당할까요?", config=config).content)
    print("저장된 메시지 수:", len(stores["traveler-1"].messages))
