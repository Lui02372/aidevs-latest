# 02_llm-api-integration

이 단원은 FastAPI 백엔드에서 LLM API를 호출하는 기본 흐름을 다룹니다.

비용과 API key 오류를 줄이기 위해 먼저 mock-first 방식으로 요청/응답 구조를 확인합니다. 이후 Gemini SDK를 기본 구현 방식으로 사용하고, OpenAI SDK는 선택 비교 예제로 다룹니다.

## 학습 순서

1. [01_llm-api-concepts](./01_llm-api-concepts/README.md)에서 LLM API 요청/응답 구조를 문서로 이해합니다.
2. [02_api-key-and-billing](./02_api-key-and-billing/README.md)에서 API key, 비용, 호출 제한, `.env` 관리 기준을 확인합니다.
3. [03_single-turn-call](./03_single-turn-call/README.md)에서 단일 요청/응답 흐름을 실습합니다.
4. [04_multi-turn-call](./04_multi-turn-call/README.md)에서 대화 이력과 multi-turn 호출을 확인합니다.
5. [05_fastapi-llm-endpoint](./05_fastapi-llm-endpoint/README.md)에서 LLM 호출 흐름을 FastAPI endpoint로 연결합니다.

## 진행 기준

- 기본 LLM 실습은 Gemini SDK 기준으로 진행합니다.
- 각 호출 단원은 `mock -> Gemini SDK 최소 예제 -> Gemini SDK 안내형 예제 -> OpenAI 선택 비교` 순서로 봅니다.
- OpenAI 예제는 선택/비교 실습으로 유지합니다.
- 실제 API key는 `.env`에만 넣고 GitHub에 올리지 않습니다.

## 실습과 과제

- [10_labs](./10_labs/README.md)는 수업 중 01~05 흐름을 따라가며 직접 실행하는 실습입니다.
- [20_assignments](./20_assignments/README.md)는 같은 흐름을 개인 과제로 다시 구현하고, 마지막에 FastAPI LLM API 구조 분리까지 연습합니다.
