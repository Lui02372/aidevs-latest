"""공통 .venv에 설치된 외부 패키지를 확인하는 예제입니다."""

# pytest는 파이썬에 기본 포함된 표준 라이브러리가 아닙니다.
# pip install -r requirements.txt로 설치해야 사용할 수 있는 외부 패키지입니다.
import pytest

# __version__은 패키지 버전을 확인할 때 자주 사용하는 속성입니다.
pytest_version = pytest.__version__

# 현재 설치된 pytest 버전을 출력합니다.
print("설치된 pytest 버전:", pytest_version)

# 이 예제에서는 실제 테스트를 실행하지 않고 import 확인만 합니다.
# 테스트 실행은 08_testing-code-quality 단원에서 자세히 다룹니다.
print("pytest import 성공: 공통 .venv와 requirements.txt 설정이 정상입니다.")
