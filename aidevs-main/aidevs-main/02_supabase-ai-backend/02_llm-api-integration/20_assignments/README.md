# 20_assignments

LLM API 연동 단원의 과제 모음입니다.

이 폴더의 과제는 `02_llm-api-integration`의 01~05 흐름을 개인 과제로 다시 정리하기 위한 자료입니다.

## 권장 순서

| 순서 | 과제 | 연결 단원 | 제출 초점 |
| --- | --- | --- | --- |
| 1 | `assignment-01_llm-message-design` | `01_llm-api-concepts` | 메시지 구조와 파라미터 설계 |
| 2 | `assignment-02_api-key-and-cost-safety` | `02_api-key-and-billing` | API key 마스킹, 비용/보안 체크 |
| 3 | `assignment-03_single-turn-mock-to-gemini-sdk` | `03_single-turn-call` | single-turn mock 응답과 SDK 확장 지점 |
| 4 | `assignment-04_multi-turn-memory-and-sdk-design` | `04_multi-turn-call` | 대화 이력 관리와 SDK 변환 기준 |
| 99 | `assignment-99_fastapi-llm-mini-service` | 01~05 종합 | 단일 파일 FastAPI mock-first 미니 서비스 |
| 100 | `assignment-100_llm-api-structure-refactor` | 05 확장 | FastAPI LLM API를 `routers/schemas/services` 구조로 분리 |

## 제출 기준

- LLM message 구조를 설명할 수 있습니다.
- API key와 비용 관리 기준을 정리했습니다.
- mock 응답에서 Gemini SDK 호출로 확장하는 흐름을 설명했습니다.
- multi-turn 대화에서 이전 메시지를 어떻게 관리하는지 설명했습니다.
- FastAPI endpoint로 LLM 호출 결과를 반환할 수 있습니다.
- 구조 분리 과제에서는 API 경로, 요청/응답 모델, 서비스 로직을 파일별로 나눌 수 있습니다.

OpenAI 예제는 선택/비교 실습이며 필수 제출 기준은 Gemini와 mock-first 흐름을 우선합니다.

## 파일 작성 기준

각 과제 폴더에는 `starter.py`가 제공됩니다.

```text
수업 중:
  starter.py의 TODO를 채워 실행합니다.

제출 시:
  starter.py를 완성본으로 제출하거나,
  starter.py를 main.py로 복사해 완성본으로 제출합니다.

README.md:
  실행 명령, 구현한 내용, 실제 API 호출 여부, Gemini SDK 확장 위치를 정리합니다.
```
