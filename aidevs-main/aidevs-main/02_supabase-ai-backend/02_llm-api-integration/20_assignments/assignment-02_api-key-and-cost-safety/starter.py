"""Assignment 02 starter: API key와 비용 안전 점검."""

import os
from pathlib import Path


# 현재 파일 기준으로 02_supabase-ai-backend 폴더를 찾습니다.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"


def load_env_file(path: Path) -> None:
    """간단한 .env 파일을 읽어 환경 변수에 넣습니다."""
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def is_real_api_key(value: str | None) -> bool:
    """실제 API key인지 확인합니다."""
    # TODO: 값이 없거나 빈 문자열이면 False를 반환하세요.
    # TODO: your- 로 시작하는 placeholder 값이면 False를 반환하세요.
    return False


def mask_secret(value: str | None) -> str:
    """key 전체가 노출되지 않도록 일부만 보여줍니다."""
    # TODO: 실제 key가 아니면 "(not set)"을 반환하세요.
    # TODO: 실제 key이면 앞 6글자, 뒤 4글자만 남기세요.
    return "(not set)"


load_env_file(ENV_PATH)

gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

print("[API key check]")
print("GEMINI_API_KEY:", mask_secret(gemini_key))
print("OPENAI_API_KEY:", mask_secret(openai_key))

print("\n[model defaults]")
print("Gemini:", os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
print("OpenAI:", os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))

print("\n[cost safety checklist]")
print("- 실제 API 호출 전에 무료 한도와 과금 기준을 확인합니다.")
print("- 실습 기본값은 mock 호출입니다.")
print("- 실제 호출 여부는 actual_api_called로 표시합니다.")
