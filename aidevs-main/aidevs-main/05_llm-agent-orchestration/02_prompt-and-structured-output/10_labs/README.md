# 02 Labs

## 실행 위치

Lab 1과 Lab 5~7은 Python과 Pydantic만 사용합니다. Lab 2~4와 Lab 8은 다음
Mini Agent Backend를 먼저 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_02_structured_output\backend
uvicorn app.main:app --reload --port 8000
```

실제 Prompt 차이를 확인할 때 사용할 Provider를 선택합니다.

```powershell
$env:PROMPT_EXAMPLE_PROVIDER="gemini"  # mock, gemini, openai, ollama
```

## Lab 1. 재사용 가능한 Prompt Template

`01_prompt_template_and_variables.py`에 상품 리뷰 분류 업무를 추가합니다. Prompt
구조는 유지하고 Role, Instruction, Context, Constraint, Output Format 값만
교체하세요.

## Lab 2. Zero-shot과 Few-shot

`02_zero_shot_few_shot.py`의 고객 문의를 세 개로 늘리고 Zero-shot과 Few-shot으로
각각 실행합니다. 분류값, 형식 준수 여부, 근거의 일관성을 표로 기록하세요.

## Lab 3. 사용자 입력과 지시 분리

다음 세 방식으로 같은 입력을 실행하고 결과를 비교합니다.

- 사용자 입력을 Prompt에 그대로 연결
- XML 구분자로 감싸기
- 구분자와 함께 입력 안의 명령을 데이터로 취급하라는 제약 추가

구분자는 방어의 한 요소일 뿐 완전한 보안 기능은 아니라는 점도 설명하세요.

## Lab 4. Before와 After Prompt

모호한 회의 요약 Prompt를 Role, Instruction, Context, Constraint, Output Format으로
개선합니다. 개선 전후 결과에서 누락된 할 일과 잘못 확정된 결정 사항을 찾으세요.

## Lab 5. 여행 계획 Schema 확장

`TravelPlan`에 다음 필드를 추가하세요.

- `estimated_budget`: 0보다 큰 정수
- `transportation`: `public`, `car`, `flight`, `mixed`
- `daily_itinerary`: 날짜별 활동을 담은 문자열 목록

정상 예제와 필드가 누락된 예제를 각각 한 개 추가합니다.

## Lab 6. 검증 실패를 사용자 문장으로 바꾸기

다음 오류를 사용자가 이해할 수 있는 한국어 문장으로 변환하세요.

- `recommended_days`가 0
- `activities`가 빈 목록
- `category`가 `refund`
- `priority`가 `urgent`
- `requires_human`이 문자열 `"yes"`
- Schema에 없는 필드

## Lab 7. 고객 문의 Schema 확장

`SupportTicket`에 `sentiment`와 `suggested_team` 필드를 추가합니다. 각 필드는
허용값을 `Literal`로 제한하고 정상 문의와 잘못된 문의를 검증하세요.

## Lab 8. Mock과 실제 Provider 비교

`01_structured_provider_comparison.py`를 실행해 `TravelPlan`과 `SupportTicket`을
Provider별로 비교하고 다음을 기록하세요.

- 모든 결과가 같은 필드를 가지는가?
- 내용은 어떻게 다른가?
- 실패한 Provider가 있어도 다른 결과가 남는가?
