# Uvicorn 실행

FastAPI 코드는 Python 파일이지만, 웹 서버로 실행하려면 `uvicorn`이 필요합니다.

## 기본 실행 명령

`main.py`가 있는 폴더에서 실행합니다.

```powershell
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

## 명령 구조

```text
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
        ---- ---
         |    |
         |    └─ main.py 안에 있는 app 변수
         └──── main.py 파일
```

## 실행 위치가 중요한 이유

아래 명령은 `main.py`가 있는 폴더에서 실행해야 합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\01_fastapi-project-setup
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

다른 폴더에서 실행하면 `main.py`를 찾지 못해 아래와 같은 오류가 날 수 있습니다.

```text
Error loading ASGI app
```

## 포트 변경

기본 포트 `8000`이 이미 사용 중이면 다른 포트로 실행합니다.

```powershell
uvicorn main:app --reload --port 8001
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload --port 8001
```

이 경우 접속 주소도 바뀝니다.

```text
http://127.0.0.1:8001/docs
```

## 서버 종료

서버를 실행한 터미널에서 아래 키를 누릅니다.

```text
Ctrl + C
```

## 파일명 주의

`01_hello-fastapi.py`처럼 하이픈(`-`)이 들어간 파일도 수업에서는 `uvicorn 파일명:app` 형태를 확인합니다. 다만 실제 프로젝트에서는 import 경로를 단순하게 유지하기 위해 `main.py`, `app.py`, `server.py`처럼 단순한 파일명을 권장합니다.
