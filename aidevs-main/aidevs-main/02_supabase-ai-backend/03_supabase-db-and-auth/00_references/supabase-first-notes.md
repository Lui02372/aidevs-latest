# Supabase First Notes

`02_supabase-ai-backend`는 Supabase 중심으로 진행합니다.

처음부터 로컬 노트북에 PostgreSQL과 Redis를 직접 설치하고 운영하면 환경 오류가 많아질 수 있습니다. 이 과정에서는 먼저 Supabase와 Upstash Redis를 사용해 백엔드 서비스 구조를 이해하고, Docker 기반 운영은 이후 과정에서 따로 학습합니다.

## 이 과정에서 사용하는 기준

```text
주 DB: Supabase managed PostgreSQL
인증: Supabase Auth
접근 제어: Supabase Auth/JWT를 먼저 이해하고, RLS는 이후 사용자별 데이터 접근 제어로 확장
로그/대화 이력: Supabase table
임시 캐시/TTL: Upstash Redis
요청 제한/세션/cache-aside: 뒤 과정에서 확장
```

## Supabase와 Upstash Redis의 역할

```text
Supabase
-> 오래 보관할 데이터
-> 사용자 정보, 대화 이력, 서비스 로그, 피드백

Upstash Redis
-> 짧게 보관할 임시 데이터
-> TTL 기반 캐시
-> 중복 요청 방지, 요청 횟수 제한, 임시 세션 상태는 뒤 과정에서 확장
```

## 이 과정에서 하지 않는 것

아래 내용은 `07_multi-agent-service-ops`에서 본격적으로 다룹니다.

```text
Docker로 PostgreSQL 직접 실행
Docker로 Redis 직접 실행
Docker Compose 기반 여러 서비스 운영
AWS 배포
운영 모니터링
Auto Healing
```

## 안내 문장

이 단원에서는 데이터베이스를 직접 설치하지 않고 Supabase를 사용합니다.

Redis도 Docker로 띄우지 않고 Upstash Redis를 사용해 캐시와 TTL 개념을 먼저 익힙니다.

Docker로 DB와 Redis를 직접 운영하는 방식은 이후 `07_multi-agent-service-ops`에서 다룹니다.

지금은 FastAPI가 Supabase와 Upstash Redis에 연결되는 흐름에 집중합니다.
