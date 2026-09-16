# 20_assignments

`05_ai-chatbot-interface` 과제 안내입니다.

과제의 핵심은 챗봇 UI의 기본 흐름을 직접 구성하는 것입니다. 실제 로그인, Supabase 저장, 사용자별 대화 관리까지 한 번에 만들지 않습니다.

## 제출 과제

```text
assignment-01-basic-chatbot-ui.md
assignment-02-chat-history-app.md
assignment-03-ai-service-client.md
assignment-04-context-chat-client.md
```

## 제출 기준

- `st.chat_message`와 `st.chat_input`을 사용합니다.
- 사용자 메시지와 assistant 메시지를 구분합니다.
- mock 응답 함수를 별도로 분리합니다.
- 대화 이력은 화면에서 확인 가능한 간단한 목록으로 구성합니다.
- 백엔드 API를 사용하는 경우 `05_ai-chatbot-interface/00_sample_backend`의 `/api/chat/mock` 호출과 연결 실패 처리를 포함합니다.
- 최근 대화 이력을 함께 보내는 경우 최근 6개 메시지만 전송합니다.
- 프론트엔드에서 Gemini/OpenAI API key를 직접 사용하지 않고, 실제 AI 호출은 백엔드 API로 분리합니다.
- 주요 코드 줄에 본인이 이해한 한글 주석을 작성합니다.

## 백엔드 사용 기준

`assignment-03`, `assignment-04`에서 백엔드 API를 호출할 때는 아래 백엔드를 사용합니다.

```text
05_ai-chatbot-interface/00_sample_backend
```

기본 과제는 `/api/chat/mock`을 사용하므로 Gemini API key가 없어도 제출할 수 있습니다.

```text
POST /api/chat/mock
```

`/api/chat/gemini` 연결은 선택 기능입니다. 선택 기능을 구현하더라도 `GEMINI_API_KEY`는 프론트엔드 코드나 프론트엔드 `.env`가 아니라 `05_ai-chatbot-interface/00_sample_backend/.env`에 둡니다.
