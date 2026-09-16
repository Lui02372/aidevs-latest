# 00_sample_backend

`03_api-integration` 실습을 위한 최소 FastAPI 백엔드입니다.

이 백엔드는 실제 서비스용이 아니라 Streamlit 프론트엔드가 API를 호출하고 JSON 응답을 화면에 표시하는 흐름을 연습하기 위한 보조 서버입니다. 챗봇 API, Supabase 저장, Gemini SDK 호출, 로그인 인증은 여기서 다루지 않습니다.

챗봇 전용 mock/Gemini 백엔드는 `05_ai-chatbot-interface/00_sample_backend`에서 다룹니다.

## 제공 API

| Method | URL | 역할 |
| --- | --- | --- |
| `GET` | `/health` | 백엔드 서버가 실행 중인지 확인합니다. |
| `GET` | `/api/courses` | 과정 목록을 JSON으로 반환합니다. |
| `POST` | `/api/message` | 프론트엔드가 보낸 이름과 메시지를 받아 mock 응답을 반환합니다. |
| `POST` | `/api/score-feedback` | 점수를 받아 조건에 맞는 피드백 문장을 반환합니다. |

## 실행 방법

PowerShell을 하나 열고 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\03_api-integration\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

브라우저에서 아래 주소를 열어 확인합니다.

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 사용 기준

```text
03_api-integration
-> 이 sample backend를 사용해 API 호출과 응답 처리 흐름을 연습합니다.

04_state-session-and-data
-> 응답 결과를 session_state와 대화 이력 구조에 누적합니다.
```

실제 Supabase 저장과 인증 흐름은 `02_supabase-ai-backend`와 연결해 확인합니다.
