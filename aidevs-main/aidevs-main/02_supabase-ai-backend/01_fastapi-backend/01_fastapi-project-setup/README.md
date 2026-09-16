# 01_fastapi-project-setup

FastAPI 프로젝트를 만들고 첫 API 서버를 실행하는 단원입니다.

이 단원에서는 복잡한 API를 만들기 전에 아래 흐름을 먼저 익힙니다.

```text
FastAPI 앱 만들기
-> uvicorn으로 서버 실행하기
-> 브라우저에서 API 확인하기
-> Swagger UI 열기
-> 서버 종료하기
```

## 이 폴더의 파일

| 파일 | 역할 |
| --- | --- |
| `main.py` | 기본 프로젝트 실행 흐름을 확인하는 FastAPI 앱 파일 |
| `01_hello-fastapi.py` | 첫 FastAPI 코드 구조를 읽고 독립 실행해 보는 학습용 파일 |
| `02_project-structure.md` | FastAPI 프로젝트 폴더 구조 설명 |
| `03_uvicorn-run.md` | `uvicorn` 실행 명령 설명 |

`01_hello-fastapi.py`처럼 파일명에 하이픈(`-`)이 들어 있는 단일 예제 파일도 수업에서는 `uvicorn 파일명:app` 방식으로 실행 형태를 확인합니다. 만약 `uvicorn` 명령이 실행 정책이나 경로 문제로 막히면 `python -m uvicorn 파일명:app` 방식으로 실행합니다. 기본 프로젝트 실행 흐름은 `main.py` 기준으로도 함께 확인합니다.

## 실행 전 준비

먼저 과정 루트로 이동하고 공통 가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
```

필요한 패키지가 설치되어 있는지 확인합니다.

```powershell
pip install -r requirements.txt
python -c "import fastapi, uvicorn; print('fastapi ready')"
```

## 서버 실행

`main.py`가 있는 폴더로 이동합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\01_fastapi-project-setup
```

서버를 실행합니다.

```powershell
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

명령의 의미는 다음과 같습니다.

```text
main:
  main.py 파일을 뜻합니다.

app:
  main.py 안에 있는 app = FastAPI() 변수를 뜻합니다.

--reload:
  코드를 수정하면 서버를 자동으로 다시 시작합니다.
```

## 브라우저에서 확인

서버가 실행되면 브라우저에서 아래 주소를 확인합니다.

```text
기본 API:
http://127.0.0.1:8000/

상태 확인 API:
http://127.0.0.1:8000/health

Swagger UI:
http://127.0.0.1:8000/docs
```

PowerShell에서도 확인할 수 있습니다.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

기대 결과:

```json
{
  "status": "ok"
}
```

## 서버 종료

서버를 실행한 터미널에서 아래 키를 누릅니다.

```text
Ctrl + C
```

## 핵심 코드 설명

```python
from fastapi import FastAPI
```

FastAPI 클래스를 가져옵니다.

```python
app = FastAPI()
```

API 서버 객체를 만듭니다. `uvicorn main:app --reload`에서 `app`이 바로 이 변수입니다.

```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

`GET /health` 주소를 만들고, 서버 상태를 JSON으로 반환합니다.

## 확인 질문

```text
1. uvicorn main:app --reload에서 main은 무엇을 뜻하나요?
2. app은 어떤 변수와 연결되나요?
3. /docs 주소에서는 무엇을 확인할 수 있나요?
4. Python dict가 브라우저에서는 어떤 형태로 보이나요?
5. 서버 종료는 어떤 키로 하나요?
```
