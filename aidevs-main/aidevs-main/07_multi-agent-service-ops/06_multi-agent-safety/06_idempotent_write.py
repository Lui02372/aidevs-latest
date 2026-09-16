"""
[시나리오]
일정 저장 직후 네트워크 응답이 끊겨 Supervisor Agent가 같은 요청을 재시도합니다.

1. 첫 번째 요청은 일정을 실제로 저장합니다.
2. 두 번째 요청은 같은 사용자와 idempotency key를 사용합니다.
3. Registry는 첫 결과를 돌려주고 저장 함수는 다시 실행하지 않습니다.

[기대 결과]
두 호출의 결과는 같지만 실제 저장 횟수는 1회입니다.

[학습 포인트]
Retry는 안정성을 높이지만 변경 Tool을 중복 실행할 수 있습니다. 승인과 멱등성은
서로 다른 문제이며 둘 다 필요합니다. 이 Lab은 메모리를 쓰고 운영 단계에서는 Redis로 바꿉니다.
"""

from shared.travel_safety import IdempotencyRegistry


registry = IdempotencyRegistry()
save_count = 0


def save_itinerary() -> dict[str, str]:
    global save_count
    save_count += 1
    return {"itinerary_id": "itinerary-001"}


first, first_executed = registry.execute_once("user-101", "travel-001-save-v1", save_itinerary)
second, second_executed = registry.execute_once("user-101", "travel-001-save-v1", save_itinerary)

print("첫 요청:", first, "실행됨:", first_executed)
print("재시도:", second, "실행됨:", second_executed)
print("실제 저장 횟수:", save_count)
