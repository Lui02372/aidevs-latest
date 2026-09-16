"""관련성 점수와 글자 budget으로 Context를 선택하는 단순 예제입니다."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ContextItem:
    source: str
    text: str
    relevance: float


def select_context(items: list[ContextItem], max_chars: int) -> list[ContextItem]:
    selected: list[ContextItem] = []
    used = 0
    for item in sorted(items, key=lambda value: value.relevance, reverse=True):
        if used + len(item.text) <= max_chars:
            selected.append(item)
            used += len(item.text)
    return selected


if __name__ == "__main__":
    items = [
        ContextItem("policy", "예약 변경은 출발 3일 전까지 가능합니다.", 0.95),
        ContextItem("weather", "부산의 여름은 덥고 습합니다.", 0.35),
        ContextItem("refund", "환불 수수료는 상품별 약관을 확인해야 합니다.", 0.88),
    ]
    selected = select_context(items, max_chars=55)
    print("선택 source:", [item.source for item in selected])
    print("Context:\n" + "\n".join(item.text for item in selected))
