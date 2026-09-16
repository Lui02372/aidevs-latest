# 05 LLM Agent Orchestration

LLM 호출을 구조화된 Agent 서비스로 확장하는 과정입니다. 각 기술을 작은 예제로 확인한 뒤 같은 기술을 여행·예약 도메인에 적용하고, 마지막에는 FastAPI Backend와 Streamlit Frontend로 연결합니다.

개념 예제는 Mock으로 안정적으로 실행하고, 같은 요청을 OpenAI GPT, Google Gemini, Docker 기반 Ollama/Llama에 연결해 결과를 비교합니다. PostgreSQL/pgvector는 RAG와 장기 데이터에, Redis는 단기 상태·Cache·TTL에 사용합니다.

## 이전 과정과 달라지는 점

`02`~`04`에서는 Supabase, Upstash, Render처럼 운영을 대신해 주는 Cloud 서비스를
사용했습니다. `05`에서는 같은 역할의 일부를 내 PC의 Docker Container로 직접
실행합니다. Cloud 서비스를 폐기하거나 대체하는 것이 아니라, Agent가 의존하는
Database, Redis, LLM의 동작과 장애를 가까이에서 관찰하는 학습 단계입니다.

| 이전에 사용한 기술 | 이전 과정에서 맡은 역할 | `05`에서 비교할 대상 | 새롭게 확인하는 내용 |
| --- | --- | --- | --- |
| Supabase | 관리형 PostgreSQL, Auth, RLS | Docker PostgreSQL/pgvector | DB 연결, Schema, Volume, Vector 검색 |
| Upstash Redis | 관리형 Serverless Redis | Docker Redis | Key, TTL, 영속화, 재시작과 장애 |
| Render | Backend를 실행하는 Cloud 배포 환경 | 로컬 Docker Container | Image, Container, Port, 실행 환경 격리 |
| Streamlit | Python 기반 Frontend Framework | 로컬 Streamlit + 두 Agent API | UI는 유지하고 연결할 Backend를 선택 |
| Gemini/OpenAI | Cloud LLM API | Ollama/Llama | Cloud API와 Local LLM의 속도·비용·기능 차이 |

Supabase와 Upstash는 계정 생성, 업데이트, 백업, 가용성 같은 운영 부담을 줄여
줍니다. 로컬 PostgreSQL과 Redis는 학생이 직접 시작·중지하고 데이터를 확인할 수
있어 내부 동작을 학습하기 좋습니다. 실제 서비스에서는 요구사항에 따라 관리형
Cloud 서비스와 직접 운영 방식을 선택하거나 함께 사용할 수 있습니다.

## 왜 로컬 Docker를 사용하는가

- 모든 학생이 같은 Image로 비슷한 실행 환경을 재현할 수 있습니다.
- PostgreSQL, Redis, Ollama를 Windows에 각각 직접 설치하지 않고 격리해 실행합니다.
- Container 중지, 재시작, 연결 실패 같은 장애 상황을 안전하게 연습할 수 있습니다.
- API 사용량과 Cloud 비용 없이 Mock, Redis, PostgreSQL 실습을 반복할 수 있습니다.
- Agent의 데이터가 LLM, Database, Cache 사이를 어떻게 이동하는지 직접 확인합니다.

Docker를 사용해도 데이터 검증, 비밀정보 관리, 사용자 권한 검사가 자동으로
해결되지는 않습니다. 또한 로컬 서비스는 학습용이므로 외부 네트워크에 공개하지
않습니다.

## 학습 흐름

```text
Local Docker 환경
→ GPT·Gemini·Ollama/Llama Provider
LLM과 Agent 구분
→ Prompt와 Structured Output
→ GPT 이미지 분석과 TTS 선택 확장
→ Tool Use
→ MCP로 Tool 표준화
→ RAG
→ Memory
→ LangGraph Workflow
→ Human Approval과 Safety
→ 평가와 실행 추적
→ 누적 Backend·Frontend 통합 Lab
```

## 교육 원칙

1. 개념을 가장 작은 Python 예제로 먼저 확인합니다.
2. 같은 기술을 여행·예약 예제에 적용합니다.
3. 외부 API 없이 실행되는 Mock 모드를 기본으로 사용합니다.
4. 각 핵심 개념 뒤에는 여행·예약 도메인의 실제 연동 예제를 실행합니다.
5. 요청·응답 Schema를 먼저 정하고 Backend와 Frontend를 연결합니다.
6. 실제 예약·결제·환불은 수행하지 않습니다.
7. 변경 작업은 사용자의 승인을 받은 뒤 Mock Tool로 실행합니다.

## 과정 구조

| 폴더 | 학습 내용 |
| --- | --- |
| `00_local-runtime` | Docker 기반 Ollama, PostgreSQL/pgvector, Redis |
| `00_references` | 전체 학습 지도, 설계 원칙, 오류 해결 |
| `01_llm-to-agent` | LLM, Workflow, Agent 비교와 OpenAI 멀티모달 선택 확장 |
| `02_prompt-and-structured-output` | Prompt 구성과 Pydantic 응답 |
| `03_tool-use` | Function Calling과 Tool 실행 |
| `03_mcp` | stdio MCP Server, Tool 발견·호출, Resource |
| `04_rag` | 문서 검색과 근거 기반 답변 |
| `05_memory` | 사용자별 단기·장기 기억 |
| `06_agent-workflow` | Workflow·Rule Loop·OpenAI Agent, LangGraph 비교와 Multi-Agent 연결 |
| `07_human-approval-and-safety` | Agent 경계 설계, Single/Multi-Agent 선택, 권한·승인과 안전한 실행 |
| `08_agent-evaluation-and-tracing` | Mini Agent 06·07의 실제 Live 실행 평가 |
| `09_integrated-agent-lab` | 다음 과정에서 별도로 구성할 통합 실습 |

## 예제 진행 방식

각 단원은 가능한 한 다음 순서를 따릅니다.

```text
01_concept_example.py
→ 02_travel_example.py
→ 10_labs
→ 20_assignments
```

여행 예제를 학습한 뒤 과제에서는 병원, 식당, 회의 일정, 공연 예매, 교육 상담 등 다른 도메인으로 변형합니다.

실제 연동 단원은 다음 순서를 따릅니다.

```text
Mock 결과 확인
→ GPT 연결
→ Gemini 연결
→ Ollama/Llama 연결
→ 같은 Pydantic Schema로 비교
→ PostgreSQL/pgvector·Redis 연결
→ 장애와 fallback 확인
```

멀티 LLM은 초반 비교 예제로 끝나지 않고 다음 단원까지 같은 Provider 계약으로
이어집니다.

```text
03 Tool Calling
→ 06 Single Agent와 Workflow 구분
→ 07 승인과 안전 경계 적용
→ 08 동일 Agent의 Scenario·Trace 회귀 평가
→ 09 별도 통합 Mini Project
```

Provider가 바뀌어도 Pydantic Schema, Tool 권한 검사, Graph 흐름, 평가
시나리오는 동일하게 유지합니다.

## Lab 실행 전 Backend 빠른 확인

각 `10_labs/README.md`의 `실행 위치`를 먼저 확인합니다. 작은 Python 예제는 대부분
Backend 없이 실행하며, 실제 Provider 또는 완성 화면을 사용하는 Lab만 아래 Backend를
먼저 실행합니다.

| 단원 | 기본 Lab | 실제 연동·완성 화면에서 실행할 위치 |
| --- | --- | --- |
| 01 | Backend 불필요 | `C:\mini_agent_st\mini_agent_01_llm\backend` · Port 8000 |
| 02 | Lab 1~3 불필요 | Lab 4: `mini_agent_02_structured_output\backend` · Port 8000 |
| 03 | 실습 1~5 불필요 | 실습 6: `mini_agent_03_tool\backend` · Port 8000 |
| 03 MCP | Backend 불필요 | stdio Client가 MCP Server를 자동 실행 |
| 04 | 실습 1~3 불필요 | 실습 4는 Backend가 아니라 `C:\mini_agent_st\infra`의 PostgreSQL·Ollama 사용 |
| 05 | 실습 1~5 불필요 | 실습 6~7은 Redis·PostgreSQL, 완성 화면은 `mini_agent_05_memory\backend` |
| 06 | 필수 Python 예제는 Backend 불필요 | 완성 화면: `mini_agent_06_agent_workflow\backend` · Port 8000 |
| 07 | 필수 Python 예제는 Backend 불필요 | 완성 화면: `mini_agent_07_human_approval\backend` · Port 8000 |
| 08 | Mini Agent Backend 필요 | Live 평가 대상: `mini_agent_06_agent_workflow`, `mini_agent_07_human_approval` |
| 09 | 별도 안내 예정 | 별도 통합 Mini Project |

Python 파일 맨 위의 `실행 전 준비` 주석도 같은 경로를 안내합니다.

## 빠른 시작

Docker가 아직 없어도 `APP_MODE=mock`, `STORAGE_MODE=memory`로 각 단원의 기본
예제를 먼저 학습할 수 있습니다. pgvector, Redis, Ollama가 필요한 확장 실습에
도달했을 때 [Docker 첫 사용 가이드](./00_local-runtime/00_docker-first-guide.md)부터
진행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

상세 환경 준비는 [SETUP.md](./SETUP.md)를 확인합니다.
두 Backend는 모두 `app` 패키지 이름을 사용하므로 루트에서 한 번에 수집하지
않고 [SETUP.md의 테스트 절차](./SETUP.md#8-테스트)처럼 Backend별 폴더에서
각각 실행합니다.

## Docker 학습의 다음 단계

`05`에서는 각 서비스를 `docker run`으로 하나씩 실행하며 Image, Container,
Port, Volume을 배웁니다. `07_multi-agent-service-ops`에서는 여러 Container를
Docker Compose로 함께 실행하고, 같은 Compose 구성을 Amazon EC2 한 대에 수동
배포합니다. 이후 GitHub Actions, 관측성, 보안, 리소스 정리까지 운영 흐름으로
확장합니다.

```text
05: docker run으로 서비스 하나씩 이해
→ 07: Dockerfile과 Docker Compose로 여러 서비스 연결
→ 07: GitHub Actions에서 Test·Compose 검사·Image Build
→ 07: AWS EC2에서 Simple Compose 수동 배포와 리소스 정리
```

## 완료 기준

- 일반 LLM 호출과 Agent를 구분할 수 있습니다.
- Tool 선택과 Tool 실행을 분리할 수 있습니다.
- RAG와 Memory의 역할을 구분할 수 있습니다.
- LangGraph State와 분기·종료 조건을 설계할 수 있습니다.
- 승인 없는 변경 Tool을 차단할 수 있습니다.
- Mock 모드에서 Backend와 Frontend 통합 흐름을 실행할 수 있습니다.
- GPT·Gemini·Ollama/Llama를 공통 Provider 계약으로 교체할 수 있습니다.
- PostgreSQL/pgvector와 Redis를 목적에 맞게 구분해 연결할 수 있습니다.
- 정상·정보 부족·Tool 실패·정책 위반 시나리오를 평가할 수 있습니다.
- OpenAI 이미지 입력과 TTS를 일반 멀티 LLM 계약과 분리해 사용할 수 있습니다.

## 다음 과정

`06_llm-agent-mini-project`에서는 이 과정의 기능을 새로운 도메인에 적용해 3일간 팀 프로젝트를 진행합니다.
