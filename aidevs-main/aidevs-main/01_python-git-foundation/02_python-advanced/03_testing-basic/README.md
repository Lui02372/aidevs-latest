# 03_testing-basic

이 단원에서는 테스트를 아주 작게 시작합니다.

목표는 pytest를 깊게 배우는 것이 아니라, `print`로 눈으로 확인하던 방식을 `assert`와 `pytest`로 자동 확인하는 것입니다.

## 예제

| 파일 | 내용 |
| --- | --- |
| `01_assert_basic.py` | `assert` 기본 사용 |
| `02_print_vs_assert.py` | `print` 확인과 `assert` 확인 비교 |
| `service_logic.py` | 테스트할 함수 모음 |
| `test_service_logic.py` | pytest 테스트 |

## 실행 방법

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\03_testing-basic\01_assert_basic.py
python .\02_python-advanced\03_testing-basic\02_print_vs_assert.py
python -m pytest .\02_python-advanced\03_testing-basic
```

## 핵심 정리

```text
print:
  값을 보여 줍니다. 맞는지 틀린지는 사람이 직접 봐야 합니다.

assert:
  코드가 예상값과 실제값을 비교합니다. 틀리면 실패합니다.

pytest:
  test_*.py 파일을 찾아 여러 테스트를 한 번에 실행합니다.
```
