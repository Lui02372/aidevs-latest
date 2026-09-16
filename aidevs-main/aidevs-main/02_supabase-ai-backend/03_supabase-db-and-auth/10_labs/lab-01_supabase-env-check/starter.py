"""
Lab 01 starter - Supabase 환경변수 확인.

이 파일은 `.env`에 필요한 값이 들어 있는지 확인하는 연습용 starter입니다.
TODO 부분을 채운 뒤 solution.py와 비교합니다.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


def mask_secret(value: str) -> str:
    """민감한 key 전체가 보이지 않도록 일부만 보여 주는 함수를 완성합니다."""

    # TODO: value 길이가 짧으면 "설정됨"만 반환합니다.
    # TODO: value 길이가 충분하면 앞 6글자와 뒤 4글자만 보여 줍니다.
    return value


def main() -> None:
    """필수 Supabase 환경변수 이름을 하나씩 확인합니다."""

    load_dotenv()

    required_names = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
    ]

    for name in required_names:
        value = os.getenv(name)

        # TODO: 값이 없으면 "[없음] 변수명" 형식으로 출력합니다.
        # TODO: 값이 있으면 mask_secret 함수를 사용해 안전하게 출력합니다.
        print(name, value)


if __name__ == "__main__":
    main()
