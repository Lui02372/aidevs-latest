"""
Lab 01 solution - Supabase 환경변수 확인.

Supabase에 접속하기 전에는 URL과 key가 준비되어 있어야 합니다.
이 예제는 실제 key 값을 그대로 출력하지 않고, 앞뒤 일부만 마스킹해서 보여 줍니다.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


def is_placeholder(value: str) -> bool:
    """환경변수 값이 .env.example에 있는 예시 값인지 확인합니다."""

    return value.strip().startswith(("your-", "https://your-"))


def mask_secret(value: str) -> str:
    """민감한 key가 화면에 그대로 노출되지 않도록 가립니다."""

    if len(value) <= 12:
        return "설정됨"

    return f"{value[:6]}...{value[-4:]}"


def main() -> None:
    """필수 Supabase 환경변수 3개를 확인합니다."""

    load_dotenv()

    required_names = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
    ]

    for name in required_names:
        value = os.getenv(name)

        if not value:
            print(f"[없음] {name}")
            continue

        if is_placeholder(value):
            print(f"[수정 필요] {name}: placeholder 값으로 보입니다.")
            continue

        print(f"[설정됨] {name}: {mask_secret(value)}")


if __name__ == "__main__":
    main()
