
import json
from pathlib import Path


CURRENT_DIR = Path(__file__).parent


def read_json_safely(file_name: str) -> dict:
    """JSON 파일을 읽고 dict로 반환합니다.

    오류가 나면 프로그램을 바로 종료하지 않고 빈 dict를 반환합니다.
    """
    file_path = CURRENT_DIR / file_name
    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError("파일이 없어요")

    try:
        # JSON 파일을 Dict로 변경
        return json.loads(text)
    except json.decoder.JSONDecodeError as error:
        raise error

