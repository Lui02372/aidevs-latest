"""
[시나리오]
Redis의 실시간 Task가 TTL로 사라진 뒤에도 운영자는 과거 실패를 조사해야 합니다.

1. PostgreSQL의 최근 실행 이력을 조회합니다.
2. task_id, trace_id, 상태, 오류와 시간을 확인합니다.
3. 조회 결과가 없으면 아직 서비스 Task를 실행하지 않았다고 출력합니다.

[기대 결과]
실제 PostgreSQL의 최근 Task가 출력되거나 이력이 없다는 안내가 출력됩니다.

[학습 포인트]
현재 State와 영구 History는 수명이 다릅니다. PostgreSQL은 감사·분석을 위해 완료된
실행과 Trace를 보존합니다. 이 Lab은 실제 DB를 읽고 데이터를 만들지 않습니다.
"""

from app.repositories import PostgresHistory


history = PostgresHistory().recent_runs(limit=10)
if history:
    for task in history:
        print(task)
else:
    print("아직 저장된 실행 이력이 없습니다. 서비스를 한 번 실행한 뒤 다시 확인하세요.")
