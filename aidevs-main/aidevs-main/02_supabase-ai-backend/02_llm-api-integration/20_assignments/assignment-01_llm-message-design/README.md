# Assignment 01. LLM 메시지 구조 설계

LLM API를 호출하기 전에 메시지 구조와 파라미터를 명확히 설계하는 과제입니다.

실제 API를 호출하지 않고, 사용자의 질문과 메모 컨텍스트를 LLM 요청 구조로 정리합니다.

## 제출 목표

- `system` 메시지와 `user` 메시지를 구분합니다.
- 사용자의 메모와 질문을 하나의 요청 메시지로 구성합니다.
- `provider`, `model`, `temperature`, `top_p`, `max_tokens`, `actual_api_called`를 포함합니다.
- Gemini 기본 모델은 `gemini-2.5-flash-lite`로 둡니다.

## 제출 파일

```text
starter.py 또는 main.py
README.md
```

## 실행 예시

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\20_assignments\assignment-01_llm-message-design\starter.py
```

## 완성 기준

1. 메시지 리스트에 `system`과 `user` 역할이 들어갑니다.
2. 메모 컨텍스트와 사용자 질문이 모두 요청에 포함됩니다.
3. 실제 API를 호출하지 않았다는 의미로 `actual_api_called`가 `False`입니다.
4. 출력 결과만 보고 LLM API 요청 구조를 이해할 수 있습니다.
5. README에 실제 Gemini SDK 호출 전에 왜 message 구조를 먼저 설계하는지 설명합니다.
