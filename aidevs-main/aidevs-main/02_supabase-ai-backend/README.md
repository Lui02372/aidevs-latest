# 02_supabase-ai-backend

FastAPI, LLM API, Supabase를 연결해 AI 백엔드 개발의 기본 흐름을 학습하는 과정입니다.

이 과정은 초보자가 제한된 시간 안에 백엔드의 핵심 흐름을 직접 실행해 보는 것을 목표로 합니다. Python/Git 기초는 `01_python-git-foundation`에서 먼저 다루고, 여기서는 FastAPI 서버, LLM 호출, Supabase 저장과 인증, 간단한 캐시 흐름에 집중합니다.

## 과정 목표

- FastAPI로 REST API 서버를 만들고 Swagger UI에서 테스트합니다.
- Pydantic으로 요청 데이터와 응답 구조를 검증합니다.
- mock-first 방식으로 비용 없이 API 흐름을 먼저 확인합니다.
- Gemini SDK를 기본 LLM 호출 방식으로 사용합니다.
- OpenAI SDK 예제는 선택 비교 자료로만 다룹니다.
- Supabase 테이블 CRUD, Auth, JWT, RLS의 역할을 이해합니다.
- Upstash Redis로 TTL 기반 캐시의 최소 흐름을 확인합니다.
- Codex를 활용해 오류를 분석하고 코드 리뷰 결과를 정리합니다.
- 최종 프로젝트에서 01~03에서 배운 내용을 하나의 백엔드 결과물로 정리합니다.

## 진행 순서

1. `SETUP.md`를 보고 `02_supabase-ai-backend` 폴더의 `.venv`를 준비합니다.
2. `pip install -r requirements.txt`로 공통 패키지를 설치합니다.
3. `01_fastapi-backend`에서 FastAPI의 기본 실행 흐름을 익힙니다.
4. `02_llm-api-integration`에서 mock, Gemini SDK, OpenAI 선택 비교 흐름을 확인합니다.
5. `03_supabase-db-and-auth`에서 Supabase CRUD, Auth/JWT/RLS, Redis 캐시를 실습합니다.
6. `90_ai-assisted-code-review-and-debugging`에서 앞 실습의 오류와 리뷰 방법을 정리합니다.
7. `99_final-backend-project`에서 최종 프로젝트를 설계하고 제출 기준을 점검합니다.

이 과정에서는 하위 단원마다 `.venv`를 따로 만들지 않고, `02_supabase-ai-backend` 최상위의 `.venv` 하나를 사용합니다.

## 과정 구조

```text
02_supabase-ai-backend
├─ 01_fastapi-backend
├─ 02_llm-api-integration
├─ 03_supabase-db-and-auth
├─ 90_ai-assisted-code-review-and-debugging
└─ 99_final-backend-project
```

`00_references`는 공통 참고 자료입니다. 수업 흐름의 필수 순서에 넣기보다는 API key 보안, AI 리터러시, 프롬프트 작성 기준이 필요할 때 참고합니다.

## 단원 역할

| 단원 | 역할 |
| --- | --- |
| `01_fastapi-backend` | FastAPI, HTTP Method, REST API, Pydantic, async, 오류 처리, Swagger/Postman 테스트를 학습합니다. |
| `02_llm-api-integration` | LLM API 개념, API key와 비용, mock-first, Gemini SDK 싱글턴/멀티턴 호출, FastAPI LLM endpoint를 학습합니다. |
| `03_supabase-db-and-auth` | Supabase 프로젝트, 테이블 CRUD, FastAPI 연동, Auth/JWT/RLS, 대화 로그 저장, Upstash Redis 캐시를 학습합니다. |
| `90_ai-assisted-code-review-and-debugging` | 01~03에서 만난 오류를 Codex와 함께 분석하고, 코드 리뷰와 보안 점검 방법을 연습합니다. |
| `99_final-backend-project` | 01~03에서 배운 내용을 바탕으로 작은 AI 백엔드 프로젝트를 설계하고 제출합니다. |

## 필수와 선택 기준

| 구분 | 내용 |
| --- | --- |
| 필수 | FastAPI 기본 API, Pydantic 검증, mock-first LLM 호출, Gemini SDK 기본 호출, Supabase CRUD, Auth/JWT/RLS 개념, Swagger 테스트 |
| 선택 | OpenAI 비교 예제, Upstash Redis 캐시 확장, 구조 분리 리팩토링, 추가 테스트 코드 |
| 제외 | Streamlit/React 화면, SSE 스트리밍, Docker Compose, AWS 배포, 운영 모니터링 |

화면과 API 연동은 `03_supabase-ai-frontend`, SSE 기반 통합 프로젝트는 `04_supabase-ai-mini-project`, Docker/AWS/GitHub Actions 운영은 `07_multi-agent-service-ops`에서 다룹니다.

## 공통 실행 준비

자세한 환경 준비는 [SETUP.md](./SETUP.md)를 참고합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
pip install -r requirements.txt
```

정상이라면 Python 경로가 아래처럼 `02_supabase-ai-backend\.venv`를 가리켜야 합니다.

```text
C:\aidev\02_supabase-ai-backend\.venv\Scripts\python.exe
```

## 막혔을 때 바로 보기

| 막히는 지점 | 확인 문서 |
| --- | --- |
| Python, `.venv`, 패키지 설치 | [SETUP.md](./SETUP.md) |
| FastAPI 실행 오류와 포트 충돌 | [공통 트러블슈팅](../00_course-guide/03_learning-support/troubleshooting.md), [01_fastapi-backend](./01_fastapi-backend/README.md) |
| Gemini/OpenAI API key, 비용, 호출 제한 | [API key and billing](./02_llm-api-integration/02_api-key-and-billing/README.md) |
| Supabase 프로젝트, RLS, service role key 구분 | [Supabase DB and Auth](./03_supabase-db-and-auth/README.md), [환경 변수와 key 관리](./03_supabase-db-and-auth/00_references/env-and-secret-management.md) |
| 오류 메시지를 어떻게 물어봐야 할지 모름 | [90_ai-assisted-code-review-and-debugging](./90_ai-assisted-code-review-and-debugging/README.md) |

## 다음 과정으로 넘어가기 전

- `uvicorn`으로 FastAPI 앱을 실행할 수 있어야 합니다.
- Swagger UI에서 요청을 보내고 응답을 확인할 수 있어야 합니다.
- `.env`와 `.env.example`의 차이를 설명할 수 있어야 합니다.
- Supabase `anon key`와 `service_role key`의 차이를 설명할 수 있어야 합니다.
- LLM 호출이 mock인지 실제 Gemini 호출인지 구분할 수 있어야 합니다.
- 오류가 발생했을 때 실행 명령, 오류 메시지, 기대 결과를 함께 정리할 수 있어야 합니다.
