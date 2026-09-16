# 03_supabase-ai-frontend

Streamlit으로 AI 서비스 화면을 만들고, FastAPI 백엔드를 호출하는 프론트엔드 과정입니다.

이 과정의 핵심은 “프론트엔드가 직접 Supabase나 LLM API key를 다루지 않고, 백엔드 API를 호출해 화면에 표시한다”는 흐름을 익히는 것입니다. 초보자 기준으로 화면 구성, API 호출, 로딩/오류 처리, 대화 UI, 로그인 상태 관리에 집중합니다.

## 과정 목표

- Streamlit 앱을 실행하고 기본 화면을 구성합니다.
- 버튼, 입력창, 폼, 표, 차트, 파일 업로드 UI를 사용합니다.
- `API_BASE_URL`을 기준으로 FastAPI 백엔드를 호출합니다.
- API 호출 중 로딩 상태와 오류 메시지를 화면에 표시합니다.
- 챗봇 UI에서 사용자 메시지와 assistant 응답을 구분해 보여 줍니다.
- `st.session_state`로 로그인 token, 입력값, 대화 상태를 관리합니다.
- Authorization header로 보호된 백엔드 API를 호출하는 흐름을 이해합니다.
- 대화 이력과 서비스 로그를 프론트엔드에서 조회합니다.
- AI 보조 도구로 Streamlit 오류와 UI 구조를 점검합니다.

## 진행 순서

1. `SETUP.md`를 보고 `03_supabase-ai-frontend` 폴더의 `.venv`를 준비합니다.
2. `pip install -r requirements.txt`로 공통 패키지를 설치합니다.
3. `01_streamlit-basic`에서 Streamlit 기본 실행과 화면 출력을 익힙니다.
4. `02_streamlit-ui-components`에서 입력, 폼, 표, 차트를 연습합니다.
5. `03_api-integration`에서 샘플 백엔드로 API 호출 흐름을 연습합니다.
6. `04_state-session-and-data`에서 session state, token, Authorization header, 대화 이력 조회를 다룹니다.
7. `05_ai-chatbot-interface`에서 mock 기반 챗봇 UI와 백엔드 chat API 연결을 다룹니다.
8. `06_streamlit-multipage-app`에서 `st.Page`, `st.navigation()` 기반 왼쪽 메뉴 구조를 연습합니다.
9. `07_streamlit-tabs-app`에서 `st.tabs()` 기반 탭 구조와 `tab_pages` 파일 분리를 연습합니다.
10. `90_ai-assisted-ui-review-and-debugging`에서 오류 분석과 UI 리뷰를 정리합니다.
11. `99_final-frontend-project`에서 `backend_mock`으로 개인화 AI 챗봇 통합 UX를 완성하고, 선택적으로 `backend_service`로 실제 Supabase/Gemini/배포 흐름을 확인합니다.

이 과정에서는 하위 폴더마다 `.venv`를 따로 만들지 않고, `03_supabase-ai-frontend` 최상위의 `.venv` 하나를 사용합니다.

## 과정 구조

```text
03_supabase-ai-frontend
├─ 01_streamlit-basic
├─ 02_streamlit-ui-components
├─ 03_api-integration
├─ 04_state-session-and-data
├─ 05_ai-chatbot-interface
├─ 06_streamlit-multipage-app
├─ 07_streamlit-tabs-app
├─ 90_ai-assisted-ui-review-and-debugging
└─ 99_final-frontend-project
```

`00_references`는 공통 참고 자료입니다. 필수 진도에 넣기보다는 보안 기준, 배포 범위, SSE 학습 위치, Streamlit/React 비교가 필요할 때 확인합니다.
Streamlit 전체 사용법이 필요하면 [Streamlit 사용 가이드](./00_references/streamlit-usage-guide.md)를 먼저 확인합니다.

## 단원 역할

| 단원 | 역할 |
| --- | --- |
| `01_streamlit-basic` | Streamlit 실행, 텍스트 출력, 입력값 처리, 기본 레이아웃을 학습합니다. |
| `02_streamlit-ui-components` | 버튼, 폼, 표, 차트, 파일 업로드, 간단한 대시보드 구성을 학습합니다. |
| `03_api-integration` | `httpx`로 FastAPI API를 호출하고, 로딩/오류/응답 검증을 화면에 표시합니다. |
| `04_state-session-and-data` | `st.session_state`, 로그인 token, Authorization header, 대화 이력, 서비스 로그 조회를 다룹니다. |
| `05_ai-chatbot-interface` | mock 응답 중심으로 챗봇 UI, 프롬프트 입력, 대화 미리보기, 챗봇 전용 백엔드 호출을 구성합니다. |
| `06_streamlit-multipage-app` | Streamlit `st.Page`, `st.navigation()` 구조로 회원가입, 로그조회, Chat, 데이터베이스조회 화면을 나누고 팀 개발 방식을 연습합니다. |
| `07_streamlit-tabs-app` | Streamlit `st.tabs()` 구조로 한 화면 안에서 탭을 전환하고, `tab_pages`로 탭별 코드를 분리하는 방식을 연습합니다. |
| `90_ai-assisted-ui-review-and-debugging` | Streamlit 실행 오류, API 연결 실패, session state 문제를 AI와 함께 분석합니다. |
| `99_final-frontend-project` | `backend_mock`으로 회원가입/로그인/챗봇/대화 기록/서비스 로그 UX를 통합하고, 선택적으로 `backend_service`로 Supabase/Gemini/배포 흐름을 연결합니다. 완성 예제는 탭 방식 `solution_tabs`와 멀티페이지 방식 `solution_multipage` 중 선택해 확인합니다. |

## 필수와 선택 기준

| 구분 | 내용 |
| --- | --- |
| 필수 | Streamlit 기본 화면, UI 컴포넌트, `API_BASE_URL`, FastAPI 호출, 로딩/오류 표시, 챗봇 UI, 회원가입/로그인, session state, Authorization header |
| 선택 | `backend_service` 실제 연결, React 구조 비교, 백엔드 실제 LLM 응답 연결, 무료 배포 안내, 추가 차트/캐시 최적화 |
| 제외 | Supabase DB 직접 접속, service role key 사용, LLM API key를 프론트엔드에 저장, SSE 본격 구현, Docker/AWS 운영 자동화 |

SSE 기반 실시간 응답 스트리밍은 `04_supabase-ai-mini-project`에서 백엔드 SSE endpoint, Streamlit 표시, Supabase 최종 메시지 저장을 함께 연결하며 다룹니다. Docker, AWS, GitHub Actions 기반 운영 자동화는 `07_multi-agent-service-ops`에서 다룹니다.

## 프론트엔드와 백엔드 역할

03 과정에서는 백엔드를 단계별로 다르게 사용합니다.

| 구분 | 사용 위치 | 역할 |
| --- | --- | --- |
| 샘플 백엔드 | `03_api-integration/00_sample_backend` | API 호출, 로딩, 오류 처리를 연습합니다. |
| 챗봇 샘플 백엔드 | `05_ai-chatbot-interface/00_sample_backend` | `/api/chat/mock`, `/api/chat/gemini`으로 챗봇 UI 연동을 연습합니다. |
| 02 과정 백엔드 | `02_supabase-ai-backend` | Supabase, Auth, Gemini가 포함된 실제 백엔드 흐름을 연결합니다. |
| `backend_mock` | `99_final-frontend-project` | 최종 프론트 UX를 끊기지 않게 완성하기 위한 필수 제공 백엔드입니다. |
| `backend_service` | `99_final-frontend-project` | Supabase/Gemini/Upstash/Render 배포를 연결하는 선택/심화 백엔드입니다. |

기본 호출 흐름은 다음과 같습니다.

```text
사용자
-> Streamlit 화면
-> API_BASE_URL 기준 httpx 요청
-> FastAPI 백엔드
-> 필요 시 Gemini/Supabase/Auth 처리
-> JSON 응답
-> Streamlit 화면 표시
```

프론트엔드는 Supabase `service_role` key, Gemini API key, OpenAI API key, Upstash token을 직접 가지지 않습니다. 이런 값은 백엔드 `.env`에서 관리합니다.

## 공통 실행 준비

자세한 환경 준비는 [SETUP.md](./SETUP.md)를 참고합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

정상이라면 Python 경로가 아래처럼 `03_supabase-ai-frontend\.venv`를 가리켜야 합니다.

```text
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\python.exe
```

가장 작은 Streamlit 실행 예시는 다음과 같습니다.

```powershell
streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

## 막혔을 때 바로 보기

| 막히는 지점 | 확인 문서 |
| --- | --- |
| Streamlit 실행 오류 | [SETUP.md](./SETUP.md), [공통 트러블슈팅](../00_course-guide/03_learning-support/troubleshooting.md) |
| Streamlit 기본 사용법 | [Streamlit 사용 가이드](./00_references/streamlit-usage-guide.md) |
| 백엔드 연결 실패 | [03_api-integration](./03_api-integration/README.md), [02 Backend SETUP](../02_supabase-ai-backend/SETUP.md) |
| `API_BASE_URL` 또는 `.env` 위치 | [SETUP.md](./SETUP.md), [프론트 보안 참고](./00_references/frontend-security-and-deployment-notes.md) |
| token과 Authorization header | [04_state-session-and-data](./04_state-session-and-data/README.md) |
| Streamlit 왼쪽 메뉴 구조와 팀 개발 방식 | [06_streamlit-multipage-app](./06_streamlit-multipage-app/README.md) |
| Streamlit tabs 구조와 탭별 파일 분리 | [07_streamlit-tabs-app](./07_streamlit-tabs-app/README.md) |
| 99 최종 프로젝트 실행 | [99 README](./99_final-frontend-project/README.md), [final checklist](./99_final-frontend-project/checklist/final-checklist.md) |
| 배포 기준 | [deployment checklist](./99_final-frontend-project/templates/06_deployment-checklist.md) |
| Streamlit 오류를 어떻게 물어볼지 모름 | [90_ai-assisted-ui-review-and-debugging](./90_ai-assisted-ui-review-and-debugging/README.md) |

## 04 미니 프로젝트 연결

03 과정에서는 Streamlit 화면 구성, API 호출, 로그인 상태 관리, 챗봇 UI를 먼저 익힙니다. FastAPI backend, Supabase DB, Redis/SSE, Streamlit 대시보드를 함께 연결하는 실시간 로그 대시보드 통합 실습은 [04_supabase-ai-mini-project/01_realtime-log-dashboard-practice](../04_supabase-ai-mini-project/01_realtime-log-dashboard-practice/README.md)에서 진행합니다.
## 다음 과정으로 넘어가기 전

- `streamlit run`으로 앱을 실행할 수 있어야 합니다.
- `.env`의 `API_BASE_URL`이 어떤 역할인지 설명할 수 있어야 합니다.
- 백엔드가 꺼져 있을 때 오류 메시지를 화면에 표시할 수 있어야 합니다.
- 프론트엔드에 `SUPABASE_SERVICE_ROLE_KEY`를 두면 안 되는 이유를 설명할 수 있어야 합니다.
- 로그인 token을 `st.session_state`에 저장하고 Authorization header로 보내는 흐름을 설명할 수 있어야 합니다.
- SSE는 왜 `04_supabase-ai-mini-project`에서 다루는지 설명할 수 있어야 합니다.
