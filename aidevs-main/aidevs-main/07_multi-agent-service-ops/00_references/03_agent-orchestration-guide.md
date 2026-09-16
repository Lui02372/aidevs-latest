# Agent Orchestration 가이드

Agent Orchestration은 Agent를 연속 호출하는 코드가 아닙니다.

```text
계획
→ 선택
→ 의존성
→ 상태
→ 실행
→ 결과 수집
→ 검증
→ 실패 통제
→ 종료
```

## 구분

```text
retry   같은 Agent와 작업을 제한적으로 다시 실행
replan  Agent·순서·의존성을 다시 결정
fallback 대체 Provider·Tool·결과를 사용
escalation 사람이 판단하도록 전달
```

LangGraph는 Orchestration을 구현하는 도구 중 하나입니다. 먼저 Python 코드로
상태와 종료 조건을 이해한 뒤 Graph로 변환합니다.

## Python Orchestration에서 LangGraph로 이동하기

이 과정에서는 LangGraph를 바로 사용하기 전에 순수 Python 코드로 다음 내용을 먼저
이해합니다.

- 어떤 Agent를 실행할지 결정하는 방법
- Agent 결과를 공통 State에 저장하는 방법
- 조건에 따라 다음 Agent를 선택하는 방법
- 평가 실패 후 Agent를 다시 실행하는 방법
- 최대 반복 횟수와 종료 조건을 적용하는 방법

이 구조를 이해한 후 다음과 같이 Graph 구성 요소로 옮깁니다.

| Python Orchestration | LangGraph |
| --- | --- |
| Agent 실행 함수 | Node |
| 함수 실행 순서 | Edge |
| `if` 조건 분기 | Conditional Edge |
| 공유 실행 데이터 | State |
| 반복문 | 순환 Edge와 종료 조건 |
| 실행 종료 | `END` |

LangGraph가 Workflow를 자동으로 설계하는 것은 아닙니다. Agent 역할, State, 분기 조건,
재시도, 권한과 종료 기준은 개발자가 먼저 설계해야 합니다.

## 이 과정의 실제 LangGraph 실습

선택 실습은 다음 위치에 있습니다.

```text
04_orchestration/
└─ 10_optional_langgraph/
   ├─ README.md
   └─ 01_same_plan_graph.py
```

`01_same_plan_graph.py`는 일반 Python으로 표현한 순차 Orchestration을 다음 Graph로
변환합니다.

```text
START → research → join → itinerary → END
```

이 예제에서 `StateGraph`, `add_node`, `add_edge`, `START`, `END`를 직접 확인할 수 있습니다.
현재 선택 실습의 범위는 순차 Graph 비교까지이며, Conditional Edge와 순환 Edge는 앞의
Python 분기·반복 예제를 이해하기 위한 대응 개념으로 설명합니다.

