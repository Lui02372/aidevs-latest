"""Lab 02 solution: API Key 안전 점검."""

import os
from pathlib import Path


# 02_supabase-ai-backend 폴더를 기준으로 .env 파일을 찾습니다.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"


def load_env_file(path: Path) -> None:
    """간단한 .env 파일을 읽어 현재 프로그램의 환경 변수에 넣습니다."""
    if not path.exists():
        print(f"[안내] .env 파일이 없습니다: {path}")
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # 빈 줄과 주석 줄은 환경 변수로 읽지 않습니다.
        if not line or line.startswith("#"):
            continue

        # KEY=VALUE 형태만 처리합니다.
        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        # setdefault를 쓰면 이미 운영체제 환경 변수로 들어온 값은 덮어쓰지 않습니다.
        os.environ.setdefault(key.strip(), value.strip())


def is_real_api_key(value: str | None) -> bool:
    """API key가 비어 있지 않고 예시 값도 아닌지 확인합니다."""

    key = (value or "").strip()

    if not key:
        return False

    return not key.startswith(("your-", "your_", "sk-your", "AIza-your"))


def mask_secret(value: str | None) -> str:
    """key 전체를 출력하지 않고 앞뒤 일부만 보여줍니다."""
    if not is_real_api_key(value):
        return "(not set)"

    cleaned = value.strip()
    if len(cleaned) <= 10:
        return "***"

    return f"{cleaned[:6]}***{cleaned[-4:]}"


load_env_file(ENV_PATH)

gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

print("[API Key 점검]")
print("GEMINI_API_KEY:", mask_secret(gemini_key))
print("OPENAI_API_KEY:", mask_secret(openai_key))

print("\n[기본 모델]")
print("Gemini 기본:", os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
print("OpenAI 선택:", os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))

print("\n[안전 기준]")
print("- 실제 호출 전에는 무료 한도와 사용량을 확인합니다.")
print("- 실습 코드에서는 기본적으로 mock 응답을 사용합니다.")
print("- 실제 호출 여부는 actual_api_called 값으로 구분합니다.")
