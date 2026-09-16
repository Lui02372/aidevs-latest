"""Prompt 변경을 감상이 아닌 시나리오 기대값으로 평가하는 최소 예제."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    request: str
    expected: str


SCENARIOS = [
    Scenario("부산 날씨가 궁금해", "information"),
    Scenario("제주 호텔을 예약해 줘", "reservation"),
    Scenario("예약을 취소하고 싶어", "cancellation"),
    Scenario("그거 해 줘", "needs_clarification"),
]


def deterministic_candidate(request: str) -> str:
    """평가 구조를 보여 주는 규칙 기반 대역이며 LLM 품질 평가 결과가 아닙니다."""
    if "취소" in request:
        return "cancellation"
    if "예약" in request:
        return "reservation"
    if any(word in request for word in ("날씨", "정보", "추천")):
        return "information"
    return "needs_clarification"


if __name__ == "__main__":
    passed = 0
    for scenario in SCENARIOS:
        actual = deterministic_candidate(scenario.request)
        ok = actual == scenario.expected
        passed += ok
        print("PASS" if ok else "FAIL", scenario.request, "expected=", scenario.expected, "actual=", actual)
    print(f"score={passed / len(SCENARIOS):.0%} ({passed}/{len(SCENARIOS)})")
