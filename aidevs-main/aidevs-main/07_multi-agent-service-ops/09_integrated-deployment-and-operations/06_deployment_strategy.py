"""
[시나리오]
새 버전을 한 번에 모두 교체하지 않고 일부 트래픽만 Canary로 전달합니다. Error Rate와
P95 Latency가 기준을 만족하면 트래픽을 늘리고, 기준을 벗어나면 이전 버전으로 Rollback
합니다. 실제 AWS Resource를 변경하지 않고 배포 판단만 연습합니다.
"""


def deployment_decision(error_rate: float, p95_latency_ms: int) -> str:
    if error_rate > 0.05:
        return "ROLLBACK"
    if p95_latency_ms > 3000:
        return "HOLD"
    return "PROMOTE"


if __name__ == "__main__":
    observations = ((0.01, 1200), (0.02, 4200), (0.12, 900))
    for error_rate, latency in observations:
        print(f"오류율={error_rate:.0%}, P95={latency}ms -> {deployment_decision(error_rate, latency)}")
