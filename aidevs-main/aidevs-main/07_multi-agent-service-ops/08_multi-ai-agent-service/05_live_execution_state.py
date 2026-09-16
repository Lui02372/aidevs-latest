"""
[시나리오]
실행 중인 Multi-Agent Task의 최신 상태를 Frontend가 빠르게 조회해야 합니다.

1. 교육용 Task를 Redis에 queued 상태로 저장합니다.
2. 같은 task_id로 다시 읽어 현재 Agent와 Progress를 확인합니다.
3. Redis Key에는 TTL이 있어 실시간 상태가 영구적으로 쌓이지 않습니다.
4. 이 예제는 Queue에 넣지 않으므로 Worker와 실제 LLM을 실행하지 않습니다.

[기대 결과]
저장한 task_id, queued 상태, 0% Progress가 Redis에서 그대로 조회됩니다.

[학습 포인트]
Redis는 현재 상태와 빠른 폴링에 적합합니다. 완료 후 장기간 보존할 이력은 PostgreSQL에
저장합니다. 이 Lab은 실제 Redis를 사용하며 고정 성공 결과로 대체하지 않습니다.
"""

from app.models import TaskRecord
from app.repositories import RedisTasks


repository = RedisTasks()
learning_task = TaskRecord(
    user_id="learning-user",
    request="Redis에서 관찰할 부산 여행 Task 상태를 만들어 주세요.",
    current_agent="supervisor_agent",
)
repository.save(learning_task)
loaded_task = repository.get(learning_task.task_id)

print("저장한 Task:", learning_task.task_id)
print("Redis 조회 결과:", loaded_task.model_dump(mode="json") if loaded_task else None)
