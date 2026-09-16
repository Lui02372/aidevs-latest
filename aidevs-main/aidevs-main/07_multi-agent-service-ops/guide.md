# 07_multi-agent-service-ops 실행 가이드

이 파일이 실행 순서의 기준입니다. 한 단계씩 실행하고 결과를 확인하세요. player 주석은 버튼에 연결되는 실행 종류이며 임의 셸 명령을 실행하지 않습니다.

## 1. 프로젝트 구조 확인
<!-- player: {"action": "read"} -->

README와 아래 구조를 읽고 실행 단위와 역할을 확인합니다.

- .pytest_cache/README.md
- 00_references/README.md
- 00_runtime-and-deployment/00_local-services/README.md
- 00_runtime-and-deployment/01_simple-multi-llm-compose/README.md
- 00_runtime-and-deployment/01_simple-multi-llm-compose2/README.md
- 00_runtime-and-deployment/01_simple-multi-llm-compose3/README.md
- 00_runtime-and-deployment/02_github-actions-ci/README.md
- 00_runtime-and-deployment/03_aws-ec2/README.md
- 00_runtime-and-deployment/04_github-actions-aws-deploy/README.md
- 00_runtime-and-deployment/05_weather-mcp-deployment-project/README.md
- 00_runtime-and-deployment/05_weather-mcp-deployment-project/deploy/README.md
- 00_runtime-and-deployment/06_weather-mcp-stateful-deployment/README.md
- 00_runtime-and-deployment/06_weather-mcp-stateful-deployment/deploy/README.md
- 00_runtime-and-deployment/README.md
- 01_single-vs-multi-agent/01_single_ai_agent.py
- 01_single-vs-multi-agent/02_independent_specialists.py
- 01_single-vs-multi-agent/03_split_decision.py
- 01_single-vs-multi-agent/04_compare_architectures.py
- 01_single-vs-multi-agent/05_context_and_permission_boundaries.py
- 01_single-vs-multi-agent/06_orchestration_preview.py
- 01_single-vs-multi-agent/07_sequential_orchestration.py
- 01_single-vs-multi-agent/08_parallel_and_join.py
- 01_single-vs-multi-agent/09_router_orchestration.py
- 01_single-vs-multi-agent/10_supervisor_worker.py
- 01_single-vs-multi-agent/11_handoff_preview.py
- 01_single-vs-multi-agent/12_evaluator_reviser.py
- 01_single-vs-multi-agent/13_provider_failover.py
- 01_single-vs-multi-agent/README.md
- 02_agent-role-and-contract/01_role_definition.py
- 02_agent-role-and-contract/02_task_decomposition.py
- 02_agent-role-and-contract/03_input_output_contract.py
- 02_agent-role-and-contract/04_role_specific_contracts.py
- 02_agent-role-and-contract/05_contract_validation.py
- 02_agent-role-and-contract/06_incomplete_result.py
- 02_agent-role-and-contract/07_real_multi_llm_contracts.py
- 02_agent-role-and-contract/08_verified_result_flow.py
- 02_agent-role-and-contract/README.md
- 03_supervisor-and-routing/01_rule_router.py
- 03_supervisor-and-routing/02_llm_router.py
- 03_supervisor-and-routing/03_router_contract.py
- 03_supervisor-and-routing/04_supervisor_decision.py
- 03_supervisor-and-routing/05_supervisor_worker_loop.py
- 03_supervisor-and-routing/06_router_vs_supervisor.py
- 03_supervisor-and-routing/07_multi_llm_supervisor_team.py
- 03_supervisor-and-routing/README.md

## 2. 공통 가상환경 준비
<!-- player: {"action": "prepare"} -->

과정 루트 .venv에 requirements.txt를 설치합니다. 완료 로그를 확인하면 다음 단계로 진행합니다.

## 3. 저장소 연결 준비
<!-- player: {"action": "infra"} -->

전용 PostgreSQL 15433과 Redis 16379를 준비하고 원본 SQL을 적용합니다. 영구 기록과 Queue의 역할을 구분하세요.

## 4. 01_single-vs-multi-agent/01_single_ai_agent.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/01_single_ai_agent.py"} -->

Lab 01-1: 하나의 Travel AI Agent가 전체 요청을 처리합니다.

시나리오:
    사용자는 부산 2박 3일 여행 초안을 요청합니다. 두 번째 요청에는 알레르기와
    대중교통 조건도 추가합니다. 하나의 Travel Agent가 같은 Goal과 같은 권한 안에서
    전체 초안을 작성합니다. 실제 예약·결제·날씨 조회는 수행하지 않습니다.

학습 질문:
    역할처럼 보이는 작업이 여러 개 있어도 하나의 판단 주체로 처리할 수 있을까요?
    사용자 제약이 늘어나는 것과 Agent를 분리하는 것은 같은 문제일까요?

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 5. 01_single-vs-multi-agent/02_independent_specialists.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/02_independent_specialists.py"} -->

Lab 01-2: 독립 Goal을 가진 Specialist를 Orchestration 없이 실행합니다.

시나리오:
    Weather·Place·Budget·Safety Agent가 같은 여행 요청을 각각 처리합니다.
    GPT·Gemini·Llama·Gemma를 하나씩 배정하지만 Agent마다 독립
    Goal은 있지만 누가 실행 순서를 정하고 결과를 합치며 전체 완료를 선언하는지는
    아직 구현하지 않습니다.

학습 질문:
    Agent가 여러 개 존재하는 것과 Multi-Agent Orchestration은 무엇이 다를까요?

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 6. 01_single-vs-multi-agent/03_split_decision.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/03_split_decision.py"} -->

Lab 01-3: 여러 업무를 같은 기준으로 평가해 Agent 분리를 판단합니다.

시나리오:
    여행, 고객지원, 코드검토, 콘텐츠 검사, 장애대응 사례를 독립 Goal·Context·권한·
    평가·Handoff 기준으로 판정합니다. Tool이나 단계가 많다는 이유만으로 분리하지
    않습니다.

학습 질문:
    도메인이 달라져도 반복해서 사용할 수 있는 Agent 분리 기준은 무엇일까요?

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 7. 01_single-vs-multi-agent/04_compare_architectures.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/04_compare_architectures.py"} -->

Lab 01-4: Single과 Multi 구조의 호출·Context·실패 범위를 비교합니다.

시나리오:
    같은 여행 요청을 하나의 Agent와 Supervisor·세 Specialist·Join 구조로 각각
    설계했다고 가정합니다. 실제 LLM을 호출하지 않고 호출 수, Context 복사, 실패
    지점과 권한 격리의 차이만 비교합니다.

학습 질문:
    Multi-Agent로 분리해서 얻는 이점은 늘어난 비용과 실패 지점을 감수할 만큼
    구체적인가요?

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 8. 01_single-vs-multi-agent/05_context_and_permission_boundaries.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/05_context_and_permission_boundaries.py"} -->

Lab 01-5: Context와 Tool 권한이 역할 분리의 근거가 되는지 확인합니다.

시나리오:
    여행 서비스에서는 Weather Agent와 Budget Agent가 서로 다른 정보와 Tool을
    사용합니다. 고객지원 서비스에서는 Support Agent가 주문을 조회하고 Refund Agent만
    승인된 환불을 실행합니다. 전체 Context를 모든 Agent에게 전달하지 않습니다.

학습 질문:
    역할 이름만 나눈 것이 아니라 실제 데이터와 실행 권한도 분리됐는지 어떻게
    확인할 수 있을까요?

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 9. 01_single-vs-multi-agent/06_orchestration_preview.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/06_orchestration_preview.py"} -->

Lab 01-6: 여러 독립 Agent와 Orchestration이 아닌 구조를 확인합니다.

시나리오:
    Weather Agent와 Budget Agent가 각각 결과를 반환합니다. 두 Agent 사이에는 결과
    전달이 없고 전체 상태와 종료 조건도 없습니다. 뒤쪽 비교 함수에서는 Coordinator가
    최소한의 선택·결과 수집·종료를 담당하면 무엇이 달라지는지 확인합니다.

학습 질문:
    여러 Agent를 한 파일에서 호출했다는 사실만으로 Orchestration이라고 할 수 있을까요?

범위:
    Agent 결과는 실제 LLM이 만들고 Python은 선택·수집·종료 차이만 보여줍니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 10. 01_single-vs-multi-agent/07_sequential_orchestration.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/07_sequential_orchestration.py"} -->

Lab 01-7: Sequential Orchestration을 가장 작은 예로 확인합니다.

시나리오:
    콘텐츠 팀이 부산 여행 안내문을 만듭니다. Research Agent가 핵심 사실을 정리하고,
    Writer Agent가 그 결과로 초안을 작성하며, Reviewer Agent가 초안을 검토합니다.
    앞 단계가 실패하면 뒤 Agent는 실행하지 않습니다.

학습 질문:
    이전 Agent의 결과가 다음 Agent의 필수 입력일 때 어떤 실행 구조가 적합할까요?

범위:
    세 실제 AI Agent를 사용하고 Python은 순서·결과 전달·실패 중단을 담당합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 11. 01_single-vs-multi-agent/08_parallel_and_join.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/08_parallel_and_join.py"} -->

Lab 01-8: Parallel + Join 구조를 실제 LLM 결과로 미리 확인합니다.

시나리오:
    Weather·Place·Budget Agent는 같은 여행 요청만 있으면 서로 기다리지 않고 조사할
    수 있습니다. 세 결과가 모두 준비된 뒤 Itinerary Agent가 하나의 일정으로 합칩니다.

학습 질문:
    어떤 작업이 독립적이며, Join 전에 반드시 준비돼야 하는 결과는 무엇일까요?

범위:
    GPT·Gemini·Llama·Gemma Agent 결과를 사용합니다. Thread 병렬 실행은 04에서
    구현하고 여기서는 독립 호출과 필수 Join 경계에 집중합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 12. 01_single-vs-multi-agent/09_router_orchestration.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/09_router_orchestration.py"} -->

Lab 01-9: Router 패턴으로 필요한 Agent만 선택합니다.

시나리오:
    고객지원 서비스에 배송, 환불, 기술지원 Agent가 있습니다. 모든 문의에 세 Agent를
    실행하지 않고 GPT Router Agent가 한 Agent를 선택합니다. 선택된 실제 AI Agent만
    사용자 요청을 처리합니다.

학습 질문:
    요청마다 필요한 역할이 하나로 달라질 때 전체 Agent를 실행해야 할까요?

범위:
    구조화 계약으로 Router의 허용 Agent를 제한합니다. 상세 Routing 평가는 03에서 학습합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 13. 01_single-vs-multi-agent/10_supervisor_worker.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/10_supervisor_worker.py"} -->

Lab 01-10: Supervisor–Worker 패턴의 반복과 종료를 확인합니다.

시나리오:
    코드 변경 요청을 받은 Supervisor가 Analyst, Developer, Reviewer 순서로 Worker를
    선택합니다. 각 결과를 확인한 뒤 다음 Worker를 선택하고, 모든 역할이 완료되면
    종료합니다. 최대 단계를 넘으면 무한 반복 대신 실패합니다.

학습 질문:
    한 번 선택하고 끝나는 Router와 결과를 보며 다음 역할을 선택하는 Supervisor는
    무엇이 다를까요?

범위:
    Worker는 실제 Gemini·Llama·Gemma를 사용하고 Python Supervisor가 허용 순서와
    최대 단계를 통제합니다. 동적 LLM Supervisor는 03에서 확장합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 14. 01_single-vs-multi-agent/11_handoff_preview.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/11_handoff_preview.py"} -->

Lab 01-11: Handoff로 실행 책임을 다른 Agent에게 넘깁니다.

시나리오:
    Support Agent가 배송 지연 상담을 처리하다가 승인된 환불이 필요하다고 판단합니다.
    Support Agent는 환불을 직접 실행하지 않고 Refund Agent에게 책임과 최소 Context를
    전달합니다. Refund Agent가 Handoff를 수락한 뒤 책임 주체가 바뀝니다.

학습 질문:
    함수 호출 결과를 받는 것과 현재 업무 책임을 다른 Agent에게 넘기는 것은 무엇이
    다를까요?

범위:
    최소 필드만 사용합니다. 사용자·Task·민감정보·hop count Guard는 05에서 다룹니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 15. 01_single-vs-multi-agent/12_evaluator_reviser.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/12_evaluator_reviser.py"} -->

Lab 01-12: Evaluator–Reviser 패턴의 제한된 반복을 확인합니다.

시나리오:
    Writer Agent가 안내 문장을 작성하고 Evaluator Agent가 필수 안전 문구를 검사합니다.
    기준을 통과하지 못하면 Reviser가 문장을 수정한 뒤 다시 평가합니다. 반복 횟수는
    Python이 최대 5회로 제한하며 Evaluator가 통과시키거나 한도에 도달하면 종료합니다.
    기준을 일찍 통과하면 남은 횟수를 모두 실행하지 않고 즉시 종료합니다.

학습 질문:
    생성 Agent와 평가 Agent의 기준을 분리하면 어떤 장점이 있으며, 반복은 누가
    멈춰야 할까요?

범위:
    Evaluator와 Reviser는 실제 LLM을 사용합니다. 필수 문구 최종 판정과 최대 5회
    종료는 Python이 결정적으로 보장합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 16. 01_single-vs-multi-agent/13_provider_failover.py
<!-- player: {"action": "example", "target": "01_single-vs-multi-agent/13_provider_failover.py"} -->

Lab 01-13: 실제 LLM Provider Failover를 투명하게 확인합니다.

시나리오:
    Summary Agent가 먼저 로컬 Gemma를 호출합니다. Gemma Container 또는 Model이
    준비되지 않아 실패하면 GPT를 두 번째 후보로 호출합니다. 첫 실패를 감추거나
    Mock 답변으로 바꾸지 않고 attempts에 모든 시도와 오류를 남깁니다.

학습 질문:
    Failover로 최종 응답에 성공했더라도 어떤 Provider가 먼저 실패했는지 운영자가
    확인할 수 있어야 하지 않을까요?

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 17. 02_agent-role-and-contract/01_role_definition.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/01_role_definition.py"} -->

Lab 02-01: AI Agent의 역할을 실행 코드보다 먼저 정의합니다.

시나리오:
    여행 서비스에 Weather Agent와 Budget Agent를 추가하려고 합니다. 단순히 이름만
    나누면 두 Agent가 서로의 일을 대신할 수 있으므로 Goal, Responsibility, Non-goal을
    명시해 책임 경계를 먼저 만듭니다.

학습 질문:
    Agent 이름과 Prompt만 다르면 서로 다른 역할이라고 할 수 있을까요?

확인할 내용:
    Role Card에는 Agent가 달성할 목표, 해야 할 일, 하지 말아야 할 일이 함께 들어갑니다.
    이 단계는 역할 설계 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 18. 02_agent-role-and-contract/02_task_decomposition.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/02_task_decomposition.py"} -->

Lab 02-02: 사용자 업무를 Agent가 담당할 작은 Task로 분할합니다.

시나리오:
    사용자는 "부산 여행을 계획해 줘"라고 요청했습니다. 하나의 Agent가 날씨, 장소,
    예산, 안전, 일정 작성을 모두 담당하면 책임과 실패 지점을 구분하기 어렵습니다.
    먼저 업무를 작은 Task로 나누고 각 Task의 담당 Agent와 완료 조건을 정합니다.

학습 질문:
    큰 요청을 문장 길이나 Tool 개수로 나누는 것과 독립 책임으로 나누는 것은 무엇이
    다를까요?

확인할 내용:
    각 Task에는 담당 Agent, 필요한 입력, 기대 출력, 완료 조건이 있습니다. 이 단계는
    Task 설계 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 19. 02_agent-role-and-contract/03_input_output_contract.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/03_input_output_contract.py"} -->

Lab 02-03: 자유 문자열 대신 명시적인 Agent 입출력 계약을 만듭니다.

시나리오:
    Budget Agent가 "부산 여행 예산을 짜 줘"라는 문장만 받으면 기간과 예산 한도를
    추측해야 합니다. 입력 계약으로 필수 정보를 정하고 출력 계약으로 다음 Agent가
    읽을 필드를 고정합니다.

학습 질문:
    자연어 Prompt만으로 Agent 사이의 데이터 형식을 보장할 수 있을까요?

확인할 내용:
    입력과 출력이 Pydantic Model로 검증되고 다음 단계가 필드 이름을 예측하지 않아도
    됩니다. 이 단계는 계약 구조 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 20. 02_agent-role-and-contract/04_role_specific_contracts.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/04_role_specific_contracts.py"} -->

Lab 02-04: Agent 역할마다 다른 출력 계약을 사용합니다.

시나리오:
    Weather Agent는 사용자가 제공한 확인된 날씨를 받고, Budget Agent는 확정된 총예산을
    항목별로 배분합니다. 두 Agent는 서로 다른 업무 결과를 반환해야 합니다.

학습 질문:
    모든 Agent가 summary 하나만 반환하면 다음 Agent가 필요한 정보를 안전하게 사용할
    수 있을까요?

확인할 내용:
    역할별 계약은 Agent의 책임을 코드로 드러냅니다. 이 단계는 계약 비교 예제이므로
    실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 21. 02_agent-role-and-contract/05_contract_validation.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/05_contract_validation.py"} -->

Lab 02-05: Agent 결과의 형식과 업무 의미를 차례로 검증합니다.

시나리오:
    외부 Agent가 필수 필드를 빠뜨리거나 다른 역할의 ID를 반환했습니다. 어떤 결과는
    정수 타입을 지켰지만 항목 합계가 total과 다릅니다. Orchestrator는 이런 결과를
    다음 Agent에게 전달하기 전에 차단해야 합니다.

학습 질문:
    JSON 형식과 타입이 올바르면 업무 결과도 올바르다고 볼 수 있을까요?

확인할 내용:
    Pydantic의 필드 검증은 형식 오류를, model_validator는 필드 사이의 업무 규칙을
    검사합니다. 의도적으로 만든 오류 데이터이며 실제 LLM 성공을 흉내 내지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 22. 02_agent-role-and-contract/06_incomplete_result.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/06_incomplete_result.py"} -->

Lab 02-06: 정보가 부족한 Agent 결과를 실패가 아닌 상태로 표현합니다.

시나리오:
    Budget Agent가 여행 요청을 받았지만 숙박 가격과 출발지 교통비가 없습니다. Agent가
    값을 추측하거나 단순 오류를 내는 대신 completed와 missing_information으로 다음
    행동에 필요한 정보를 알려 줍니다.

학습 질문:
    실행 실패와 사용자 정보 부족을 같은 오류로 처리해야 할까요?

확인할 내용:
    Orchestrator는 completed=False를 보고 사용자에게 추가 정보를 요청할 수 있습니다.
    이 단계는 상태 계약 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 23. 02_agent-role-and-contract/07_real_multi_llm_contracts.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/07_real_multi_llm_contracts.py"} -->

Lab 02-07: 네 실제 AI Agent가 역할별 출력 계약을 지키는지 확인합니다.

시나리오:
    하나의 부산 여행 요청을 Weather, Place, Budget, Safety Agent가 각자의 관점에서
    처리합니다. 네 Agent는 Gemini, Llama, GPT, Gemma를 하나씩 사용하고 서로 다른
    Pydantic 계약으로 결과를 반환합니다.

학습 질문:
    Provider가 달라져도 Agent 사이의 출력 계약을 동일한 방식으로 검증할 수 있을까요?

확인할 내용:
    실제 Provider, Model, 지연 시간, 결과 또는 오류를 그대로 출력합니다. Provider
    실패나 계약 오류를 고정된 성공 데이터로 바꾸지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 24. 02_agent-role-and-contract/08_verified_result_flow.py
<!-- player: {"action": "example", "target": "02_agent-role-and-contract/08_verified_result_flow.py"} -->

Lab 02-08: 검증된 Agent 결과만 다음 Agent의 Context로 전달합니다.

시나리오:
    GPT Budget Agent가 부산 여행 예산을 작성합니다. Python은 BudgetResult 계약 검증이
    성공한 경우에만 그 결과를 Gemma Itinerary Agent에게 전달합니다. 첫 Agent가
    실패하면 두 번째 Agent는 실행하지 않습니다.

학습 질문:
    첫 Agent가 반환한 자유 문자열을 검증 없이 다음 Agent의 Prompt에 넣으면 어떤
    문제가 생길까요?

확인할 내용:
    이 예제는 복잡한 Orchestration이 아니라 계약 경계만 다룹니다. 실제 GPT와 Gemma를
    호출하며 오류를 고정된 성공 데이터로 대체하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 25. 03_supervisor-and-routing/01_rule_router.py
<!-- player: {"action": "example", "target": "03_supervisor-and-routing/01_rule_router.py"} -->

Lab 03-01: 명확한 고객지원 요청을 Python Rule Router로 분배합니다.

시나리오:
    고객지원 서비스에는 배송, 환불, 기술지원 Agent가 있습니다. 문의에 명확한 Keyword가
    있으면 LLM을 호출하지 않고 담당 Agent 하나를 선택할 수 있습니다. 정보가 모호하면
    임의로 배정하지 않고 request_information을 반환합니다.

학습 질문:
    모든 자연어 분류에 LLM Router가 필요할까요?

확인할 내용:
    Router Agent는 담당자를 선택할 뿐 고객지원 답변을 직접 작성하지 않습니다. 이
    단계는 결정적인 Routing 규칙 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 26. 03_supervisor-and-routing/02_llm_router.py
<!-- player: {"action": "example", "target": "03_supervisor-and-routing/02_llm_router.py"} -->

Lab 03-02: 실제 GPT Router가 담당 Worker 하나를 선택하고 선택된 Worker만 실행합니다.

시나리오:
    사용자가 "배송이 늦어서 취소하고 싶다"처럼 두 의도가 섞인 문의를 보냈습니다.
    GPT Router Agent가 현재 가장 먼저 필요한 역할을 구조화된 계약으로 선택하고,
    선택된 실제 Worker Agent만 자신의 Goal을 수행합니다.

학습 질문:
    담당 Agent를 선택하는 책임과 실제 문의에 답하는 책임은 왜 분리해야 할까요?

확인할 내용:
    Router 결과와 Worker 결과, Provider Metadata를 따로 출력합니다. 오류를 고정된 성공
    결과로 바꾸지 않습니다. 정상 흐름에서는 실제 LLM을 2회 호출합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 27. 03_supervisor-and-routing/03_router_contract.py
<!-- player: {"action": "example", "target": "03_supervisor-and-routing/03_router_contract.py"} -->

Lab 03-03: Router의 선택 범위와 정보 부족 상태를 계약으로 제한합니다.

시나리오:
    외부 Router가 존재하지 않는 payment_agent를 선택하거나, 추가 정보가 필요하다고
    하면서 어떤 정보가 필요한지는 반환하지 않았습니다. 반대로 Worker를 선택하면서
    missing_information도 함께 반환한 모순 사례가 있습니다.

학습 질문:
    LLM Router의 선택을 Prompt 지시만으로 안전하게 제한할 수 있을까요?

확인할 내용:
    Pydantic Literal과 의미 검증이 허용 목록 및 상태 모순을 차단합니다. 의도적으로
    만든 오류 입력이며 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 28. 03_supervisor-and-routing/04_supervisor_decision.py
<!-- player: {"action": "example", "target": "03_supervisor-and-routing/04_supervisor_decision.py"} -->

Lab 03-04: 실제 GPT Supervisor가 현재 State를 보고 다음 행동을 한 번 결정합니다.

시나리오:
    사용자 입력 검증 기능을 개발 중입니다. 요구사항 분석은 끝났지만 구현과 검토는
    남아 있습니다. Supervisor Agent는 사용자 요청과 현재 State를 읽고 다음 Worker
    또는 finish를 선택합니다.

학습 질문:
    사용자 요청만 보는 Router와 중간 State를 함께 보는 Supervisor는 무엇이 다를까요?

확인할 내용:
    Supervisor는 구현 결과를 직접 작성하지 않고 다음 행동, 지시, 전달할 Context Key와
    이유만 반환합니다. 실제 GPT를 1회 호출합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 29. 03_supervisor-and-routing/05_supervisor_worker_loop.py
<!-- player: {"action": "example", "target": "03_supervisor-and-routing/05_supervisor_worker_loop.py"} -->

Lab 03-05: 실제 Supervisor가 Worker 결과를 확인하며 제한된 Loop를 실행합니다.

시나리오:
    입력 검증 기능의 요구사항을 분석하고 안전성 검토까지 수행합니다. GPT Supervisor는
    현재 State를 보고 Gemini Analyst와 Gemma Reviewer를 차례로 선택하며, 각 Worker
    결과가 계약을 통과한 경우에만 다음 결정을 내립니다.

학습 질문:
    Supervisor가 다음 Agent를 선택한다면 최대 단계와 허용 순서도 LLM에 맡겨야 할까요?

확인할 내용:
    Python이 Worker Allowlist, 의존 순서, 중복 실행, 최대 5회 LLM 호출과 실패 종료를
    보장합니다. 정상 흐름은 Supervisor 3회와 Worker 2회로 최대 5회 호출합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 30. 03_supervisor-and-routing/06_router_vs_supervisor.py
<!-- player: {"action": "example", "target": "03_supervisor-and-routing/06_router_vs_supervisor.py"} -->

Lab 03-06: Router와 Supervisor가 적합한 업무를 결정적으로 비교합니다.

시나리오:
    고객지원 단일 문의와 여러 단계가 필요한 코드 변경 요청이 섞여 있습니다. 각 사례에
    필요한 선택 횟수, State, 종료 조건과 실패 지점을 비교해 더 단순한 구조를 고릅니다.

학습 질문:
    LLM이 여러 Agent 중 하나를 선택한다는 이유만으로 모두 Supervisor일까요?

확인할 내용:
    한 번의 담당자 선택은 Router, 중간 결과를 보고 다음 행동을 반복하면 Supervisor가
    적합합니다. 이 단계는 구조 비교 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 31. 03_supervisor-and-routing/07_multi_llm_supervisor_team.py
<!-- player: {"action": "example", "target": "03_supervisor-and-routing/07_multi_llm_supervisor_team.py"} -->

Lab 03-07: GPT Supervisor와 Gemini·Llama·Gemma Worker가 한 Team으로 협업합니다.

시나리오:
    사용자 입력 검증 기능을 분석하고 구현 방법을 작성한 뒤 보안 관점에서 검토합니다.
    GPT Supervisor가 State를 확인하며 Gemini Analyst, Llama Developer, Gemma Reviewer를
    순서대로 선택하고 마지막에 finish를 반환합니다.

학습 질문:
    여러 Provider를 사용해도 누가 다음 Worker를 선택하고 언제 종료할지는 어떻게
    일관되게 통제할 수 있을까요?

확인할 내용:
    반복되는 Worker 설정은 YAML에서 읽지만 허용 순서·중복 실행·최대 7회 호출은
    Python이 통제합니다. 실제 네 LLM의 결과와 오류를 Trace에 보존합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 32. 04_orchestration/01_execution_plan.py
<!-- player: {"action": "example", "target": "04_orchestration/01_execution_plan.py"} -->

Lab 04-01: Agent를 실행하기 전에 의존성이 있는 실행 계획을 검증합니다.

시나리오:
    부산 여행 계획에는 Weather, Place, Budget 조사와 Itinerary 작성이 필요합니다.
    세 Specialist는 서로 독립적이지만 Itinerary Agent는 세 결과가 모두 준비된 뒤에만
    실행할 수 있습니다.

학습 질문:
    Agent 목록만 있으면 어떤 작업을 동시에 실행하고 어디서 기다릴지 알 수 있을까요?

확인할 내용:
    PlanStep의 depends_on과 join으로 병렬 구간과 Join Barrier를 표현합니다. 이 단계는
    실행 계획 학습이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 33. 04_orchestration/02_sequential_workflow.py
<!-- player: {"action": "example", "target": "04_orchestration/02_sequential_workflow.py"} -->

Lab 04-02: 실제 AI Agent 결과를 다음 Agent 입력으로 순서대로 전달합니다.

시나리오:
    부산 소개 콘텐츠를 만들기 위해 Gemini Research Agent가 핵심 내용을 정리하고,
    GPT Writer Agent가 초안을 작성한 뒤 Gemma Reviewer Agent가 누락을 검토합니다.

학습 질문:
    앞 결과가 다음 작업의 필수 입력이라면 Agent를 동시에 실행할 수 있을까요?

확인할 내용:
    앞 Agent 결과가 성공한 경우에만 다음 Agent를 실행하고 오류가 발생하면 뒤 단계를
    Skip합니다. 정상 흐름에서는 실제 LLM을 최대 3회 호출합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 34. 04_orchestration/03_parallel_workers.py
<!-- player: {"action": "example", "target": "04_orchestration/03_parallel_workers.py"} -->

Lab 04-03: 서로 독립적인 실제 LLM Worker를 병렬 실행합니다.

시나리오:
    Weather, Place, Budget Agent는 같은 부산 여행 요청을 받지만 서로의 결과가 없어도
    작업을 시작할 수 있습니다. Gemini, Llama, GPT를 ThreadPool에서 동시에 실행하고
    완료되는 순서대로 결과를 수집합니다.

학습 질문:
    병렬 Worker가 하나의 Shared State를 동시에 직접 수정해도 안전할까요?

확인할 내용:
    Worker는 독립 결과만 반환하고 Orchestrator가 Main Thread에서 결과를 State에
    저장합니다. 실제 LLM을 3회 호출하며 완료 순서는 매번 달라질 수 있습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 35. 04_orchestration/04_join_results.py
<!-- player: {"action": "example", "target": "04_orchestration/04_join_results.py"} -->

Lab 04-04: 검증된 여러 Agent 결과를 Join한 뒤 실제 Itinerary Agent를 실행합니다.

시나리오:
    Weather, Place, Budget Agent의 역할별 결과가 이미 계약 검증을 통과했습니다. Join
    Guard가 세 필수 결과를 확인한 뒤 최소 Context만 Gemma Itinerary Agent에 전달합니다.

학습 질문:
    병렬 Agent가 모두 끝났다는 사실만으로 안전하게 결과를 통합할 수 있을까요?

확인할 내용:
    필수 결과 존재와 역할별 계약을 먼저 확인하고 Join 성공 후에만 실제 Gemma를 1회
    호출합니다. 앞 단계는 고정된 계약 예제이며 LLM 성공을 흉내 내는 결과가 아닙니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 36. 04_orchestration/05_partial_failure.py
<!-- player: {"action": "example", "target": "04_orchestration/05_partial_failure.py"} -->

Lab 04-05: 병렬 Agent 일부가 실패했을 때 세 가지 계속 실행 정책을 비교합니다.

시나리오:
    Weather와 Budget Agent는 성공했지만 Place Agent는 실패했습니다. Fail Fast,
    Best Effort, Required/Optional 정책이 같은 실패를 어떻게 다르게 처리하는지 봅니다.

학습 질문:
    Agent 하나가 실패하면 항상 전체 Workflow를 실패시켜야 할까요?

확인할 내용:
    실패 정책은 LLM이 즉석에서 정하지 않고 업무 요구사항으로 미리 정의합니다. 이
    단계는 결정적인 정책 비교 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 37. 04_orchestration/06_handoff_workflow.py
<!-- player: {"action": "example", "target": "04_orchestration/06_handoff_workflow.py"} -->

Lab 04-06: 실제 Support Agent가 최소 Context와 업무 책임을 Refund Agent에 넘깁니다.

시나리오:
    배송 지연 문의를 처리하던 Gemini Support Agent가 환불 조건 확인이 필요하다고
    판단합니다. Handoff 계약과 Python Guard를 통과한 경우에만 Gemma Refund Agent가
    현재 업무의 책임을 인수합니다.

학습 질문:
    결과를 요청하고 돌려받는 함수 호출과 현재 업무 책임을 넘기는 Handoff는 무엇이
    다를까요?

확인할 내용:
    누가 누구에게 어떤 책임과 Context를 넘겼는지 기록하고 사용자, 허용 경로, 민감정보,
    최대 Hop을 검사합니다. 정상 흐름에서는 실제 LLM을 최대 2회 호출합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 38. 04_orchestration/07_distributed_workflow.py
<!-- player: {"action": "example", "target": "04_orchestration/07_distributed_workflow.py"} -->

Lab 04-07: 실제 네 AI Agent의 병렬 실행, Join, State와 Trace를 통합합니다.

시나리오:
    Gemini Weather, Llama Place, GPT Budget Agent가 부산 여행 요청을 병렬 처리합니다.
    Main Thread의 Orchestrator가 결과를 검증해 Shared State에 기록합니다. Weather와
    Budget 필수 결과가 성공하면 선택 결과인 Place가 실패해도 Join을 진행할 수 있습니다.

학습 질문:
    여러 Agent가 동시에 실행돼도 State와 전체 종료를 일관되게 관리하려면 누가 결과를
    기록해야 할까요?

확인할 내용:
    반복 Worker와 Team 구성은 YAML에서 읽지만 병렬 실행, 필수 결과 확인과 종료는
    Python이 통제합니다. 정상 흐름에서는 실제 LLM을 최대 4회 호출합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 39. 05_handoff-and-context/01_minimum_context.py
<!-- player: {"action": "example", "target": "05_handoff-and-context/01_minimum_context.py"} -->

Lab 05-01: 전체 State에서 다음 Agent에 필요한 최소 Context만 선택합니다.

시나리오:
    Weather Agent가 Itinerary Agent에게 일정 조정 책임을 넘깁니다. 전체 대화와 내부
    정보가 아니라 목적지, 기간과 검증된 날씨 결과만 전달합니다.

학습 질문:
    Context를 많이 전달할수록 다음 Agent의 결과가 항상 좋아질까요?

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 40. 05_handoff-and-context/02_handoff_contract.py
<!-- player: {"action": "example", "target": "05_handoff-and-context/02_handoff_contract.py"} -->

Lab 05-02: 책임, 추적 ID, Context 버전을 포함한 Handoff Envelope를 만듭니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 41. 05_handoff-and-context/03_handoff_guard.py
<!-- player: {"action": "example", "target": "05_handoff-and-context/03_handoff_guard.py"} -->

Lab 05-03: YAML 경로 설정과 Python Guard로 Handoff를 검증합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 42. 05_handoff-and-context/04_ownership_transition.py
<!-- player: {"action": "example", "target": "05_handoff-and-context/04_ownership_transition.py"} -->

Lab 05-04: 대상 Agent가 수락한 뒤에만 업무 책임자를 변경합니다.

시나리오:
    Weather Agent가 Handoff를 제안했습니다. Python Guard 검증만으로 소유권을 바꾸지
    않고 Itinerary Agent가 수락한 경우에만 owner_agent를 변경합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 43. 05_handoff-and-context/05_rejection_and_failure.py
<!-- player: {"action": "example", "target": "05_handoff-and-context/05_rejection_and_failure.py"} -->

Lab 05-05: 거절·중복·잘못된 책임자와 대상 실패를 처리합니다.

Handoff가 실패하면 원래 Agent가 책임을 유지합니다. 같은 handoff_id를 다시 처리하거나
현재 책임자가 아닌 Agent가 Handoff를 제안하면 Python이 차단합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 44. 05_handoff-and-context/06_real_agent_handoff.py
<!-- player: {"action": "example", "target": "05_handoff-and-context/06_real_agent_handoff.py"} -->

Lab 05-06: 실제 날씨와 두 LLM으로 Handoff 전체 흐름을 실행합니다.

Open-Meteo 예보를 Gemini Weather Agent가 해석해 Handoff를 제안하고, Python Guard를
통과한 최소 Context만 Gemma Itinerary Agent가 받아 일정을 작성합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 45. 06_multi-agent-safety/01_prompt_injection_defense.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/01_prompt_injection_defense.py"} -->

[시나리오]
여행 계획 서비스의 Supervisor Agent가 사용자 요청을 받습니다.

1. 정상 사용자는 "부산 2박 3일 여행을 계획해 줘"라고 요청합니다.
2. 공격자는 요청 안에 "이전 지시를 무시" 또는 "시스템 프롬프트를 보여 줘"처럼
   Agent의 원래 규칙을 바꾸려는 문장을 넣습니다.
3. Prompt Guard Agent는 LLM보다 먼저 요청을 검사합니다.
4. 정상 요청은 다음 단계로 보내고, 의심 문구가 발견되면 실행을 중단합니다.

[기대 결과]
- 정상 요청: allowed=True
- Injection 의심 요청: allowed=False와 차단 근거 출력

[학습 포인트]
시스템 프롬프트에 "공격을 따르지 마"라고 쓰는 것만으로는 충분하지 않습니다.
입력 검사, Tool 권한, 출력 검증을 서로 독립된 방어선으로 둬야 합니다.
이 예제의 문자열 규칙은 개념 학습용 1차 방어이며 완전한 탐지기가 아닙니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 46. 06_multi-agent-safety/02_input_validation.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/02_input_validation.py"} -->

[시나리오]
Prompt Injection 검사를 통과한 요청을 Input Validation Agent가 구조적으로 검사합니다.

1. 여행지는 비어 있으면 안 됩니다.
2. 여행 일수는 1~14일, 인원은 1~20명이어야 합니다.
3. 사용자 요청은 YAML 정책에 정한 최대 길이를 넘을 수 없습니다.
4. 올바른 입력과 잘못된 입력을 각각 실행해 차이를 확인합니다.

[기대 결과]
- 올바른 입력은 검증된 TravelRequest로 변환됩니다.
- 잘못된 입력은 프로그램을 숨겨서 성공시키지 않고 검증 오류를 출력합니다.

[학습 포인트]
LLM에게 숫자 범위를 판단시키지 않습니다. 형식과 범위는 Pydantic과 Python이
결정적으로 검사하고, LLM에는 검증을 통과한 값만 전달합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 47. 06_multi-agent-safety/03_policy_response_guard.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/03_policy_response_guard.py"} -->

[시나리오]
여러 Worker Agent의 결과를 합친 뒤, 답변을 사용자에게 보내기 직전입니다.

1. 정상 초안은 추천 일정과 예상 비용만 설명합니다.
2. 위험 초안은 실제로 실행하지 않은 예약·결제를 완료했다고 주장합니다.
3. 또 다른 위험 초안은 내부 비밀값 이름과 값을 포함합니다.
4. Response Guard Agent가 Policy를 검사하고 통과한 답변만 반환합니다.

[기대 결과]
- 근거 범위 안의 정상 답변은 허용됩니다.
- 허위 실행 주장이나 민감 정보가 포함된 답변은 차단됩니다.

[학습 포인트]
입력이 안전해도 LLM 출력이 항상 안전한 것은 아닙니다. 응답은 사용자에게 보내기
직전에 별도로 검증하며, 차단된 답변은 그대로 노출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 48. 06_multi-agent-safety/04_agent_tool_permissions.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/04_agent_tool_permissions.py"} -->

[시나리오]
Supervisor Agent가 두 개의 Tool 요청을 전달합니다.

1. Weather Agent는 자신에게 허용된 get_weather Tool을 요청합니다.
2. 같은 Weather Agent가 일정 저장 Tool인 save_itinerary도 요청합니다.
3. Tool Guard는 Agent 이름을 믿지 않고 서버의 allowlist와 요청을 비교합니다.

[기대 결과]
- 날씨 조회는 허용됩니다.
- Weather Agent의 일정 저장은 권한 밖이므로 차단됩니다.

[학습 포인트]
LLM 프롬프트의 역할 설명은 권한 통제가 아닙니다. 실제 Tool 실행 직전에 Python이
Agent별 최소 권한을 강제해야 Prompt Injection이나 잘못된 Routing도 피해를 줄입니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 49. 06_multi-agent-safety/05_approval_boundary.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/05_approval_boundary.py"} -->

[시나리오]
Itinerary Agent가 완성한 부산 일정을 저장하려고 합니다.

1. 승인 정보가 없는 요청을 먼저 검사합니다.
2. 다른 task_id에 발급된 승인을 붙여 다시 검사합니다.
3. 마지막으로 사용자·Task·Tool이 모두 일치하는 승인을 사용합니다.

[기대 결과]
앞의 두 요청은 차단되고, 현재 요청과 정확히 연결된 승인만 허용됩니다.

[학습 포인트]
"승인됨"이라는 Boolean 하나만 확인하면 승인을 다른 작업에 재사용할 수 있습니다.
승인은 사용자, Task, Tool과 함께 묶어서 검증해야 합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 50. 06_multi-agent-safety/06_idempotent_write.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/06_idempotent_write.py"} -->

[시나리오]
일정 저장 직후 네트워크 응답이 끊겨 Supervisor Agent가 같은 요청을 재시도합니다.

1. 첫 번째 요청은 일정을 실제로 저장합니다.
2. 두 번째 요청은 같은 사용자와 idempotency key를 사용합니다.
3. Registry는 첫 결과를 돌려주고 저장 함수는 다시 실행하지 않습니다.

[기대 결과]
두 호출의 결과는 같지만 실제 저장 횟수는 1회입니다.

[학습 포인트]
Retry는 안정성을 높이지만 변경 Tool을 중복 실행할 수 있습니다. 승인과 멱등성은
서로 다른 문제이며 둘 다 필요합니다. 이 Lab은 메모리를 쓰고 운영 단계에서는 Redis로 바꿉니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 51. 06_multi-agent-safety/07_role_context_access_control.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/07_role_context_access_control.py"} -->

[시나리오]
Supervisor Agent가 Weather Agent와 Place Agent에 작업을 나누어 줍니다.

1. 전체 Context에는 여행지, 날짜, 취향, 예산, 내부 메모가 들어 있습니다.
2. 각 Worker Agent에는 YAML에 허용된 필드만 전달합니다.
3. Tool 요청도 같은 사용자의 요청인지 다시 검사합니다.
4. 다른 사용자 ID를 넣은 Agent 요청은 내부에서 왔더라도 차단합니다.

[기대 결과]
- Weather Agent와 Place Agent가 받는 Context가 서로 다르게 출력됩니다.
- 올바른 사용자 요청은 허용되고 다른 사용자 요청은 차단됩니다.

[학습 포인트]
멀티 Agent 내부 통신도 신뢰 경계입니다. Agent마다 필요한 최소 Context만 전달하고
모든 Tool 요청에서 사용자 범위와 역할 권한을 다시 확인합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 52. 06_multi-agent-safety/08_integrated_guardrails.py
<!-- player: {"action": "example", "target": "06_multi-agent-safety/08_integrated_guardrails.py"} -->

[시나리오]
지금까지 분리해서 배운 Guardrail을 하나의 여행 요청 처리 흐름으로 연결합니다.

1. 사용자의 입력 길이와 Prompt Injection 의심 문구를 검사합니다.
2. Supervisor가 만든 Tool 요청을 Agent allowlist로 검사합니다.
3. 변경 Tool이라면 현재 요청과 일치하는 사용자 승인을 검사합니다.
4. 최종 응답에서 허위 예약·결제 표현을 검사합니다.
5. 각 단계의 허용·차단 결과를 Audit Event로 남깁니다.

정상 사례와 공격 사례를 모두 실행합니다. 공격 사례는 입력 단계에서 중단되며,
뒤 단계가 실행되지 않았다는 사실도 Audit Log에서 확인할 수 있습니다.

[기대 결과]
- 정상 사례: input → tool → response 단계가 모두 allowed
- 공격 사례: input 단계가 blocked이고 즉시 종료

[학습 포인트]
Guardrail은 한 번의 LLM 호출이나 하나의 필터가 아닙니다. 입력, Context, Tool,
승인, 출력의 여러 경계에 작고 결정적인 검사를 배치하고 그 결과를 추적해야 합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 53. 07_failure-evaluation-and-tracing/01_evaluation_criteria.py
<!-- player: {"action": "example", "target": "07_failure-evaluation-and-tracing/01_evaluation_criteria.py"} -->

[시나리오]
Itinerary Agent가 부산 여행 일정 초안을 만들었습니다. 바로 사용자에게 전달하지 않고
Evaluation Agent가 평가할 기준을 먼저 정의합니다.

1. 목적지 "부산"이 유지되었는지 검사합니다.
2. 사용자의 "해산물 알레르기" 조건이 포함되었는지 검사합니다.
3. "대중교통" 조건과 예산 정보가 포함되었는지 검사합니다.
4. 모든 조건을 하나의 평균 점수로 숨기지 않고 항목별 True/False로 출력합니다.

[기대 결과]
예제 초안에는 알레르기 조건이 빠져 있으므로 전체 평가는 실패합니다. 출력에서
어떤 기준이 실패했는지 바로 확인할 수 있어야 합니다.

[학습 포인트]
Evaluator Agent를 호출하기 전에 사람이 이해할 수 있는 성공 기준을 먼저 정해야 합니다.
형식·필수 문구처럼 코드로 확인할 수 있는 기준은 LLM이 아니라 Python으로 검사합니다.
이 Lab은 개념 설명용이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 54. 07_failure-evaluation-and-tracing/02_evaluator_agent.py
<!-- player: {"action": "example", "target": "07_failure-evaluation-and-tracing/02_evaluator_agent.py"} -->

[시나리오]
네 Specialist Agent가 만든 결과를 Itinerary Agent가 하나의 일정으로 합쳤습니다.
독립된 Evaluator Agent가 최종 결과에서 사용자 조건과 안전 조건을 확인합니다.

1. 필요한 Agent 네 개가 모두 완료되었는지 검사합니다.
2. 목적지·예산·알레르기·대중교통 조건이 최종 일정에 남았는지 검사합니다.
3. 승인되지 않은 변경 Tool이 실행되지 않았는지 검사합니다.
4. 전체 점수만 출력하지 않고 각 검사 이름과 결과를 출력합니다.

[기대 결과]
준비된 정상 결과는 모든 항목을 통과합니다. 일부 조건을 지우고 다시 실행하면 어떤
검사가 실패하는지 확인할 수 있습니다.

[학습 포인트]
결과를 만든 Agent와 평가하는 Agent의 책임을 분리합니다. 이 Lab은 반복 개선 전에
Evaluator의 입력·출력 구조를 배우는 결정적 예제이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 55. 07_failure-evaluation-and-tracing/03_feedback_loop.py
<!-- player: {"action": "example", "target": "07_failure-evaluation-and-tracing/03_feedback_loop.py"} -->

[시나리오]
실제 AI Agent 세 개가 안전한 여행 예약 안내문을 반복해서 개선합니다.

1. OpenAI Writer Agent가 최초 안내문을 작성합니다.
2. Gemini Evaluator Agent가 필수 안전 문구와 응답 품질을 평가합니다.
3. 실패하면 OpenAI Reviser Agent가 Evaluator의 Feedback을 반영합니다.
4. 수정한 답변을 다시 Evaluator Agent가 검사합니다.
5. 기준을 통과하면 즉시 종료하고, 통과하지 못해도 최대 5회에서 종료합니다.

[기대 결과]
Trace에는 Writer, 각 회차의 Evaluator, 필요한 경우 Reviser 실행이 순서대로 출력됩니다.
통과했다면 5회를 모두 채우지 않고 조기 종료합니다. Provider 오류가 발생하면 Mock
성공으로 바꾸지 않고 failed 상태와 원인을 출력합니다.

[학습 포인트]
Feedback Loop는 같은 질문을 무한 반복하는 Retry가 아닙니다. Evaluator가 구체적인
수정 근거를 만들고 Reviser가 그 근거를 반영합니다. 반복 횟수와 최종 통과 조건은
LLM이 아니라 Python Orchestrator가 결정적으로 통제합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 56. 07_failure-evaluation-and-tracing/04_bounded_retry.py
<!-- player: {"action": "example", "target": "07_failure-evaluation-and-tracing/04_bounded_retry.py"} -->

[시나리오]
Weather Agent가 외부 날씨 서비스에 연결하지만 처음 두 번은 Timeout이 발생합니다.

1. Orchestrator는 Timeout을 일시적 오류로 분류합니다.
2. 같은 작업을 최대 3회까지만 Retry합니다.
3. 각 실패와 성공의 attempt 번호를 Trace에 남깁니다.
4. 셋째 시도에서 성공하면 즉시 반복을 끝냅니다.

[기대 결과]
Trace에는 failed, failed, completed 순서와 1·2·3 attempt가 출력됩니다. 최대 횟수
안에 성공하지 못하면 실패를 숨기지 않고 종료합니다.

[학습 포인트]
Retry는 동일한 작업의 일시적 실패를 다시 시도하는 것입니다. 품질 Feedback을 반영해
내용을 고치는 Reviser Loop와 다릅니다. 이 Lab은 흐름 재현용이라 외부 API를 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 57. 07_failure-evaluation-and-tracing/05_failure_policy.py
<!-- player: {"action": "example", "target": "07_failure-evaluation-and-tracing/05_failure_policy.py"} -->

[시나리오]
Multi-Agent 실행 중 서로 다른 네 종류의 오류가 발생했습니다. Orchestrator Agent는
모든 오류를 무조건 Retry하지 않고 오류 성격에 맞는 다음 행동을 선택합니다.

1. TimeoutError는 제한적으로 Retry합니다.
2. 입력 누락 ValueError는 계획과 입력을 다시 구성합니다.
3. PermissionError는 보안 위반이므로 즉시 차단합니다.
4. 자동 복구할 수 없는 오류는 사람에게 전달합니다.

[기대 결과]
오류마다 retry, replan, block, human이 각각 출력됩니다.

[학습 포인트]
권한 오류를 Retry하면 보안 정책을 반복 공격하게 됩니다. 실패 유형을 분류한 뒤에만
재시도 여부를 결정해야 합니다. 이 Lab은 결정적 정책 예제로 실제 LLM을 사용하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 58. 07_failure-evaluation-and-tracing/06_partial_recovery.py
<!-- player: {"action": "example", "target": "07_failure-evaluation-and-tracing/06_partial_recovery.py"} -->

[시나리오]
Weather, Place, Budget Agent가 병렬 실행되었고 Place Agent만 실패했습니다.

1. 이미 성공한 Weather와 Budget 결과는 버리지 않고 보존합니다.
2. 실패한 Agent가 필수 Agent인지 확인합니다.
3. 선택 Agent만 실패했다면 성공 결과로 계획을 다시 구성합니다.
4. 필수 Agent가 실패했다면 자동 완성을 멈추고 사람에게 전달합니다.

[기대 결과]
현재 예제에서 Place Agent는 선택 Agent이므로 성공 결과를 보존하고 Replan합니다.

[학습 포인트]
Multi-Agent 전체를 처음부터 다시 실행하면 비용과 중복 Tool 실행이 늘어납니다.
실패 범위와 의존성을 확인하고 필요한 부분만 복구합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 59. 07_failure-evaluation-and-tracing/07_quality_trace.py
<!-- player: {"action": "example", "target": "07_failure-evaluation-and-tracing/07_quality_trace.py"} -->

[시나리오]
Supervisor, Worker, Evaluator, Reviser가 참여한 한 번의 여행 계획 실행을 추적합니다.

1. Supervisor가 Worker를 선택합니다.
2. Place Agent가 Timeout으로 실패합니다.
3. Orchestrator가 성공한 결과를 보존하고 Replan합니다.
4. Evaluator가 알레르기 조건 누락을 발견해 Feedback을 남깁니다.
5. Reviser가 수정하고 Evaluator가 다시 통과시킵니다.

[기대 결과]
Trace에서 actor, action, status, attempt, duration, 실패 원인과 Feedback을 시간순으로
확인할 수 있습니다. 최종 답변만 보지 않고 품질이 개선된 과정을 추적합니다.

[학습 포인트]
Trace는 print 문을 많이 남기는 것이 아닙니다. Task·Trace ID와 구조화된 필드를
사용해야 Agent별 지연, 실패, 평가 회차를 나중에 검색하고 비교할 수 있습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 60. 08_multi-ai-agent-service/01_structured_logging.py
<!-- player: {"action": "example", "target": "08_multi-ai-agent-service/01_structured_logging.py"} -->

[시나리오]
Supervisor Agent가 사용자 요청을 Weather Agent에 전달했습니다. 운영자는 나중에 같은
요청에서 어떤 Agent가 무엇을 했는지 검색해야 합니다.

1. 사람이 읽는 자유 문장 대신 정해진 필드의 JSON Log를 만듭니다.
2. task_id와 trace_id로 동일한 요청의 사건을 연결합니다.
3. actor와 event로 어느 Agent가 어떤 행동을 했는지 기록합니다.
4. API Key나 전체 Prompt 같은 민감·과도한 데이터는 기록하지 않습니다.

[기대 결과]
동일한 trace_id를 가진 Supervisor와 Weather Agent Log 두 줄이 JSON으로 출력됩니다.

[학습 포인트]
Log는 최종 결과가 아니라 하나의 사건입니다. 문자열을 이어 붙이기보다 검색 가능한
구조화 필드를 사용합니다. 이 Lab은 형식 설명용이므로 실제 LLM을 호출하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 61. 08_multi-ai-agent-service/02_trace_context.py
<!-- player: {"action": "example", "target": "08_multi-ai-agent-service/02_trace_context.py"} -->

[시나리오]
한 사용자 요청이 Backend, Worker, Supervisor, Weather Agent를 차례로 통과합니다.

1. Backend가 task_id와 trace_id를 한 번 생성합니다.
2. 각 하위 단계는 새 trace_id를 만들지 않고 같은 Trace Context를 전달받습니다.
3. 대신 자신의 순서를 나타내는 step과 actor만 변경합니다.
4. 출력된 Event를 trace_id로 묶으면 전체 실행 경로를 복원할 수 있습니다.

[기대 결과]
네 Event의 trace_id는 같고 step은 1부터 4까지 증가합니다.

[학습 포인트]
Trace는 여러 Log를 하나의 요청 경로로 연결합니다. Agent마다 trace_id를 새로 만들면
분산 실행의 전체 흐름을 찾을 수 없습니다. 이 Lab은 실제 LLM 없이 Context 전파만 봅니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 62. 08_multi-ai-agent-service/03_agent_provider_status.py
<!-- player: {"action": "example", "target": "08_multi-ai-agent-service/03_agent_provider_status.py"} -->

[시나리오]
운영 화면에서 Agent가 어떤 Provider를 사용하는지와 실행 준비 여부를 확인합니다.

1. Supervisor와 Budget Agent는 OpenAI Key가 있는지 확인합니다.
2. Weather와 Itinerary Agent는 Gemini Key가 있는지 확인합니다.
3. Place Agent는 실제 Ollama `/api/tags`에 연결해 Llama 설치 여부를 확인합니다.
4. 상태 확인은 LLM 답변을 생성하지 않으므로 Token을 사용하지 않습니다.

[기대 결과]
각 Agent의 Provider·Model·configured 또는 reachable 상태가 출력됩니다. 연결 실패를
항상 정상으로 바꾸지 않고 오류를 그대로 표시합니다.

[학습 포인트]
Agent 상태와 Provider 상태는 다릅니다. Agent 코드는 준비되어 있어도 API Key나
로컬 Model이 없으면 실제 요청을 처리할 수 없습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 63. 08_multi-ai-agent-service/04_health_check.py
<!-- player: {"action": "example", "target": "08_multi-ai-agent-service/04_health_check.py"} -->

[시나리오]
Load Balancer가 Backend Process만 살아 있는지 확인하면 Redis나 PostgreSQL 장애를
놓칠 수 있습니다. Service Health Agent가 실제 의존성을 각각 확인합니다.

1. Redis에 PING을 보냅니다.
2. PostgreSQL에 SELECT 1을 실행합니다.
3. 두 저장소가 모두 정상이면 ready, 하나라도 실패하면 degraded로 판단합니다.
4. 실패 원인을 숨기지 않고 의존성별 결과를 출력합니다.

[기대 결과]
현재 실행 중인 Redis와 PostgreSQL 연결 결과 및 전체 상태가 출력됩니다.

[학습 포인트]
Process가 실행 중인 liveness와 요청 처리 준비가 된 readiness는 다릅니다. 이 Lab은
실제 저장소를 조회하며 데이터를 변경하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 64. 08_multi-ai-agent-service/05_live_execution_state.py
<!-- player: {"action": "example", "target": "08_multi-ai-agent-service/05_live_execution_state.py"} -->

[시나리오]
실행 중인 Multi-Agent Task의 최신 상태를 Frontend가 빠르게 조회해야 합니다.

1. 교육용 Task를 Redis에 queued 상태로 저장합니다.
2. 같은 task_id로 다시 읽어 현재 Agent와 Progress를 확인합니다.
3. Redis Key에는 TTL이 있어 실시간 상태가 영구적으로 쌓이지 않습니다.
4. 이 예제는 Queue에 넣지 않으므로 Worker와 실제 LLM을 실행하지 않습니다.

[기대 결과]
저장한 task_id, queued 상태, 0% Progress가 Redis에서 그대로 조회됩니다.

[학습 포인트]
Redis는 현재 상태와 빠른 폴링에 적합합니다. 완료 후 장기간 보존할 이력은 PostgreSQL에
저장합니다. 이 Lab은 실제 Redis를 사용하며 고정 성공 결과로 대체하지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 65. 08_multi-ai-agent-service/06_execution_history.py
<!-- player: {"action": "example", "target": "08_multi-ai-agent-service/06_execution_history.py"} -->

[시나리오]
Redis의 실시간 Task가 TTL로 사라진 뒤에도 운영자는 과거 실패를 조사해야 합니다.

1. PostgreSQL의 최근 실행 이력을 조회합니다.
2. task_id, trace_id, 상태, 오류와 시간을 확인합니다.
3. 조회 결과가 없으면 아직 서비스 Task를 실행하지 않았다고 출력합니다.

[기대 결과]
실제 PostgreSQL의 최근 Task가 출력되거나 이력이 없다는 안내가 출력됩니다.

[학습 포인트]
현재 State와 영구 History는 수명이 다릅니다. PostgreSQL은 감사·분석을 위해 완료된
실행과 Trace를 보존합니다. 이 Lab은 실제 DB를 읽고 데이터를 만들지 않습니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 66. 08_multi-ai-agent-service/07_operations_dashboard.py
<!-- player: {"action": "example", "target": "08_multi-ai-agent-service/07_operations_dashboard.py"} -->

[시나리오]
운영자는 개별 Log뿐 아니라 서비스 전체 상태를 한눈에 확인해야 합니다.

1. Redis에서 현재 실행 중이거나 최근 갱신된 Task를 조회합니다.
2. PostgreSQL에서 상태별 Task 수를 집계합니다.
3. Agent별 Event 수와 실패 수를 집계합니다.
4. Dashboard가 사용할 하나의 구조화된 결과로 출력합니다.

[기대 결과]
현재 실행 수, 상태별 Task 수, Agent별 Event·실패 수가 출력됩니다.

[학습 포인트]
Dashboard는 원본 Log를 전부 보여 주는 화면이 아닙니다. 운영자가 판단할 수 있는
상태·횟수·실패 지표를 집계하고, 상세 조사가 필요할 때 task_id와 trace_id로 이동합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 67. 09_integrated-deployment-and-operations/01_deployment_boundary.py
<!-- player: {"action": "example", "target": "09_integrated-deployment-and-operations/01_deployment_boundary.py"} -->

[시나리오]
개발자는 08에서 Backend, Worker, Frontend를 각각 실행했습니다. 운영 환경에서는 세
Process의 책임과 의존성을 먼저 구분해야 장애 범위를 찾을 수 있습니다. 이 예제는 서비스
구성 요소가 어떤 Port와 저장소를 사용하는지 출력합니다. Docker 실행 전 배포 경계를 배웁니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 68. 09_integrated-deployment-and-operations/02_release_config.py
<!-- player: {"action": "example", "target": "09_integrated-deployment-and-operations/02_release_config.py"} -->

[시나리오]
같은 Container Image를 개발·검증·운영에서 재사용하고 환경 변수만 바꿉니다. 비밀값
자체를 출력하지 않고 필수 설정의 존재 여부와 주소 형식만 확인합니다. 코드에 Key를 적지
않고, 배포 전에 잘못된 설정을 발견하면 실행을 멈추는 원칙을 익힙니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 69. 09_integrated-deployment-and-operations/03_health_and_restart.py
<!-- player: {"action": "example", "target": "09_integrated-deployment-and-operations/03_health_and_restart.py"} -->

[시나리오]
Container가 실행 중이라는 사실만으로 요청을 처리할 수 있다고 판단하면 안 됩니다.
Liveness는 Process가 살아 있는지, Readiness는 Redis·PostgreSQL이 준비됐는지 판단합니다.
Health 결과에 따라 재시작할지, 트래픽에서 제외할지, 정상 서비스할지를 출력합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 70. 09_integrated-deployment-and-operations/04_retry_and_fallback.py
<!-- player: {"action": "example", "target": "09_integrated-deployment-and-operations/04_retry_and_fallback.py"} -->

[시나리오]
LLM Provider가 일시적으로 429 또는 503 오류를 반환합니다. 일시 오류만 제한적으로
재시도하고 최대 횟수를 넘으면 Fallback Provider로 넘깁니다. 인증 실패처럼 재시도로
해결되지 않는 오류는 즉시 중단합니다. 실제 대기 없이 판단 흐름만 확인합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 71. 09_integrated-deployment-and-operations/05_release_gate.py
<!-- player: {"action": "example", "target": "09_integrated-deployment-and-operations/05_release_gate.py"} -->

[시나리오]
GitHub Actions가 새 버전을 배포하기 전에 최소 품질 기준을 확인합니다. 구문·보안 검사는
반드시 통과하고, 회귀 평가 점수와 Readiness도 기준을 만족해야 합니다. 여러 결과를 하나의
Release Gate로 합치고 실패 항목을 모두 출력하는 원리를 보여 줍니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 72. 09_integrated-deployment-and-operations/06_deployment_strategy.py
<!-- player: {"action": "example", "target": "09_integrated-deployment-and-operations/06_deployment_strategy.py"} -->

[시나리오]
새 버전을 한 번에 모두 교체하지 않고 일부 트래픽만 Canary로 전달합니다. Error Rate와
P95 Latency가 기준을 만족하면 트래픽을 늘리고, 기준을 벗어나면 이전 버전으로 Rollback
합니다. 실제 AWS Resource를 변경하지 않고 배포 판단만 연습합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 73. 09_integrated-deployment-and-operations/07_incident_drill.py
<!-- player: {"action": "example", "target": "09_integrated-deployment-and-operations/07_incident_drill.py"} -->

[종합 실습 시나리오]
배포 직후 Worker의 LLM 요청 실패율이 높아지고 Queue가 적체됐습니다. 운영자는 Dashboard에서
이상을 발견하고 Trace ID로 실패 범위를 확인한 뒤 재시작·Fallback·Rollback 중 적절한
조치를 선택합니다. 관측 신호를 입력받아 우선 대응 순서를 출력합니다.

실행 위치: 과정 루트. 결과의 error/provider_used/fallback_used를 확인하세요. 특정 외부 Provider 비교는 별도 연결이 필요할 수 있습니다.

## 74. 통합 서비스 실행·구조 확인
<!-- player: {"action": "service"} -->

MCP 18010 → Backend 18108 → Worker → Redis/PostgreSQL. Frontend 18508에서 실행 상태와 이력을 확인합니다.

## 75. 로컬 CI 확인
<!-- player: {"action": "ci"} -->

실제 백엔드 테스트 → Compose config → 이미지 Build. 성공 후 GitHub Workflow의 jobs/steps와 비교합니다.

## 76. GitHub Actions 연결
<!-- player: {"action": "read"} -->

저장소 루트 .github/workflows/07-runtime-ci.yml을 확인하세요. 본인 GitHub 저장소를 연결하고 commit/push 또는 PR로 CI를 실행합니다. 원격 저장소가 없으면 연결 주소를 먼저 정해야 합니다. AWS 배포는 별도 계정·대상 서버·권한이 필요합니다.
