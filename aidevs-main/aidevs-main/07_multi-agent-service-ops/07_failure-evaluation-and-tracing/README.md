# 07 Evaluation, Feedback, Retry and Tracing

Multi-Agent 서비스는 답변을 한 번 생성하고 끝내지 않습니다. 결과가 기준을 만족하는지 평가하고, 부족하면 구체적인 Feedback으로 필요한 부분을 수정하며, 일시적 오류는 제한적으로 Retry하고, 모든 과정을 Trace로 남겨야 합니다.

## 전체 학습 시나리오

```text
Writer Agent가 결과 생성
→ Evaluator Agent가 항목별 기준 검사
   ├─ 통과 → 최종 결과
   └─ 실패 → 구체적인 Feedback
              → Reviser Agent가 수정
              → 다시 평가 (최대 5회)

외부 연결 실패
→ 오류 유형 분류
   ├─ 일시적 오류 → 제한된 Retry
   ├─ 입력·계획 오류 → Replan
   ├─ 권한 위반 → Block
   └─ 자동 복구 불가 → Human Escalation

모든 생성·평가·수정·실패·재시도
→ 구조화 Trace
```

## 먼저 구분할 개념

| 개념 | 질문 | 다음 행동 |
| --- | --- | --- |
| Validation | 형식과 필수 값이 올바른가? | 잘못된 입력·출력 차단 |
| Evaluation | 결과가 품질 기준을 만족하는가? | 항목별 통과·실패 판정 |
| Feedback | 무엇을 어떻게 고쳐야 하는가? | Reviser에 구체적인 수정 근거 전달 |
| Retry | 같은 작업이 일시적으로 실패했는가? | 동일 작업을 제한적으로 재시도 |
| Replan | Agent나 실행 순서가 잘못되었는가? | 계획·입력·경로 변경 |
| Partial Recovery | 일부 Agent만 실패했는가? | 성공 결과를 보존하고 실패 부분만 복구 |
| Tracing | 어느 단계에서 왜 바뀌고 실패했는가? | 전체 실행 이력 추적 |

Feedback Loop와 Retry는 다릅니다. Feedback Loop는 **결과 내용을 개선**하고, Retry는 **같은 실행의 일시적 실패를 복구**합니다.

## Lab 구성

| Lab | 파일 | 핵심 내용 | 실제 LLM |
| ---: | --- | --- | --- |
| 01 | `01_evaluation_criteria.py` | 평가 기준을 먼저 정의 | 없음 |
| 02 | `02_evaluator_agent.py` | 독립 Evaluator와 항목별 결과 | 없음 |
| 03 | `03_feedback_loop.py` | Writer → Evaluator → Reviser, 최대 5회 | OpenAI·Gemini |
| 04 | `04_bounded_retry.py` | Timeout의 제한된 Retry | 없음 |
| 05 | `05_failure_policy.py` | Retry·Replan·Block·Human 분류 | 없음 |
| 06 | `06_partial_recovery.py` | 성공 결과 보존과 부분 복구 | 없음 |
| 07 | `07_quality_trace.py` | 평가·Feedback·Retry 구조화 Trace | 없음 |

모든 Python 파일 상단에는 정상·실패 시나리오, 기대 결과, 학습 포인트와 LLM 사용 여부를 상세하게 적었습니다. 수업에서는 먼저 상단 시나리오를 읽고 출력을 예상한 다음 코드를 실행합니다.

## Lab별 관찰 내용

### 01 Evaluation Criteria

평가를 시작하기 전에 목적지, 알레르기, 교통, 예산처럼 사람이 이해할 수 있는 성공 기준을 정합니다. 평균 점수 하나가 아니라 실패한 기준 이름을 남깁니다.

### 02 Evaluator Agent

결과 생성 Agent와 평가 책임을 분리합니다. 원래 사용자 요청이 아니라 **최종 산출물**에서 조건이 실제로 유지되었는지 확인합니다.

### 03 Feedback Loop

OpenAI Writer Agent가 초안을 만들고 Gemini Evaluator Agent가 평가합니다. 실패하면 OpenAI Reviser Agent가 Feedback을 반영합니다.

```text
최대 평가 횟수: 5회
최대 수정 횟수: 4회
기준 통과: 즉시 조기 종료
Provider 오류: failed 상태로 종료
```

LLM 호출은 최초 통과 시 2회, 최대 반복 시 10회입니다. 따라서 수업에서는 먼저 코드로 흐름을 설명하고 한 팀씩 실제 실행하는 것이 좋습니다.

### 04 Bounded Retry

Timeout을 의도적으로 재현하여 `failed → failed → completed`와 attempt 번호를 확인합니다. 실제 외부 API 성공처럼 위장한 Mock 데이터가 아니라 Retry 구조만 설명하는 결정적 시뮬레이션입니다.

### 05 Failure Policy

모든 오류를 Retry하지 않습니다. 특히 PermissionError는 재시도하지 않고 즉시 차단해야 합니다.

### 06 Partial Recovery

선택 Agent 하나가 실패했다고 이미 성공한 모든 Agent를 다시 실행하지 않습니다. 필수 Agent 여부와 의존성을 확인하고 실패한 부분만 복구합니다.

### 07 Quality Trace

Routing, Tool 실행, 실패, Replan, 평가, Feedback, 수정, 재평가를 같은 `task_id`와 `trace_id`로 연결합니다.

## Trace에 남길 최소 정보

```text
task_id · trace_id · step · actor · action · status
attempt · duration_ms · error_type · timestamp · details
```

Trace에 프롬프트 전체, API Key, 비밀번호, 불필요한 개인정보를 남기지 않습니다. Redis에는 진행 중인 Snapshot을 두고 PostgreSQL에는 시간순 평가·감사 이력을 저장하는 운영 구현은 08에서 연결합니다.

## 환경과 실행

03을 제외한 Lab은 API Key가 필요하지 않습니다. `03_feedback_loop.py`는 `.env`의 OpenAI와 Gemini 설정을 사용합니다.

```dotenv
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
WRITER_AGENT_PROVIDER=openai
EVALUATOR_AGENT_PROVIDER=gemini
REVISER_AGENT_PROVIDER=openai
```

과정 루트에서 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python .\07_failure-evaluation-and-tracing\01_evaluation_criteria.py
python .\07_failure-evaluation-and-tracing\02_evaluator_agent.py
python .\07_failure-evaluation-and-tracing\03_feedback_loop.py
python .\07_failure-evaluation-and-tracing\04_bounded_retry.py
python .\07_failure-evaluation-and-tracing\05_failure_policy.py
python .\07_failure-evaluation-and-tracing\06_partial_recovery.py
python .\07_failure-evaluation-and-tracing\07_quality_trace.py
```

## 수업 중 확인할 질문

1. Validation과 Evaluation은 어떤 입력을 검사하나요?
2. Feedback Loop와 Retry의 차이는 무엇인가요?
3. Evaluator와 Writer를 분리하면 어떤 장점이 있나요?
4. 기준을 통과하면 5회를 모두 실행하지 않아야 하는 이유는 무엇인가요?
5. PermissionError를 Retry하면 안 되는 이유는 무엇인가요?
6. 일부 Agent 실패 시 어떤 성공 결과를 보존해야 하나요?
7. Trace에 Prompt 전체와 API Key를 기록하면 안 되는 이유는 무엇인가요?

## 완료 기준

- 평가 기준을 항목별로 정의할 수 있습니다.
- Evaluator Feedback을 Reviser 입력으로 전달할 수 있습니다.
- Feedback Loop를 최대 5회로 제한하고 조기 종료할 수 있습니다.
- 오류 유형에 따라 Retry·Replan·Block·Human을 선택할 수 있습니다.
- 성공 결과를 보존하면서 실패한 부분만 복구할 수 있습니다.
- 생성부터 재평가까지 구조화 Trace를 읽을 수 있습니다.
