# Lab 02. API Key 안전 점검

LLM API를 사용할 때 가장 중요한 것은 **API key를 코드에 직접 적지 않는 것**입니다.

이 실습에서는 `.env` 파일이나 환경 변수에 들어 있는 값을 확인하고, placeholder key를 실제 key로 착각하지 않도록 점검합니다. 실제 API 호출은 하지 않습니다.

## 학습 목표

- `GEMINI_API_KEY`, `OPENAI_API_KEY`의 역할을 이해합니다.
- placeholder key와 실제 key를 구분합니다.
- key 일부만 마스킹해서 출력하는 방법을 익힙니다.
- 비용이 발생할 수 있는 실제 호출 전 확인할 항목을 정리합니다.

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\10_labs\lab-02_api-key-safety-check\starter.py
```

## 확인 질문

1. API key를 GitHub에 올리면 어떤 문제가 생길 수 있나요?
2. `.env` 파일은 왜 `.gitignore`에 포함해야 하나요?
3. 실제 API 호출 전에 `actual_api_called` 같은 필드를 두는 이유는 무엇인가요?
