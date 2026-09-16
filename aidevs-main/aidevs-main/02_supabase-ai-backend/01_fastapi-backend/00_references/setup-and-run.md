# FastAPI 설치와 실행

## 설치

```powershell
pip install fastapi uvicorn
```

## 실행

`main.py`가 있는 폴더에서 실행합니다.

```powershell
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

## 접속 주소

```text
API 서버: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
```

## 실행 명령 의미

```text
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

- `main`: `main.py` 파일
- `app`: FastAPI 인스턴스 변수명
- `--reload`: 코드 변경 시 서버 자동 재시작

