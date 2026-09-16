"""
[시나리오]
Multi-Agent 실행 중 서로 다른 네 종류의 오류가 발생했습니다. Orchestrator Agent는
모든 오류를 무조건 Retry하지 않고 오류 성격에 맞는 다음 행동을 선택합니다.

1. TimeoutError는 제한적으로 Retry합니다.
2. 입력 누락 ValueError는 계획과 입력을 다시 구성합니다.
3. PermissionError는 보안 위반이므로 즉시 차단합니다.
4. 자동 복구할 수 없는 오류는 사람에게 전달합니다.

[기대 결과]
오류마다 retry, replan, block, human이 각각 출력됩니다.

[학습 포인트]
권한 오류를 Retry하면 보안 정책을 반복 공격하게 됩니다. 실패 유형을 분류한 뒤에만
재시도 여부를 결정해야 합니다. 이 Lab은 결정적 정책 예제로 실제 LLM을 사용하지 않습니다.
"""

from shared.travel_observability import classify_failure


failures = [
    TimeoutError("날씨 서비스 응답 지연"),
    ValueError("일정 Agent에 필요한 입력 누락"),
    PermissionError("허용되지 않은 Tool"),
    RuntimeError("원인을 자동으로 복구할 수 없음"),
]

for error in failures:
    print(type(error).__name__, "->", classify_failure(error))
