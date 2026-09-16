"""07~08 예제가 공유하는 최소 Ollama RAG 함수입니다."""

import os

import httpx

from _pgvector_store import OLLAMA_BASE_URL, similarity_search


COLLECTION = "rag_lesson"
CHAT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def answer_question(question: str) -> dict:
    results = similarity_search(question, collection=COLLECTION, top_k=3)
    if not results:
        return {"answer": "관련 문서를 찾지 못했습니다.", "sources": []}

    context = "\n".join(
        f"[{item['source']}] {item['content']}" for item in results
    )
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": "Context만 사용해 한국어로 답하고 출처를 표시하세요.",
                },
                {"role": "user", "content": f"질문: {question}\n\nContext:\n{context}"},
            ],
        },
        timeout=120,
    )
    response.raise_for_status()
    return {
        "answer": response.json()["message"]["content"],
        "sources": sorted({item["source"] for item in results}),
    }
