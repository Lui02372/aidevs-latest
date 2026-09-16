"""의도적으로 깨진 실행 환경 예제입니다.

실행:
    python .\broken_app.py

이 파일은 수강생이 import 오류와 .env 오류를 분석하도록 일부러 문제가 들어 있습니다.
처음부터 코드를 고치기보다 Traceback을 복사해 Codex에게 원인 분석을 요청합니다.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# 의도된 오류입니다.
# 실제 프로젝트에는 이런 패키지가 없으므로 ModuleNotFoundError가 발생합니다.
from missing_demo_package import create_demo_message  # type: ignore


ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)


def read_demo_key() -> str:
    """DEMO_API_KEY를 읽고 없으면 실행 오류를 발생시킵니다."""

    value = os.getenv("DEMO_API_KEY", "").strip()
    if not value or value.startswith("your-"):
        raise RuntimeError("DEMO_API_KEY가 없습니다. .env 파일과 예시값 여부를 확인하세요.")
    return value


def main() -> None:
    """환경변수와 import가 준비되었는지 확인합니다."""

    api_key = read_demo_key()
    print(create_demo_message(api_key))


if __name__ == "__main__":
    main()
