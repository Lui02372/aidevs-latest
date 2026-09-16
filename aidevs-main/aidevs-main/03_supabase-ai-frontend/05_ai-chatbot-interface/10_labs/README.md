# 10_labs

`05_ai-chatbot-interface`에서 진행하는 챗봇 UI 실습입니다.

이 실습은 완성형 챗봇 서비스를 만드는 단계가 아닙니다. 사용자 질문을 입력하고, mock assistant 응답을 보여 주고, 필요하면 04 단원의 챗봇 샘플 백엔드 API와 연결하는 흐름을 익히는 단계입니다.

## 실습 목록

```text
lab-01-basic-chat-page.py
lab-02-chat-history-page.py
lab-03-backend-chat-client.py
lab-04-context-chat-client.py
```

## 실행 예시

```powershell
streamlit run .\05_ai-chatbot-interface\10_labs\lab-01-basic-chat-page.py
```

`lab-03`, `lab-04`는 챗봇 샘플 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\05_ai-chatbot-interface\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

그 다음 다른 PowerShell에서 실습 파일을 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\10_labs\lab-04-context-chat-client.py
```

## 실습 기준

- 사용자 메시지와 assistant 메시지를 구분합니다.
- mock 응답 함수를 먼저 사용합니다.
- `lab-03`에서는 `05_ai-chatbot-interface/00_sample_backend`의 `/api/chat/mock`을 호출합니다.
- `lab-04`에서는 최근 6개 메시지를 `messages`로 함께 보내는 구조를 연습합니다.
- `lab-04`의 기본 호출 대상도 `/api/chat/mock`이므로 Gemini API key가 없어도 실습할 수 있습니다.
- 오류 상황은 사용자에게 이해할 수 있는 문장으로 안내합니다.
- 대화 이력은 간단한 화면 미리보기 수준으로만 다루고, 본격적인 상태 관리는 `04_state-session-and-data`에서 진행합니다.
