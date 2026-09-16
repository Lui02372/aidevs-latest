"""
[시나리오]
GitHub Actions가 새 버전을 배포하기 전에 최소 품질 기준을 확인합니다. 구문·보안 검사는
반드시 통과하고, 회귀 평가 점수와 Readiness도 기준을 만족해야 합니다. 여러 결과를 하나의
Release Gate로 합치고 실패 항목을 모두 출력하는 원리를 보여 줍니다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseEvidence:
    syntax_ok: bool
    security_ok: bool
    evaluation_score: float
    readiness_ok: bool


def evaluate_release(evidence: ReleaseEvidence) -> list[str]:
    failures: list[str] = []
    if not evidence.syntax_ok:
        failures.append("Python 구문 검사 실패")
    if not evidence.security_ok:
        failures.append("보안 정책 검사 실패")
    if evidence.evaluation_score < 0.8:
        failures.append("회귀 평가 점수가 0.8 미만")
    if not evidence.readiness_ok:
        failures.append("Readiness 실패")
    return failures


if __name__ == "__main__":
    release_failures = evaluate_release(ReleaseEvidence(True, True, 0.86, True))
    print("배포 가능" if not release_failures else "배포 중단")
    for failure in release_failures:
        print(f"- {failure}")
