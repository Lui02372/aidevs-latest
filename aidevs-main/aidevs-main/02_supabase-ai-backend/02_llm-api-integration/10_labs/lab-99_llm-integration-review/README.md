# Lab 99. LLM API 연동 흐름 종합 복습

이번 lab은 `02_llm-api-integration` 단원의 마무리 실습입니다.

실제 API 호출 없이 FastAPI 서버에서 single-turn과 multi-turn 흐름을 모두 mock으로 구현합니다. 완성한 구조는 이후 Gemini SDK 실제 호출, Supabase 대화 이력 저장, Streamlit 화면 연동, 최종 프로젝트로 확장할 수 있습니다.

## 학습 목표

- LLM 요청/응답 구조를 FastAPI 서비스로 정리합니다.
- 단일 질문 응답과 대화 이력 기반 응답의 차이를 구분합니다.
- 실제 호출 여부를 `actual_api_called`로 명확히 표시합니다.
- 대화 이력을 Supabase에 저장하기 좋은 형태로 반환합니다.
- mock 함수가 이후 Gemini SDK 호출 함수로 교체될 수 있도록 함수 경계를 나눕니다.

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\10_labs\lab-99_llm-integration-review
..\..\..\.venv\Scripts\Activate.ps1
uvicorn starter:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn starter:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 완성 기준

1. `GET /health`가 정상 응답을 반환합니다.
2. `POST /ai/chat`이 단일 질문에 대한 mock 응답을 반환합니다.
3. `POST /ai/chat-with-history`가 이전 대화 이력을 포함해 mock 응답을 반환합니다.
4. 모든 응답에 `provider`, `model`, `actual_api_called`가 포함됩니다.
5. README에 `mock -> Gemini SDK 최소 예제 -> Gemini SDK 안내형 예제 -> OpenAI 선택 비교` 흐름으로 확장할 위치를 설명합니다.
