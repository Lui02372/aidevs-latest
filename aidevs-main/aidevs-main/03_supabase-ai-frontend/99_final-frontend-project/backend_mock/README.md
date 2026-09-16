# Backend Mock

`backend_mock`은 `99_final-frontend-project`에서 프론트엔드 UX 실습을 안정적으로 진행하기 위한 제공용 mock backend입니다.

이 backend는 Supabase Auth, Gemini API, Upstash Redis를 사용하지 않습니다. 기본 저장소는 메모리이며, 서버를 재시작하면 회원, 대화 기록, 서비스 로그가 초기화됩니다.

## 언제 사용하나요?

수강생이 Streamlit 화면을 만들 때는 먼저 `backend_mock`을 사용합니다.

- 회원가입/로그인 화면 만들기
- `access_token`을 `st.session_state`에 저장하기
- `Authorization: Bearer ...` header 보내기
- 챗봇 UI와 대화 기록 UI 만들기
- 서비스 로그를 표로 표시하기

실제 Supabase/Gemini/Redis 연결은 같은 프로젝트의 `backend_service`에서 선택/심화로 진행합니다.

## 폴더 구조

```text
backend_mock
├─ README.md
├─ requirements.txt
├─ app
│  ├─ main.py
│  ├─ core
│  │  ├─ config.py
│  │  └─ security.py
│  ├─ routers
│  │  ├─ auth_router.py
│  │  ├─ chat_router.py
│  │  └─ log_router.py
│  ├─ schemas
│  │  ├─ auth_schema.py
│  │  ├─ chat_schema.py
│  │  └─ log_schema.py
│  └─ services
│     ├─ auth_service.py
│     ├─ chat_service.py
│     ├─ log_service.py
│     └─ memory_store.py
└─ tests
   └─ test_backend_api.py
```

## 실행 방법

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 자주 나는 오류

### HTTP 500 또는 ModuleNotFoundError: 패키지가 설치되어 있지 않음

다음과 비슷한 오류가 나오면 `backend_mock`에 필요한 패키지가 설치되지 않은 상태입니다.

```text
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'httpx'
```

`03_supabase-ai-frontend` 가상환경이 활성화된 상태에서 아래 명령을 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
```

설치 확인:

```powershell
python -c "import fastapi, uvicorn, httpx; print('backend_mock packages installed')"
```

그 다음 서버를 다시 실행합니다.

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Authorization 사용 흐름

`backend_mock`과 `backend_service`는 같은 Authorization 방식을 사용합니다.

```text
Authorization: Bearer <access_token>
```

진행 순서는 다음과 같습니다.

1. `/auth/signin`으로 로그인합니다.
2. 응답의 `access_token`을 복사합니다.
3. Swagger UI에서는 오른쪽 위 `Authorize` 버튼을 누르고 `access_token` 값만 입력합니다.
4. Streamlit에서는 `st.session_state.access_token`에 저장합니다.
5. 보호된 API를 호출할 때 아래 header를 보냅니다.

```python
headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
```

주의: Swagger UI의 `Authorize` 입력칸에는 `Bearer`를 붙이지 않습니다. Swagger가 자동으로 `Authorization: Bearer <access_token>` header를 만들어 보냅니다. Streamlit 코드에서 직접 header를 만들 때만 `Bearer`를 붙입니다.

`backend_mock`의 token은 수업용 문자열입니다. 실제 Supabase JWT는 아니지만, 프론트엔드에서는 `backend_service`와 같은 방식으로 다룹니다.

## Swagger 테스트용 샘플 데이터

Swagger UI에서 아래 순서로 테스트합니다.

1. `POST /auth/signup`

```json
{
  "email": "student@example.com",
  "password": "pass1234",
  "display_name": "수강생"
}
```

2. `POST /auth/signin`

```json
{
  "email": "student@example.com",
  "password": "pass1234"
}
```

3. 로그인 응답의 `access_token` 값을 복사합니다.
4. Swagger UI 오른쪽 위 `Authorize` 버튼에 `access_token` 값만 입력합니다.
5. `POST /chat`

```json
{
  "message": "오늘 학습한 Streamlit 상태 관리 내용을 초보자에게 설명해줘."
}
```

6. `GET /me`, `GET /conversations`, `GET /service-logs`를 실행해 로그인 사용자 기준 데이터가 조회되는지 확인합니다.

`backend_mock`은 메모리 저장소를 사용하므로 서버를 재시작하면 위 회원가입 데이터도 초기화됩니다.

## 제공 API

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | backend 실행 상태 확인 |
| POST | `/auth/signup` | 수업용 회원가입 |
| POST | `/auth/signin` | 수업용 로그인과 mock access token 발급 |
| POST | `/auth/signout` | 현재 token 로그아웃 |
| GET | `/me` | 현재 로그인 사용자 정보 조회 |
| POST | `/chat` | mock AI 답변 생성과 대화 기록 저장 |
| GET | `/conversations` | 현재 사용자 대화 기록 조회 |
| GET | `/service-logs` | 현재 사용자 서비스 로그 조회 |

## 테스트

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pytest tests -q
```

## 실행 파일이 차단될 때

일부 교육장 PC나 회사 PC에서는 Windows 애플리케이션 제어 정책 때문에 `uvicorn.exe`, `pytest.exe` 같은 실행 파일이 차단될 수 있습니다.

예시:

```text
'pytest.exe' 프로그램을 실행하지 못했습니다.
애플리케이션 제어 정책에서 이 파일을 차단했습니다.
```

이 경우 아래처럼 `.exe`를 직접 실행하지 말고 Python 모듈 실행 방식으로 실행합니다.

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python -m pytest tests -q
```

가상환경이 제대로 잡혔는지 먼저 확인하려면 다음 명령을 실행합니다.

```powershell
python -c "import sys; print(sys.executable)"
```

정상이라면 `C:\aidev\03_supabase-ai-frontend\.venv\Scripts\python.exe`처럼 현재 과정의 `.venv` 아래 Python 경로가 출력됩니다.
