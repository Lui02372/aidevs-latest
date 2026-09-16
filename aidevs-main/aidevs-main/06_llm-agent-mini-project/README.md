# 06_llm-agent-mini-project

`06_llm-agent-mini-project`는 `05_llm-agent-orchestration`에서 배운 LangGraph, Tool Use, Memory, Self-Reflection을 하나의 팀 프로젝트로 묶는 24시간 단위 프로젝트입니다.

주제는 **복합 API 연계 일정 조정 에이전트**입니다. 사용자의 일정 요청을 분석하고, 필요한 도구를 선택하고, 도구 실행 결과를 검증한 뒤, 오류가 있으면 재시도하거나 fallback 응답을 만드는 단일 에이전트를 설계하고 구현합니다.

## 프로젝트 목표

```text
1. LangGraph를 이용한 다중 도구(Multi-tool) 선택 및 순환형 워크플로우 설계
2. 에이전트의 판단 오류를 스스로 수정하는 자기 성찰 및 피드백 루프 구현
3. 실시간 API 데이터 기반 의사결정 시나리오 테스트 및 서비스 배포 실습
```

## 전체 구조

```text
06_llm-agent-mini-project
├─ README.md
├─ SETUP.md
├─ .env.example
├─ requirements.txt
├─ 00_references
├─ 01_project-deliverables
└─ 02_project_structure
```

## 폴더 역할

| 폴더 | 역할 |
| --- | --- |
| `00_references` | 프로젝트 개요, Agent 아키텍처, Tool/API 시나리오, Self-Reflection, 테스트/평가, 배포 참고 문서를 제공합니다. |
| `01_project-deliverables` | 필수 산출물인 에이전트 아키텍처 설계서와 에이전트 시험 결과 보고서 샘플을 제공합니다. |
| `02_project_structure` | 학생들이 복사해서 시작할 수 있는 backend/frontend/docs starter 구조입니다. |

## 필수 구현 범위

| 항목 | 기준 |
| --- | --- |
| LangGraph StateGraph | Start, Decision, Tools, Review 또는 Reflection, End 흐름이 있어야 합니다. |
| Multi-tool | 일정 조회, 가능 시간 탐색, 메시지 생성 등 2개 이상의 Tool을 사용합니다. |
| 상태 객체 | `messages`, `tools_called`, `tool_results`, `error_count`, `iteration`, `final_answer` 같은 필드를 타입 힌트와 함께 정의합니다. |
| 분기와 fallback | 도구 필요 여부, 데이터 충분성, 오류 여부에 따라 다음 노드가 달라져야 합니다. |
| Self-Reflection | 도구 선택 오류, 파라미터 누락, 응답 불일치 등을 감지하고 수정 전략을 선택합니다. |
| 테스트 시나리오 | 정상 요청, 정보 부족 요청, 일정 충돌, Tool 오류 상황을 검증합니다. |

## 필수 산출물

| 산출물 | 파일 예시 | 핵심 확인 기준 |
| --- | --- | --- |
| 에이전트 아키텍처 설계서 | `docs/agent-architecture.md` | StateGraph Node/Edge, 상태 필드, Tool 호출 흐름, Memory 전략이 명확한가 |
| 에이전트 시험 결과 보고서 | `docs/agent-test-report.md` | 오류 감지 기준, 재시도/fallback 전략, 자기 성찰 전후 비교가 정리되었는가 |

발표 자료, 배포 노트, 회고 문서는 선택 산출물입니다.

## 선택 구현 범위

| 항목 | 설명 |
| --- | --- |
| 실제 외부 API 연결 | 처음에는 Mock data로 구현하고, 시간이 남으면 Google Calendar, Notion, 공공 API 등으로 확장합니다. |
| 장기 기억 | 05 과정의 pgvector/RAG 또는 대화 이력 저장 구조를 선택적으로 적용합니다. |
| 배포 | FastAPI는 Render, UI는 Streamlit Community Cloud 같은 무료 배포 서비스를 참고합니다. |
| LangSmith | Agent 실행 추적과 디버깅을 선택적으로 적용합니다. |

## 제외 범위

```text
Docker Compose 운영 구성
AWS 배포
GitHub Actions CI/CD
장애 복구 자동화
멀티 에이전트 협업 구조
```

위 내용은 `07_multi-agent-service-ops`에서 본격적으로 다룹니다. 06 과정에서는 단일 에이전트의 판단 흐름, 도구 호출, 자기 성찰, 테스트 결과 문서화에 집중합니다.

## 진행 순서

1. [SETUP.md](./SETUP.md)를 보고 `.venv`, `.env`, 패키지를 준비합니다.
2. [00_references](./00_references/README.md)에서 프로젝트 목표와 설계 기준을 확인합니다.
3. [01_project-deliverables](./01_project-deliverables/README.md)에서 필수 산출물 기준을 확인합니다.
4. [02_project_structure](./02_project_structure/README.md)를 복사하거나 참고해 팀 프로젝트를 시작합니다.
5. Mock data 기반으로 먼저 Agent 흐름을 완성한 뒤, 필요하면 실제 API 또는 배포로 확장합니다.
