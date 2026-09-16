# lab-01_llm-message-and-parameters

LLM API에 전달할 message 구조와 기본 파라미터를 설계하는 실습입니다.

## 할 일

1. 사용자 입력 예시를 3개 작성합니다.
2. 각 입력에 필요한 system/user message를 구분합니다.
3. temperature, max output, model 이름을 표로 정리합니다.
4. mock 응답과 실제 LLM 응답에서 공통으로 필요한 필드를 정리합니다.

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\10_labs\lab-01_llm-message-and-parameters\starter.py
```

## 확인 기준

```text
messages:
  system 메시지가 먼저 있는가?
  user 메시지에 메모와 질문이 함께 들어 있는가?

request_options:
  provider, model, temperature, top_p, max_tokens가 있는가?
  실제 호출이 아니므로 actual_api_called가 False인가?
```
