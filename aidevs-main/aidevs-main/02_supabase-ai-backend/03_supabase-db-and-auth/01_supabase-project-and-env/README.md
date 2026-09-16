# 01. Supabase 프로젝트와 환경 변수 준비

이 챕터에서는 Supabase 프로젝트를 만들고, Python/FastAPI 코드에서 사용할 환경 변수를 준비합니다.

`02_supabase-ai-backend` 과정은 Supabase 중심으로 진행합니다. Docker로 PostgreSQL이나 Redis를 직접 실행하지 않습니다. 데이터베이스는 Supabase managed PostgreSQL을 사용하고, Redis가 필요한 실습은 Upstash Redis를 사용합니다. Docker, Docker Compose, 로컬 PostgreSQL/Redis 운영은 `C:\aidev\07_multi-agent-service-ops`에서 본격적으로 다룹니다.

## Supabase란 무엇인가요?

Supabase는 PostgreSQL 데이터베이스, 인증(Auth), 파일 저장소(Storage), API 기능을 한곳에서 제공하는 백엔드 플랫폼입니다.

초보자 입장에서는 다음처럼 이해하면 됩니다.

```text
직접 DB 서버를 설치하지 않고도
웹 브라우저에서 PostgreSQL 데이터베이스를 만들고
Python/FastAPI 코드에서 바로 연결할 수 있게 해주는 서비스
```

이 과정에서 Supabase를 사용하는 이유는 다음과 같습니다.

| 이유 | 설명 |
| --- | --- |
| 설치 부담 감소 | 초반에는 로컬 PostgreSQL 설치보다 API와 DB 연동 흐름을 먼저 이해합니다. |
| 실제 서비스 구조와 유사 | 사용자, 대화 이력, 서비스 로그를 관리형 DB에 저장하는 구조를 익힙니다. |
| 인증 학습 가능 | Supabase Auth로 회원가입/로그인과 사용자별 데이터 접근 개념을 배웁니다. |
| SQL과 API를 함께 학습 | SQL Editor, Table Editor, Python client, FastAPI endpoint를 함께 연결합니다. |

나중에는 실제 노트북에 Docker와 PostgreSQL/Redis를 설치해서 운영하는 방식도 배웁니다. 하지만 이 과정의 01~06 구간에서는 Supabase와 Upstash Redis를 이용해 백엔드 데이터 흐름을 먼저 익힙니다.

## 학습 목표

- Supabase 프로젝트를 생성합니다.
- Supabase Project URL, anon key, service role key의 차이를 이해합니다.
- `.env.example`을 `.env`로 복사하고 필요한 값을 입력합니다.
- placeholder 값을 실제 key로 착각하지 않도록 점검합니다.
- 이후 챕터에서 사용할 Upstash Redis 환경 변수 위치도 함께 확인합니다.

## 준비 순서

### 1. Supabase 계정 접속

1. Supabase 웹사이트에 접속합니다.
2. GitHub 계정 또는 이메일로 로그인합니다.
3. 처음 사용하는 경우 Organization을 생성합니다.

### 2. 새 프로젝트 생성

1. Supabase Dashboard에서 `New project`를 선택합니다.
2. Project name을 입력합니다.
3. Database Password를 설정합니다.
4. Region은 가까운 지역을 선택합니다.
5. 프로젝트 생성이 완료될 때까지 기다립니다.

Database Password는 나중에 직접 PostgreSQL 연결 문자열을 사용할 때 필요할 수 있습니다. 분실하지 않도록 안전한 곳에 보관합니다.

### 3. API URL과 key 확인

Supabase Dashboard에서 다음 위치로 이동합니다.

```text
Project Settings
-> API
```

확인할 값은 다음과 같습니다.

| 값 | `.env` 변수명 | 용도 |
| --- | --- | --- |
| Project URL | `SUPABASE_URL` | Python/FastAPI가 Supabase 프로젝트에 접속할 주소 |
| anon public key | `SUPABASE_ANON_KEY` | 공개 가능한 기본 API key. RLS 정책과 함께 사용 |
| service_role key | `SUPABASE_SERVICE_ROLE_KEY` | 서버에서만 사용하는 강한 권한의 key |

중요한 기준:

```text
anon key:
  공개 가능한 key이지만 RLS 정책을 함께 사용해야 안전합니다.

service role key:
  RLS를 우회할 수 있는 강한 key입니다.
  FastAPI 같은 서버 코드에서만 사용합니다.
  프론트엔드, Streamlit 화면, GitHub 저장소에 노출하면 안 됩니다.
```

## `.env` 파일 만들기

최상위 과정 폴더로 이동합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
```

`.env.example`을 `.env`로 복사합니다.

```powershell
Copy-Item .env.example .env
```

VS Code에서 `.env` 파일을 열고 Supabase 값을 입력합니다.

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
```

Upstash Redis 값은 이 챕터에서 필수는 아닙니다. `06_upstash-redis-cache-and-session`에서 본격적으로 사용합니다.

```env
UPSTASH_REDIS_REST_URL=https://your-upstash-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-redis-rest-token
```

## `.env` 확인 방법

가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
```

`.env` 파일이 있는지 확인합니다.

```powershell
dir .env
```

VS Code에서 `.env` 파일을 열고 아래 항목이 실제 값으로 입력되어 있는지 확인합니다.

```text
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
```

주의할 점:

```text
1. your-... 형태의 예시 값이면 아직 설정이 끝난 것이 아닙니다.
2. SUPABASE_URL은 https:// 로 시작해야 합니다.
3. SUPABASE_ANON_KEY와 SUPABASE_SERVICE_ROLE_KEY를 서로 바꾸어 넣지 않습니다.
4. key 전체 값을 터미널, README, 채팅, 화면 공유에 노출하지 않습니다.
```

수업 중 코드로 확인해야 한다면 `10_labs/lab-01_supabase-env-check`의 `solution.py`를 사용합니다.

## 자주 만나는 문제

### `.env` 파일을 찾지 못하는 경우

이 과정의 Supabase 예제는 `C:\aidev\02_supabase-ai-backend\.env`를 기준으로 값을 읽습니다.

확인 명령:

```powershell
cd C:\aidev\02_supabase-ai-backend
dir .env
```

### 값이 `your-...`로 출력되는 경우

`.env.example`의 예시 값을 그대로 둔 상태입니다. Supabase Dashboard에서 실제 값을 복사해 넣어야 합니다.

### service role key를 어디에 써야 할지 헷갈리는 경우

이 과정에서는 FastAPI 서버 코드에서만 사용한다고 기억하면 됩니다. Streamlit 화면이나 브라우저에서 실행되는 코드에는 넣지 않습니다.

### Supabase 프로젝트가 paused 상태인 경우

무료 프로젝트는 일정 기간 사용하지 않으면 paused 상태가 될 수 있습니다. Supabase Dashboard에서 프로젝트를 다시 활성화한 뒤 실행합니다.

## 완료 체크리스트

```text
[ ] Supabase 계정에 로그인했습니다.
[ ] 새 Supabase 프로젝트를 만들었습니다.
[ ] Project URL을 확인했습니다.
[ ] anon key를 확인했습니다.
[ ] service role key를 확인했습니다.
[ ] .env.example을 .env로 복사했습니다.
[ ] .env에 Supabase 값을 입력했습니다.
[ ] your-... 예시 값을 실제 Supabase 값으로 바꾸었습니다.
[ ] key 전체 값을 문서나 화면에 노출하지 않았습니다.
```
