"""
[시나리오]
같은 Container Image를 개발·검증·운영에서 재사용하고 환경 변수만 바꿉니다. 비밀값
자체를 출력하지 않고 필수 설정의 존재 여부와 주소 형식만 확인합니다. 코드에 Key를 적지
않고, 배포 전에 잘못된 설정을 발견하면 실행을 멈추는 원칙을 익힙니다.
"""

import os
from urllib.parse import urlparse


REQUIRED_SETTINGS = ("OPENAI_API_KEY", "GEMINI_API_KEY", "REDIS_URL", "DATABASE_URL")


def validate_release_config() -> list[str]:
    problems: list[str] = []
    for setting_name in REQUIRED_SETTINGS:
        if not os.getenv(setting_name, "").strip():
            problems.append(f"{setting_name} 값이 없습니다.")
    api_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    if urlparse(api_url).scheme not in {"http", "https"}:
        problems.append("API_BASE_URL은 http 또는 https 주소여야 합니다.")
    return problems


if __name__ == "__main__":
    config_problems = validate_release_config()
    print("배포 설정을 보완해야 합니다." if config_problems else "필수 배포 설정이 준비되었습니다.")
    for problem in config_problems:
        print(f"- {problem}")
