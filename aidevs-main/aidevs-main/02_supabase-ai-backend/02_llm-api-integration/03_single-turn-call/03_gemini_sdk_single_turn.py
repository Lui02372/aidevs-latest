r"""Gemini SDK 기반 싱글턴 호출 예제입니다.

이 파일은 Google Gen AI SDK를 사용해 Gemini API를 호출합니다.
02_gemini_sdk_single_turn_small.py보다 오류 안내와 안전장치를 조금 더 포함합니다.

현재 폴더의 호출 흐름:
    01_mock_single_turn.py
        실제 API를 호출하지 않고 싱글턴 구조를 먼저 이해합니다.

    02_gemini_sdk_single_turn_small.py
        예외 처리 없이 가장 작은 Gemini SDK 호출 코드를 확인합니다.

    03_gemini_sdk_single_turn.py
        key 확인, 패키지 확인, Gemini API 오류 안내를 포함한 실제 호출을 연습합니다.

    04_openai_sdk_single_turn.py
        OpenAI SDK를 선택/비교 실습으로 확인합니다.

주의:
    이 파일은 GEMINI_API_KEY가 실제 key로 설정되어 있을 때만 API를 호출합니다.
    key가 없거나 placeholder 값이면 실제 API를 호출하지 않고 안내 메시지를 출력합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\03_single-turn-call\03_gemini_sdk_single_turn.py
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# .env 파일은 02_supabase-ai-backend 폴더에 있으므로 두 단계 위로 이동합니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def is_real_api_key(value: str | None) -> bool:
    """API key가 비어 있지 않고 예시 값도 아닌지 확인합니다.

    .env.example에는 `your-...` 형태의 안내용 값이 들어 있습니다.
    이런 값이면 실제 API를 호출하지 않습니다.
    """

    key = (value or "").strip()

    if not key:
        return False

    return not key.startswith(("your-", "your_", "sk-your", "AIza-your"))


def print_gemini_error(error: Exception, model: str) -> None:
    """Gemini API 호출 오류를 수업 중 이해하기 쉬운 메시지로 출력합니다."""

    status_code = getattr(error, "status_code", None)
    message = str(error)

    print("Gemini API 호출에 실패했습니다.")
    print(f"사용 모델: {model}")

    if status_code == 503 or "UNAVAILABLE" in message or "high demand" in message:
        print("원인: Gemini 서버가 일시적으로 바쁘거나 해당 모델 수요가 높은 상태입니다.")
        print("해결: 잠시 뒤 다시 실행하거나, .env의 GEMINI_MODEL을 다른 사용 가능한 모델로 바꿔 봅니다.")
    elif status_code == 429 or "RESOURCE_EXHAUSTED" in message:
        print("원인: 호출 횟수 또는 quota/rate limit에 도달했을 수 있습니다.")
        print("해결: Google AI Studio에서 현재 quota와 rate limit을 확인하고 잠시 뒤 다시 실행합니다.")
    elif status_code in {400, 401, 403}:
        print("원인: API key, 모델 이름, 권한 설정 중 하나가 잘못되었을 수 있습니다.")
        print("해결: .env의 GEMINI_API_KEY와 GEMINI_MODEL 값을 다시 확인합니다.")
    else:
        print("원인: 외부 API 호출 중 예기치 않은 오류가 발생했습니다.")

    print(f"원본 오류: {message}")


def main() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    if not is_real_api_key(api_key):
        print("GEMINI_API_KEY가 없거나 placeholder 값입니다.")
        print("먼저 01_mock_single_turn.py로 구조를 이해한 뒤, .env에 실제 Gemini API key를 설정하세요.")
        return

    try:
        from google import genai
    except ModuleNotFoundError:
        print("google-genai 패키지가 설치되어 있지 않습니다.")
        print("다음 명령으로 requirements.txt의 패키지를 먼저 설치하세요.")
        print(r"pip install -r requirements.txt")
        return

    # SDK 방식은 URL, query parameter, JSON payload를 직접 만들지 않아도 되므로
    # 초보자가 실제 LLM 호출 흐름을 이해하기에 가장 단순한 방식입니다.
    client = genai.Client(api_key=api_key)

    prompt = (
        # "참고 메모: Pydantic은 요청 데이터를 검증하고 잘못된 요청을 422 오류로 처리한다.\n"
        "질문: 1+1이 뭐야"
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 500,
            },
        )
    except Exception as error:
        print_gemini_error(error, model)
        return

    # SDK는 응답 텍스트를 response.text로 쉽게 꺼낼 수 있습니다.
    print(response.text)


if __name__ == "__main__":
    main()
