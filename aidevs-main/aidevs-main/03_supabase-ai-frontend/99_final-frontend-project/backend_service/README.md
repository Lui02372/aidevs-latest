# Backend Service

`backend_service`는 `99_final-frontend-project`에서 실제 서비스 연결과 배포 실습을 할 때 사용하는 FastAPI 백엔드입니다.

프론트엔드가 호출하는 API 주소와 응답 구조는 `backend_mock`과 최대한 동일하게 유지합니다. 그래서 Streamlit 앱은 `API_BASE_URL`만 바꾸면 mock backend에서 service backend로 전환할 수 있습니다.

## 언제 사용하나요?

| 구분 | 사용 시점 |
| --- | --- |
| `backend_mock` | 프론트 화면, 로그인 상태, 챗봇 UI, 대화 기록 UI를 빠르게 만들 때 |
| `backend_service` | Supabase Auth, Supabase DB, Gemini API, Upstash Redis, Render 배포까지 연결할 때 |

수업 시간이 부족하면 `backend_mock`만 필수로 진행하고, `backend_service`는 선택/심화 또는 참고 자료로 다룹니다.

## 폴더 구조

```text
backend_service
├─ README.md
├─ requirements.txt
├─ .env.example
├─ schema.sql
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
│     ├─ cache_service.py
│     ├─ chat_service.py
│     ├─ gemini_service.py
│     ├─ log_service.py
│     └─ supabase_service.py
└─ tests
   └─ test_service_app_routes.py
```

## 준비 순서

1. Supabase 프로젝트를 만들고 `schema.sql`을 SQL Editor에서 실행합니다.
2. Supabase Auth에서 이메일 가입 방식을 확인합니다.
3. Gemini API key를 준비합니다.
4. 선택 사항으로 Upstash Redis REST URL/TOKEN을 준비합니다.
5. `.env.example`을 참고해 `.env`를 만듭니다.

## 실행 방법

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service
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

### HTTP 500: supabase 패키지가 설치되어 있지 않습니다

다음 오류가 나오면 `backend_service`에 필요한 패키지가 설치되지 않은 상태입니다.

```text
HTTP 500: {"detail":"supabase 패키지가 설치되어 있지 않습니다. pip install -r requirements.txt를 실행하세요."}
```

`03_supabase-ai-frontend` 가상환경이 활성화된 상태에서 아래 명령을 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
```

설치 확인:

```powershell
python -c "import supabase, google.genai, httpx; print('backend_service packages installed')"
```

그 다음 서버를 다시 실행합니다.

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### HTTP 500: frontend_service_logs 또는 frontend_chat_logs 테이블을 찾을 수 없음

다음과 비슷한 오류가 나오면 Supabase 프로젝트에 필요한 테이블이 아직 만들어지지 않은 상태입니다.

```text
Could not find the table 'public.frontend_service_logs' in the schema cache
Could not find the table 'public.frontend_chat_logs' in the schema cache
```

해결 방법:

1. Supabase Dashboard로 이동합니다.
2. 현재 `.env`의 `SUPABASE_URL`과 같은 프로젝트인지 확인합니다.
3. SQL Editor를 엽니다.
4. `backend_service/schema.sql` 전체 내용을 복사해 실행합니다.
5. FastAPI 서버를 재시작합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

로그인은 성공했는데 서비스 로그 저장 중 오류가 난 경우에도 원인은 같습니다. `schema.sql`을 실행하면 `/chat`, `/conversations`, `/service-logs`까지 정상적으로 이어집니다.

## Authorization 사용 흐름

`backend_service`는 Supabase Auth가 발급한 `access_token`을 사용합니다. 프론트엔드에서 사용하는 방식은 `backend_mock`과 같습니다.

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

`backend_mock`에서 사용하던 프론트엔드 코드는 `API_BASE_URL`만 `backend_service` 주소로 바꾸면 같은 Authorization 방식으로 연결할 수 있습니다.

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

이미 가입된 이메일이라는 오류가 나오면 `student2@example.com`처럼 다른 이메일로 바꿔 테스트합니다.

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
  "message": "내 대화 이력을 바탕으로 오늘 학습한 내용을 세 줄로 요약해줘."
}
```

6. `GET /me`, `GET /conversations`, `GET /service-logs`를 실행해 Supabase에 저장된 데이터가 조회되는지 확인합니다.

## 제공 API

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | backend 실행 상태 확인 |
| POST | `/auth/signup` | Supabase Auth 회원가입, 사용자 정보 반환 |
| POST | `/auth/signin` | Supabase Auth 로그인과 access token 발급 |
| POST | `/auth/signout` | 현재 token 로그아웃 |
| GET | `/me` | 현재 로그인 사용자 정보 조회 |
| POST | `/chat` | Gemini 응답 생성, 선택형 Redis 캐시, Supabase 대화 기록 저장 |
| GET | `/conversations` | 현재 사용자 대화 기록 조회 |
| GET | `/service-logs` | 현재 사용자 서비스 로그 조회 |

## 이메일 인증 주의

Supabase Auth에서 `Confirm email`이 켜져 있으면 회원가입 직후 바로 로그인되지 않을 수 있습니다.

이 경우 수강생은 다음 순서로 진행합니다.

1. `/auth/signup`으로 회원가입합니다.
2. 이메일함에서 인증 메일을 확인합니다.
3. 인증 링크를 누른 뒤 `/auth/signin`으로 로그인합니다.

수업 중 인증 메일 대기가 길어지면 Supabase Auth 설정에서 이메일 인증을 잠시 끄고 진행할 수 있습니다.

## 테스트

이 테스트는 Supabase/Gemini를 실제 호출하지 않고, FastAPI route가 로드되는지만 확인합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pytest tests -q
```

## 실행 파일이 차단될 때

일부 교육장 PC나 회사 PC에서는 Windows 애플리케이션 제어 정책 때문에 `uvicorn.exe`, `pytest.exe` 같은 실행 파일이 차단될 수 있습니다.

이 경우 아래처럼 `.exe`를 직접 실행하지 말고 Python 모듈 실행 방식으로 실행합니다.

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python -m pytest tests -q
```

## 배포 참고

Render 배포 시 시작 명령은 다음과 같습니다.

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

환경변수는 Render의 Environment 메뉴에 등록합니다. `SUPABASE_SERVICE_ROLE_KEY`, `GEMINI_API_KEY`, `UPSTASH_REDIS_REST_TOKEN`은 프론트엔드나 GitHub에 올리지 않습니다.
