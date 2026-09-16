"""PromptTemplate과 OutputParser의 책임을 API Key 없이 확인합니다.

관찰: prompt는 입력을 문자열로 만들고 parser는 모델 문자열을 애플리케이션 값으로
바꿉니다. 실제 모델 대신 RunnableLambda를 끼워 각 경계를 눈으로 확인합니다.
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import BaseMessage


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{audience}에게 여행지를 한 문장으로 추천하세요."),
        ("human", "관심사: {interest}"),
    ]
)


def mock_chat_model(prompt_value) -> BaseMessage:
    """ChatPromptValue를 받은 모델처럼 AIMessage를 반환합니다."""
    from langchain_core.messages import AIMessage

    rendered = prompt_value.to_messages()[-1].content
    return AIMessage(content=f"제주를 추천합니다. 입력 내용은 '{rendered}'입니다.")


chain = prompt | RunnableLambda(mock_chat_model) | StrOutputParser()


if __name__ == "__main__":
    result = chain.invoke({"audience": "초보 여행자", "interest": "바다와 산책"})
    print(result)
