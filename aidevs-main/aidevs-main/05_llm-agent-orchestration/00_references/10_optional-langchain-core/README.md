# 선택 참고 · LangChain과 LangGraph 비교 예제

LangChain은 필수 과정에서 사용하지 않습니다. Prompt, Pydantic Structured Output,
Tool, RAG, LangGraph는 각 공식 SDK와 일반 Python 코드로 먼저 학습합니다.

다음 경우에만 이 폴더를 선택적으로 확인합니다.

- 여러 Provider를 LangChain의 공통 Model Interface로 바꾸어 보고 싶을 때
- `Runnable`과 LCEL의 `|` 연결 문법을 비교하고 싶을 때
- 기존 LangChain 프로젝트를 읽어야 할 때

이 과정은 LangChain 1.x API를 기준으로 합니다. 처음 네 예제는 Model Interface와
Structured Output을 소개하고, 이후 예제는 Tool, Agent, RAG, Memory, Streaming,
LangGraph와의 역할 차이를 단계적으로 다룹니다.

## 설치

공통 `requirements.txt`에는 LangChain을 넣지 않습니다.

```powershell
pip install -r .\requirements.txt
```

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\03_multi_provider_chain.py
python .\04_structured_chain_comparison.py
python .\05_prompt_and_output_parser.py
python .\06_runnable_composition.py
python .\07_tool_definition_and_execution.py
python .\08_create_agent.py
python .\09_rag_pipeline.py
python .\10_message_history.py
python .\11_streaming.py
python .\12_langchain_vs_langgraph.py
python .\13_prompt_components.py
python .\14_zero_shot_and_few_shot.py
python .\15_delimiters_and_prompt_injection.py
python .\16_messages_and_placeholders.py
python .\17_dynamic_prompt_routing.py
python .\18_prompt_partial_and_reuse.py
python .\19_structured_output_contract.py
python .\20_validation_retry.py
python .\21_context_budget.py
python .\22_prompt_versioning.py
python .\23_prompt_evaluation.py
python .\24_real_prompt_experiment.py
```

`01`, `02`, `05`~`07`, `09`~`12`는 API Key 없이 실행할 수 있습니다. `03`, `04`,
`08`은 `.env`에 Provider 설정이 있어야 합니다.

`13`~`23`은 Prompt Engineering을 API Key 없이 학습하는 예제입니다. `24`는 같은
질문에 대한 zero-shot과 few-shot prompt를 실제 Provider로 비교하는 선택 실험입니다.

## 권장 학습 순서

| 단계 | 예제 | 핵심 내용 |
| --- | --- | --- |
| 1 | `01`, `02` | Runnable과 Pydantic 결과 |
| 2 | `05`, `06` | Prompt, Parser, LCEL 조합과 분기·병렬 실행 |
| 3 | `07` | Tool schema와 직접 실행의 차이 |
| 4 | `08` | `create_agent`가 수행하는 Agent loop |
| 5 | `09` | 검색과 답변 생성을 분리한 RAG pipeline |
| 6 | `10`, `11` | 대화 기록과 Streaming |
| 7 | `12` | LangChain Agent와 LangGraph Workflow 선택 기준 |
| 8 | `13`~`18` | Prompt 구성, 예시, 경계 표시, 대화, routing, 재사용 |
| 9 | `19`, `20` | 출력 계약 검증과 제한된 재시도 |
| 10 | `21`~`23` | Context budget, 버전 관리, 회귀 평가 |
| 11 | `24` | 실제 Provider로 Prompt 전략 비교 |

각 파일은 실행 가능한 작은 강의 단위입니다. 파일 상단 docstring에 학습 목표와
관찰할 항목을 적었으며, 외부 API가 필요 없는 예제는 Mock 함수로 내부 동작을
먼저 보여 줍니다.

## Prompt Engineering 예제 지도

| 주제 | 예제 | 관찰할 질문 |
| --- | --- | --- |
| Role·Instruction·Context·Constraint | `13` | 각 부분을 분리하면 무엇을 변경하기 쉬운가? |
| Zero-shot·Few-shot | `14`, `24` | 예시는 출력 형식과 판단 기준에 어떤 영향을 주는가? |
| 입력 경계와 Prompt Injection | `15` | 외부 문장을 명령이 아닌 데이터로 어떻게 취급하는가? |
| Multi-turn Prompt | `16` | 고정 지침과 대화 기록은 어떻게 분리되는가? |
| Dynamic Prompt | `17` | 요청 유형에 따라 어떤 지침을 선택하는가? |
| Partial Variables·재사용 | `18` | 공통 정책을 중복 없이 어떻게 주입하는가? |
| Structured Output | `19` | 자연어 지시와 Python 검증은 왜 둘 다 필요한가? |
| Validation·Retry | `20` | 실패를 무한 재호출하지 않고 어떻게 보정하는가? |
| Context Engineering | `21` | 관련성과 길이 제한을 어떻게 함께 다루는가? |
| Prompt Versioning | `22` | 변경 이유와 버전을 어떻게 추적하는가? |
| Evaluation | `23` | 느낌이 아니라 테스트 케이스로 어떻게 비교하는가? |

이 자료는 Mini Agent 필수 메뉴에 연결하지 않으며 과제와 평가 범위에도 포함하지
않습니다.
