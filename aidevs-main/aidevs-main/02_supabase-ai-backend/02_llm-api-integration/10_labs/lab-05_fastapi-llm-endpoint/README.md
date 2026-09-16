# Lab 05. FastAPI LLM endpoint

이번 실습에서는 LLM 호출 구조를 FastAPI 엔드포인트로 감쌉니다.

먼저 실제 Gemini API를 호출하지 않고 mock 응답을 반환합니다. 다만 요청 모델과 응답 모델은 `05_fastapi-llm-endpoint/03_gemini_sdk_endpoint.py`로 확장하기 쉬운 형태로 구성합니다. 이 구조는 이후 Supabase 저장과 프론트엔드 연동으로 이어질 수 있습니다.

## 학습 목표

- `POST /ai/chat` 엔드포인트를 만듭니다.
- Pydantic으로 요청과 응답 구조를 정의합니다.
- 응답에 `provider`, `model`, `actual_api_called`를 포함합니다.
- Swagger UI에서 직접 요청을 테스트합니다.
- 실제 프로젝트에서는 mock 함수 위치가 Gemini SDK 호출 위치로 바뀐다는 것을 이해합니다.

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\10_labs\lab-05_fastapi-llm-endpoint
..\..\..\.venv\Scripts\Activate.ps1
uvicorn starter:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn starter:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 확장 기준

```text
현재 lab:
  POST /ai/chat
  -> Pydantic 요청 검증
  -> mock 응답 반환

실제 프로젝트:
  POST /ai/chat
  -> Pydantic 요청 검증
  -> 05_fastapi-llm-endpoint/02_gemini_sdk_endpoint_small.py로 최소 호출 확인
  -> 05_fastapi-llm-endpoint/03_gemini_sdk_endpoint.py로 오류 안내 포함 구현 확인
  -> Supabase 대화 이력 저장으로 확장
```
