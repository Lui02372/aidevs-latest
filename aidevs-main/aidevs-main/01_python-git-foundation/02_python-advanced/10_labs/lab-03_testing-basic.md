# Lab 03. 테스트 기초

## 목표

`print`로 눈으로 확인하던 방식을 `pytest` 테스트로 바꿉니다.

## 먼저 실행

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\03_testing-basic\02_print_vs_assert.py
python -m pytest .\02_python-advanced\03_testing-basic
```

## 해야 할 일

`03_testing-basic/test_service_logic.py`에 테스트를 하나 추가합니다.

추가할 테스트:

```python
def test_build_response_answer_contains_question() -> None:
    response = build_response("테스트란?")

    assert "테스트란?" in response["answer"]
```

## 완료 기준

```text
[ ] 새 테스트 함수를 추가했다.
[ ] python -m pytest 명령이 성공한다.
[ ] 테스트 실패 시 어느 줄이 실패했는지 확인할 수 있다.
```

## 생각해 보기

```text
print로 확인하는 방식과 pytest로 확인하는 방식은 무엇이 다를까요?
나중에 API 코드가 길어지면 테스트가 왜 필요할까요?
```
