# Course Sequence

이 과정은 Python 기초에서 시작해 AI 웹 서비스 개발, 단일 LLM Agent, 멀티 에이전트 서비스 운영 프로젝트까지 이어집니다.

처음에는 작은 Python 파일을 실행하는 것부터 시작하고, 이후 FastAPI 백엔드, Streamlit 프론트엔드, Supabase 저장소, 실시간 대시보드, Agent 오케스트레이션, Docker/AWS 운영까지 단계적으로 확장합니다.

## 전체 순서

| 순서 | 과정 | 핵심 역할 |
| --- | --- | --- |
| 01 | Python/Git Foundation | Python 기본 문법, 테스트, Git/GitHub, VS Code Source Control |
| 02 | Supabase AI Backend | FastAPI, Gemini API, Supabase DB/Auth/RLS, Upstash Redis, 백엔드 API |
| 03 | Supabase AI Frontend | Streamlit UI, 백엔드 API 호출, 로그인 상태, 챗봇 화면, 멀티페이지/탭 구조 |
| 04 | Supabase AI Mini Project | AI 서비스 로그 분석과 실시간 운영 대시보드 팀 프로젝트 |
| 05 | LLM Agent Orchestration | Prompt, Structured Output, Tool Use, MCP, RAG, Memory, LangGraph |
| 06 | LLM Agent Mini Project | 복합 API 연계 일정 조정 Agent 프로젝트 |
| 07 | Multi-Agent Service Ops | 멀티 에이전트 협업, Docker Compose, GitHub Actions, AWS 배포, 모니터링, 가드레일 |
| 08 | Multi-Agent Service Mini Project | Auto Healing 워크플로우와 배포/장애 복구 프로젝트 |

## 흐름

```text
01 Python/Git Foundation
-> 02 Supabase AI Backend
-> 03 Supabase AI Frontend
-> 04 Supabase AI Mini Project
-> 05 LLM Agent Orchestration
-> 06 LLM Agent Mini Project
-> 07 Multi-Agent Service Ops
-> 08 Multi-Agent Service Mini Project
```

## 단계별 의미

### 01. 기초 준비

`01_python-git-foundation`에서는 Python 파일을 실행하고, 함수와 테스트를 이해하고, GitHub에 코드를 올리는 기본 흐름을 익힙니다.

이 과정이 끝나면 수강생은 최소한 다음을 할 수 있어야 합니다.

```text
Python 파일 실행
.venv 활성화
pip install
pytest 실행
VS Code Source Control로 commit/push
README.md 작성
```

### 02~04. AI 웹 서비스

`02`에서는 FastAPI 백엔드를 만들고 Supabase, Gemini, Redis 캐시 흐름을 연결합니다.

`03`에서는 Streamlit 화면을 만들고 백엔드 API를 호출합니다.

`04`에서는 백엔드, DB, Upstash Redis, SSE, Streamlit 대시보드를 연결해 **AI 서비스 로그 분석 및 운영 대시보드**를 구현합니다.

### 05~06. 단일 Agent

`05`에서는 Prompt, Tool Use, MCP, RAG, Memory, LangGraph를 학습합니다. Docker는 Agent 실습에 필요한 도구를 `docker run`으로 실행하는 수준에서 사용합니다.

`06`에서는 배운 내용을 바탕으로 **복합 API 연계 일정 조정 Agent** 프로젝트를 진행합니다.

### 07~08. 멀티 Agent와 운영

`07`에서는 멀티 에이전트 협업 구조를 서비스 운영 관점으로 확장합니다. Docker Compose, GitHub Actions, AWS 배포, CloudWatch 로그, 보안 가드레일을 다룹니다.

`08`에서는 **에러 자가 치유(Auto Healing) 워크플로우** 프로젝트를 진행합니다. 장애 감지, 복구 흐름, 배포 결과, 파이프라인 결과까지 정리합니다.

## 프로젝트 과정

| 과정 | 프로젝트 주제 | 핵심 산출물 |
| --- | --- | --- |
| 04 | AI 서비스 로그 분석 및 운영 대시보드 구축 | API 설계서, 화면 설계서, DB 설계서, 대시보드 구현 결과물 |
| 06 | 복합 API 연계 일정 조정 Agent | 에이전트 아키텍처 설계서, 에이전트 시험 결과 보고서 |
| 08 | 에러 자가 치유(Auto Healing) 워크플로우 | 멀티 에이전트 아키텍처 설계서, 배포/장애 복구 보고서, 파이프라인 결과 보고서 |
