# 로컬 Docker 또는 관리형 Cloud 선택

이 실습을 마친 뒤 모든 프로젝트를 Docker와 AWS로 운영해야 하는 것은 아닙니다.
목적·시간·비용·운영 경험에 따라 각자 경로를 선택합니다.

## 같은 역할의 대응 관계

| 이번 로컬 실습 | 관리형 Cloud 예시 |
| --- | --- |
| PostgreSQL Container | Supabase PostgreSQL |
| Redis Container | Upstash Redis |
| FastAPI Container | Render 등의 Backend 서비스 |
| Streamlit Container | Streamlit Community Cloud |
| `.env` | 각 플랫폼의 Secret·환경 변수 설정 |
| EC2와 Compose 직접 운영 | 플랫폼이 Runtime과 배포 일부 관리 |

09에서 다루는 AWS 운영형 경로는 다음과 대응합니다.

| Local Compose | AWS 운영형 구성 |
| --- | --- |
| Application Image | ECR |
| FastAPI API | ECS Service + ALB |
| Queue Worker | 별도 ECS Service |
| PostgreSQL | RDS PostgreSQL |
| Redis | ElastiCache for Redis |
| `.env` Secret | Secrets Manager |
| 구조화 Log | CloudWatch Logs |

Supabase는 각 Project에 PostgreSQL Database를 제공하고, Upstash는 Redis 호환
Database 접속 정보를 제공합니다. 애플리케이션의 Repository 계약을 유지하면 URL과
TLS 설정을 바꾸는 방식으로 이전할 수 있습니다.

## Docker Compose가 적합한 경우

- Container·Network·Volume을 직접 배우고 싶음
- 로컬에서 여러 서비스를 동일하게 재현해야 함
- 팀이 Docker 운영과 장애 대응을 맡을 수 있음
- 서비스 버전과 실행 환경을 직접 통제하고 싶음

## 관리형 Cloud가 적합한 경우

- 수업·Prototype을 빠르게 공개해야 함
- Database 백업·가용성·업데이트 운영 부담을 줄이고 싶음
- Container와 서버 운영보다 애플리케이션 기능에 집중하고 싶음
- 이전 과정에서 Supabase·Upstash·Render·Streamlit Cloud에 익숙함

## 혼합해도 됩니다

```text
로컬 개발: Docker Compose PostgreSQL + Redis
배포: Supabase + Upstash + Render + Streamlit Community Cloud
```

또는 다음처럼 일부만 관리형으로 바꿀 수 있습니다.

```text
EC2 Docker Compose Frontend + Backend
→ Supabase PostgreSQL
→ Upstash Redis
```

중요한 것은 제품 이름이 아니라 역할입니다.

```text
현재 Session은 어디에 저장하는가?
영구 이력은 어디에 저장하는가?
Secret은 누가 관리하는가?
장애와 백업은 누가 책임지는가?
예상 비용과 정리 방법을 알고 있는가?
```

## 선택 체크리스트

| 질문 | 그렇다 | 추천 방향 |
| --- | --- | --- |
| Docker 자체가 학습 목표인가? | 예 | Local Compose부터 |
| 빠른 공개가 가장 중요한가? | 예 | 관리형 Cloud 우선 |
| 서버 장애를 직접 대응할 수 있는가? | 아니요 | 관리형 Cloud 우선 |
| 같은 환경을 여러 PC에서 재현해야 하는가? | 예 | Docker Compose |
| 이전 Supabase·Upstash 실습을 재사용하고 싶은가? | 예 | 관리형 Cloud 또는 혼합 |

## 공식 문서

- [Supabase Database](https://supabase.com/docs/guides/database/overview)
- [Upstash Redis 시작](https://upstash.com/docs/redis/overall/getstarted)
- [Streamlit Community Cloud 배포](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Streamlit Secret 관리](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
