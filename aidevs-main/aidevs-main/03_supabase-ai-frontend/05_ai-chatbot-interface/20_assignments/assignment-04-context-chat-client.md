# Assignment 04: Context Chat Client

## 목표

Streamlit 챗봇 화면에서 최근 대화 이력 일부를 백엔드로 함께 보내는 앱을 만듭니다.

이 과제는 장기 기억, DB 저장, 사용자별 대화 조회를 요구하지 않습니다. 본격적인 사용자별 대화 이력 관리는 `04_state-session-and-data`와 `99_final-frontend-project`에서 다룹니다.

## 요구사항

- 메시지 목록을 `st.session_state`에 저장합니다.
- 각 메시지는 `role`, `content`를 포함합니다.
- 최근 6개 메시지만 백엔드로 보냅니다.
- 요청 JSON은 아래 형식을 사용합니다.

```json
{
  "question": "현재 질문",
  "messages": [
    {"role": "user", "content": "이전 질문"},
    {"role": "assistant", "content": "이전 응답"}
  ]
}
```

- 기본 호출 대상은 `05_ai-chatbot-interface/00_sample_backend`의 `/api/chat/mock`입니다.
- 선택 기능으로 `/api/chat/gemini`를 호출할 수 있지만, Gemini API key는 프론트엔드에 두지 않습니다.
- 연결 실패, 타임아웃, HTTP 오류를 처리합니다.
- 대화 초기화 버튼을 제공합니다.

## 주석 기준

코드 안에 다음 내용을 본인 말로 주석 처리합니다.

```text
왜 전체 대화를 보내지 않고 최근 6개 메시지만 보내는가?
나중에는 더 많은 메시지, 요약된 메시지, DB/Vector DB 검색 결과를 함께 보낼 수 있다는 점
Gemini API key는 왜 프론트엔드가 아니라 백엔드 .env에 있어야 하는가?
```

## 제출 파일 예시

```text
assignment-04-context-chat-client.py
```
