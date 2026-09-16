# 10_labs

LLM API 연동 단원의 실습 모음입니다.

이 폴더의 실습은 `02_llm-api-integration`의 01~05 학습 흐름을 수업 중에 직접 확인하기 위한 자료입니다.

## 권장 순서

| 순서 | 실습 | 연결 단원 | 역할 |
| --- | --- | --- | --- |
| 1 | `lab-01_llm-message-and-parameters` | `01_llm-api-concepts` | 메시지와 파라미터 구조를 코드로 확인 |
| 2 | `lab-02_api-key-safety-check` | `02_api-key-and-billing` | API key, 비용, `.env` 안전 점검 |
| 3 | `lab-03_single-turn-mock-to-gemini-sdk` | `03_single-turn-call` | single-turn mock 구조와 Gemini SDK 확장 위치 확인 |
| 4 | `lab-04_multi-turn-mock-to-gemini-sdk` | `04_multi-turn-call` | 대화 이력 기반 multi-turn 구조 확인 |
| 5 | `lab-05_fastapi-llm-endpoint` | `05_fastapi-llm-endpoint` | FastAPI `POST /ai/chat` endpoint 연결 |
| 99 | `lab-99_llm-integration-review` | 01~05 종합 | 전체 흐름을 FastAPI mock 서비스로 복습 |

먼저 mock으로 요청/응답 구조를 확인합니다. 실제 호출은 `02_gemini_sdk_*_small.py`처럼 가장 작은 Gemini SDK 예제로 확인하고, 수업용 기본 구현은 오류 안내가 포함된 `03_gemini_sdk_*` 예제로 확장합니다.
