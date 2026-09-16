# Frontend Course Map

이 문서는 `03_supabase-ai-frontend` 과정의 전체 흐름을 한눈에 보기 위한 참고 자료입니다.

## 과정 흐름

```text
00_references
-> 01_streamlit-basic
-> 02_streamlit-ui-components
-> 03_api-integration
-> 04_state-session-and-data
-> 05_ai-chatbot-interface
-> 06_streamlit-multipage-app
-> 07_streamlit-tabs-app
-> 90_ai-assisted-ui-review-and-debugging
-> 99_final-frontend-project
```

## 단원별 핵심 질문

| 단원 | 핵심 질문 |
| --- | --- |
| `00_references` | 프론트엔드는 전체 AI 서비스에서 어떤 역할을 하나요? |
| `01_streamlit-basic` | Streamlit 앱은 어떻게 실행하고 화면은 어떻게 구성하나요? |
| `02_streamlit-ui-components` | 버튼, 입력창, 테이블, 차트 같은 UI 요소를 어떻게 구성하나요? |
| `03_api-integration` | Streamlit 화면에서 FastAPI API를 어떻게 호출하나요? |
| `04_state-session-and-data` | 로그인 상태, 대화 이력, 서비스 로그를 화면에서 어떻게 관리하나요? |
| `05_ai-chatbot-interface` | 사용자 질문과 AI 응답을 대화형 UI로 어떻게 표현하나요? |
| `06_streamlit-multipage-app` | 왼쪽 메뉴 기반 멀티페이지 구조를 어떻게 만들고 화면별로 파일을 나누나요? |
| `07_streamlit-tabs-app` | 탭 기반 화면을 어떻게 만들고 탭별 코드를 파일로 분리하나요? |
| `90_ai-assisted-ui-review-and-debugging` | AI 보조 도구로 UI 코드 오류와 개선점을 어떻게 찾나요? |
| `99_final-frontend-project` | 회원가입/로그인, 챗봇, 대화 이력/로그 조회, 배포 점검을 하나의 UX로 어떻게 정리하나요? |

## 백엔드 과정과의 연결

`03_supabase-ai-frontend`는 프론트엔드 화면만 따로 완성하는 과정이 아닙니다. 화면은 항상 어떤 백엔드 API를 호출하는지와 함께 이해합니다.

```text
02_supabase-ai-backend
-> FastAPI
-> Supabase Auth / Database
-> Upstash Redis
-> LLM API 호출

03_supabase-ai-frontend
-> Streamlit 화면
-> API 호출
-> 로그인 상태 표시
-> 대화 이력 표시
-> 서비스 로그 조회
```

초반 API 호출 연습은 `03_api-integration/00_sample_backend`로 진행합니다. 챗봇 화면 연동은 `05_ai-chatbot-interface/00_sample_backend`에서 mock/Gemini chat API로 확인합니다. 실제 Supabase/Auth/Gemini 흐름은 `02_supabase-ai-backend`와 연결하고, 99 최종 프로젝트에서는 `backend_mock`으로 필수 UX를 완성한 뒤 선택적으로 `backend_service`로 실제 서비스 연결과 배포를 확인합니다.

## 04 미니 프로젝트와의 연결

`04_supabase-ai-mini-project`에서는 02 백엔드와 03 프론트엔드에서 배운 내용을 묶어 통합 프로젝트를 진행합니다.

특히 다음 내용은 04에서 본격적으로 다룹니다.

```text
SSE 기반 실시간 AI 응답 스트리밍
백엔드 스트리밍 응답
Streamlit 실시간 표시
Supabase 최종 메시지 저장
통합 대시보드 산출물
```

03 과정에서는 SSE를 깊게 구현하기보다, 프론트엔드가 백엔드 API를 호출하고 응답을 화면에 표시하는 기본 흐름을 확실히 익히는 데 집중합니다.

## 07_multi-agent-service-ops 과정과의 연결

`03`에서는 무료 배포 서비스 기반의 간단한 배포 기준만 선택 참고로 안내합니다.

```text
FastAPI -> Render
Redis -> Upstash
Streamlit -> Streamlit Community Cloud
```

Docker Compose, AWS, GitHub Actions, 모니터링, Auto Healing은 `07_multi-agent-service-ops`에서 더 깊게 다룹니다.

## 99 최종 프론트엔드 프로젝트

`99_final-frontend-project`는 03 과정에서 배운 화면 구성, API 호출, 회원가입/로그인, 대화 이력 조회, 서비스 로그 조회를 하나의 통합 UX로 정리합니다. 이때 프론트엔드 실습이 끊기지 않도록 `backend_mock`을 필수로 사용합니다.

```text
Streamlit 프론트엔드
-> backend_mock
-> 회원가입/로그인
-> Authorization header
-> 챗봇 질문/응답
-> 대화 이력 조회
-> 서비스 로그 조회
-> 로딩/오류 상태 표시
-> 보안 점검과 실행 결과 문서화
```

선택/심화에서는 같은 Streamlit 화면을 `backend_service`와 연결합니다.

```text
Streamlit 프론트엔드
-> backend_service
-> Supabase Auth/DB
-> Gemini API
-> 선택형 Upstash Redis
-> Render/Streamlit Community Cloud 배포
```

프론트엔드는 03 과정 최상위 `.env`의 `API_BASE_URL`을 기준으로 백엔드 주소를 확인합니다.

```text
C:\aidev\03_supabase-ai-frontend\.env
```

04 미니 프로젝트에서는 이 흐름을 Supabase 테이블 저장, Gemini 응답 생성, SSE 스트리밍, 프로젝트 산출물 작성으로 확장합니다.
