"""
[종합 실습 시나리오]
배포 직후 Worker의 LLM 요청 실패율이 높아지고 Queue가 적체됐습니다. 운영자는 Dashboard에서
이상을 발견하고 Trace ID로 실패 범위를 확인한 뒤 재시작·Fallback·Rollback 중 적절한
조치를 선택합니다. 관측 신호를 입력받아 우선 대응 순서를 출력합니다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class IncidentSignals:
    worker_live: bool
    queue_depth: int
    provider_error_rate: float
    new_release: bool


def make_incident_plan(signals: IncidentSignals) -> list[str]:
    actions = ["Trace ID와 배포 Version으로 실패 범위를 확인합니다."]
    if not signals.worker_live:
        actions.append("Worker Container를 재시작합니다.")
    if signals.provider_error_rate > 0.05:
        actions.append("Provider Circuit을 열고 검증된 Fallback을 사용합니다.")
    if signals.queue_depth > 100:
        actions.append("Worker 수를 늘리고 오래된 Task 처리 정책을 확인합니다.")
    if signals.new_release:
        actions.append("새 Version과 장애의 상관관계를 확인하고 필요하면 Rollback합니다.")
    actions.append("PostgreSQL 실행 이력과 구조화 Log로 사후 분석합니다.")
    return actions


if __name__ == "__main__":
    signals = IncidentSignals(False, 160, 0.18, True)
    for order, action in enumerate(make_incident_plan(signals), start=1):
        print(f"{order}. {action}")
