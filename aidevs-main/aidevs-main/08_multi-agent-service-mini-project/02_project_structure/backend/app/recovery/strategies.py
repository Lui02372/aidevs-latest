"""장애 유형별 복구 전략을 선택합니다.

초기 프로젝트에서는 실제 서버 재시작 같은 위험한 작업을 하지 않고,
어떤 전략을 선택할지 시뮬레이션하는 방식으로 시작합니다.
"""


def choose_recovery_strategy(failure_type: str) -> str:
    """장애 유형에 맞는 복구 전략 이름을 반환합니다."""

    strategies = {
        "network_timeout": "retry_with_backoff",
        "api_5xx": "fallback_response",
        "prompt_injection": "block_request",
        "unknown_failure": "manual_review",
    }
    return strategies.get(failure_type, "manual_review")
