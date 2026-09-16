"""pgvector 검색 결과를 Context로 전달해 Ollama 답변을 생성합니다."""

from _ollama_rag import answer_question


QUESTION = "호텔을 당일 취소하면 환불받을 수 있나요?"


if __name__ == "__main__":
    result = answer_question(QUESTION)
    print("질문:", QUESTION)
    print("답변:", result["answer"])
    print("출처:", result["sources"])
