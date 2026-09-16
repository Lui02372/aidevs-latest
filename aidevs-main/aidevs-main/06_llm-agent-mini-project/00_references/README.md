# 00_references

이 폴더는 `06_llm-agent-mini-project`를 진행하기 전에 확인하는 참고 문서입니다.

06 과정의 핵심은 코드를 많이 만드는 것이 아니라, **단일 에이전트가 어떻게 판단하고, 도구를 선택하고, 오류를 복구하는지**를 설계하고 검증하는 것입니다.

## 문서 목록

| 파일 | 내용 |
| --- | --- |
| `01_project-overview.md` | 프로젝트 주제, 목표, 필수 범위를 정리합니다. |
| `02_agent-architecture-guide.md` | LangGraph StateGraph, Node, Edge, State 설계 기준을 설명합니다. |
| `03_tool-and-api-scenario-guide.md` | 일정 조정 Agent에 필요한 Tool과 API 시나리오를 정리합니다. |
| `04_self-reflection-feedback-loop.md` | 자기 성찰, 오류 감지, 재시도, fallback 흐름을 설명합니다. |
| `05_test-and-evaluation-guide.md` | 테스트 시나리오와 평가 지표를 정리합니다. |
| `06_deployment-guide.md` | 선택 배포 방향과 07 과정으로 넘길 운영 범위를 구분합니다. |

## 먼저 기억할 기준

- 처음부터 실제 Calendar API를 붙이지 않아도 됩니다.
- Mock data로 Tool 호출 흐름을 먼저 완성합니다.
- 최종 산출물은 코드뿐 아니라 설계와 시험 결과 보고서까지 포함합니다.
- Docker Compose, AWS, GitHub Actions는 07 과정에서 다룹니다.
