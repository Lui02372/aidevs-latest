"""같은 질문의 첫 답변을 Redis에 저장하고 두 번째 질문에서 재사용합니다."""

from _ollama_rag import CHAT_MODEL, answer_question
from _pgvector_store import EMBEDDING_MODEL
from _redis_cache import JsonCache, cache_key


CACHE_NAMESPACE = "simple-rag-answer:v1"
QUESTION = "호텔을 당일 취소하면 환불받을 수 있나요?"


def ask(question: str, cache: JsonCache) -> dict:
    key = cache_key(CACHE_NAMESPACE, {
        "question": question,
        "embedding_model": EMBEDDING_MODEL,
        "chat_model": CHAT_MODEL,
    })
    cached = cache.get(key)
    if cached:
        return {**cached, "cache_hit": True, "ttl": cache.ttl(key)}

    result = answer_question(question)
    saved = cache.set(key, result)
    return {**result, "cache_hit": False, "cache_saved": saved}


if __name__ == "__main__":
    redis_cache = JsonCache()
    redis_cache.delete_namespace(CACHE_NAMESPACE)

    first = ask(QUESTION, redis_cache)
    print("1차 질문: Redis MISS → RAG 실행")
    print(first)

    second = ask(QUESTION, redis_cache)
    if second["cache_hit"]:
        print("\n2차 동일 질문: Redis HIT → 저장된 답변 반환")
    else:
        print("\n2차 동일 질문: Redis 저장 실패 → RAG 다시 실행")
    print(second)
