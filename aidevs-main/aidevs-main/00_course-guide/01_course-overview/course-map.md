# Course Map

이 문서는 각 과정에서 반드시 잡아야 할 핵심 범위와, 시간이 남을 때 확장할 수 있는 범위를 구분합니다.

초보자 기준에서는 모든 내용을 한 번에 완벽하게 이해하려고 하기보다, **필수 흐름을 먼저 실행하고 선택/확장은 수업 진도와 팀 수준에 따라 적용**합니다.

## 과정별 지도

| 과정 | 필수로 잡아야 할 것 | 선택/확장 | 다음 과정으로 넘어가기 전 |
| --- | --- | --- | --- |
| 01 Python/Git Foundation | Python 기본 문법, 함수, 파일/JSON, 테스트, Git/GitHub, VS Code Source Control | 추가 알고리즘, Git 명령어 심화, 팀 협업 심화 | `.venv` 활성화, Python 파일 실행, pytest 실행, Git 상태 확인과 push를 할 수 있다 |
| 02 Supabase AI Backend | FastAPI API, Pydantic, mock-first LLM 호출, Gemini SDK, Supabase CRUD/Auth/JWT/RLS, Upstash Redis 기본 | OpenAI 비교, 구조 분리 리팩토링, 추가 테스트 | `uvicorn` 실행, Swagger 테스트, `.env` 보안, Supabase key 차이를 설명할 수 있다 |
| 03 Supabase AI Frontend | Streamlit UI, API 호출, 로딩/오류 처리, session state, Authorization header, 챗봇 UI | React 구조 비교, 실제 `backend_service` 연결, 무료 배포 | `API_BASE_URL`로 백엔드와 연결하고, token을 화면 상태로 관리할 수 있다 |
| 04 Supabase AI Mini Project | API 설계서, 화면 설계서, DB 설계서, 실시간 로그 대시보드 구현 결과물 | 배포 고도화, 사용자별 권한, 추가 차트/필터, 발표 자료 | 필수 산출물 4종과 동작하는 대시보드를 정리한다 |
| 05 LLM Agent Orchestration | Prompt, Structured Output, Prompt Injection 방어, Function Calling, Tool Use, MCP 기본, RAG, Memory, LangGraph 상태 흐름 | LangSmith tracing, Ollama 비교, RAGAS, 고급 MCP 서버 | Agent 상태, 도구 호출, 메모리/RAG 흐름을 코드나 다이어그램으로 설명할 수 있다 |
| 06 LLM Agent Mini Project | LangGraph 기반 다중 도구 일정 조정 Agent, 자기 성찰, 피드백 루프, 테스트 결과 보고 | 배포, 장기 기억 확장, 추가 API 도구, 발표 자료 | 에이전트 아키텍처 설계서와 시험 결과 보고서를 정리한다 |
| 07 Multi-Agent Service Ops | 멀티 에이전트 협업, 역할 분리, Docker Compose, GitHub Actions, AWS ECR/App Runner 배포, CloudWatch 로그, 보안 가드레일 | Slack/Teams 알림, OIDC, 고급 모니터링, Guardrails 도구 확장 | 여러 서비스를 실행하고, AWS 배포와 리소스 삭제까지 수행할 수 있다 |
| 08 Multi-Agent Service Mini Project | Auto Healing 시나리오, 장애 유형별 복구 로직, 멀티 컨테이너 실행, 배포/복구 보고서, 파이프라인 결과 보고서 | 보안 감사, 알림/에스컬레이션, 운영 대시보드 고도화 | 필수 산출물 3종과 배포/장애 복구 결과를 정리한다 |

## 필수와 선택을 나누는 기준

필수는 다음 기준으로 정합니다.

```text
수업 시간 안에 대부분의 수강생이 따라 할 수 있는가?
다음 과정으로 넘어갈 때 반드시 필요한가?
실제 프로젝트 산출물과 직접 연결되는가?
```

선택/확장은 다음 기준으로 둡니다.

```text
진도가 빠른 팀이 더 깊게 해볼 수 있는가?
실무적으로는 의미 있지만 초보자에게는 부담이 큰가?
다음 과정에서 다시 다룰 수 있는가?
```

## 설치와 실행 문서 연결

과정별 실행 방법은 각 과정 폴더의 `SETUP.md`에서 확인합니다.

공통 설치와 계정 준비는 아래 문서에서 확인합니다.

```text
00_course-guide/02_setup-guides
```

막히는 지점별 빠른 해결 링크는 아래 문서에서 확인합니다.

```text
00_course-guide/03_learning-support/troubleshooting.md
```
