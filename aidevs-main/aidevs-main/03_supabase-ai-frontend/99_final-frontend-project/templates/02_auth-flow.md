# 02. Auth Flow

이 문서는 회원가입, 로그인, token 저장, 보호 API 호출 흐름을 정리하는 템플릿입니다.

기본 실습은 `backend_mock`을 사용합니다. 실제 서비스 연결을 진행할 때는 같은 API 흐름을 `backend_service`와 연결합니다.

## 회원가입

```text
Streamlit 회원가입 폼
-> POST /auth/signup
-> 성공/실패 메시지 표시
```

응답 예시:

```json
{
  "email": "student@example.com",
  "display_name": "수강생"
}
```

## 로그인

```text
Streamlit 로그인 폼
-> POST /auth/signin
-> access_token 수신
-> st.session_state["access_token"] 저장
-> st.session_state["current_user"] 저장
```

응답 예시:

```json
{
  "access_token": "token-value",
  "token_type": "bearer",
  "user": {
    "email": "student@example.com",
    "display_name": "수강생"
  }
}
```

## 보호 API 호출

```text
Authorization: Bearer {access_token}
```

보호 API 예:

```text
GET /me
POST /chat
GET /conversations
GET /service-logs
```

## 로그아웃

```text
POST /auth/signout
-> session_state 초기화
```

## 확인 기준

- [ ] 로그인 전에는 보호 API를 호출하지 않는다.
- [ ] 로그인 성공 후 token을 저장한다.
- [ ] 로그아웃 후 token과 대화 상태를 정리한다.
- [ ] token 전체를 화면이나 제출 문서에 노출하지 않는다.
- [ ] `backend_service` 사용 시 Supabase 이메일 인증 설정을 확인한다.
