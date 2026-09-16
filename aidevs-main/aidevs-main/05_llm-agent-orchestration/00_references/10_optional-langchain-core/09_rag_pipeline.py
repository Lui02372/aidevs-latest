"""문서→검색→Context→답변의 RAG 경계를 API Key 없이 학습합니다."""

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


DOCUMENTS = [
    Document(page_content="부산 감천문화마을은 경사지가 많아 편한 신발이 좋습니다.", metadata={"id": "busan-1"}),
    Document(page_content="부산 지하철 1일권은 지하철 이동이 많은 일정에 유용합니다.", metadata={"id": "busan-2"}),
    Document(page_content="제주 일부 관광지는 버스 배차 간격이 길 수 있습니다.", metadata={"id": "jeju-1"}),
]


def retrieve(question: str) -> list[Document]:
    words = {word for word in question.replace("?", "").split() if len(word) >= 2}
    ranked = sorted(
        DOCUMENTS,
        key=lambda doc: sum(word in doc.page_content for word in words),
        reverse=True,
    )
    return ranked[:2]


def build_context(data: dict) -> dict:
    return {
        "question": data["question"],
        "documents": data["documents"],
        "context": "\n".join(doc.page_content for doc in data["documents"]),
    }


def grounded_mock_answer(data: dict) -> dict:
    return {
        "answer": f"검색 근거에 따르면 다음을 참고하세요: {data['context']}",
        "sources": [doc.metadata["id"] for doc in data["documents"]],
    }


chain = {
    "question": RunnablePassthrough(),
    "documents": RunnableLambda(retrieve),
} | RunnableLambda(build_context) | RunnableLambda(grounded_mock_answer)


if __name__ == "__main__":
    print(chain.invoke("부산에서 이동할 때 무엇을 준비해야 하나요?"))
