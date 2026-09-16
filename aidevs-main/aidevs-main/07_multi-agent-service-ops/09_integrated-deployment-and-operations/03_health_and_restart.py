"""
[시나리오]
Container가 실행 중이라는 사실만으로 요청을 처리할 수 있다고 판단하면 안 됩니다.
Liveness는 Process가 살아 있는지, Readiness는 Redis·PostgreSQL이 준비됐는지 판단합니다.
Health 결과에 따라 재시작할지, 트래픽에서 제외할지, 정상 서비스할지를 출력합니다.
"""


def decide_operation(live: bool, ready: bool) -> str:
    if not live:
        return "RESTART: Process가 응답하지 않으므로 Container를 재시작합니다."
    if not ready:
        return "DRAIN: Process는 살아 있지만 트래픽을 보내지 않습니다."
    return "SERVE: 신규 요청을 받을 수 있습니다."


if __name__ == "__main__":
    scenarios = ((True, True, "정상"), (True, False, "의존성 준비 안 됨"), (False, False, "중단"))
    for live_status, ready_status, description in scenarios:
        print(f"{description}: {decide_operation(live_status, ready_status)}")
