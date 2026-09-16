# Lab 03. Single-turn mock to Gemini SDK

Single-turn 호출은 사용자의 질문 하나에 대해 AI가 한 번 답하는 구조입니다.

이 실습에서는 실제 Gemini API를 호출하지 않고, 요청 구조를 만든 뒤 mock 응답을 반환합니다. 이렇게 하면 비용 없이 LLM 연동 흐름을 먼저 이해할 수 있습니다. 이후 실제 호출이 필요할 때는 `03_single-turn-call/02_gemini_sdk_single_turn_small.py`로 가장 작은 Gemini SDK 호출을 먼저 확인하고, 오류 처리까지 포함하려면 `03_single-turn-call/03_gemini_sdk_single_turn.py`의 구조로 확장합니다.

## 학습 목표

- 사용자 질문과 메모 컨텍스트를 하나의 프롬프트로 정리합니다.
- mock 응답에 `provider`, `model`, `actual_api_called`를 포함합니다.
- 응답 토큰 수를 대략적으로 계산해 사용량 구조를 이해합니다.
- Gemini SDK로 확장할 때 어느 위치에서 실제 모델 호출이 들어가는지 설명할 수 있습니다.

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\10_labs\lab-03_single-turn-mock-to-gemini-sdk\starter.py
```

## Gemini SDK 확장 기준

```text
현재 lab:
  build_prompt()
  -> call_mock_llm()
  -> actual_api_called=False

실제 프로젝트:
  build_prompt()
  -> Gemini SDK generate_content()
  -> actual_api_called=True
```
