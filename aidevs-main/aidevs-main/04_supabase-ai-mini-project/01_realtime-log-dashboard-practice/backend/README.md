# Backend

FastAPI로 로그 생성, 최근 로그 조회, SSE 실시간 로그 스트림을 제공합니다.

## 처음 실행 준비

04 과정은 `backend` 폴더 안에 `.venv`를 따로 만들지 않고, 과정 최상위 폴더의 `.venv` 하나를 사용합니다.

```text
C:\aidev\04_supabase-ai-mini-project\.venv
```

아직 04 과정 가상환경을 만들지 않았다면 아래 순서대로 실행합니다.

```powershell
cd C:\aidev\04_supabase-ai-mini-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

정상이라면 Python 경로가 아래처럼 보여야 합니다.

```text
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\python.exe
```

이미 `.venv`가 있고 패키지 설치도 끝났다면 이 단계는 다시 하지 않아도 됩니다. 패키지를 다시 설치해야 할 때만 아래 명령을 실행합니다.

```powershell
cd C:\aidev\04_supabase-ai-mini-project
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## API

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | backend 상태 확인 |
| POST | `/logs` | 로그 생성, DB 저장, Upstash Redis publish |
| GET | `/logs` | 최근 로그 조회 |
| GET | `/logs/summary` | level별 로그 수 조회 |
| GET | `/stream/logs` | SSE 실시간 로그 스트림 |

## 저장/이벤트 모드 확인

`GET /health`는 설정값과 최근 실행 모드를 함께 보여 줍니다.

| 응답 필드 | 의미 |
| --- | --- |
| `expected_storage_mode` | `.env` 설정 기준으로 예상되는 저장 방식 |
| `last_storage_mode` | 최근 요청에서 실제 사용된 저장 방식 |
| `last_storage_error` | Supabase 저장 실패 후 memory fallback으로 내려갔을 때의 오류 |
| `expected_event_mode` | `.env` 설정 기준으로 예상되는 이벤트 전달 방식 |
| `last_event_mode` | 최근 요청에서 실제 사용된 이벤트 전달 방식 |
| `last_event_error` | Upstash Redis 연결 실패 후 memory fallback으로 내려갔을 때의 오류 |

`POST /logs` 응답의 `storage_mode`가 `supabase`이면 Supabase DB에 저장된 것이고, `memory`이면 수업용 memory fallback에 저장된 것입니다. memory fallback 데이터는 서버를 끄면 사라집니다.

## 환경변수

기본값은 04 과정 최상위 `.env`에서 읽습니다.

```text
C:\aidev\04_supabase-ai-mini-project\.env
```

`backend/.env.example`은 backend만 따로 배포할 때 참고합니다. 이번 과정에서는 로컬 Redis를 설치하지 않고 Upstash Redis의 `rediss://...` URL을 사용합니다. `REDIS_URL`이 비어 있으면 임시 memory fallback으로 SSE 흐름만 확인합니다.

### Upstash Redis URL 확인 방법

1. [Upstash Console](https://console.upstash.com/)에 로그인합니다.
2. `Redis` 메뉴에서 database를 선택합니다.
3. database 상세 화면의 `Connect` 또는 `Details` 영역을 엽니다.
4. `TLS`, `Redis`, `Redis URL`처럼 표시된 항목에서 `rediss://`로 시작하는 값을 복사합니다.
5. 과정 최상위 `.env`에 아래처럼 입력합니다.

```env
REDIS_URL=rediss://default:password@host:port
```

이 예제는 `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`을 사용하지 않습니다. REST URL/TOKEN은 Upstash REST API 또는 `upstash-redis` SDK 방식에서 사용합니다.

| 구분 | 이번 SSE 예제 | REST API 예제 |
| --- | --- | --- |
| 환경 변수 | `REDIS_URL` | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` |
| 값 형태 | `rediss://default:password@host:port` | `https://...upstash.io` + token |
| Python 코드 | `redis.from_url(REDIS_URL)` | `Redis.from_env()` 또는 HTTP 요청 |
| 주 용도 | pub/sub, 실시간 이벤트 구독 | cache, session, rate-limit |

이번 backend는 `/stream/logs`에서 Redis pub/sub 이벤트를 계속 기다리므로 `REDIS_URL` 방식을 사용합니다.

`UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`은 `02_supabase-ai-backend`의 `03_supabase-db-and-auth/06_upstash-redis-cache-and-session`에서 TTL cache 예제로 먼저 사용했습니다. 최종 미니 프로젝트에서 캐시, 세션, rate-limit 기능을 추가한다면 이 REST 방식 값을 함께 사용할 수 있습니다. 다만 이 01 실습 backend는 REST URL/TOKEN을 읽지 않습니다.

## 테스트

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m pytest tests -q
```

## 자주 나는 오류

### Supabase 테이블을 찾을 수 없음

`realtime_service_logs` 테이블을 찾을 수 없다는 오류가 나오면 Supabase SQL Editor에서 아래 파일을 실행합니다.

```text
C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\schema.sql
```

실행 후 FastAPI backend를 재시작합니다.

### SSE 화면이 멈춘 것처럼 보임

SSE는 새 이벤트가 생길 때까지 연결을 계속 열어 두는 방식입니다. Streamlit에서 `GET /stream/logs 실시간 보기` 버튼을 누르면 정해진 수신 시간 동안 새 로그를 기다립니다.

확인하기 쉬운 방법:

1. Streamlit 화면에서 `GET /stream/logs 실시간 보기`를 누릅니다.
2. 다른 브라우저 탭에서 `http://127.0.0.1:8000/docs`를 엽니다.
3. Swagger에서 `POST /logs`를 실행합니다.
4. Streamlit SSE 영역에 새 로그가 들어오는지 확인합니다.

계속 수신에 가까운 흐름을 확인하고 싶다면 Streamlit 왼쪽 메뉴의 `3. SSE 3분 자동 수신` 화면을 사용합니다. 이 화면은 들어가자마자 `/stream/logs` 연결을 열고, 약 3분 동안 새 로그 이벤트를 받습니다. 연결되면 backend에서는 `event: connected`를 먼저 보내고, 이후 새 로그가 생성될 때마다 `event: log`를 보냅니다. 화면에서 다른 메뉴로 이동하거나 새로고침하면 수신을 다시 시작할 수 있습니다.
