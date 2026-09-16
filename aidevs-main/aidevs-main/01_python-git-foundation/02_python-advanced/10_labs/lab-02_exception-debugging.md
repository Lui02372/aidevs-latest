# Lab 02. 예외 처리와 JSON

## 목표

잘못된 입력과 JSON 파일 오류를 처리합니다.

## 먼저 실행

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\02_exception-debugging\01_try_except_basic.py
python .\02_python-advanced\02_exception-debugging\03_read_json_safely.py
```

## 해야 할 일

`02_raise_validation.py`의 질문 목록에 빈 문자열과 정상 질문을 하나씩 추가합니다.

예:

```python
questions = ["FastAPI란?", "   ", "Supabase란?", "", "pytest는 왜 쓰나요?"]
```

실행 후 어떤 입력이 정상이고 어떤 입력이 오류 처리되는지 확인합니다.

## 완료 기준

```text
[ ] 정상 질문은 그대로 출력된다.
[ ] 빈 질문은 ValueError로 처리된다.
[ ] 프로그램이 중간에 멈추지 않고 끝까지 실행된다.
[ ] broken_config.json을 읽을 때 JSON 오류 메시지가 출력된다.
```

## 생각해 보기

```text
try/except가 없다면 프로그램은 어디에서 멈출까요?
FastAPI에서는 이런 오류를 어떤 응답으로 바꿀 수 있을까요?
```
