"""Lab 01-1: 하나의 Travel AI Agent가 전체 요청을 처리합니다.

시나리오:
    사용자는 부산 2박 3일 여행 초안을 요청합니다. 두 번째 요청에는 알레르기와
    대중교통 조건도 추가합니다. 하나의 Travel Agent가 같은 Goal과 같은 권한 안에서
    전체 초안을 작성합니다. 실제 예약·결제·날씨 조회는 수행하지 않습니다.

학습 질문:
    역할처럼 보이는 작업이 여러 개 있어도 하나의 판단 주체로 처리할 수 있을까요?
    사용자 제약이 늘어나는 것과 Agent를 분리하는 것은 같은 문제일까요?
"""

import json
import os

from shared.travel_contracts import TravelPlanDraft
from shared.travel_llm import run_with_metadata


REQUESTS = [
    "부산 2박 3일 여행 초안을 만들어 줘.",
    "부산 2박 3일 여행을 계획해 줘. 해산물 알레르기가 있고 대중교통을 이용할 거야.",
]


def travel_agent(request: str, provider: str) -> dict:
    prompt = f"""
당신은 하나의 Travel AI Agent입니다.
여행 초안 작성이라는 하나의 Goal만 수행하세요.
실제 예약이나 결제를 하지 마세요.
실시간 Tool을 사용하지 않았으므로 확인하지 않은 날씨와 가격은 단정하지 마세요.
요청: {request}
""".strip()
    return run_with_metadata(provider, prompt, TravelPlanDraft)


if __name__ == "__main__":
    provider = os.getenv("LLM_PROVIDER", "openai")
    for number, request in enumerate(REQUESTS, start=1):
        print(f"\n=== 요청 {number}: {request} ===")
        response = travel_agent(request, provider)
        print(json.dumps(response, ensure_ascii=False, indent=2))
        if response["error"]:
            print("확인: Provider 실패가 성공 결과로 바뀌지 않았습니다.")
        else:
            print("Provider 일치:", response["provider_used"] == provider)
            print("Fallback 미사용:", response["fallback_used"] is False)

    print("\n비교 질문: 제약이 추가됐을 때 Prompt가 아니라 결과의 어떤 필드가 달라졌나요?")
