# 04. Conversation History

이 문서는 사용자별 대화 기록을 조회하고 화면에 표시하는 템플릿입니다.

## 조회 흐름

```text
GET /conversations
-> Authorization header 포함
-> 사용자별 대화 기록 조회
-> 표 또는 카드로 표시
```

## 표시할 항목

| 항목 | 설명 |
| --- | --- |
| `created_at` | 대화 생성 시각 |
| `user_message` | 사용자 질문 |
| `assistant_message` | assistant 응답 |
| `provider` | mock, gemini, upstash-cache 등 |
| `model` | 사용한 모델 이름 또는 cached |

## 이전 대화 활용 UX

프론트엔드에서는 `st.session_state["messages"]`로 현재 화면의 이전 대화를 유지합니다.

실제 LLM context window에 이전 대화를 전달하는 고급 구현은 선택 확장입니다.

## 확인 기준

- [ ] 로그인 전에는 대화 기록 조회를 막는다.
- [ ] 기록이 없을 때 빈 상태 메시지를 표시한다.
- [ ] 기록이 있을 때 표 또는 카드로 표시한다.
- [ ] API 오류가 나면 원인을 화면에 표시한다.
- [ ] `backend_mock`과 `backend_service` 모두 같은 화면에서 표시할 수 있다.
