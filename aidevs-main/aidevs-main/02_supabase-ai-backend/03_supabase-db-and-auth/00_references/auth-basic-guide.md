# 인증과 접근 제어 기초

인증은 “사용자가 누구인지 확인하는 것”이고, 접근 제어는 “확인된 사용자가 어떤 데이터에 접근할 수 있는지 결정하는 것”입니다.

Supabase 과정에서는 먼저 Supabase Auth, JWT, Bearer token 흐름을 이해하고, RLS는 “사용자별 데이터 접근 제어에 쓰는 기능”으로 연결해서 이해합니다.

## 기본 흐름

```text
회원가입
-> 로그인
-> access token 발급
-> 백엔드 API 호출
-> 현재 사용자 확인
-> 이후 사용자별 데이터 접근 제어로 확장
```

## 용어 정리

| 용어 | 의미 |
|---|---|
| Auth | 사용자가 누구인지 확인하는 기능 |
| access token | 로그인한 사용자를 증명하는 토큰 |
| Bearer token | API 요청의 `Authorization` 헤더에 access token을 담아 보내는 방식 |
| RLS | Row Level Security, 행 단위 접근 제어 |
| anon key | 공개 클라이언트에서 사용할 수 있는 key |
| service role key | 서버에서만 사용해야 하는 강한 권한의 key |

## 주의할 점

- 비밀번호 원문은 저장하지 않습니다.
- service role key는 FastAPI 같은 서버 코드에서만 사용합니다.
- Streamlit 화면이나 브라우저 코드에는 service role key를 넣지 않습니다.
- 사용자별 데이터는 현재 사용자 ID와 연결해서 다루어야 합니다.
- RLS 정책 SQL 작성은 현재 본문 필수 실습이 아니라 이후 프로젝트에서 확인합니다.

## 현재 과정의 학습 범위

이 단원에서는 Auth/JWT/Bearer token 흐름과 RLS의 필요성을 먼저 이해합니다. 실제 서비스 수준의 보안 심화, 권한 감사, 운영 보안 정책은 이후 과정에서 더 깊게 다룹니다.
