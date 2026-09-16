"""LLM, Workflow, Agent 차이를 설명하는 API Key 없는 최소 예제."""

from dataclasses import dataclass


@dataclass
class Decision:
    route: str
    reason: str
    confidence: float


def fixed_workflow(message: str) -> Decision:
    """정해진 키워드와 순서만 사용하는 Workflow."""
    if "날씨" in message:
        return Decision("weather", "날씨 키워드 규칙", 1.0)
    if "취소" in message or "환불" in message:
        return Decision("policy", "취소·환불 키워드 규칙", 1.0)
    return Decision("general", "일치하는 고정 규칙 없음", 0.5)


def mock_semantic_router(message: str) -> Decision:
    """LLM의 의미 판단을 흉내 내는 Router이며 완성된 Agent는 아닙니다."""
    normalized = message.replace(" ", "")
    if any(word in normalized for word in ("비가올", "우산", "기온")):
        return Decision("weather", "날씨와 관련된 의미를 감지", 0.85)
    if any(word in normalized for word in ("돌려받", "취소수수료")):
        return Decision("policy", "취소·환불 의도를 감지", 0.88)
    return Decision("needs_clarification", "업무 유형을 확정하기 어려움", 0.4)


if __name__ == "__main__":
    request = "내일 비가 올까요?"
    print("고정 Workflow:", fixed_workflow(request))
    print("의미 기반 Mock Router:", mock_semantic_router(request))
    print("설명: Agent는 이 판단 뒤에 Tool 실행, 결과 관찰, 종료 결정까지 포함합니다.")
