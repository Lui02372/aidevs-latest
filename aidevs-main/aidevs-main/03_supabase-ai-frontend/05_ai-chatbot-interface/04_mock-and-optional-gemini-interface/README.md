# 04_mock-and-optional-gemini-interface

챗봇 화면과 응답 생성 로직을 분리하는 방법을 학습합니다.

기본 실습은 비용이 들지 않는 mock 응답과 샘플 백엔드 응답으로 진행합니다. 프론트엔드 화면에서 Gemini/OpenAI API를 직접 호출하지 않고, 실제 LLM 호출은 FastAPI 백엔드가 담당한다는 기준을 유지합니다.

## 학습 목표

- 화면 코드와 응답 생성 코드를 분리할 수 있습니다.
- 로컬 mock 응답 함수를 만들 수 있습니다.
- `05_ai-chatbot-interface/00_sample_backend`의 `/api/chat/mock` 응답을 화면에 표시할 수 있습니다.
- 선택 실습으로 백엔드의 `/api/chat/gemini` 응답을 화면에 표시할 수 있습니다.
- `st.session_state`로 대화 내용이 화면에 계속 누적되는 구조를 만들 수 있습니다.
- 실제 서비스에서는 LLM API key를 프론트엔드에 두지 않는 이유를 설명할 수 있습니다.

## 예제 파일

```text
01_local-ai-function.py
02_backend-chat-api-client.py
03_chat-api-error-handling.py
04_chat-service-config.py
05_chat-history-session.py
06_backend-gemini-chat-client.py
07_backend-gemini-chat-history.py
08_backend-gemini-chat-with-history.py
```

## 샘플 백엔드 실행

챗봇 UI 실습에서는 `05_ai-chatbot-interface` 안의 챗봇 전용 샘플 백엔드를 사용합니다.

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

## 프론트엔드 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\02_backend-chat-api-client.py
```

## 대화 이력 누적 예제 실행

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\05_chat-history-session.py
```

## 백엔드 Gemini API 호출 예제 실행

이 예제는 Streamlit에서 Gemini SDK를 직접 호출하지 않습니다. `05_ai-chatbot-interface/00_sample_backend`의 `/api/chat/gemini`를 호출하고, 실제 Gemini API key는 백엔드 전용 `.env`에 둡니다.

백엔드 전용 `.env` 준비:

```powershell
cd C:\aidev\03_supabase-ai-frontend\05_ai-chatbot-interface\00_sample_backend
Copy-Item .env.example .env
```

`.env`에 실제 key를 입력합니다.

```env
GEMINI_API_KEY=실제-Gemini-API-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

프론트엔드 실행:

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\06_backend-gemini-chat-client.py
```

## 백엔드 Gemini 대화 이력 예제 실행

`07_backend-gemini-chat-history.py`는 `/api/chat/gemini` 응답을 `st.session_state`에 계속 누적해 화면에 표시합니다.

질문을 입력할 때마다 실제 Gemini API 호출이 발생할 수 있으므로 선택 실습으로 다룹니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\07_backend-gemini-chat-history.py
```

## 최근 대화 이력 함께 전송 예제 실행

`08_backend-gemini-chat-with-history.py`는 화면에 쌓인 대화 중 최근 6개 메시지를 백엔드로 함께 보냅니다. 최근 6개 메시지는 보통 최근 3턴 정도의 대화입니다.

전체 대화를 계속 보내면 요청 크기와 비용이 커질 수 있으므로, 이 예제에서는 최근 일부만 보냅니다. 실제 서비스에서는 더 많은 메시지를 보내거나, 오래된 대화를 요약하거나, DB/Vector DB에서 필요한 기억만 검색해 함께 보내는 방식으로 확장할 수 있습니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\08_backend-gemini-chat-with-history.py
```

## 확인할 내용

- 화면 코드와 응답 생성 코드가 분리되어 있는가?
- mock 응답을 챗봇 메시지로 표시할 수 있는가?
- 백엔드 mock chat API 응답을 챗봇 메시지로 표시할 수 있는가?
- 백엔드 Gemini chat API 응답을 챗봇 메시지로 표시할 수 있는가?
- 백엔드 Gemini chat API 응답을 대화 이력으로 계속 누적할 수 있는가?
- 최근 대화 이력 일부를 백엔드로 함께 보내 문맥을 이어갈 수 있는가?
- API 호출 실패 시 오류 메시지를 보여줄 수 있는가?
- 사용자가 질문을 여러 번 입력해도 이전 대화가 화면에 계속 남아 있는가?
- 대화 초기화 버튼으로 `session_state`의 메시지를 비울 수 있는가?

## 수업 메모

Streamlit 화면은 사용자 입력, 대화 표시, 로딩/오류 표시를 담당합니다. Gemini/OpenAI 같은 실제 LLM API 호출과 API key 관리는 FastAPI 백엔드에서 처리합니다.

Docker와 배포는 이 챕터에서 다루지 않습니다. 서비스 실행 환경과 운영은 `07_multi-agent-service-ops`에서 학습합니다.
