# 환경변수와 비밀 정보 관리

API key, database key, Redis token 같은 값은 코드에 직접 적지 않고 `.env` 파일로 관리합니다.

`02_supabase-ai-backend`는 Supabase 중심으로 진행하고, Redis는 Upstash Redis를 사용합니다.

## 기본 원칙

- API key를 코드에 직접 적지 않습니다.
- `.env` 파일을 GitHub에 올리지 않습니다.
- 공유용 예시는 `.env.example`에 작성합니다.
- 실제 key 값은 제출 문서나 README에 적지 않습니다.
- `SUPABASE_SERVICE_ROLE_KEY`는 강한 권한을 가진 key이므로 FastAPI 같은 서버 코드에서만 사용합니다.
- Streamlit 화면이나 브라우저 코드에는 service role key를 넣지 않습니다.
- Upstash Redis token도 FastAPI 서버 코드에서만 사용합니다.

## 환경변수 예시

아래 값은 형식 예시입니다. 실제 값은 Supabase Dashboard와 Upstash Console에서 발급받아 `.env`에 입력합니다.

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

UPSTASH_REDIS_REST_URL=https://your-upstash-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-redis-rest-token

GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite

OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
```

## Key 역할

| 환경변수 | 역할 | 사용 위치 |
|---|---|---|
| `SUPABASE_URL` | Supabase 프로젝트 API 주소 | FastAPI, 필요 시 프론트엔드 |
| `SUPABASE_ANON_KEY` | 공개 클라이언트에서도 사용할 수 있는 제한된 key | RLS와 함께 사용 |
| `SUPABASE_SERVICE_ROLE_KEY` | RLS를 우회할 수 있는 서버 전용 key | FastAPI 서버 |
| `UPSTASH_REDIS_REST_URL` | Upstash Redis REST API 주소 | FastAPI 서버 |
| `UPSTASH_REDIS_REST_TOKEN` | Upstash Redis 호출용 token | FastAPI 서버 |
| `GEMINI_API_KEY` | Gemini API 호출용 key | AI 응답 생성 실습 |
| `OPENAI_API_KEY` | OpenAI API 호출용 key | 선택 실습 또는 비교 실습 |

## Docker 관련 환경변수

`DATABASE_URL`, `REDIS_URL` 같은 로컬 DB/Redis 환경변수는 이 과정의 기본 흐름에서 사용하지 않습니다.

`02_supabase-ai-backend`에서 Redis가 필요할 때는 로컬 Redis 주소 대신 Upstash Redis의 REST URL과 token을 사용합니다.

Docker, PostgreSQL, Redis 운영은 아래 과정에서 본격적으로 다룹니다.

```text
C:\aidev\07_multi-agent-service-ops
```

## 제출 전 확인

문서나 GitHub에 아래 값이 그대로 들어가 있으면 안 됩니다.

```text
eyJ...
sk-...
Bearer ...
```

README에는 “설정 완료”, “실제 값은 제출하지 않음”처럼 상태만 적습니다.
