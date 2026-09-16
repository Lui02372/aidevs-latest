# 01_realtime-log-dashboard-practice

이 단원은 최종 프로젝트를 만들기 전에 **Supabase DB + Upstash Redis + SSE + Streamlit 대시보드** 흐름을 작게 실행해 보는 실습입니다.

## 실습 목표

```text
POST /logs
-> Supabase DB에 로그 저장
-> Upstash Redis로 새 로그 이벤트 publish
-> GET /stream/logs에서 SSE로 이벤트 전송
-> Streamlit 화면에서 실시간 로그 표시
```

## 폴더 구조

```text
01_realtime-log-dashboard-practice
├─ README.md
├─ schema.sql
├─ backend
│  ├─ README.md
│  ├─ requirements.txt
│  ├─ .env.example
│  └─ app
└─ frontend
   ├─ README.md
   ├─ requirements.txt
   ├─ app.py
   ├─ frontend_common.py
   └─ pages
      ├─ 00_overview.py
      ├─ 01_log_input_and_query.py
      ├─ 02_sse_timed_receive.py
      └─ 03_sse_continuous_receive.py
```

## 실행 순서

1. Supabase SQL Editor에서 `schema.sql`을 실행합니다.
2. `C:\aidev\04_supabase-ai-mini-project`에 `.venv`를 만들고 패키지를 설치합니다.
3. `C:\aidev\04_supabase-ai-mini-project\.env`를 준비합니다.
4. Upstash Redis의 `rediss://...` URL을 `REDIS_URL`에 입력합니다.
5. backend를 실행합니다.
6. frontend를 실행합니다.
7. Streamlit 왼쪽 메뉴에서 `화면설명`, `1. 로그입력.조회`, `2. SSE 시간 설정 수신`, `3. SSE 3분 자동 수신`을 순서대로 확인합니다.

Streamlit 화면은 다음처럼 나누어져 있습니다.

| 화면 | 목적 | 확인할 내용 |
| --- | --- | --- |
| `화면설명` | 전체 흐름 안내 | REST 조회와 SSE 수신의 차이, fallback 개념 |
| `1. 로그입력.조회` | 로그 입력/조회 | `POST /logs`, `GET /logs`, `storage_mode` |
| `2. SSE 시간 설정 수신` | 제한 시간 SSE 수신 | 5~60초 동안 새 이벤트 수신, 표/그래프 확인 |
| `3. SSE 3분 자동 수신` | 자동 수신 | 화면 진입 즉시 수신 시작, 약 3분 동안 새 이벤트 수신, 표/그래프 확인 |

`/health`와 `POST /logs` 응답에는 현재 저장/이벤트 전달 방식이 표시됩니다.

```text
storage_mode 또는 last_storage_mode = supabase -> Supabase DB에 저장됨
storage_mode 또는 last_storage_mode = memory -> 수업용 memory fallback에 저장됨
last_event_mode = upstash-redis -> Upstash Redis pub/sub으로 이벤트 전달
last_event_mode = memory -> 수업용 memory queue로 이벤트 전달
```

## 가상환경과 패키지 설치

04 과정은 과정 최상위 `.venv` 하나를 사용합니다. `backend`나 `frontend` 폴더 안에 `.venv`를 따로 만들지 않습니다.

```powershell
cd C:\aidev\04_supabase-ai-mini-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

이미 `.venv`를 만들었다면 `python -m venv .venv`는 다시 실행하지 않아도 됩니다.

## backend 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## frontend 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\frontend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

SSE는 새 이벤트를 기다리는 동안 연결을 열어 두는 방식입니다. 한 화면에서 모든 것을 하려고 하면 버튼을 누른 뒤 멈춘 것처럼 보일 수 있습니다. 그래서 frontend는 `로그입력.조회`, `SSE 시간 설정 수신`, `SSE 3분 자동 수신` 화면으로 분리했습니다.

초보자 실습에서는 한 브라우저 탭에서 `2. SSE 시간 설정 수신` 또는 `3. SSE 3분 자동 수신` 화면을 열고, 다른 탭에서 FastAPI Swagger `http://127.0.0.1:8000/docs` 또는 `1. 로그입력.조회` 화면으로 `POST /logs`를 실행하면서 확인하는 방식을 권장합니다.

`3. SSE 3분 자동 수신` 화면은 화면에 들어가면 바로 `/stream/logs`에 연결합니다. 별도 시작 버튼 없이 약 3분 동안 새 이벤트를 수신하고, 다시 확인하려면 화면을 새로고침하거나 왼쪽 메뉴에서 다른 화면을 눌렀다가 돌아옵니다.

SSE 연결이 오래 열려 있으면 중간에 아무 이벤트가 없을 때 브라우저나 네트워크가 연결을 끊었다고 판단할 수 있습니다. 이를 막기 위해 backend는 10초마다 `event: heartbeat`를 보내 연결을 유지합니다.

## Upstash Redis와 fallback

이 실습의 기본 경로는 Upstash Redis입니다. `REDIS_URL`에 Upstash의 `rediss://...` URL이 있으면 backend는 Upstash Redis publish/subscribe를 사용합니다. `REDIS_URL`이 비어 있으면 수업 중 실습이 멈추지 않도록 임시 메모리 큐로 SSE 흐름을 확인합니다.

```text
REDIS_URL 있음 -> Upstash Redis 기반 실시간 이벤트
REDIS_URL 없음 -> 임시 메모리 큐 기반 실시간 이벤트
```

최종 프로젝트 설명에서는 Upstash Redis를 기본 구성 요소로 다룹니다.

### Upstash Redis URL은 어디서 확인하나요?

1. [Upstash Console](https://console.upstash.com/)에 로그인합니다.
2. `Redis` 메뉴에서 사용할 database를 선택합니다.
3. database 상세 화면에서 `Connect`, `Details`, `Redis`, `TLS`와 비슷한 이름의 연결 정보 영역을 찾습니다.
4. `rediss://`로 시작하는 Redis protocol URL을 복사합니다.
5. `C:\aidev\04_supabase-ai-mini-project\.env`의 `REDIS_URL`에 붙여 넣습니다.

예시:

```env
REDIS_URL=rediss://default:password@host:port
```

주의:

```text
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
```

위 두 값은 Upstash REST API 방식에서 사용하는 값입니다. 이 실습의 SSE 예제는 Python `redis` 패키지의 `redis.from_url()`을 사용하므로 `rediss://...` 형태의 `REDIS_URL`을 입력합니다.

### `REDIS_URL`과 `UPSTASH_REDIS_REST_URL/TOKEN` 차이

Upstash는 Redis에 연결하는 방법을 크게 두 가지로 제공합니다.

| 구분 | Redis protocol 방식 | REST API 방식 |
| --- | --- | --- |
| 사용하는 환경 변수 | `REDIS_URL` | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` |
| 값의 형태 | `rediss://default:password@host:port` | `https://...upstash.io` + token |
| Python 라이브러리 | `redis`, `redis.asyncio` | `upstash-redis` 또는 HTTP client |
| 연결 방식 | Redis client가 서버에 연결해서 명령 실행 | HTTP 요청으로 Redis 명령 실행 |
| 잘 맞는 예 | pub/sub, queue, 실시간 이벤트 구독 | cache, session, rate-limit, 간단한 key/value 조회 |
| 이번 실습 사용 여부 | 사용 | 사용하지 않음 |

이번 01 실습은 `/stream/logs`에서 새 로그 이벤트를 계속 기다리는 SSE 예제입니다. backend가 Redis pub/sub 채널을 구독해야 하므로 Redis protocol 방식인 `REDIS_URL=rediss://...`를 사용합니다.

반대로 `UPSTASH_REDIS_REST_URL`과 `UPSTASH_REDIS_REST_TOKEN`은 HTTP 요청으로 Redis 명령을 실행할 때 사용합니다. 예를 들어 “질문에 대한 AI 답변을 캐시에 저장”, “사용자 세션 값 저장”, “1분에 몇 번 호출했는지 rate-limit 확인” 같은 예제에 더 잘 맞습니다.

이 REST 방식은 `02_supabase-ai-backend`의 `03_supabase-db-and-auth/06_upstash-redis-cache-and-session`에서 TTL cache로 먼저 다뤘습니다. 04 미니 프로젝트에서는 그 흐름을 필요에 따라 cache, session, rate-limit 기능으로 확장한다고 이해하면 됩니다.

따라서 최종 미니 프로젝트에서는 두 방식이 모두 필요할 수 있습니다.

```text
실시간 로그 스트리밍, pub/sub -> REDIS_URL
캐시, 세션, rate-limit -> UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN
```

단, 01 실습을 실행하는 데는 `REDIS_URL`만 사용합니다.

## schema.sql의 테이블

`schema.sql`에는 두 개의 테이블이 있습니다.

| 테이블 | 이번 01 실습 사용 여부 | 설명 |
| --- | --- | --- |
| `realtime_service_logs` | 사용 | `POST /logs`로 생성한 서비스 로그를 저장합니다. |
| `ai_answer_feedback` | 확장용 | 최종 미니 프로젝트에서 사용자 피드백을 반영한 AI 답변 품질 개선 기능을 만들 때 참고합니다. |

## 자주 나는 오류

### Supabase 테이블을 찾을 수 없음

다음 오류가 나오면 `schema.sql`을 Supabase SQL Editor에서 실행해야 합니다.

```text
Could not find the table 'public.realtime_service_logs'
```

확인할 것:

1. `.env`의 `SUPABASE_URL`이 현재 Supabase 프로젝트와 같은가?
2. `01_realtime-log-dashboard-practice/schema.sql`을 SQL Editor에서 실행했는가?
3. 실행 후 FastAPI backend를 재시작했는가?
