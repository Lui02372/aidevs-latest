# Assignment 03: AI Service Client

## 목표

Streamlit 챗봇 화면에서 04 단원의 챗봇 샘플 백엔드 mock chat API를 호출하는 앱을 만듭니다.

## 요구사항

- API 기본 주소를 변수로 분리합니다.
- 질문을 `/api/chat/mock`에 POST 요청으로 보냅니다.
- 요청 JSON은 `{"question": "질문 내용"}` 형식을 사용합니다.
- 응답 JSON의 `answer` 값을 assistant 메시지로 표시합니다.
- 연결 실패, 타임아웃, HTTP 오류를 처리합니다.
- 실제 AI 모델 호출은 필수가 아닙니다.
- 프론트엔드에서 Gemini/OpenAI API key를 직접 사용하지 않습니다.
- 실제 AI 모델 호출이 필요하면 FastAPI 백엔드 API를 통해 연결합니다.

## 백엔드 기준

이 과제에서 사용하는 백엔드는 다음 폴더입니다.

```text
05_ai-chatbot-interface/00_sample_backend
```

mock 응답은 `.env` 없이도 동작합니다.

```text
POST /api/chat/mock
```

Gemini 실제 호출은 선택 기능이며, 이 경우에도 key는 프론트엔드가 아니라 백엔드 전용 `.env`에 둡니다.

```text
05_ai-chatbot-interface/00_sample_backend/.env
```

## 제출 파일 예시

```text
assignment-03-ai-service-client.py
```
