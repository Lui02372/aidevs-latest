"""여행 문의를 분류하는 초보자용 Mock Agent."""

from dataclasses import asdict, dataclass
import json


@dataclass
class TravelIntent:
    intent: str
    reason: str
    confidence: float
    missing_information: list[str]


def classify_travel_request(message: str) -> TravelIntent:
    text = message.replace(" ", "")
    if any(word in text for word in ("취소", "환불", "수수료")):
        return TravelIntent("policy", "취소·환불 관련 표현", 0.94, [])
    if any(word in text for word in ("날씨", "비가", "비예보", "기온", "우산")):
        return TravelIntent("weather", "날씨 관련 표현", 0.9, [])
    if any(word in text for word in ("호텔", "숙소", "체크인")):
        return TravelIntent("accommodation", "숙소 관련 표현", 0.92, [])
    if any(word in text for word in ("일정", "여행", "코스")):
        missing = [] if any(city in text for city in ("서울", "부산", "제주", "강릉")) else ["destination"]
        return TravelIntent("travel_plan", "여행 일정 관련 표현", 0.87, missing)
    return TravelIntent("needs_clarification", "분류 근거가 부족함", 0.35, ["request_detail"])


def decide_next_action(result: TravelIntent) -> dict[str, str]:
    """낮은 confidence와 누락 정보를 안전한 추가 질문으로 연결합니다."""
    if result.confidence < 0.6:
        return {
            "action": "ask_user",
            "question": "어떤 도움을 원하는지 조금 더 구체적으로 알려주세요.",
        }
    if "destination" in result.missing_information:
        return {
            "action": "ask_user",
            "question": "어느 지역으로 여행하고 싶은가요?",
        }
    return {"action": "continue", "question": ""}


if __name__ == "__main__":
    samples = [
        "부산 2박 3일 여행 코스를 만들어 줘.",
        "호텔을 하루 전에 취소하면 수수료가 있나요?",
        "제주도에 우산을 가져가야 할까요?",
        "도와주세요.",
    ]
    for sample in samples:
        result = classify_travel_request(sample)
        print(sample)
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        print("다음 행동:", json.dumps(decide_next_action(result), ensure_ascii=False))
