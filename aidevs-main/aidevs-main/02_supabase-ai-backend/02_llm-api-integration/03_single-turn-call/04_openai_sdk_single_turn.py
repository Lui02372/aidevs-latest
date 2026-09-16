r"""OpenAI SDK 기반 싱글턴 호출 예제입니다.

주의:
    이 파일은 OPENAI_API_KEY가 설정되어 있을 때 실제 API를 호출합니다.
    실제 호출은 비용이 발생할 수 있습니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\03_single-turn-call\04_openai_sdk_single_turn.py
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# .env 파일은 02_supabase-ai-backend 폴더에 있으므로 두 단계 위로 이동합니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def is_real_api_key(value: str | None) -> bool:
    """API key가 비어 있지 않고 예시 값도 아닌지 확인합니다."""

    key = (value or "").strip()

    if not key:
        return False

    return not key.startswith(("your-", "your_", "sk-your", "AIza-your"))


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not is_real_api_key(api_key):
        # key가 없으면 실제 API를 호출하지 않고 종료합니다.
        # 초보자 수업에서는 이 안전 장치가 있어야 실수로 비용이 발생하지 않습니다.
        print("OPENAI_API_KEY가 없거나 placeholder 값입니다.")
        print("OpenAI 예제는 선택/비교 실습입니다. 먼저 mock 또는 Gemini 예제로 학습하세요.")
        return

    # openai 패키지는 실제 호출이 필요한 시점에 import합니다.
    # 이렇게 하면 key가 없는 학생도 이 파일을 실행해 안내 메시지를 볼 수 있습니다.
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    # chat.completions.create는 messages 목록을 보내고 모델 응답을 받는 호출입니다.
    # system에는 역할과 규칙을, user에는 실제 질문을 넣습니다.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "당신은 FastAPI를 쉽게 설명하는 학습 도우미입니다."},
            {
                "role": "user",
                "content": (
                    "참고 메모: Pydantic은 요청 데이터를 검증하고 잘못된 요청을 422 오류로 처리한다.\n"
                    "질문: FastAPI에서 Pydantic을 왜 사용하나요?"
                ),
            },
        ],
        # temperature를 낮게 두면 코드 설명처럼 일관성이 중요한 답변에 유리합니다.
        temperature=0.2,
        # max_tokens는 출력 길이와 비용을 제한하는 안전장치입니다.
        max_tokens=300,
    )

    # choices[0]은 첫 번째 후보 답변입니다.
    # 초보 단계에서는 후보 1개를 사용하는 흐름부터 익힙니다.
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
