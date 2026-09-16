# 00_references

`05_ai-chatbot-interface`에서 챗봇 화면을 만들 때 참고하는 보조 문서입니다.

## 문서 목록

| 파일 | 설명 |
| --- | --- |
| `chatbot-interface-notes.md` | 챗봇 UI 구성 요소, mock 응답 기준, 백엔드 연결 흐름을 정리합니다. |

## 학습 기준

- 기본 실습은 mock 응답으로 진행합니다.
- 백엔드 API 연결은 `05_ai-chatbot-interface/00_sample_backend`의 `/api/chat/mock`을 기준으로 먼저 연습합니다.
- Gemini 실제 호출은 `05_ai-chatbot-interface/00_sample_backend`의 `/api/chat/gemini` 선택 API로 확인합니다.
- 프론트엔드에서는 Gemini/OpenAI API key를 직접 사용하지 않고, 실제 LLM 호출은 백엔드 API를 통해 처리합니다.
- 로그인 상태, 사용자별 대화 이력, 서비스 로그는 `04_state-session-and-data`에서 본격적으로 다룹니다.
