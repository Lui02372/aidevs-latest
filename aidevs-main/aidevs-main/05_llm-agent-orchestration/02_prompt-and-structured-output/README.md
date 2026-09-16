# 02 Prompt and Structured Output

## 학습 목표

- Role, Instruction, Context, Constraint를 구분해 Prompt를 작성합니다.
- Prompt Template, Zero-shot, Few-shot, 메시지 역할과 데이터 경계를 비교합니다.
- 같은 입력을 서로 다른 Prompt로 실제 LLM에 보내 결과 차이를 관찰합니다.
- 일반 dict/JSON과 Pydantic 검증의 차이를 설명합니다.
- 누락값, 잘못된 값, 계약에 없는 값을 명시적으로 처리합니다.
- 생성형 `TravelPlan`과 분류형 `SupportTicket` 계약의 차이를 설명합니다.
- 같은 Pydantic Schema로 Mock, Gemini, GPT, Ollama/Llama 결과를 비교합니다.

## 먼저 구분할 세 가지

```text
1. JSON/dict             데이터를 key-value 형태로 표현
2. Pydantic Validation   Python에서 타입·범위·필드 계약 검증
3. Structured Output     LLM에게 Schema에 맞는 응답 생성을 요청하고 다시 검증
```

JSON처럼 보이는 문자열이라고 해서 안전한 데이터는 아닙니다. Backend에서
Pydantic 검증을 통과해야 Tool, Database, Frontend로 전달할 수 있습니다.

## 학습 순서

1. `00_prompt_components.py`: 세 업무의 Prompt 구성 요소를 구분합니다.
2. `01_prompt_template_and_variables.py`: 고정 구조와 업무별 변수를 분리합니다.
3. `02_zero_shot_few_shot.py`: Zero-shot과 Few-shot 실제 응답을 비교합니다.
4. `03_delimiters_and_prompt_injection.py`: 지시와 사용자 데이터의 경계를 비교합니다.
5. `04_system_and_user_messages.py`: System·User 역할 분리 효과를 확인합니다.
6. `05_prompt_before_after.py`: 모호한 Prompt와 개선된 Prompt를 비교합니다.
7. `06_prompt_to_structured_output.py`: 자유 응답과 Structured Output을 연결합니다.
8. `07_pydantic_validation.py`: 일반 dict의 정상·오류·추가 필드를 검증합니다.
9. `08_travel_structured_output.py`: 생성형 `TravelPlan` JSON을 검증합니다.
10. `09_support_ticket_structured_output.py`: 분류형 `SupportTicket` JSON을 검증합니다.

## 실행

```powershell
python .\00_prompt_components.py
python .\01_prompt_template_and_variables.py
python .\07_pydantic_validation.py
python .\08_travel_structured_output.py
python .\09_support_ticket_structured_output.py
```

`02`~`06`은 `C:\mini_agent_st\mini_agent_02_structured_output` Backend를 먼저
실행한 뒤 사용합니다. 기본 `mock`은 호출 흐름만 확인하므로 Prompt에 따른 실제
응답 차이는 Gemini, OpenAI 또는 Ollama를 선택해 관찰합니다.

```powershell
cd C:\mini_agent_st\mini_agent_02_structured_output\backend
uvicorn app.main:app --reload --port 8000
```

새 PowerShell에서 과정 폴더로 이동하고 Provider를 선택합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration\02_prompt-and-structured-output
$env:PROMPT_EXAMPLE_PROVIDER="gemini"  # mock, gemini, openai, ollama
python .\02_zero_shot_few_shot.py
python .\03_delimiters_and_prompt_injection.py
python .\04_system_and_user_messages.py
python .\05_prompt_before_after.py
python .\06_prompt_to_structured_output.py
```

실제 Provider는 호출 횟수와 비용을 먼저 확인합니다. Structured Output의
Provider별 비교는 `10_labs\01_structured_provider_comparison.py`에서 진행합니다.
`mock`은 System Prompt를 해석하지 않는 결정적 응답이므로 Before/After 품질
비교에는 사용하지 않습니다.

## Mini Agent 연결

```text
여러 도메인의 Prompt 구성 예제
→ Prompt 구성 메뉴의 예제 선택
→ Before / After 실제 응답 비교
→ TravelPlan·SupportTicket 검증 예제
→ Schema별 JSON 검증 메뉴
→ Schema별 Structured Output API
→ Provider 비교 메뉴
```

## 완료 체크

- [ ] Prompt의 Role, Instruction, Context, Constraint를 설명할 수 있다.
- [ ] Zero-shot과 Few-shot 결과 차이를 실제 응답 근거로 설명할 수 있다.
- [ ] System 지시와 사용자 데이터를 분리해야 하는 이유를 설명할 수 있다.
- [ ] JSON 파싱 성공과 Schema 검증 성공이 다르다는 것을 설명할 수 있다.
- [ ] ValidationError에서 문제가 생긴 필드를 찾을 수 있다.
- [ ] 생성형 Schema와 분류형 Schema를 목적에 맞게 설계할 수 있다.
- [ ] LLM의 구조화 결과도 Backend에서 다시 검증해야 하는 이유를 설명할 수 있다.
