# 10. Upstash Redis 가이드

Upstash Redis는 관리형 Redis 서비스입니다. 이 과정에서는 로컬 Redis를 설치하지 않고, Upstash Redis로 캐시, 세션, 실시간 이벤트 전달을 실습합니다.

공식 사이트:

```text
Upstash: https://upstash.com/
Upstash Console: https://console.upstash.com/
Upstash Redis Docs: https://upstash.com/docs/redis
REST API Docs: https://upstash.com/docs/redis/features/restapi
```

## 1. Upstash 로그인

브라우저에서 Upstash에 접속합니다.

```text
https://console.upstash.com/
```

GitHub 계정 또는 이메일로 로그인합니다.

## 2. Redis Database 생성

Dashboard에서 Redis database를 만듭니다.

확인할 항목:

```text
Database name
Region
Plan
```

수업에서는 가능한 무료 또는 낮은 비용 범위를 사용합니다.

## 3. REST URL과 REST Token

Upstash Redis 상세 화면에서 REST API 정보를 확인합니다.

보통 아래 값이 있습니다.

```text
UPSTASH_REDIS_REST_URL
UPSTASH_REDIS_REST_TOKEN
```

`.env` 예시:

```env
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-token
```

REST Token은 비밀번호처럼 다룹니다.

## 4. REDIS_URL

일부 예제는 Redis Pub/Sub 또는 일반 Redis client 연결을 위해 `REDIS_URL`을 사용합니다.

예시:

```env
REDIS_URL=rediss://default:password@host:port
```

## 5. REST URL/TOKEN과 REDIS_URL 차이

| 항목 | 사용 방식 | 주로 쓰는 곳 |
| --- | --- | --- |
| `UPSTASH_REDIS_REST_URL` + `UPSTASH_REDIS_REST_TOKEN` | HTTPS REST API 호출 | TTL 캐시, 간단한 get/set |
| `REDIS_URL=rediss://...` | Redis 프로토콜 연결 | Pub/Sub, SSE 이벤트 전달, redis-py |

02 과정의 기본 Redis 예제는 REST URL/TOKEN을 주로 사용합니다.

04 미니 프로젝트의 SSE 실시간 로그 이벤트 전달은 `REDIS_URL`을 사용할 수 있습니다.

## 6. 보안 기준

```text
REST Token은 GitHub에 올리지 않습니다.
REDIS_URL에 포함된 password도 GitHub에 올리지 않습니다.
.env.example에는 예시 값만 둡니다.
화면 캡처에 token 전체가 보이지 않게 합니다.
```

## 7. 체크리스트

```text
[ ] Upstash에 로그인했다.
[ ] Redis database를 만들었다.
[ ] REST URL을 확인했다.
[ ] REST Token을 확인했다.
[ ] 필요한 경우 REDIS_URL을 확인했다.
[ ] token과 password를 .env에만 저장했다.
```

