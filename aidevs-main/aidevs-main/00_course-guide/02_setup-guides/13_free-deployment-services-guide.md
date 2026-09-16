# 무료 배포 서비스 준비 가이드

이 문서는 03, 04, 06 과정의 선택/확장 배포와 07~08 과정의 운영 실습 전에 참고하는 배포 준비 문서입니다.

처음 배포를 할 때는 한 번에 모든 서비스를 올리려고 하지 말고, 아래 순서로 나누어 진행합니다.

```text
1. Supabase Cloud에 DB/Auth 준비
2. Upstash Redis 준비
3. FastAPI backend_service를 Render에 배포
4. Streamlit frontend를 Streamlit Community Cloud에 배포
5. frontend의 API_BASE_URL을 Render backend 주소로 연결
```

공통 기준:

| 구성 요소 | 배포 서비스 |
| --- | --- |
| FastAPI backend_service | Render |
| Streamlit frontend | Streamlit Community Cloud |
| Supabase DB/Auth | Supabase Cloud |
| Redis | Upstash Redis |

## 1. 배포 전에 알아야 할 것

로컬 실행과 배포 실행은 환경이 다릅니다.

| 구분 | 로컬 실행 | 배포 실행 |
| --- | --- | --- |
| 실행 위치 | 내 컴퓨터 | Render, Streamlit Cloud 같은 외부 서버 |
| 주소 | `http://127.0.0.1:8000` | `https://프로젝트명.onrender.com` |
| 환경 변수 | `.env` 파일 | 배포 서비스의 Environment Variables 또는 Secrets |
| 파일 저장 | 내 컴퓨터 폴더 | 서버 임시 저장소 또는 외부 DB |
| DB/Auth | Supabase Cloud | Supabase Cloud |

배포할 때 가장 많이 실수하는 부분은 `.env` 파일을 서버에 직접 올리려고 하는 것입니다. 배포 서비스에서는 `.env` 파일 대신 환경 변수 입력 화면에 값을 등록합니다.

## 2. FastAPI backend_service -> Render

공식 사이트:

- [Render](https://render.com/)
- [Render Web Services 문서](https://render.com/docs/web-services)

### 2.1 Render 로그인

1. [Render](https://render.com/)에 접속합니다.
2. `Get Started` 또는 `Sign In`을 선택합니다.
3. GitHub 계정으로 로그인합니다.
4. GitHub 저장소 접근 권한을 허용합니다.

### 2.2 Web Service 만들기

1. Render Dashboard에서 `New +`를 누릅니다.
2. `Web Service`를 선택합니다.
3. 배포할 GitHub repository를 선택합니다.
4. 배포할 branch를 선택합니다. 보통 `main`을 사용합니다.
5. `Root Directory`를 입력합니다.

예:

```text
03_supabase-ai-frontend/99_final-frontend-project/backend_service
```

또는 백엔드 프로젝트 위치에 따라 다음처럼 입력할 수 있습니다.

```text
02_supabase-ai-backend/99_final-backend-project/solution
```

### 2.3 Build Command와 Start Command

FastAPI 예시:

```text
Build Command:
pip install -r requirements.txt

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

중요:

```text
Render에서는 127.0.0.1이 아니라 0.0.0.0으로 실행합니다.
포트는 고정 숫자 8000이 아니라 $PORT를 사용합니다.
```

### 2.4 Environment Variables 등록

Render의 `Environment` 또는 `Environment Variables` 영역에 필요한 값을 등록합니다.

예:

```text
APP_ENV=production
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite
UPSTASH_REDIS_REST_URL=https://your-upstash-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-token
```

주의:

```text
.env 파일은 GitHub에 올리지 않습니다.
Render 환경 변수 화면에 직접 입력합니다.
SUPABASE_SERVICE_ROLE_KEY와 GEMINI_API_KEY는 프론트엔드에 넣지 않습니다.
```

### 2.5 배포 확인

배포가 끝나면 Render가 URL을 제공합니다.

예:

```text
https://aidev-backend.onrender.com
```

브라우저에서 확인합니다.

```text
https://aidev-backend.onrender.com/health
https://aidev-backend.onrender.com/docs
```

`/health`가 정상 응답하면 backend가 배포된 것입니다.

## 3. Streamlit frontend -> Streamlit Community Cloud

공식 사이트:

- [Streamlit Community Cloud](https://streamlit.io/cloud)
- [Streamlit Community Cloud 배포 문서](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)

### 3.1 Streamlit Cloud 로그인

1. [Streamlit Community Cloud](https://streamlit.io/cloud)에 접속합니다.
2. GitHub 계정으로 로그인합니다.
3. GitHub repository 접근 권한을 허용합니다.

### 3.2 앱 만들기

1. `New app`을 선택합니다.
2. GitHub repository를 선택합니다.
3. branch를 선택합니다.
4. `Main file path`를 입력합니다.

예:

```text
03_supabase-ai-frontend/99_final-frontend-project/solution_tabs/app.py
```

또는 멀티페이지 구조라면:

```text
03_supabase-ai-frontend/99_final-frontend-project/solution_multipage/app.py
```

### 3.3 Secrets 등록

Streamlit 화면에서는 백엔드 주소 정도만 필요합니다.

예:

```toml
API_BASE_URL = "https://aidev-backend.onrender.com"
```

주의:

```text
Streamlit frontend secrets에 SUPABASE_SERVICE_ROLE_KEY를 넣지 않습니다.
Streamlit frontend secrets에 GEMINI_API_KEY를 넣지 않습니다.
LLM과 Supabase는 backend_service가 처리합니다.
```

### 3.4 배포 확인

배포 후 Streamlit URL에서 화면을 확인합니다.

확인할 것:

```text
[ ] 화면이 열린다.
[ ] 로그인 또는 mock 로그인 흐름이 동작한다.
[ ] 챗봇 요청이 Render backend로 전달된다.
[ ] Render backend 로그에 요청이 찍힌다.
[ ] 오류가 나면 화면에 오류 메시지가 표시된다.
```

## 4. Supabase DB/Auth -> Supabase Cloud

공식 사이트:

- [Supabase Dashboard](https://supabase.com/dashboard)

### 4.1 프로젝트 준비

1. Supabase Dashboard에 로그인합니다.
2. 프로젝트를 선택하거나 새로 만듭니다.
3. `Project Settings -> API`에서 URL과 key를 확인합니다.
4. `SQL Editor`에서 필요한 `schema.sql`을 실행합니다.
5. Auth를 사용하는 경우 `Authentication` 설정을 확인합니다.

### 4.2 배포 서비스에 넣을 값

backend_service가 Supabase를 사용한다면 Render 환경 변수에 아래 값을 넣습니다.

```text
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
```

역할:

| 값 | 역할 |
| --- | --- |
| `SUPABASE_URL` | Supabase 프로젝트 주소 |
| `SUPABASE_ANON_KEY` | 일반 클라이언트 권한 key |
| `SUPABASE_SERVICE_ROLE_KEY` | 서버 전용 관리자 권한 key |

`SUPABASE_SERVICE_ROLE_KEY`는 절대 Streamlit 화면이나 GitHub 문서에 넣지 않습니다.

## 5. Redis -> Upstash Redis

공식 사이트:

- [Upstash Console](https://console.upstash.com/)
- [Upstash Redis REST API 문서](https://upstash.com/docs/redis/features/restapi)

### 5.1 Redis database 만들기

1. Upstash Console에 로그인합니다.
2. `Create Database`를 선택합니다.
3. 이름을 입력합니다.
4. 가까운 region을 선택합니다.
5. 생성 후 database 상세 화면으로 이동합니다.

### 5.2 REST 방식과 Redis URL 방식

Upstash에서는 보통 두 종류의 연결 정보를 볼 수 있습니다.

| 방식 | 예시 | 언제 쓰는가 |
| --- | --- | --- |
| REST URL/TOKEN | `https://...upstash.io`, `UPSTASH_REDIS_REST_TOKEN` | `httpx`로 Redis REST API를 호출하는 예제에서 사용 |
| Redis URL | `rediss://default:password@host:port` | Redis client 라이브러리가 직접 Redis protocol로 접속할 때 사용 |

02~04 과정의 초보자 예제는 주로 REST URL/TOKEN 방식을 사용합니다.

예:

```env
UPSTASH_REDIS_REST_URL=https://your-upstash-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-token
```

미니 프로젝트나 심화 예제에서 Redis client를 직접 쓰는 구조라면 `REDIS_URL`을 사용할 수 있습니다.

예:

```env
REDIS_URL=rediss://default:password@host:port
```

어떤 값을 써야 하는지는 예제의 `.env.example`을 기준으로 판단합니다.

## 6. 배포 순서 추천

처음에는 아래 순서를 추천합니다.

```text
1. Supabase schema.sql 실행
2. Upstash Redis 생성
3. backend_service 로컬 실행
4. backend_service Render 배포
5. Render /health 확인
6. Streamlit frontend 로컬 실행
7. Streamlit Cloud 배포
8. Streamlit secrets에 API_BASE_URL 등록
9. 최종 화면에서 API 호출 확인
```

## 7. 배포 전 체크리스트

```text
[ ] GitHub 저장소에 최신 코드가 push되어 있다.
[ ] backend_service에 requirements.txt가 있다.
[ ] Streamlit app.py 경로를 알고 있다.
[ ] .env 파일은 GitHub에 없다.
[ ] .env.example에는 예시 값만 있다.
[ ] Render Environment Variables에 backend secret을 등록했다.
[ ] Streamlit secrets에는 API_BASE_URL만 넣었다.
[ ] Supabase schema.sql을 실행했다.
[ ] Upstash Redis 연결 정보를 확인했다.
[ ] backend /health가 정상이다.
[ ] frontend가 backend 배포 주소를 호출한다.
```

## 8. 자주 나는 오류

| 오류 | 확인할 것 |
| --- | --- |
| Render 배포는 성공했지만 `/docs`가 안 열림 | Start Command의 `app.main:app`, `$PORT`, `0.0.0.0` 확인 |
| `ModuleNotFoundError` | `requirements.txt`에 패키지가 있는지 확인 |
| Supabase 연결 실패 | Render 환경 변수에 `SUPABASE_URL`, key가 들어갔는지 확인 |
| Gemini 호출 실패 | `GEMINI_API_KEY`, 모델명, 호출 제한 확인 |
| Streamlit에서 backend 연결 실패 | Streamlit secrets의 `API_BASE_URL`이 Render 주소인지 확인 |
| CORS 오류 | backend CORS 설정에 Streamlit 배포 URL을 허용했는지 확인 |
