# 99_final-frontend-project

이 단원은 `03_supabase-ai-frontend`의 최종 프로젝트입니다.

목표는 **개인화 AI 챗봇 서비스 UI를 구현하고, 로그인 상태 유지, 대화 기록 조회, 서비스 로그 조회, 배포 흐름까지 연결하는 것**입니다. 초보자 실습에서는 먼저 `backend_mock`으로 안정적으로 화면을 완성하고, 선택/심화로 `backend_service`를 연결합니다.

## 프로젝트 목표

```text
회원가입
-> 로그인
-> access_token 저장
-> Authorization header로 보호 API 호출
-> 챗봇 질문/응답
-> 이전 대화 기록 조회
-> 서비스 로그 조회
-> 배포 전 점검
```

## backend 사용 기준

| 폴더 | 역할 | 수업 기준 |
| --- | --- | --- |
| `backend_mock` | 프론트엔드 개발용 제공 backend입니다. Supabase, Gemini, Redis 없이 메모리로 동작합니다. | 필수 |
| `backend_service` | 실제 서비스 연결용 backend입니다. Supabase Auth/DB, Gemini, 선택적으로 Upstash Redis를 사용합니다. | 선택/심화 |

초보자 수업에서는 먼저 `backend_mock`으로 화면과 API 연결 흐름을 완성합니다. 이후 시간이 있거나 배포 실습까지 진행할 때 `backend_service`로 바꿔 연결합니다.

## 제공 API

`backend_mock`과 `backend_service`는 같은 API 계약을 사용합니다.

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | backend 상태 확인 |
| POST | `/auth/signup` | 회원가입 |
| POST | `/auth/signin` | 로그인과 token 발급 |
| POST | `/auth/signout` | 로그아웃 |
| GET | `/me` | 현재 사용자 조회 |
| POST | `/chat` | AI 응답 생성 |
| GET | `/conversations` | 사용자 대화 기록 조회 |
| GET | `/service-logs` | 서비스 로그 조회 |

보호 API를 호출할 때는 다음 header를 보냅니다.

```text
Authorization: Bearer <access_token>
```

## 폴더 구조

```text
99_final-frontend-project
├─ README.md
├─ backend_mock
├─ backend_service
├─ starter
├─ solution_tabs
├─ solution_multipage
├─ templates
└─ checklist
```

| 폴더 | 설명 |
| --- | --- |
| `starter` | 학생이 직접 구현을 시작하는 기본 구조 |
| `solution_tabs` | `st.tabs()` 기반 완성 예제 |
| `solution_multipage` | `st.Page`, `st.navigation()`, `pages/`로 화면을 나눈 멀티페이지 완성 예제 |
| `templates` | 배포 체크리스트와 제출 문서 템플릿 |
| `checklist` | 최종 점검 체크리스트 |

## Frontend 선택 기준

| 폴더 | 방식 | 추천 상황 |
| --- | --- | --- |
| `solution_tabs` | 한 화면 안에서 탭으로 전환 | 빠르게 전체 기능을 확인하고 실습할 때 |
| `solution_multipage` | 왼쪽 메뉴로 화면 이동 | 화면별로 파일을 나누어 개발하거나 팀 프로젝트 구조를 연습할 때 |

`solution_tabs`는 탭 기반 화면이므로 `03_project_structure/frontend_tabs`와 대응됩니다.  
`solution_multipage`는 왼쪽 메뉴 기반 화면이므로 `03_project_structure/frontend_multipage`와 대응됩니다.

## 필수 구현 범위

| 항목 | 기준 |
| --- | --- |
| Streamlit 챗봇 UI | 사용자 메시지와 assistant 응답을 구분해 표시합니다. |
| 회원가입/로그인 UI | backend의 `/auth/signup`, `/auth/signin`을 호출합니다. |
| 로그인 상태 유지 | `st.session_state`에 `access_token`과 사용자 정보를 저장합니다. |
| Authorization header | 보호 API 호출 시 `Bearer token`을 보냅니다. |
| 대화 기록 조회 | `/conversations` 응답을 화면에 표시합니다. |
| 응답 생성 상태 | `st.spinner`, `st.status`, `st.empty` 등으로 생성 중 상태를 보여 줍니다. |
| 서비스 로그 조회 | `/service-logs` 응답을 표로 표시합니다. |
| 보안 | 프론트엔드 코드에 service role key, LLM API key, Redis token을 넣지 않습니다. |

## 실행 순서

PowerShell 1: mock backend 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_mock
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

PowerShell 2: 탭 기반 solution 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\solution_tabs
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

선택: 멀티페이지 solution 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\solution_multipage
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

`solution_multipage`는 Streamlit `st.navigation()` 기반 멀티페이지 구조를 설명하기 위한 추가 예제입니다. 실행은 항상 `app.py`로 시작하고, 각 화면 개발은 `pages/*.py` 파일을 수정한 뒤 브라우저 왼쪽 메뉴에서 해당 화면을 선택해 확인합니다.

선택: 실제 서비스 backend 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`backend_mock`과 `backend_service`는 같은 Authorization 방식을 사용합니다. 따라서 frontend에서는 `API_BASE_URL`만 바꾸면 mock backend에서 실제 service backend로 전환할 수 있습니다.

## 배포 실습 기준

무료 배포 서비스는 선택/심화로 다룹니다.

```text
FastAPI -> Render
Redis -> Upstash
Streamlit -> Streamlit Community Cloud
```

자세한 배포 절차는 [06_deployment-checklist.md](templates/06_deployment-checklist.md)를 확인합니다.  
완성 후 평가는 [final-checklist.md](checklist/final-checklist.md)를 확인합니다.

Docker, AWS, GitHub Actions 기반 운영 자동화는 `07_multi-agent-service-ops`에서 다룹니다.
