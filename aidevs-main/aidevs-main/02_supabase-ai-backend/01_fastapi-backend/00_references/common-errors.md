# FastAPI 자주 발생하는 오류

## ModuleNotFoundError: No module named 'fastapi'

FastAPI가 설치되지 않은 상태입니다.

```powershell
pip install fastapi uvicorn
```

## Error loading ASGI app

`uvicorn main:app --reload`에서 파일명 또는 변수명이 맞지 않을 때 발생합니다.

확인할 것:

- 파일명이 `main.py`인가
- FastAPI 인스턴스 이름이 `app`인가
- 현재 위치가 `main.py`가 있는 폴더인가

## 422 Unprocessable Entity

요청 데이터가 Pydantic 모델과 맞지 않을 때 발생합니다.

확인할 것:

- 필수 필드를 보냈는가
- 숫자/문자열 타입이 맞는가
- JSON 형식이 올바른가

