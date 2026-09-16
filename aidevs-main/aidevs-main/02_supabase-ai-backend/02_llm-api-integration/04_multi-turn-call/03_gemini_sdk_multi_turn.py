r"""Gemini SDK 기반 멀티턴 호출 예제입니다.

이 파일은 Google Gen AI SDK를 사용해 이전 대화가 포함된 질문을 보냅니다.
02_gemini_sdk_multi_turn_small.py보다 오류 안내와 안전장치를 조금 더 포함합니다.

현재 폴더의 호출 흐름:
    01_mock_multi_turn.py
        실제 API 호출 없이 멀티턴 구조를 확인합니다.

    02_gemini_sdk_multi_turn_small.py
        예외 처리 없이 가장 작은 Gemini SDK 멀티턴 호출 코드를 확인합니다.

    03_gemini_sdk_multi_turn.py
        key 확인, 패키지 확인, Gemini API 오류 안내를 포함한 실제 호출을 연습합니다.

    04_openai_sdk_multi_turn.py
        OpenAI SDK를 선택/비교 실습으로 확인합니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\04_multi-turn-call\03_gemini_sdk_multi_turn.py
"""

from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def is_real_api_key(value: str | None) -> bool:
    """API key가 비어 있지 않고 예시 값도 아닌지 확인합니다."""

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


def build_gemini_contents() -> list[dict[str, object]]:
    """Gemini SDK에 전달할 멀티턴 대화 이력을 만듭니다.

    Gemini에서는 AI가 이전에 답한 메시지를 `model` 역할로 표현합니다.
    OpenAI의 `assistant` 역할과 비슷하다고 생각하면 됩니다.
    """

    return [
        {
            "role": "user",
            "parts": [{"text": "FastAPI에서 Pydantic을 왜 사용하나요?"}],
        },
        {
            "role": "model",
            "parts": [{"text": "요청 데이터를 검증하고 응답 모델을 정리하는 데 사용합니다."}],
        },
        {
            "role": "user",
            "parts": [{"text": "그럼 메모 API에서는 어떤 부분에 도움이 되나요? 초보자에게 설명해 주세요."}],
        },
    ]


def main() -> None:
    """Gemini SDK로 이전 대화가 포함된 질문을 보냅니다."""

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    if not is_real_api_key(api_key):
        print("GEMINI_API_KEY가 없거나 placeholder 값입니다.")
        print("먼저 01_mock_multi_turn.py로 멀티턴 구조를 이해한 뒤 실제 key를 설정하세요.")
        return

    try:
        from google import genai
    except ModuleNotFoundError:
        print("google-genai 패키지가 설치되어 있지 않습니다.")
        print("다음 명령으로 requirements.txt의 패키지를 먼저 설치하세요.")
        print(r"pip install -r requirements.txt")
        return

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model,
            contents=build_gemini_contents(),
            config={
                "temperature": 0.3,
                "max_output_tokens": 400,
            },
        )
    except Exception as error:
        print_gemini_error(error, model)
        return

    print(response.text)


if __name__ == "__main__":
    main()
