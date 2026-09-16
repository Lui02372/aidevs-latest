"""
[시나리오]
Load Balancer가 Backend Process만 살아 있는지 확인하면 Redis나 PostgreSQL 장애를
놓칠 수 있습니다. Service Health Agent가 실제 의존성을 각각 확인합니다.

1. Redis에 PING을 보냅니다.
2. PostgreSQL에 SELECT 1을 실행합니다.
3. 두 저장소가 모두 정상이면 ready, 하나라도 실패하면 degraded로 판단합니다.
4. 실패 원인을 숨기지 않고 의존성별 결과를 출력합니다.

[기대 결과]
현재 실행 중인 Redis와 PostgreSQL 연결 결과 및 전체 상태가 출력됩니다.

[학습 포인트]
Process가 실행 중인 liveness와 요청 처리 준비가 된 readiness는 다릅니다. 이 Lab은
실제 저장소를 조회하며 데이터를 변경하지 않습니다.
"""

from app.repositories import PostgresHistory, RedisTasks


checks: dict[str, object] = {}
for name, repository in (("redis", RedisTasks()), ("postgresql", PostgresHistory())):
    try:
        checks[name] = repository.ping()
    except Exception as error:
        checks[name] = f"{type(error).__name__}: {error}"

status = "ready" if checks == {"redis": True, "postgresql": True} else "degraded"
print({"status": status, "dependencies": checks})
