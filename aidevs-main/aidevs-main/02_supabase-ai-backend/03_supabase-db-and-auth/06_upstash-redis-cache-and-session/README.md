# 06. Upstash Redis Cache And Session

이 단원은 Redis를 깊게 다루기보다, AI 백엔드에서 Redis가 왜 필요한지 최소 예제로 확인합니다.

시간이 부족한 수업에서는 아래 두 가지만 진행합니다.

1. Redis에 값을 저장하고 TTL로 자동 만료되는지 확인합니다.
2. FastAPI 응답을 Redis에 잠깐 저장해 캐시 흐름을 확인합니다.

Rate limit, session, cache-aside 같은 패턴은 실제 서비스에서 중요하지만, 이 단원에서는 용어만 소개하고 구현 실습은 뒤 과정에서 확장합니다.

## Redis를 먼저 이렇게 이해합니다

Supabase는 오래 보관해야 하는 데이터를 저장하는 곳입니다.

예:

- 사용자 정보
- 학습 노트
- 대화 이력
- 서비스 로그

Redis는 짧게 보관하고 빠르게 꺼내 쓰는 임시 저장소입니다.

예:

- 같은 질문에 대한 임시 AI 답변 캐시
- 잠깐 유지할 화면 상태
- 일정 시간 동안의 요청 횟수
- 중복 요청 방지용 값

이 단원에서는 “임시 AI 답변 캐시”만 실습합니다.

## 실행 전 준비

백엔드 과정 루트로 이동하고 가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
```

패키지가 설치되어 있지 않다면 설치합니다.

```powershell
pip install -r requirements.txt
```

`.env` 파일에 Upstash Redis 값이 필요합니다.

```text
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
```

실제 token은 GitHub, 문서, 캡처 화면에 올리지 않습니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `01_redis_set_get_ttl.py` | Redis에 값 저장, 조회, TTL 확인을 가장 작게 실습합니다. |
| `02_fastapi_redis_cache.py` | FastAPI 응답을 Redis에 60초 동안 캐시합니다. |

## 1단계. Redis SET, GET, TTL 확인

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\06_upstash-redis-cache-and-session\01_redis_set_get_ttl.py
```

확인할 흐름:

1. `SET`으로 값을 저장합니다.
2. `GET`으로 값을 다시 조회합니다.
3. `TTL`로 값이 몇 초 뒤 사라지는지 확인합니다.

TTL은 Time To Live의 줄임말입니다. Redis에 저장한 값이 얼마나 오래 살아 있을지 정하는 시간입니다.

## 2단계. FastAPI에서 Redis 캐시 사용

예제 폴더로 이동합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\06_upstash-redis-cache-and-session
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
```

Swagger를 엽니다.

```text
http://127.0.0.1:8004/docs
```

먼저 상태를 확인합니다.

```text
GET /health
```

그다음 같은 질문을 두 번 호출합니다.

```text
GET /ai/mock-answer?question=Redis 캐시는 언제 쓰나요?
```

첫 번째 호출은 `cached: false`가 나옵니다. Redis에 저장된 답변이 없어서 새 mock 답변을 만들기 때문입니다.

두 번째 호출은 `cached: true`가 나옵니다. 같은 질문의 답변을 Redis에서 바로 꺼내 쓰기 때문입니다.

캐시를 지우고 다시 확인하고 싶다면 아래 endpoint를 사용합니다.

```text
DELETE /ai/mock-answer-cache?question=Redis 캐시는 언제 쓰나요?
```

## 이 단원에서 하지 않는 것

아래 내용은 중요하지만 초반 실습에서는 제외합니다.

| 제외한 내용 | 뒤에서 다루는 이유 |
|---|---|
| rate limit | FastAPI, Redis, 사용자 식별 기준을 함께 알아야 해서 초보자에게 흐름이 복잡합니다. |
| session 저장 | 로그인, JWT, 만료 정책을 함께 봐야 해서 Auth 흐름 이후가 더 적절합니다. |
| cache-aside 패턴 | 데이터베이스 조회와 캐시 갱신 전략을 함께 설계해야 합니다. |

이번 단원에서는 Redis가 “짧게 저장했다가 빠르게 꺼내 쓰는 곳”이라는 감각을 만드는 것이 목표입니다.

## 자주 막히는 지점

| 증상 | 확인할 것 |
|---|---|
| `UPSTASH_REDIS_REST_URL` 오류 | `.env` 파일이 `C:\aidev\02_supabase-ai-backend` 아래에 있는지 확인합니다. |
| `401 Unauthorized` | `UPSTASH_REDIS_REST_TOKEN` 값이 올바른지 확인합니다. |
| `404` 또는 연결 오류 | Upstash Console에서 REST URL을 다시 복사합니다. |
| Swagger에서 `cached`가 계속 `false` | 질문 문장이 매번 달라지는지 확인합니다. 캐시는 같은 key일 때만 재사용됩니다. |
| 한글 질문이 이상하게 보임 | 예제는 URL 인코딩을 처리합니다. 브라우저 주소창보다 Swagger에서 먼저 확인합니다. |

## 정리 질문

- Supabase에 저장할 데이터와 Redis에 저장할 데이터는 어떻게 다른가요?
- TTL이 없으면 Redis 캐시에 어떤 문제가 생길 수 있나요?
- AI API 호출 결과를 캐시하면 비용과 응답 속도에 어떤 영향을 줄 수 있나요?
