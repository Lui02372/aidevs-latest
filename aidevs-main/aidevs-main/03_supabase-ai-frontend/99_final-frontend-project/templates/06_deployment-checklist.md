# 06. Deployment Checklist

이 문서는 `99_final-frontend-project`를 무료 배포 서비스로 외부에서 접속할 수 있게 만드는 선택 실습 안내입니다.

초보자 기준 추천 순서는 다음과 같습니다.

```text
1. 로컬에서 backend_mock + Streamlit solution_tabs 또는 solution_multipage 실행 확인
2. backend_service를 Supabase/Gemini와 연결해 로컬 실행 확인
3. FastAPI backend_service를 Render에 배포
4. 선택한 Streamlit solution을 Streamlit Community Cloud에 배포
5. 선택: Upstash Redis를 연결해 캐시 확장
```

실제 배포는 계정 생성, 카드 등록, 무료 사용량 정책 확인이 필요할 수 있으므로 수업 시간과 훈련생 수준에 따라 선택 적용합니다.

## 0. 배포 전 공통 점검

- [ ] GitHub에 프로젝트 코드가 올라가 있다.
- [ ] `.env`, `.venv`, `__pycache__`, `.pytest_cache`는 GitHub에 올라가지 않는다.
- [ ] 프론트엔드 코드에 `SUPABASE_SERVICE_ROLE_KEY`, `GEMINI_API_KEY`, `UPSTASH_REDIS_REST_TOKEN`을 적지 않았다.
- [ ] 로컬에서 `backend_service`의 `/health`가 정상 응답한다.
- [ ] 로컬에서 Streamlit solution이 `backend_service`를 호출할 수 있다.
- [ ] Supabase SQL Editor에서 `backend_service/schema.sql`을 실행했다.
- [ ] Supabase Auth 회원가입/로그인 설정을 확인했다.
- [ ] Gemini API key를 발급했다.

## 1. FastAPI backend_service -> Render

Render 접속:

- [Render](https://render.com)
- [Render Docs](https://render.com/docs)

### 1-1. Render 계정 준비

1. 브라우저에서 `https://render.com`에 접속합니다.
2. `Get Started` 또는 `Sign Up`을 누릅니다.
3. GitHub 계정으로 로그인합니다.
4. Render가 GitHub repository에 접근할 수 있도록 권한을 허용합니다.

### 1-2. Web Service 생성

1. Render Dashboard에서 `New +`를 누릅니다.
2. `Web Service`를 선택합니다.
3. GitHub repository 목록에서 `aidev` repository를 선택합니다.
4. 서비스 이름을 입력합니다.

예시:

```text
aidev-final-frontend-backend
```

### 1-3. Root Directory 설정

Render가 실행할 backend 폴더를 지정합니다.

```text
03_supabase-ai-frontend/99_final-frontend-project/backend_service
```

### 1-4. Build Command 설정

```text
pip install -r requirements.txt
```

### 1-5. Start Command 설정

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Render는 실행 포트를 `$PORT` 환경변수로 전달합니다. 로컬에서 쓰던 `--port 8000`을 그대로 쓰면 배포 환경에서 접속이 안 될 수 있습니다.

### 1-6. Environment Variables 등록

Render 서비스 설정 화면의 `Environment` 메뉴에서 아래 값을 등록합니다.

| Key | 설명 |
| --- | --- |
| `SUPABASE_URL` | Supabase Project URL |
| `SUPABASE_ANON_KEY` | Supabase anon public key |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key, backend에만 저장 |
| `GEMINI_API_KEY` | Gemini API key |
| `GEMINI_MODEL` | 예: `gemini-2.5-flash-lite` |
| `CORS_ALLOW_ORIGINS` | Streamlit 배포 주소, 로컬 주소 |
| `UPSTASH_REDIS_REST_URL` | 선택: Upstash Redis REST URL |
| `UPSTASH_REDIS_REST_TOKEN` | 선택: Upstash Redis REST TOKEN |

로컬 개발 중에는 다음 값을 사용할 수 있습니다.

```text
CORS_ALLOW_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

Streamlit을 배포한 뒤에는 Streamlit 배포 주소를 추가합니다.

```text
CORS_ALLOW_ORIGINS=https://your-streamlit-app.streamlit.app,http://localhost:8501,http://127.0.0.1:8501
```

### 1-7. 배포 확인

Render 배포가 끝나면 서비스 URL이 생깁니다.

예시:

```text
https://aidev-final-frontend-backend.onrender.com
```

브라우저에서 아래 주소를 확인합니다.

```text
https://aidev-final-frontend-backend.onrender.com/health
```

정상 응답 예시:

```json
{
  "status": "ok",
  "mode": "supabase-gemini-upstash-optional",
  "message": "99 final frontend project service backend is running"
}
```

Swagger UI도 확인합니다.

```text
https://aidev-final-frontend-backend.onrender.com/docs
```

## 2. Redis -> Upstash

Upstash 접속:

- [Upstash](https://upstash.com)
- [Upstash Redis Docs](https://upstash.com/docs/redis)

Upstash Redis는 필수가 아닙니다. 이 프로젝트에서는 같은 사용자가 같은 질문을 반복했을 때 Gemini를 다시 호출하지 않고 캐시된 답변을 사용할 수 있는 선택 확장입니다.

### 2-1. Upstash 계정 준비

1. 브라우저에서 `https://upstash.com`에 접속합니다.
2. GitHub 또는 Google 계정으로 로그인합니다.
3. Dashboard로 이동합니다.

### 2-2. Redis Database 생성

1. `Create Database`를 누릅니다.
2. 이름을 입력합니다.

예시:

```text
aidev-final-chat-cache
```

3. Region은 Render와 가까운 지역을 선택합니다.
4. 무료 요금제 한도와 사용량 제한을 확인합니다.
5. 생성 후 database 상세 화면으로 이동합니다.

### 2-3. REST URL/TOKEN 확인

Upstash Redis 상세 화면에서 `REST API` 영역을 찾습니다.

Render 환경변수에 아래 값을 등록합니다.

| Render Key | Upstash에서 복사할 값 |
| --- | --- |
| `UPSTASH_REDIS_REST_URL` | REST URL |
| `UPSTASH_REDIS_REST_TOKEN` | REST TOKEN |

이 값은 프론트엔드에 넣지 않습니다. 반드시 `backend_service`의 Render 환경변수에만 등록합니다.

### 2-4. 캐시 동작 확인

1. Streamlit에서 로그인합니다.
2. 같은 질문을 두 번 보냅니다.
3. 첫 번째 응답은 Gemini를 호출합니다.
4. 두 번째 응답은 캐시가 적용되면 `provider=upstash-cache`, `actual_api_called=False`로 표시됩니다.

Upstash 연결을 생략하면 매번 Gemini를 호출합니다.

## 3. Streamlit solution_tabs/solution_multipage -> Streamlit Community Cloud

Streamlit 접속:

- [Streamlit Community Cloud](https://streamlit.io/cloud)
- [Streamlit Deploy Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [Streamlit Secrets Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

### 3-1. Streamlit 계정 준비

1. 브라우저에서 `https://streamlit.io/cloud`에 접속합니다.
2. `Sign in`을 누릅니다.
3. GitHub 계정으로 로그인합니다.
4. GitHub repository 접근 권한을 허용합니다.

### 3-2. New app 생성

1. Streamlit Community Cloud에서 `New app`을 누릅니다.
2. GitHub repository를 선택합니다.
3. Branch를 선택합니다.

예시:

```text
main
```

4. Main file path에 Streamlit 앱 파일 경로를 입력합니다.

탭 기반 solution을 배포한다면:

```text
03_supabase-ai-frontend/99_final-frontend-project/solution_tabs/app.py
```

멀티페이지 solution을 배포한다면:

```text
03_supabase-ai-frontend/99_final-frontend-project/solution_multipage/app.py
```

둘 중 하나만 선택합니다. `solution_multipage`를 선택해도 실행 시작 파일은 `pages/*.py`가 아니라 항상 `solution_multipage/app.py`입니다.

### 3-3. Python dependencies 확인

Streamlit Community Cloud는 repository의 `requirements.txt`를 기준으로 패키지를 설치합니다.

이 과정에서는 다음 파일을 기준으로 확인합니다.

```text
03_supabase-ai-frontend/requirements.txt
```

필요 패키지:

```text
streamlit
httpx
pandas
python-dotenv
```

### 3-4. Secrets 등록

Streamlit 앱 설정에서 `Secrets` 메뉴를 엽니다.

아래 값을 등록합니다.

```toml
API_BASE_URL = "https://aidev-final-frontend-backend.onrender.com"
```

`API_BASE_URL`에는 Render에 배포한 `backend_service` 주소를 입력합니다.

주의:

- `SUPABASE_SERVICE_ROLE_KEY`를 Streamlit Secrets에 넣지 않습니다.
- `GEMINI_API_KEY`를 Streamlit Secrets에 넣지 않습니다.
- `UPSTASH_REDIS_REST_TOKEN`을 Streamlit Secrets에 넣지 않습니다.
- 위 값들은 모두 Render의 backend 환경변수에만 둡니다.

### 3-5. 배포 확인

1. Streamlit 앱을 열어 `백엔드 상태 확인` 버튼을 누릅니다.
2. `backend 연결 성공`이 표시되는지 확인합니다.
3. 회원가입을 진행합니다.
4. Supabase Auth에서 이메일 인증이 켜져 있다면 인증 메일을 먼저 확인합니다.
5. 로그인합니다.
6. 챗봇 질문을 보냅니다.
7. 대화 기록과 서비스 로그 탭을 새로고침합니다.

## 4. 자주 막히는 지점

| 증상 | 확인할 것 |
| --- | --- |
| Streamlit에서 백엔드 연결 실패 | `API_BASE_URL`이 Render 주소인지 확인합니다. 주소 끝에 `/`가 없어도 됩니다. |
| Render `/health`는 되는데 `/chat` 실패 | `GEMINI_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, Supabase 테이블 생성 여부를 확인합니다. |
| 회원가입 후 로그인이 안 됨 | Supabase Auth의 `Confirm email` 설정과 인증 메일 확인 여부를 봅니다. |
| CORS 오류 | Render의 `CORS_ALLOW_ORIGINS`에 Streamlit 배포 주소가 포함되어 있는지 확인합니다. |
| Upstash 캐시가 안 됨 | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`이 Render backend 환경변수에 있는지 확인합니다. |
| GitHub에 key가 올라갈까 걱정됨 | `.env`가 `.gitignore`에 포함되어 있는지 확인합니다. |

## 5. 제출 전 체크리스트

- [ ] Streamlit 배포 주소를 제출했다.
- [ ] Render backend `/health` 주소를 제출했다.
- [ ] 회원가입/로그인 화면 캡처를 준비했다.
- [ ] 챗봇 질문/응답 화면 캡처를 준비했다.
- [ ] 대화 기록 화면 캡처를 준비했다.
- [ ] 서비스 로그 화면 캡처를 준비했다.
- [ ] 민감한 key가 GitHub에 올라가지 않았음을 확인했다.

## 운영 자동화

Docker, AWS, GitHub Actions 기반 운영 자동화는 `07_multi-agent-service-ops`에서 다룹니다.
