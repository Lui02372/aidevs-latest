# 05. Usage Log And Realtime Status

이 문서는 서비스 로그 조회와 응답 생성 중 상태 표시를 정리하는 템플릿입니다.

## 서비스 로그 조회

```text
GET /service-logs
-> Authorization header 포함
-> 회원가입, 로그인, 챗봇 호출, 로그아웃 기록 표시
```

## 표시할 항목

| 항목 | 설명 |
| --- | --- |
| `action` | signup, signin, chat, signout |
| `status` | success 또는 failed |
| `detail` 또는 `message` | 로그 상세. `backend_mock`은 `detail`, `backend_service`는 `message`를 사용한다. |
| `created_at` | 발생 시각 |

## 응답 생성 중 상태

99에서는 SSE를 필수로 구현하지 않습니다. 대신 아래 UI로 사용자가 기다리는 상태를 이해할 수 있게 합니다.

```text
st.spinner
st.status
st.empty
```

SSE 기반 실시간 응답 스트리밍은 `04_supabase-ai-mini-project`에서 다룹니다.

## 확인 기준

- [ ] 로그인 전에는 서비스 로그 조회를 막는다.
- [ ] 로그가 없을 때 빈 상태 메시지를 표시한다.
- [ ] 로그가 있을 때 표로 표시한다.
- [ ] 응답 생성 중 상태를 보여 준다.
- [ ] 실패한 API 호출도 사용자가 이해할 수 있는 오류 메시지로 표시한다.
