"""선택 실습: OpenAI Responses API 기본 호출.

실행 전 .env에 OPENAI_API_KEY를 설정하고 APP_MODE=real로 변경합니다.
필수 수업 흐름은 이 파일 없이 Mock 모드로 완료할 수 있습니다.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def main() -> None:
    if os.getenv("APP_MODE", "mock") != "real":
        raise RuntimeError("실제 호출은 APP_MODE=real일 때만 허용합니다.")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다.")
    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=(
            "다음 문의를 travel_plan, accommodation, weather, policy, "
            "needs_clarification 중 하나로 분류하고 짧은 이유를 설명하세요.\n"
            "문의: 부산 2박 3일 여행 일정을 만들어 주세요."
        ),
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
