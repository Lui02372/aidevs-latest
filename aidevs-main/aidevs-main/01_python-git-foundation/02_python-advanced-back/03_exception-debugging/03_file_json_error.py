"""파일 없음 오류와 JSON 형식 오류를 함께 처리하는 예제입니다."""

import json
from pathlib import Path


def load_json_file(path: Path) -> dict[str, str]:
    """JSON 파일을 읽어 딕셔너리로 반환합니다."""

    try:
        # 파일이 없으면 FileNotFoundError가 발생합니다.
        raw_text = path.read_text(encoding="utf-8")

        # JSON 형식이 잘못되면 json.JSONDecodeError가 발생합니다.
        data = json.loads(raw_text)

    except FileNotFoundError:
        # 파일이 없을 때 사용할 기본값을 반환합니다.
        print(f"{path} 파일이 없습니다.")
        return {}

    except json.JSONDecodeError:
        # 파일은 있지만 JSON 형식이 잘못되었을 때 실행됩니다.
        print(f"{path} 파일의 JSON 형식이 올바르지 않습니다.")
        return {}

    # 파일 읽기와 JSON 변환이 모두 성공하면 데이터를 반환합니다.
    return data


# 일부러 없는 파일을 읽어 봅니다.
missing_path = Path("data") / "missing_config.json"
print("없는 파일 결과:", load_json_file(missing_path))

# 잘못된 JSON 문자열도 함수 흐름을 이해하기 위해 직접 테스트합니다.
try:
    json.loads('{name: "Mina"}')
except json.JSONDecodeError as error:
    print("직접 JSON 변환 테스트 오류:", error)
