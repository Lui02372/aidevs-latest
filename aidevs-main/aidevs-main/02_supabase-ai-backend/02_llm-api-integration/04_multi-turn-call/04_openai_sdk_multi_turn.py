r"""OpenAI SDK 기반 멀티턴 호출 예제입니다.

OPENAI_API_KEY가 있을 때만 실제 API를 호출합니다.
OpenAI 예제는 선택/비교 실습용입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\04_multi-turn-call\04_openai_sdk_multi_turn.py
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# 실제 API 호출이 필요하면 .env에 OPENAI_API_KEY를 넣은 뒤 이 예제를 실행합니다.
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
        # key가 없으면 비용이 발생하는 실제 호출을 하지 않습니다.
        print("OPENAI_API_KEY가 없거나 placeholder 값입니다.")
        print("OpenAI 예제는 선택/비교 실습입니다. 먼저 mock 또는 Gemini 예제로 학습하세요.")
        return

    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    # 멀티턴 호출의 핵심은 이전 assistant 답변까지 함께 전달하는 것입니다.
    # 그래야 모델이 "그 설명을 바탕으로" 같은 후속 질문을 이해할 수 있습니다.
    messages = [
        {"role": "system", "content": "당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다."},
        {"role": "user", "content": "FastAPI에서 Pydantic을 왜 사용하나요?"},
        {"role": "assistant", "content": "요청 데이터를 검증하고 응답 모델을 정리하는 데 사용합니다."},
        {"role": "user", "content": "그럼 메모 API에서는 어떤 부분에 도움이 되나요?"},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # 멀티턴에서도 파라미터는 싱글턴과 동일하게 적용됩니다.
        temperature=0.3,
        max_tokens=400,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
