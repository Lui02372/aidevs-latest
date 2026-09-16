# Multi-Agent 학습 지도

## 한 문장으로 이해하기

Multi-Agent는 여러 LLM을 동시에 호출하는 기술이 아니라, 서로 다른 책임을 가진
Agent가 정해진 계약과 순서로 협업하도록 통제하는 구조입니다.

## 전체 과정

```text
00 Runtime과 배포
→ 01 Single vs Multi AI Agent
→ 02 Agent 역할과 계약
→ 03 Supervisor와 Routing
→ 04 Orchestration
→ 05 Handoff와 Context
→ 06 Multi-Agent Safety
→ 07 Failure·Evaluation·Tracing
→ 08 실제 Multi AI Agent Service
→ 09 HTTP MCP 통합 여행 서비스
```

Docker Compose·GitHub Actions·AWS는 이 흐름 밖의 선택 운영 실습입니다.

## 세 구간으로 나누기

| 구간 | 단원 | 학생이 답해야 하는 질문 |
| --- | --- | --- |
| Multi AI Agent 핵심 | 01~05 | 누가, 무엇을, 어떤 순서와 계약으로 처리하는가? |
| 안전과 평가 | 06~07 | 권한·실패·Trace·회귀를 어떻게 통제하는가? |
| 서비스와 통합 | 08~09 | 긴 Task와 실제 HTTP MCP를 어떻게 연결하는가? |

## 용어를 일상 표현과 연결하기

| 기술 용어 | 일상 표현 | 코드에서 확인할 것 |
| --- | --- | --- |
| Supervisor | 총괄 담당자 | 다음 Agent 선택과 종료 결정 |
| Worker | 업무 담당자 | 한 가지 역할의 입력과 결과 |
| Router | 안내 데스크 | 요청을 담당 Agent로 분류 |
| Contract | 업무 양식 | Pydantic 입력·출력 Schema |
| Handoff | 업무 인계서 | 다음 Agent와 전달 Context |
| State | 공동 작업 기록 | 현재 단계·결과·반복 횟수 |
| Trace | 처리 과정 | Agent 선택·입력·결과·오류 |
| Fallback | 대체 처리 | Provider·Tool·기본 결과 교체 |
| Replan | 계획 다시 세우기 | 실패 후 남은 단계를 변경 |
| Escalation | 사람에게 전달 | 자동 처리를 중단하고 판단 요청 |

## 단원별 핵심 질문

| 단원 | 핵심 질문 |
| --- | --- |
| 01 | 역할을 나누는 것이 정말 필요한가? |
| 02 | Worker가 어떤 입력을 받고 무엇을 반환해야 하는가? |
| 03 | 다음 Agent는 규칙과 LLM 중 누가 선택하는가? |
| 04 | 여러 Agent의 병렬·Join·State·종료를 어떻게 Orchestration하는가? |
| 05 | 다음 Agent에게 무엇을 Handoff하고 무엇을 제거해야 하는가? |
| 06 | Agent별 Tool 권한·승인·중복 실행을 어떻게 차단하는가? |
| 07 | 실패를 어떻게 복구하고 전체 Trace와 Scenario를 평가하는가? |
| 08 | API·Queue·Worker·저장소를 어떻게 실제 서비스로 연결하는가? |
| 09 | 실제 HTTP MCP Tool을 Multi AI Agent와 어떻게 통합하는가? |

## Provider 사용 원칙

```text
Pydantic과 결정적 Python 예제로 계약·정책 확인
→ 실제 Provider로 Agent 결과 확인
→ 같은 계약으로 OpenAI·Gemini·Ollama 비교
→ 실제 Provider 오류를 그대로 기록
→ 자동 테스트에서만 Fake Client로 외부 비용 차단
```

GPT·Gemini·Llama가 서로 다른 문장을 생성해도 `SpecialistResult`, `RouteDecision`,
`TravelHandoff` 계약은 동일하게 유지합니다.

## 저장소와 배포 원칙

```text
01~07 기본 학습
Pydantic + Python 정책 + 실제 Provider

08~09 실제 서비스
Redis Queue와 현재 상태
PostgreSQL Trace 이력
OpenAI·Gemini·Ollama
Streamable HTTP MCP + Open-Meteo

선택 운영 체험
Simple Compose + GitHub Actions + AWS EC2
```

운영 기술이 준비되지 않았다는 이유로 Multi-Agent 핵심 학습을 중단하지 않습니다.
