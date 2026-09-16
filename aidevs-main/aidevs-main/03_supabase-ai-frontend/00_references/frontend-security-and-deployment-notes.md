# Frontend Security And Deployment Notes

이 문서는 프론트엔드 수업에서 반드시 구분해야 하는 보안과 배포 기준을 정리합니다.

## 프론트엔드에 두어도 되는 값

```text
API_BASE_URL
화면 표시용 설정값
사용자가 직접 입력한 값
```

`API_BASE_URL`은 프론트엔드가 호출할 백엔드 주소입니다. 예를 들어 로컬에서는 다음 값을 사용할 수 있습니다.

```env
API_BASE_URL=http://127.0.0.1:8000
```

기본 단원 실습에서는 다음 파일에 값을 적습니다.

```text
C:\aidev\03_supabase-ai-frontend\.env
```

`99_final-frontend-project`의 Streamlit 앱도 수업 중에는 같은 과정 최상위 `.env`를 사용합니다.

```text
C:\aidev\03_supabase-ai-frontend\.env
```

Render에 백엔드를 배포한 뒤에는 다음처럼 바꿉니다.

```env
API_BASE_URL=https://본인-render-service.onrender.com
```

`backend_service`의 Supabase/Gemini/Upstash 값은 프론트엔드 `.env`가 아니라 아래 backend 전용 `.env`에 둡니다.

```text
C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service\.env
```

## 실제 서비스용 프론트엔드에 두면 안 되는 값

```text
SUPABASE_SERVICE_ROLE_KEY
UPSTASH_REDIS_REST_TOKEN
GEMINI_API_KEY
OPENAI_API_KEY
비밀번호
관리자 token
```

이 값들은 노출되면 비용, 데이터, 권한 문제가 생길 수 있습니다. 반드시 백엔드 또는 배포 서비스의 환경변수에 저장합니다.

`05_ai-chatbot-interface`에서도 Gemini/OpenAI API를 프론트엔드에서 직접 호출하지 않습니다. 챗봇 화면은 mock 응답 또는 백엔드 API 응답을 표시하는 역할만 맡고, 실제 서비스 구조에서는 FastAPI 백엔드가 Gemini/OpenAI API를 호출합니다.

- GitHub에 `.env`를 올리지 않습니다.
- 배포용 Streamlit Secrets에 LLM API key를 넣지 않습니다.
- 실제 서비스 구조에서는 FastAPI 백엔드가 Gemini/OpenAI API를 호출하고, Streamlit은 백엔드 API만 호출합니다.

## 배포 후 자주 틀리는 부분

| 문제 | 원인 | 확인 방법 |
| --- | --- | --- |
| Streamlit에서 API 연결 실패 | `API_BASE_URL`이 로컬 주소로 남아 있음 | 배포 후 Render URL로 바꿉니다. |
| 로그인은 되지만 데이터 조회 실패 | Authorization header 누락 | `Bearer token` 형식인지 확인합니다. |
| Render 백엔드가 실행되지 않음 | Start Command 오류 | 99의 `backend_service`는 `uvicorn app.main:app --host 0.0.0.0 --port $PORT`를 사용합니다. |
| Redis 인증 실패 | Upstash token 누락 또는 오타 | 환경변수 이름과 값을 확인합니다. |
| Supabase 권한 오류 | RLS 또는 service role 처리 위치 문제 | 프론트엔드가 아니라 백엔드 설정을 확인합니다. |

## 03 과정의 배포 참고 위치

무료 배포 흐름은 필수 구현이 아니라 선택 참고입니다. 수업 중 짧게 확인할 때는 아래 문서를 봅니다.

```text
C:\aidev\03_supabase-ai-frontend\04_state-session-and-data\06_service-log-and-integration-check\03_free-deployment-guide.md
C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\templates\06_deployment-checklist.md
```

이 문서는 다음 흐름을 기준으로 합니다.

```text
FastAPI 백엔드 -> Render
Redis 캐시/세션 보조 저장소 -> Upstash
Streamlit 프론트엔드 -> Streamlit Community Cloud
```

Docker Compose, AWS, GitHub Actions 기반 운영 자동화는 `07_multi-agent-service-ops`에서 다룹니다.

## 수업용 배포 점검 질문

```text
프론트엔드 주소는 무엇인가요?
백엔드 주소는 무엇인가요?
프론트엔드가 백엔드 주소를 어디에서 읽나요?
99 최종 프로젝트는 어떤 .env 파일을 읽나요?
Supabase service role key는 어디에 있나요?
Upstash token은 어디에 있나요?
API 호출이 실패하면 어떤 순서로 확인해야 하나요?
```
