"""
[시나리오]
LLM Provider가 일시적으로 429 또는 503 오류를 반환합니다. 일시 오류만 제한적으로
재시도하고 최대 횟수를 넘으면 Fallback Provider로 넘깁니다. 인증 실패처럼 재시도로
해결되지 않는 오류는 즉시 중단합니다. 실제 대기 없이 판단 흐름만 확인합니다.
"""


RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def recovery_action(status_code: int, attempt: int, max_attempts: int = 3) -> str:
    if status_code not in RETRYABLE_STATUS_CODES:
        return "STOP"
    if attempt < max_attempts:
        return "RETRY_WITH_BACKOFF"
    return "FALLBACK_PROVIDER"


if __name__ == "__main__":
    for current_attempt in range(1, 5):
        print(f"503 / {current_attempt}회차 -> {recovery_action(503, current_attempt)}")
    print(f"401 -> {recovery_action(401, 1)}")
