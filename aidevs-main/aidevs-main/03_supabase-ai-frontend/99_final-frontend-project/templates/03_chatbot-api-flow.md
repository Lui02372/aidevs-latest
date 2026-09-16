# 03. Chatbot API Flow

이 문서는 Streamlit 챗봇 화면이 backend의 `/chat` API를 호출하는 흐름을 정리하는 템플릿입니다.

## 챗봇 요청

```text
사용자 질문 입력
-> POST /chat
-> Authorization header 포함
-> backend_mock에서는 mock AI 응답 수신
-> backend_service에서는 Gemini 응답 수신
-> st.chat_message로 화면 표시
```

## 요청 예시

```json
{
  "message": "오늘 배운 내용을 요약해줘"
}
```

## 응답 예시

```json
{
  "answer": "수업용 mock AI 답변입니다.",
  "actual_api_called": false,
  "provider": "mock",
  "model": "mock-chat-ux-v1"
}
```

`backend_service`와 연결하면 `provider`는 `gemini` 또는 `upstash-cache`가 될 수 있습니다.

## 프론트엔드 표시 기준

| 항목 | 표시 방법 |
| --- | --- |
| 사용자 질문 | `st.chat_message("user")` |
| assistant 응답 | `st.chat_message("assistant")` |
| 생성 중 상태 | `st.spinner` 또는 `st.status` |
| provider/model | 작은 설명 텍스트 또는 캡션 |
| 오류 | `st.error` |

## 응답 생성 상태

- [ ] `st.spinner`를 사용한다.
- [ ] 오류가 나면 `st.error`로 표시한다.
- [ ] 빈 질문은 보내지 않는다.
- [ ] 로그인 전에는 `/chat`을 호출하지 않는다.
- [ ] 실제 SSE 스트리밍은 04 미니 프로젝트에서 다룬다.
