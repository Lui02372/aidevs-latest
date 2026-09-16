# Assignment 03. Single-turn mock to Gemini SDK

사용자 질문 하나와 메모 컨텍스트 하나를 받아 mock LLM 응답을 만드는 과제입니다.

실제 API를 호출하지 않지만, 응답 구조는 실제 LLM API 연동 결과처럼 설계합니다. 제출 README에는 이 mock 함수가 이후 Gemini SDK 호출로 어떻게 교체될 수 있는지 설명합니다.

## 제출 목표

- `build_prompt()` 함수로 메모와 질문을 프롬프트로 정리합니다.
- `call_mock_llm()` 함수로 mock 응답을 반환합니다.
- 응답에 `provider`, `model`, `actual_api_called`, `answer`, `usage`를 포함합니다.
- token 사용량은 정확한 계산이 아니라 추정값으로 표시합니다.
- `call_mock_llm()`을 Gemini SDK 호출 함수로 바꿀 때 필요한 입력값과 출력값을 정리합니다.

## 제출 파일

```text
starter.py 또는 main.py
README.md
```

## 실행 예시

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\20_assignments\assignment-03_single-turn-mock-to-gemini-sdk\starter.py
```

## 완성 기준

1. 질문과 메모 컨텍스트가 모두 프롬프트에 반영됩니다.
2. 실제 API 호출 없이 응답을 반환합니다.
3. 출력 결과가 이후 FastAPI 응답 구조로 옮기기 쉬운 딕셔너리 형태입니다.
4. README에 `03_single-turn-call/02_gemini_sdk_single_turn_small.py`로 최소 호출을 확인하는 방법을 설명합니다.
5. README에 `03_single-turn-call/03_gemini_sdk_single_turn.py`처럼 오류 안내를 포함해 확장할 위치를 설명합니다.
