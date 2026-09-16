# Assignment 99. FastAPI mock-first LLM 미니 서비스

`02_llm-api-integration` 단원의 최종 과제입니다.

FastAPI로 mock-first LLM API 서버를 만들고, single-turn과 multi-turn 요청을 모두 처리합니다. 실제 API 호출은 필수가 아니지만, 이후 Gemini SDK 실제 호출, Supabase 대화 이력 저장, Streamlit 화면 연동으로 확장할 수 있는 구조로 설계합니다.

## 제출 목표

- `GET /health` 엔드포인트를 구현합니다.
- `POST /ai/chat` 엔드포인트로 single-turn mock 응답을 반환합니다.
- `POST /ai/chat-with-history` 엔드포인트로 대화 이력 기반 mock 응답을 반환합니다.
- 모든 응답에 `provider`, `model`, `actual_api_called`를 포함합니다.
- 저장 가능한 메시지 목록을 `messages_for_storage`로 반환합니다.
- mock 응답 생성 함수를 Gemini SDK 호출 함수로 교체할 수 있도록 함수 경계를 분리합니다.

## 제출 파일

```text
starter.py 또는 main.py
README.md
```

## 실행 예시

```powershell
cd C:\aidev\02_supabase-ai-backend\02_llm-api-integration\20_assignments\assignment-99_fastapi-llm-mini-service
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

1. Swagger UI에서 모든 엔드포인트를 테스트할 수 있습니다.
2. Pydantic 모델로 요청과 응답 구조가 정의되어 있습니다.
3. 실제 API 호출 없이 mock 응답을 반환합니다.
4. 대화 이력을 Supabase에 저장하기 좋은 구조로 반환합니다.
5. README에 `05_fastapi-llm-endpoint/02_gemini_sdk_endpoint_small.py`와 `05_fastapi-llm-endpoint/03_gemini_sdk_endpoint.py`로 확장할 위치를 정리합니다.
6. 이후 `assignment-100_llm-api-structure-refactor`에서 같은 기능을 구조 분리 방식으로 다시 정리할 수 있습니다.
