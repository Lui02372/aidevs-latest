# 00_sample_backend

`05_ai-chatbot-interface` 실습을 위한 챗봇 전용 FastAPI 백엔드입니다.

이 백엔드는 `03_api-integration/00_sample_backend`와 역할이 다릅니다.

```text
03_api-integration/00_sample_backend
-> GET/POST API 호출 기초, 응답 표시, 오류 처리 연습

05_ai-chatbot-interface/00_sample_backend
-> 챗봇 화면에서 호출할 mock/Gemini chat API 제공
```

## 제공 API

| Method | URL | 역할 |
| --- | --- | --- |
| `GET` | `/health` | 챗봇 백엔드가 실행 중인지 확인합니다. |
| `POST` | `/api/chat/mock` | 비용 없이 챗봇 화면을 테스트하는 mock 응답을 반환합니다. |
| `POST` | `/api/chat/gemini` | 백엔드에서 Gemini API를 호출하고 응답을 반환합니다. |

`/api/chat/mock`과 `/api/chat/gemini`는 기본적으로 `question`만 받아도 동작합니다. 선택적으로 `messages`를 함께 보내면 백엔드가 최근 대화 문맥을 프롬프트에 포함합니다.

```json
{
  "question": "그럼 예제 코드는 어떻게 되나요?",
  "messages": [
    {"role": "user", "content": "FastAPI가 뭐야?"},
    {"role": "assistant", "content": "Python 웹 API 프레임워크입니다."}
  ]
}
```

## .env 기준

이 폴더의 `.env`는 **백엔드 전용**입니다.

프론트엔드 최상위 `.env`와 역할을 구분합니다.

```text
C:\aidev\03_supabase-ai-frontend\.env
-> Streamlit 프론트엔드용
-> API_BASE_URL=http://127.0.0.1:8000

C:\aidev\03_supabase-ai-frontend\05_ai-chatbot-interface\00_sample_backend\.env
-> 챗봇 FastAPI 백엔드용
-> GEMINI_API_KEY=...
-> GEMINI_MODEL=gemini-2.5-flash-lite
```

중요한 기준은 다음과 같습니다.

```text
Streamlit 화면 코드는 GEMINI_API_KEY를 읽지 않습니다.
Gemini API key는 이 백엔드 폴더의 .env에만 둡니다.
프론트엔드는 백엔드 API 주소(API_BASE_URL)만 알고 있습니다.
```

## 백엔드 .env 만들기

Gemini 실제 호출을 하지 않고 `/api/chat/mock`만 사용할 때는 `.env`가 없어도 됩니다.

`/api/chat/gemini`를 사용할 때만 아래처럼 백엔드 전용 `.env`를 만듭니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\05_ai-chatbot-interface\00_sample_backend
Copy-Item .env.example .env
```

그 다음 `.env` 파일의 값을 실제 key로 바꿉니다.

```env
GEMINI_API_KEY=실제-Gemini-API-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

`.env`는 GitHub에 올리지 않습니다. `.env.example`만 예시로 관리합니다.

## 실행 방법

PowerShell을 하나 열고 챗봇 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\05_ai-chatbot-interface\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

위 명령에서 오류가 나면 다음처럼 실행합니다.

```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

브라우저에서 아래 주소를 열어 확인합니다.

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## Streamlit 화면과 연결

Streamlit 프론트엔드는 최상위 `.env`의 `API_BASE_URL`을 사용합니다.

```env
API_BASE_URL=http://127.0.0.1:8000
```

실행 예시:

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\02_backend-chat-api-client.py
```

Gemini 호출 화면을 확인할 때는:

```powershell
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\06_backend-gemini-chat-client.py
```

최근 대화 이력을 함께 보내는 화면을 확인할 때는:

```powershell
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\08_backend-gemini-chat-with-history.py
```
