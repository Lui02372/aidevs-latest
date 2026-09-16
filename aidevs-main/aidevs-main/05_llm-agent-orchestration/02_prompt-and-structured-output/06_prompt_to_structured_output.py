"""자유 응답 Prompt와 Pydantic Structured Output API 결과를 비교합니다."""

import httpx

from _llm_backend import (
    generate_structured,
    generate_text,
    print_connection_help,
    print_result,
)


MESSAGE = "부산에서 대중교통으로 즐기는 2박 3일 여행을 제안해 주세요."
FREE_PROMPT = "안전하고 간결한 여행 계획을 작성하세요."
# Structured Output에서도 내용상 제약은 Prompt가, 필드 계약은 Schema가 담당합니다.
STRUCTURED_PROMPT = """제공된 TravelPlan Schema에 맞춰 여행 계획을 작성하세요.
입력에 없는 예약 완료 여부나 확정 가격은 추측하지 마세요."""


if __name__ == "__main__":
    try:
        # 첫 호출은 문자열, 두 번째 호출은 검증된 TravelPlan 객체를 반환합니다.
        print_result("자유 응답", generate_text(FREE_PROMPT, MESSAGE))
        print_result(
            "TravelPlan Structured Output",
            generate_structured("travel_plan", STRUCTURED_PROMPT, MESSAGE),
        )
    except httpx.HTTPError as error:
        print_connection_help(error)
