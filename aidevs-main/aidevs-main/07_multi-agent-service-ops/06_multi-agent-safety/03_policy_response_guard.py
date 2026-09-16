"""
[시나리오]
여러 Worker Agent의 결과를 합친 뒤, 답변을 사용자에게 보내기 직전입니다.

1. 정상 초안은 추천 일정과 예상 비용만 설명합니다.
2. 위험 초안은 실제로 실행하지 않은 예약·결제를 완료했다고 주장합니다.
3. 또 다른 위험 초안은 내부 비밀값 이름과 값을 포함합니다.
4. Response Guard Agent가 Policy를 검사하고 통과한 답변만 반환합니다.

[기대 결과]
- 근거 범위 안의 정상 답변은 허용됩니다.
- 허위 실행 주장이나 민감 정보가 포함된 답변은 차단됩니다.

[학습 포인트]
입력이 안전해도 LLM 출력이 항상 안전한 것은 아닙니다. 응답은 사용자에게 보내기
직전에 별도로 검증하며, 차단된 답변은 그대로 노출하지 않습니다.
"""

from dataclasses import dataclass

from security_registry import load_security_policies


@dataclass(frozen=True)
class ResponseInspection:
    allowed: bool
    reason: str


def response_guard_agent(response_text: str, metadata: dict[str, str]) -> ResponseInspection:
    response_policy = load_security_policies()["response"]

    for phrase in response_policy["blocked_phrases"]:
        if phrase in response_text:
            return ResponseInspection(False, f"실행되지 않은 작업을 주장합니다: {phrase}")
    for sensitive_key in response_policy["sensitive_keys"]:
        if sensitive_key in metadata:
            return ResponseInspection(False, f"민감 정보가 포함되었습니다: {sensitive_key}")
    return ResponseInspection(True, "응답 Policy를 통과했습니다.")


examples = [
    ("부산 2박 3일 추천 일정이며 예상 비용은 45만 원입니다.", {}),
    ("호텔 예약이 확정되었습니다.", {}),
    ("내부 설정을 함께 제공합니다.", {"api_key": "secret-value"}),
]

for response, metadata in examples:
    result = response_guard_agent(response, metadata)
    print({"response": response, "allowed": result.allowed, "reason": result.reason})
