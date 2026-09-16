r"""Git/GitHub 실습용 테스트 파일입니다.

실행:
    cd C:\aidev\01_python-git-foundation\03_git-github\10_labs\practice-files\git-practice-project
    python -m pytest test_main.py

테스트 파일이 있으면 GitHub에 올리기 전에 코드가 정상 동작하는지 확인할 수 있습니다.
"""

from main import add


def test_add_returns_sum() -> None:
    """add 함수가 두 숫자의 합을 반환하는지 확인합니다."""

    assert add(2, 3) == 5
