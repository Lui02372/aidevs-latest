# 00_sample_backend

`04_state-session-and-data` 실습용 FastAPI 샘플 백엔드입니다.

이 서버는 Supabase Auth를 직접 사용하지 않습니다. 초보자가 회원가입, 로그인, access token 저장, Authorization header, 로그인 후 화면 전환을 먼저 이해할 수 있도록 만든 mock 백엔드입니다.

## 실행 방법

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

확인 주소:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 기본 계정

```text
username: student
password: 1234
```

새 계정은 `/api/signup`으로 만들 수 있습니다. 단, 이 백엔드는 메모리 안에만 데이터를 저장하므로 서버를 재시작하면 새로 가입한 계정은 사라집니다.

## 제공 API

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | 서버 실행 상태 확인 |
| POST | `/api/signup` | 수업용 회원가입 |
| POST | `/api/login` | 로그인 후 access token 발급 |
| GET | `/api/me` | Authorization header로 현재 사용자 조회 |
| GET | `/api/conversations` | 보호된 대화 이력 조회 |
| POST | `/api/conversations` | 보호된 대화 메시지 저장 |
| GET | `/api/service-logs` | 보호된 서비스 로그 조회 |

## token 흐름

```text
Streamlit 회원가입/로그인 화면
-> POST /api/login
-> access_token 응답 수신
-> st.session_state.access_token에 저장
-> Authorization: Bearer access_token header 구성
-> GET /api/me 같은 보호된 API 호출
-> 로그인 상태 화면 표시
```

실제 서비스에서는 Supabase Auth가 JWT를 발급하고, FastAPI 백엔드가 JWT를 검증한 뒤 Supabase RLS와 연결합니다. 이 샘플은 그 전에 화면 상태 흐름을 익히기 위한 단계입니다.
