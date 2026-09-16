# 02. SSE, Upstash Redis, DB Guide

실시간 로그 대시보드는 DB, Upstash Redis, SSE의 역할을 구분해야 이해하기 쉽습니다.

## 역할 구분

| 구성요소 | 역할 |
| --- | --- |
| Supabase DB | 로그와 피드백을 영구 저장합니다. 과거 로그 조회와 통계 집계에 사용합니다. |
| Upstash Redis | 새 로그 이벤트를 빠르게 전달합니다. 실시간 화면 표시의 이벤트 통로로 사용합니다. |
| SSE | FastAPI가 프론트엔드로 실시간 이벤트를 보내는 HTTP 스트리밍 방식입니다. |
| Streamlit | 로그 테이블, 차트, 실시간 이벤트 영역을 표시합니다. |

## 기본 흐름

```text
사용자 또는 서비스 이벤트 발생
-> POST /logs
-> Supabase DB에 저장
-> Upstash Redis publish
-> GET /stream/logs SSE endpoint
-> Streamlit 실시간 로그 영역에 표시
```

## 왜 DB만으로는 부족한가요?

DB는 데이터를 안전하게 저장하고 조회하는 데 좋습니다. 하지만 새 이벤트가 생길 때마다 화면에 즉시 알려 주는 용도로는 Upstash Redis 같은 이벤트 통로가 더 단순합니다.

DB만 사용할 수도 있습니다.

```text
Streamlit이 2~3초마다 GET /logs 호출
```

하지만 이 방식은 진짜 스트리밍이라기보다 주기적 조회입니다.

## 왜 Upstash Redis를 사용하나요?

Upstash Redis는 로컬 설치 없이 새 로그 이벤트를 빠르게 전달하기 좋습니다. 이 과정에서는 복잡한 Redis 운영보다 다음 감각을 익히는 데 집중합니다.

```text
로그 저장은 DB
실시간 알림은 Upstash Redis
화면 전달은 SSE
```

## SSE와 WebSocket 차이

| 항목 | SSE | WebSocket |
| --- | --- | --- |
| 방향 | 서버 -> 클라이언트 단방향 | 양방향 |
| 구현 난이도 | 비교적 단순 | 상대적으로 복잡 |
| 적합한 경우 | 로그, 알림, 진행 상태 표시 | 채팅, 게임, 양방향 협업 |

이번 프로젝트는 서버가 새 로그를 화면에 보내면 충분하므로 SSE를 사용합니다.

## 수업용 fallback

Upstash Redis URL이 아직 준비되지 않은 환경에서도 실습이 멈추지 않도록 예제 backend는 메모리 큐 fallback을 제공합니다.

```text
REDIS_URL 있음 -> Upstash Redis publish/subscribe 사용
REDIS_URL 없음 -> 임시 메모리 큐로 SSE 동작 확인
```

최종 설명에서는 Upstash Redis를 기본 구성 요소로 다루되, 수업 진행 안정성을 위해 fallback이 있다는 점을 안내합니다.
