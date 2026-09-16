# Lab 01. 함수와 import

## 목표

하나의 긴 코드를 함수로 나누고, 다른 파일의 함수를 import해서 사용합니다.

## 먼저 실행

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\01_function-and-import\01_function_basic_review.py
python .\02_python-advanced\01_function-and-import\03_import_my_module.py
```

## 해야 할 일

`01_function-and-import/my_tools.py`에 아래 함수를 하나 추가합니다.

```python
def make_title(text: str) -> str:
    return f"[질문] {text.strip()}"
```

그 다음 `03_import_my_module.py`에서 `make_title`도 import해서 출력합니다.

## 완료 기준

```text
[ ] my_tools.py에 새 함수를 추가했다.
[ ] 03_import_my_module.py에서 새 함수를 import했다.
[ ] 실행 결과에 [질문] 문구가 출력된다.
```

## 생각해 보기

```text
왜 모든 함수를 한 파일에 두지 않고 my_tools.py로 나눌까요?
FastAPI 프로젝트에서는 이런 함수들이 어느 파일에 들어갈까요?
```
