# 09. Supabase 계정과 프로젝트 가이드

Supabase는 PostgreSQL 기반의 관리형 백엔드 플랫폼입니다. 이 과정에서는 DB, Auth, RLS, API key 관리를 실습할 때 사용합니다.

공식 사이트:

```text
Supabase: https://supabase.com/
Supabase Dashboard: https://supabase.com/dashboard
Supabase Docs: https://supabase.com/docs
```

## 1. Supabase 로그인

브라우저에서 Supabase에 접속합니다.

```text
https://supabase.com/dashboard
```

GitHub 계정 또는 이메일로 로그인합니다.

## 2. 프로젝트 생성

Dashboard에서 새 프로젝트를 만듭니다.

입력 항목:

```text
Organization
Project name
Database password
Region
```

주의:

```text
Database password는 화면 캡처나 README에 적지 않습니다.
Region은 가능하면 가까운 지역을 선택합니다.
프로젝트 생성에는 시간이 조금 걸릴 수 있습니다.
```

## 3. Project URL과 API key 확인

Dashboard에서 아래 메뉴를 찾습니다.

```text
Project Settings
-> API
```

확인할 값:

| 값 | .env 변수명 | 설명 |
| --- | --- | --- |
| Project URL | `SUPABASE_URL` | Supabase 프로젝트 주소 |
| anon public key | `SUPABASE_ANON_KEY` | 프론트/일반 클라이언트에서 제한적으로 사용 |
| service_role key | `SUPABASE_SERVICE_ROLE_KEY` | RLS를 우회할 수 있는 강한 권한의 서버용 key |

## 4. service_role key 주의

`service_role key`는 매우 중요합니다.

```text
GitHub에 올리지 않습니다.
README에 적지 않습니다.
프론트엔드 코드에 넣지 않습니다.
화면 캡처에 보이지 않게 합니다.
FastAPI 백엔드 .env에서만 사용합니다.
```

## 5. SQL Editor 사용

테이블을 만들 때는 Supabase Dashboard의 SQL Editor를 사용합니다.

흐름:

```text
1. SQL Editor를 엽니다.
2. 과정에서 제공하는 schema.sql 내용을 붙여넣습니다.
3. Run을 누릅니다.
4. Table Editor에서 테이블이 생성되었는지 확인합니다.
```

## 6. Auth와 RLS 기본

```text
Auth:
  회원가입, 로그인, 사용자 식별을 담당합니다.

JWT:
  로그인한 사용자를 식별하기 위해 발급되는 token입니다.

RLS:
  Row Level Security입니다.
  사용자별로 볼 수 있는 행을 제한하는 보안 기능입니다.
```

## 7. 체크리스트

```text
[ ] Supabase에 로그인했다.
[ ] 프로젝트를 만들었다.
[ ] SUPABASE_URL을 확인했다.
[ ] SUPABASE_ANON_KEY를 확인했다.
[ ] SUPABASE_SERVICE_ROLE_KEY를 확인했다.
[ ] service_role key를 GitHub에 올리면 안 된다는 점을 이해했다.
[ ] SQL Editor에서 schema.sql을 실행할 수 있다.
```

