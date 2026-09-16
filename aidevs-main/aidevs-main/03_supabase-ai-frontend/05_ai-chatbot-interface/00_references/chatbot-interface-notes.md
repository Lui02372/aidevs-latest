# Chatbot Interface Notes

## 이 단원의 기준

`05_ai-chatbot-interface`는 챗봇 화면의 기본 흐름을 만드는 단원입니다.

기본 실습은 mock 응답으로 진행합니다. 실제 Gemini 응답이 필요할 때도 프론트엔드에서 직접 SDK를 호출하지 않고, `05_ai-chatbot-interface/00_sample_backend`의 FastAPI 백엔드 API를 통해 응답을 받는 구조로 확장합니다.

전체 로그인 상태, 사용자별 대화 저장, 서비스 로그 관리는 다음 단원인 `04_state-session-and-data`에서 본격적으로 다룹니다.

## 챗봇 UI의 기본 요소

- 사용자 질문 입력 영역
- 사용자 메시지 출력 영역
- assistant 응답 출력 영역
- 간단한 대화 이력 미리보기
- mock 응답 함수 또는 백엔드 API 호출 함수
- 로딩 상태와 오류 메시지 표시 영역

## Streamlit 주요 기능

- `st.chat_message("user")`: 사용자 메시지 영역을 표시합니다.
- `st.chat_message("assistant")`: assistant 메시지 영역을 표시합니다.
- `st.chat_input()`: 채팅 입력창을 표시합니다.
- `st.session_state`: 화면이 다시 실행되어도 값을 유지합니다. 이 단원에서는 간단한 메시지 목록 미리보기까지만 사용합니다.
- `st.spinner()`: 응답을 기다리는 동안 로딩 상태를 보여줍니다.

## 백엔드 연결 기준

04 단원의 챗봇 샘플 백엔드를 사용할 때는 다음 엔드포인트를 호출합니다.

```text
POST /api/chat/mock
POST /api/chat/gemini
```

요청 예시는 다음과 같습니다.

```json
{
  "question": "Streamlit 챗봇 UI를 어떻게 만들까요?"
}
```

응답 예시는 다음과 같습니다.

```json
{
  "answer": "mock assistant 응답입니다.",
  "source": "sample_backend"
}
```

## 전체 흐름

```text
질문 입력
-> 화면에 사용자 메시지 표시
-> mock 함수 또는 백엔드 mock API 호출
-> 화면에 assistant 응답 표시
-> 간단한 메시지 목록에 추가
```

SSE 기반 실시간 스트리밍과 Supabase 최종 저장 흐름은 `04_supabase-ai-mini-project`에서 통합 실습으로 다룹니다.
