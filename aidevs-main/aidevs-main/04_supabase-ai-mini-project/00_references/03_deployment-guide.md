# 03. Deployment Guide

이 문서는 `04_supabase-ai-mini-project`를 무료 또는 저비용 배포 서비스에 올려 시연할 때 참고하는 가이드입니다.

초보자 기준으로 아래 4개 서비스를 연결합니다.

```text
Supabase DB -> Supabase Cloud
Upstash Redis -> Upstash
FastAPI backend -> Render
Streamlit frontend -> Streamlit Community Cloud
```

## 공식 문서

배포 서비스 화면은 시간이 지나면 조금씩 바뀔 수 있습니다. 막히면 아래 공식 문서를 함께 확인합니다.

| 서비스 | 공식 문서 |
| --- | --- |
| Render FastAPI | [Deploy a FastAPI App](https://render.com/docs/deploy-fastapi) |
| Upstash Redis | [Upstash Redis REST API](https://upstash.com/docs/redis/features/restapi), [Upstash Python SDK](https://upstash.com/docs/redis/sdks/py/gettingstarted) |
| Streamlit Community Cloud | [Deploy your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app), [Secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) |
| Supabase API Keys | [Understanding API keys](https://supabase.com/docs/guides/getting-started/api-keys) |

## 배포 순서

처음 배포할 때는 아래 순서로 진행합니다.

```text
1. GitHub에 프로젝트 코드 업로드
2. Supabase Cloud에서 DB 프로젝트 생성
3. Supabase SQL Editor에서 schema.sql 실행
4. Upstash Redis database 생성
5. Render에 FastAPI backend 배포
6. Render backend의 /health 확인
7. Streamlit Community Cloud에 frontend 배포
8. Streamlit 화면에서 Render backend URL 연결 확인
```

Streamlit frontend는 Render backend URL을 알아야 합니다. 따라서 backend를 먼저 배포한 뒤 frontend를 배포하는 흐름이 가장 쉽습니다.

## 배포 전 체크

- [ ] `.env` 파일이 GitHub에 올라가지 않는가?
- [ ] `.gitignore`에 `.env`, `.venv`, `__pycache__`, `.pytest_cache`가 포함되어 있는가?
- [ ] Supabase SQL Editor에서 `schema.sql`을 실행했는가?
- [ ] backend 로컬 실행에서 `/health`, `/logs`, `/stream/logs`가 동작하는가?
- [ ] frontend 로컬 실행에서 backend API를 호출할 수 있는가?
- [ ] Supabase service role key 또는 secret key를 frontend에 넣지 않았는가?
- [ ] Streamlit에는 `API_BASE_URL`만 넣는가?

## 1. Supabase DB 배포

Supabase는 PostgreSQL DB를 직접 설치하지 않고 사용할 수 있는 클라우드 DB입니다. 04 미니 프로젝트에서는 서비스 로그와 피드백 데이터를 저장하는 역할을 합니다.

### 1-1. Supabase 프로젝트 만들기

1. [Supabase](https://supabase.com/)에 로그인합니다.
2. Dashboard에서 `New project`를 선택합니다.
3. Organization을 선택합니다.
4. Project name을 입력합니다.
   예: `aidev-log-dashboard`
5. Database password를 입력합니다.
6. Region은 수강생 위치와 가까운 곳을 선택합니다.
7. `Create new project`를 누릅니다.

프로젝트 생성에는 몇 분 정도 걸릴 수 있습니다.

### 1-2. schema.sql 실행

1. Supabase Dashboard에서 만든 프로젝트를 엽니다.
2. 왼쪽 메뉴에서 `SQL Editor`를 엽니다.
3. `New query`를 누릅니다.
4. 아래 파일의 내용을 복사합니다.

```text
C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\schema.sql
```

또는 최종 프로젝트 starter 기준으로는 아래 파일을 사용합니다.

```text
C:\aidev\04_supabase-ai-mini-project\03_project_structure\database\schema.sql
```

5. SQL Editor에 붙여 넣고 `Run`을 누릅니다.
6. 왼쪽 메뉴의 `Table Editor`에서 테이블이 생성되었는지 확인합니다.

### 1-3. Supabase URL과 key 확인

1. Supabase Dashboard에서 프로젝트를 엽니다.
2. `Project Settings` 또는 상단 `Connect` 영역에서 Project URL을 확인합니다.
3. `Settings > API Keys`에서 key를 확인합니다.

Supabase는 새 key 체계와 legacy key 체계가 함께 보일 수 있습니다.

| 용도 | 새 key 체계 | legacy key 체계 | 어디에 넣나 |
| --- | --- | --- | --- |
| frontend 공개용 | `sb_publishable_...` | `anon` | 이번 04 frontend에는 직접 넣지 않습니다. |
| backend 서버용 | `sb_secret_...` | `service_role` | Render backend 환경 변수에 넣습니다. |

이 과정의 예제 코드는 변수명을 `SUPABASE_SERVICE_ROLE_KEY`로 사용합니다. Supabase Dashboard에서 `service_role`이 보이면 그 값을 넣습니다. 새 key 체계만 보이면 서버용 `Secret key` 값을 넣고 같은 변수명에 저장합니다.

주의:

```text
service_role 또는 secret key는 RLS를 우회할 수 있는 강한 권한입니다.
Streamlit frontend, GitHub 코드, README, 화면 캡처에 노출하면 안 됩니다.
```

### 1-4. backend에 넣을 Supabase 환경 변수

Render backend에 다음 값을 넣습니다.

```text
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-server-side-key
```

## 2. Upstash Redis 배포

Upstash Redis는 새 로그가 생겼다는 이벤트를 backend 내부에서 실시간으로 전달하는 역할을 합니다. 04 예제 backend는 `REDIS_URL`이 없으면 memory fallback으로도 동작하지만, 최종 배포 시연에서는 Upstash Redis를 연결하는 것을 권장합니다.

### 2-1. Upstash Redis database 만들기

1. [Upstash Console](https://console.upstash.com/)에 로그인합니다.
2. `Redis`를 선택합니다.
3. `Create Database`를 누릅니다.
4. Database name을 입력합니다.
   예: `aidev-log-dashboard`
5. Type 또는 Region을 선택합니다.
   무료 실습이면 기본값 또는 가까운 region을 사용합니다.
6. `Create`를 누릅니다.

### 2-2. REDIS_URL 확인

04 backend 코드는 Python `redis` 패키지의 `redis.asyncio.from_url()`을 사용합니다. 따라서 Render에는 Upstash의 REST URL이 아니라 Redis protocol URL을 넣어야 합니다.

Upstash database 상세 화면에서 `Connect`, `Details`, `Redis`, `TLS`와 비슷한 영역을 찾습니다. 아래처럼 `rediss://`로 시작하는 값을 사용합니다.

```text
REDIS_URL=rediss://default:your-password@your-host.upstash.io:6379
```

주의:

```text
https://...upstash.io 형태의 REST URL은 이 예제의 REDIS_URL 자리에 넣지 않습니다.
REST URL과 REST TOKEN은 upstash-redis SDK를 사용할 때 쓰는 방식입니다.
현재 04 예제는 redis-py 방식이므로 rediss:// URL을 사용합니다.
```

두 방식의 차이는 다음과 같습니다.

| 구분 | Redis protocol 방식 | REST API 방식 |
| --- | --- | --- |
| 환경 변수 | `REDIS_URL` | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` |
| 값 형태 | `rediss://default:password@host:port` | `https://...upstash.io` + token |
| Python 라이브러리 | `redis`, `redis.asyncio` | `upstash-redis` 또는 HTTP client |
| 사용 방식 | Redis client 연결 후 명령 실행 | HTTP 요청으로 Redis 명령 실행 |
| 적합한 예 | pub/sub, queue, 실시간 이벤트 구독 | cache, session, rate-limit, 단순 key/value 조회 |
| 04 SSE 예제 | 사용 | 사용하지 않음 |

이번 04의 01 실습 예제는 FastAPI backend가 Redis pub/sub 채널을 구독해 SSE로 브라우저에 전달합니다. 그래서 Render 환경 변수에는 먼저 `REDIS_URL=rediss://...`를 넣습니다.

REST API 방식은 `02_supabase-ai-backend`의 `03_supabase-db-and-auth/06_upstash-redis-cache-and-session`에서 TTL cache로 먼저 다뤘습니다. 최종 미니 프로젝트에서 캐시, 세션, rate-limit 기능을 추가한다면 그 흐름을 확장해 REST API 방식의 두 값도 함께 넣을 수 있습니다.

```text
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
```

정리하면 다음과 같습니다.

```text
실시간 로그 스트리밍, pub/sub -> REDIS_URL
캐시, 세션, rate-limit -> UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN
```

### 2-3. Render backend에 Upstash Redis 환경 변수 넣기

Render backend의 Environment Variables에 다음 값을 추가합니다.

```text
REDIS_URL=rediss://default:your-password@your-host.upstash.io:6379
```

Upstash Redis 연결이 실패해도 예제는 memory fallback으로 동작할 수 있습니다. 다만 최종 보고서에는 “Upstash Redis 연결 성공” 또는 “memory fallback으로 시연” 중 어떤 방식인지 명확히 적습니다.

## 3. FastAPI backend를 Render에 배포

Render는 GitHub 저장소를 연결해서 FastAPI backend를 웹 서비스로 실행할 수 있는 배포 서비스입니다.

### 3-1. GitHub 저장소 준비

1. `C:\aidev` 프로젝트를 GitHub에 push합니다.
2. GitHub 저장소에 `.env`가 올라가지 않았는지 확인합니다.
3. GitHub 저장소에서 아래 파일들이 있는지 확인합니다.

```text
04_supabase-ai-mini-project/03_project_structure/backend/requirements.txt
04_supabase-ai-mini-project/03_project_structure/backend/app/main.py
```

수업에서 완성 예제를 바로 배포한다면 아래 경로를 사용할 수도 있습니다.

```text
04_supabase-ai-mini-project/01_realtime-log-dashboard-practice/backend
```

최종 프로젝트 제출 기준은 `03_project_structure/backend`를 권장합니다.

### 3-2. Render Web Service 생성

1. [Render Dashboard](https://dashboard.render.com/)에 로그인합니다.
2. `New`를 누릅니다.
3. `Web Service`를 선택합니다.
4. GitHub 계정을 연결합니다.
5. `aidev` 저장소를 선택합니다.
6. 서비스 이름을 입력합니다.
   예: `aidev-log-dashboard-api`
7. Runtime 또는 Language는 `Python`을 선택합니다.
8. Root Directory를 입력합니다.

최종 프로젝트 starter 기준:

```text
04_supabase-ai-mini-project/03_project_structure/backend
```

완성 예제 기준:

```text
04_supabase-ai-mini-project/01_realtime-log-dashboard-practice/backend
```

### 3-3. Render build/start 명령 입력

Build Command:

```text
pip install -r requirements.txt
```

Start Command:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

참고:

Render 공식 FastAPI 문서에서도 `pip install -r requirements.txt`와 `uvicorn ... --host 0.0.0.0 --port $PORT` 형태를 사용합니다. 로컬 PowerShell에서는 실행 정책 문제를 줄이기 위해 `python -m pip`, `python -m uvicorn`을 권장하지만, Render 설정에는 위처럼 입력해도 됩니다.

### 3-4. Render 환경 변수 입력

Render Web Service 생성 화면 또는 생성 후 `Environment` 메뉴에서 아래 값을 입력합니다.

| Key | 예시 값 | 설명 |
| --- | --- | --- |
| `SUPABASE_URL` | `https://your-project-id.supabase.co` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | `your-service-role-or-secret-key` | backend 서버 전용 key |
| `REDIS_URL` | `rediss://default:...@...:6379` | Upstash Redis protocol URL |
| `UPSTASH_REDIS_REST_URL` | `https://...upstash.io` | 선택. cache/session/rate-limit 구현 시 사용 |
| `UPSTASH_REDIS_REST_TOKEN` | `your-upstash-rest-token` | 선택. cache/session/rate-limit 구현 시 사용 |
| `CORS_ALLOW_ORIGINS` | `https://your-app.streamlit.app,http://localhost:8501,http://127.0.0.1:8501` | Streamlit frontend 주소 |

처음에는 Streamlit 배포 주소를 아직 모르기 때문에 아래처럼 임시로 넣어도 됩니다.

```text
CORS_ALLOW_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

Streamlit 배포 후에는 Streamlit URL을 추가하고 Render backend를 재배포합니다.

### 3-5. Render 배포 확인

배포가 끝나면 Render가 `https://...onrender.com` 형태의 URL을 제공합니다.

브라우저에서 아래 주소를 확인합니다.

```text
https://your-render-backend.onrender.com/health
```

정상 예시:

```json
{
  "status": "ok",
  "supabase_configured": true,
  "redis_configured": true,
  "message": "04 mini project starter backend is running"
}
```

확인할 주소:

```text
https://your-render-backend.onrender.com/docs
https://your-render-backend.onrender.com/health
https://your-render-backend.onrender.com/logs
```

### 3-6. Render에서 자주 나는 문제

| 증상 | 원인 | 해결 |
| --- | --- | --- |
| `ModuleNotFoundError` | `requirements.txt`에 패키지가 없음 | 필요한 패키지를 추가하고 다시 deploy |
| `/health`가 404 | Root Directory가 잘못됨 | `backend` 폴더가 root인지 확인 |
| 서버가 바로 종료됨 | Start Command가 잘못됨 | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` 확인 |
| Supabase 저장 실패 | 환경 변수 누락 또는 schema 미실행 | `SUPABASE_URL`, key, SQL Editor 실행 확인 |
| Streamlit에서 CORS 오류 | `CORS_ALLOW_ORIGINS`에 Streamlit URL 없음 | Render 환경 변수에 Streamlit URL 추가 후 redeploy |

## 4. Streamlit frontend를 Community Cloud에 배포

Streamlit Community Cloud는 GitHub 저장소의 Streamlit 앱을 웹에 배포하는 서비스입니다.

### 4-1. frontend 배포 전 확인

GitHub 저장소에 아래 파일이 있어야 합니다.

```text
04_supabase-ai-mini-project/03_project_structure/frontend_multipage/app.py
04_supabase-ai-mini-project/03_project_structure/frontend_multipage/requirements.txt
```

탭 방식으로 구현했다면 아래 파일을 사용합니다.

```text
04_supabase-ai-mini-project/03_project_structure/frontend_tabs/app.py
04_supabase-ai-mini-project/03_project_structure/frontend_tabs/requirements.txt
```

수업 완성 예제를 바로 배포한다면 아래 파일을 사용할 수 있습니다.

```text
04_supabase-ai-mini-project/01_realtime-log-dashboard-practice/frontend/app.py
```

### 4-2. Streamlit 앱 생성

1. [Streamlit Community Cloud](https://share.streamlit.io/)에 로그인합니다.
2. GitHub 계정을 연결합니다.
3. `Create app` 또는 `New app`을 누릅니다.
4. Repository를 선택합니다.
   예: `car1403/aidev`
5. Branch를 선택합니다.
   예: `main`
6. Main file path를 입력합니다.

최종 프로젝트 starter 기준입니다. 둘 중 하나를 선택합니다.

왼쪽 메뉴 방식:

```text
04_supabase-ai-mini-project/03_project_structure/frontend_multipage/app.py
```

탭 방식:

```text
04_supabase-ai-mini-project/03_project_structure/frontend_tabs/app.py
```

완성 예제 기준:

```text
04_supabase-ai-mini-project/01_realtime-log-dashboard-practice/frontend/app.py
```

7. Python version을 선택할 수 있으면 로컬과 같은 3.12 계열을 권장합니다.

### 4-3. Streamlit secrets 입력

Streamlit 배포 화면의 `Advanced settings` 또는 배포 후 App settings의 `Secrets`에 아래 값을 넣습니다.

```toml
API_BASE_URL = "https://your-render-backend.onrender.com"
```

Streamlit에는 아래 값을 넣지 않습니다.

```text
SUPABASE_SERVICE_ROLE_KEY
SUPABASE_SECRET_KEY
REDIS_URL
GEMINI_API_KEY
OPENAI_API_KEY
```

frontend는 backend API만 호출합니다. DB key와 Upstash Redis URL은 Render backend에만 있어야 합니다.

### 4-4. Streamlit 배포 확인

배포가 끝나면 아래와 같은 URL이 생성됩니다.

```text
https://your-app-name.streamlit.app
```

확인 순서:

1. Streamlit 앱에 접속합니다.
2. 화면에서 backend 연결 상태를 확인합니다.
3. 로그 생성 버튼 또는 입력 폼으로 로그를 생성합니다.
4. 최근 로그 테이블에 데이터가 보이는지 확인합니다.
5. 실시간 로그 영역에 새 로그가 표시되는지 확인합니다.

### 4-5. Streamlit URL을 Render CORS에 추가

Streamlit URL이 확정되면 Render backend로 돌아갑니다.

Render Environment Variables에서 `CORS_ALLOW_ORIGINS`를 수정합니다.

```text
CORS_ALLOW_ORIGINS=https://your-app-name.streamlit.app,http://localhost:8501,http://127.0.0.1:8501
```

수정 후 Render에서 `Manual Deploy` 또는 `Redeploy`를 실행합니다.

### 4-6. Streamlit에서 자주 나는 문제

| 증상 | 원인 | 해결 |
| --- | --- | --- |
| `API_BASE_URL`이 없음 | Streamlit secrets 미입력 | App settings에서 secrets 추가 |
| backend 호출 실패 | Render URL 오타 | `/health` URL을 브라우저에서 먼저 확인 |
| CORS 오류 | Render CORS 허용 목록 누락 | `CORS_ALLOW_ORIGINS`에 Streamlit URL 추가 |
| 패키지 설치 실패 | frontend `requirements.txt` 누락 또는 충돌 | requirements 확인 후 재배포 |
| 화면은 뜨지만 데이터 없음 | Supabase schema 미실행 또는 backend 환경 변수 누락 | Supabase Table Editor와 Render Environment 확인 |

## 5. 전체 연결 테스트

아래 순서대로 확인하면 어디에서 문제가 나는지 좁히기 쉽습니다.

### 5-1. Supabase 확인

Supabase Table Editor에서 테이블이 보이는지 확인합니다.

```text
realtime_service_logs
user_feedback
```

테이블이 없으면 `schema.sql`을 다시 실행합니다.

### 5-2. Render backend 확인

브라우저에서 확인합니다.

```text
https://your-render-backend.onrender.com/health
```

`supabase_configured`와 `redis_configured`가 `true`인지 봅니다.

`redis_configured`가 `false`여도 앱은 memory fallback으로 실행될 수 있습니다. 하지만 Redis 연결 배포를 시연하려면 `REDIS_URL`을 확인해야 합니다.

### 5-3. Swagger에서 로그 생성

Render backend의 Swagger를 엽니다.

```text
https://your-render-backend.onrender.com/docs
```

`POST /logs`에 아래 예시를 입력합니다.

```json
{
  "level": "info",
  "source": "render-test",
  "message": "Render 배포 테스트 로그입니다.",
  "request_path": "/deploy-test",
  "status_code": 200,
  "latency_ms": 123,
  "metadata": {
    "deploy": "render"
  }
}
```

`GET /logs`에서 방금 만든 로그가 보이면 backend와 DB 저장 흐름은 정상입니다.

### 5-4. Streamlit에서 확인

Streamlit 앱에서 로그를 생성합니다.

확인할 것:

- 새 로그가 화면에 표시되는가?
- 최근 로그 테이블에 표시되는가?
- Supabase Table Editor에도 데이터가 들어갔는가?
- Render logs에 오류가 없는가?

## 6. 제출 또는 시연 자료에 넣을 것

최종 보고서나 발표 자료에는 아래 내용을 넣습니다.

| 항목 | 제출 내용 |
| --- | --- |
| Streamlit 배포 URL | `https://your-app-name.streamlit.app` |
| Render backend URL | `https://your-render-backend.onrender.com` |
| Render health URL | `https://your-render-backend.onrender.com/health` |
| Supabase 테이블 확인 | Table Editor 캡처 |
| Upstash Redis 연결 확인 | `redis_configured: true` 또는 Upstash console 캡처 |
| 실시간 로그 화면 | Streamlit 대시보드 캡처 |
| 로그 저장 결과 | Supabase Table Editor 또는 `/logs` 응답 캡처 |

## 7. 보안 체크

배포 후 반드시 확인합니다.

- [ ] GitHub에 `.env`가 올라가지 않았는가?
- [ ] GitHub에 Supabase service role key 또는 secret key가 노출되지 않았는가?
- [ ] GitHub에 `REDIS_URL`이 노출되지 않았는가?
- [ ] Streamlit secrets에는 `API_BASE_URL`만 넣었는가?
- [ ] Render Environment Variables에만 backend 비밀값을 넣었는가?
- [ ] 발표 자료 캡처에 key 값이 보이지 않는가?

## 8. 초보자용 문제 해결 순서

문제가 생기면 아래 순서로 확인합니다.

```text
1. Render /health가 열리는가?
2. Render /docs가 열리는가?
3. Render /docs에서 POST /logs가 성공하는가?
4. Supabase Table Editor에 로그가 저장되는가?
5. Streamlit secrets의 API_BASE_URL이 Render URL과 같은가?
6. Render CORS_ALLOW_ORIGINS에 Streamlit URL이 들어 있는가?
7. Streamlit 화면에서 로그 생성과 조회가 되는가?
```

이 순서를 따르면 backend 문제인지, DB 문제인지, frontend 연결 문제인지 빠르게 구분할 수 있습니다.
