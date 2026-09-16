# Optional LangChain Labs

## Lab 1. Runnable 단계 추가

일정 생성 뒤 예산 초과 여부를 검사하는 `RunnableLambda`를 추가하세요.

## Lab 2. 입력 추적

각 단계의 입력·출력을 리스트에 기록하고 마지막에 출력하세요.

## Lab 3. Tool schema 검증

`07_tool_definition_and_execution.py`에 날짜와 최소 예산 입력을 추가하세요. 잘못된
날짜와 음수 예산이 Tool 실행 전에 거부되는지 확인합니다.

## Lab 4. 검색 결과가 없을 때의 RAG

`09_rag_pipeline.py`에서 관련 점수가 0인 문서를 제외하고, 검색 결과가 없으면
"근거가 부족합니다"를 반환하는 분기를 추가하세요.

## Lab 5. Session 격리

`10_message_history.py`에 두 개의 session ID를 사용하고 서로의 메시지가 섞이지
않는지 출력으로 검증하세요.

## Lab 6. Agent 실행 관찰

`08_create_agent.py`의 반환 메시지에서 AI의 Tool Call, Tool 결과, 최종 답변을
각각 구분해 출력하세요. 실제 예약·결제 Tool은 만들지 않습니다.

## Lab 7. Workflow 확장

`12_langchain_vs_langgraph.py`에 `reject`, `approval`, `answer` 세 경로를 만들고,
각 경로를 선택하는 테스트 입력을 하나씩 작성하세요.
