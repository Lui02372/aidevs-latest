# Assignment 02. API Key와 비용 안전 점검

LLM API는 실제 호출 시 비용이 발생할 수 있습니다. 따라서 API key 관리와 실제 호출 전 점검 절차가 중요합니다.

이 과제에서는 `.env` 또는 환경 변수에서 key를 읽고, placeholder key를 실제 key로 착각하지 않도록 점검하는 프로그램을 작성합니다.

## 제출 목표

- `GEMINI_API_KEY`, `OPENAI_API_KEY`를 환경 변수에서 읽습니다.
- `your-...` 형태의 placeholder 값은 실제 key로 처리하지 않습니다.
- key를 출력할 때 전체 값을 노출하지 않고 마스킹합니다.
- 실제 호출 전 확인해야 할 비용/보안 체크리스트를 출력합니다.

## 제출 파일

```text
starter.py 또는 main.py
README.md
```

## 실행 예시

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\20_assignments\assignment-02_api-key-and-cost-safety\starter.py
```

## 완성 기준

1. key가 없을 때도 오류 없이 실행됩니다.
2. placeholder key를 실제 key로 보지 않습니다.
3. 실제 key가 있을 때도 전체 값을 출력하지 않습니다.
4. Gemini와 OpenAI의 사용 목적 차이를 README에 설명합니다.
5. 실제 호출 전 무료 한도, quota, billing 확인 위치를 README에 정리합니다.
