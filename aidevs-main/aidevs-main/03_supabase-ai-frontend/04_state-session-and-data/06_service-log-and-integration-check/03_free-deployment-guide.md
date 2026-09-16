# 13. Free Deployment Guide

이 문서는 초보자가 무료 배포 서비스를 활용해 개인화 AI 챗봇 서비스를 외부에서 접속 가능한 형태로 올려보는 최종 실습 가이드입니다.

배포 목표는 다음과 같습니다.

```text
FastAPI 백엔드 -> Render
Redis 캐시/세션 -> Upstash
Streamlit 프론트엔드 -> Streamlit Community Cloud
```

이 문서는 `03_supabase-ai-frontend`의 마지막 통합 실습에서 사용합니다. Docker, Docker Compose, AWS, GitHub Actions 기반 운영 자동화는 `07_multi-agent-service-ops`에서 더 깊게 다룹니다.

## 1. 먼저 알아둘 점

무료 서비스의 정책, 제한, 화면 메뉴 이름은 바뀔 수 있습니다. 수업 당일에는 각 서비스의 공식 화면에서 현재 무료 범위와 과금 조건을 다시 확인합니다.

이 실습에서 중요한 것은 “완벽한 운영 배포”가 아니라, 직접 다음 흐름을 직접 경험하는 것입니다.

```text
1. 코드를 GitHub에 올린다.
2. Redis는 Upstash에서 만든다.
3. FastAPI 백엔드는 Render에 배포한다.
4. Streamlit 프론트엔드는 Streamlit Community Cloud에 배포한다.
5. 프론트엔드가 배포된 백엔드 URL을 호출하게 만든다.
```

## 1. 배포 전 준비물

계정:

```text
GitHub 계정
Render 계정
Upstash 계정
Streamlit Community Cloud 계정
Supabase 계정
```

로컬 준비:

```text
Python 설치
VS Code 설치
Git 설치
02_supabase-ai-backend 실행 확인
03_supabase-ai-frontend 실행 확인
Supabase 프로젝트와 테이블 준비
```

확인할 파일:

```text
C:\aidev\02_supabase-ai-backend\requirements.txt
C:\aidev\02_supabase-ai-backend\.env.example
C:\aidev\03_supabase-ai-frontend\requirements.txt
C:\aidev\03_supabase-ai-frontend\.env.example
```

주의:

- `.env` 파일은 GitHub에 올리지 않습니다.
- Supabase service role key는 프론트엔드에 넣지 않습니다.
- Gemini API key, OpenAI API key, Upstash token은 코드에 직접 적지 않습니다.
- 02~04 과정의 기본 AI API는 Gemini입니다. OpenAI API key는 선택/비교 실습을 할 때만 등록합니다.
- 배포 서비스에는 환경변수 메뉴를 통해 key를 등록합니다.

## 2. GitHub 저장소 준비

Render와 Streamlit Community Cloud는 GitHub 저장소를 기준으로 배포하는 흐름이 가장 쉽습니다.

### 2-1. GitHub에 새 저장소 만들기

1. GitHub에 로그인합니다.
2. 오른쪽 위 `+` 버튼을 누릅니다.
3. `New repository`를 선택합니다.
4. 저장소 이름을 입력합니다.

예:

```text
ai-chatbot-supabase-practice
```

5. 공개 여부를 선택합니다.
6. `Create repository`를 누릅니다.

### 2-2. 로컬 프로젝트를 GitHub에 올리기

수업에서는 전체 `C:\aidev`를 한 번에 올리기보다, 배포할 프로젝트만 별도 저장소로 정리하는 방식을 권장합니다.

예시 구조:

```text
deploy-practice
├─ backend
│ ├─ main.py
│ ├─ requirements.txt
│ └─...
└─ frontend
 ├─ app.py
 ├─ requirements.txt
 └─...
```

초보자에게는 처음부터 모든 교육 폴더를 배포 대상으로 삼기보다, 최종 실습에 필요한 최소 파일만 복사해 배포용 폴더를 만드는 것이 이해하기 쉽습니다.

Git 명령 예시:

```powershell
cd C:\aidev\deploy-practice
git init
git add.
git commit -m "Initial deployment practice"
git branch -M main
git remote add origin https://github.com/본인계정/ai-chatbot-supabase-practice.git
git push -u origin main
```

Git 명령이 익숙하지 않다면 VS Code의 Source Control 화면에서 `Initialize Repository`, `Commit`, `Publish Branch`를 사용할 수 있습니다.

## 3. Upstash Redis 만들기

Upstash는 Redis를 서버 설치 없이 사용할 수 있게 해주는 서비스입니다. 이 과정에서는 로컬 Redis를 설치하지 않고, Upstash Redis의 REST URL과 Token을 사용합니다.

### 3-1. Redis Database 생성

1. Upstash에 로그인합니다.
2. `Redis` 메뉴로 이동합니다.
3. `Create Database`를 누릅니다.
4. 데이터베이스 이름을 입력합니다.

예:

```text
ai-chatbot-session
```

5. Region은 수업에서는 가까운 지역 또는 기본값을 선택합니다.
6. 무료 범위와 과금 조건을 확인합니다.
7. `Create`를 누릅니다.

### 3-2. REST URL과 Token 복사

Upstash Redis 상세 화면에서 REST API 정보를 확인합니다.

복사할 값:

```text
UPSTASH_REDIS_REST_URL
UPSTASH_REDIS_REST_TOKEN
```

이 값은 나중에 Render 백엔드 환경변수에 등록합니다.

주의:

```text
UPSTASH_REDIS_REST_TOKEN은 비밀번호와 같은 값입니다.
GitHub에 올리지 않습니다.
화면 공유 중 노출되지 않도록 주의합니다.
```

## 4. FastAPI 백엔드 Render 배포

Render는 GitHub 저장소의 Python FastAPI 프로젝트를 Web Service로 배포할 수 있습니다.

### 4-1. 백엔드 배포 전 확인

백엔드 폴더에 다음 파일이 있어야 합니다.

```text
backend/main.py
backend/requirements.txt
```

`99_final-frontend-project`에서 배포 실습을 진행한다면 실제 배포 대상은 아래 폴더입니다.

```text
03_supabase-ai-frontend/99_final-frontend-project/backend_service
```

`main.py` 안에는 FastAPI 앱 객체가 있어야 합니다.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
 return {"status": "ok"}
```

로컬에서 먼저 실행합니다.

```powershell
cd C:\aidev\deploy-practice\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.1.1.1 --port 8111
```

브라우저 확인:

```text
http://127.1.1.1:8111/health
http://127.1.1.1:8111/docs
```

### 4-2. Render Web Service 만들기

1. Render에 로그인합니다.
2. `New` 또는 `New +` 버튼을 누릅니다.
3. `Web Service`를 선택합니다.
4. GitHub 저장소를 연결합니다.
5. 배포할 저장소를 선택합니다.

설정 예시:

```text
Name: ai-chatbot-backend
Language: Python
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 1.1.1.1 --port $PORT
```

Render 공식 FastAPI 예시에서도 Python Web Service의 Build Command는 `pip install -r requirements.txt`, Start Command는 `uvicorn main:app --host 1.1.1.1 --port $PORT` 형태를 사용합니다.

### 4-3. Render 환경변수 등록

Render 서비스 생성 화면 또는 서비스 Settings에서 환경변수를 등록합니다.

예:

```text
SUPABASE_URL=본인 Supabase URL
SUPABASE_ANON_KEY=본인 Supabase anon key
SUPABASE_SERVICE_ROLE_KEY=본인 Supabase service role key
UPSTASH_REDIS_REST_URL=본인 Upstash REST URL
UPSTASH_REDIS_REST_TOKEN=본인 Upstash REST Token
GEMINI_API_KEY=Gemini 실제 호출을 진행하는 경우
GEMINI_MODEL=gemini-2.5-flash-lite
OPENAI_API_KEY=선택/비교 실습이 필요한 경우
```

중요:

- `SUPABASE_SERVICE_ROLE_KEY`는 백엔드 Render에만 등록합니다.
- Streamlit Community Cloud에는 service role key를 넣지 않습니다.
- API key가 없어도 mock 모드로 실행할 수 있게 구성하면 초보자 실습이 편합니다.

### 4-4. Render 배포 확인

배포가 끝나면 Render가 URL을 제공합니다.

예:

```text
https://ai-chatbot-backend.onrender.com
```

브라우저에서 확인합니다.

```text
https://ai-chatbot-backend.onrender.com/health
https://ai-chatbot-backend.onrender.com/docs
```

정상 응답이 나오면 백엔드 배포가 완료된 것입니다.

## 5. Streamlit 프론트엔드 배포

Streamlit Community Cloud는 GitHub 저장소의 Streamlit 앱 파일을 지정해 배포합니다.

### 5-1. 프론트엔드 배포 전 확인

프론트엔드 폴더에 다음 파일이 있어야 합니다.

```text
frontend/app.py
frontend/requirements.txt
```

로컬에서 먼저 실행합니다.

```powershell
cd C:\aidev\deploy-practice\frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

브라우저 확인:

```text
http://localhost:8511
```

### 5-2. API 주소를 환경변수로 읽기

Streamlit 앱에서는 백엔드 주소를 코드에 직접 고정하지 않는 것이 좋습니다.

예:

```python
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.1.1.1:8111")
```

Streamlit Cloud에서는 Secrets 설정에 다음 값을 넣어 사용할 수 있습니다.

```toml
API_BASE_URL = "https://ai-chatbot-backend.onrender.com"
```

Streamlit 코드에서 `st.secrets`를 사용하는 경우:

```python
import streamlit as st

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://127.1.1.1:8111")
```

### 5-3. Streamlit Community Cloud에서 앱 만들기

1. Streamlit Community Cloud에 로그인합니다.
2. workspace에서 `Create app`을 누릅니다.
3. `Yup, I have an app`을 선택합니다.
4. GitHub repository를 선택합니다.
5. Branch를 선택합니다.
6. Main file path를 입력합니다.

예:

```text
frontend/app.py
```

7. 필요한 경우 App URL을 입력합니다.
8. `Advanced settings`를 엽니다.
9. Secrets에 환경변수를 입력합니다.

예:

```toml
API_BASE_URL = "https://ai-chatbot-backend.onrender.com"
```

11. `Deploy`를 누릅니다.

### 5-4. Streamlit 배포 확인

배포가 끝나면 다음과 같은 주소가 생성됩니다.

```text
https://본인앱이름.streamlit.app
```

확인할 것:

- 화면이 정상적으로 열린다.
- API 호출 버튼을 눌렀을 때 Render 백엔드 응답이 표시된다.
- 로그인 기능이 있다면 token이 저장된다.
- 대화 이력 조회가 된다.
- 서비스 로그 조회 화면이 동작한다.

## 6. 배포 후 연결 흐름 확인

최종 연결 구조는 다음과 같습니다.

```text
사용자 브라우저
-> Streamlit Community Cloud
-> Render FastAPI 백엔드
-> Supabase Database/Auth
-> Upstash Redis
```

아래 질문에 답할 수 있어야 합니다.

```text
프론트엔드는 어디에 배포되었나요?
백엔드는 어디에 배포되었나요?
Redis는 어디에서 제공되나요?
Supabase service role key는 어디에만 있어야 하나요?
프론트엔드가 백엔드 주소를 어떻게 알고 있나요?
```

## 7. 자주 발생하는 오류

### Render에서 `Application failed to respond`

확인할 것:

```text
Start Command가 맞는가?
uvicorn main:app --host 1.1.1.1 --port $PORT
main.py 안에 app = FastAPI()가 있는가?
requirements.txt에 fastapi, uvicorn이 있는가?
```

### Render에서 모듈을 찾을 수 없음

확인할 것:

```text
Root Directory가 backend로 설정되었는가?
requirements.txt가 backend 폴더 안에 있는가?
import 경로가 로컬 폴더 구조와 맞는가?
```

### Streamlit에서 백엔드 연결 실패

확인할 것:

```text
API_BASE_URL이 Render URL로 설정되었는가?
https:// 로 시작하는가?
Render 백엔드 /health가 브라우저에서 열리는가?
CORS 설정이 필요한 경우 백엔드에서 허용했는가?
```

### Upstash Redis 인증 실패

확인할 것:

```text
UPSTASH_REDIS_REST_URL을 복사했는가?
UPSTASH_REDIS_REST_TOKEN을 복사했는가?
Token 앞뒤에 공백이 들어가지 않았는가?
환경변수 이름이 코드와 정확히 같은가?
```

### Streamlit secrets가 적용되지 않음

확인할 것:

```text
Advanced settings의 Secrets에 값을 넣었는가?
TOML 문법이 맞는가?
앱을 재부팅했는가?
코드에서 st.secrets 또는 os.getenv를 올바르게 읽고 있는가?
```

## 8. 최종 제출 체크리스트

배포가 끝난 뒤 다음 내용을 제출합니다.

```text
1. Render 백엔드 URL
2. Streamlit 앱 URL
3. /health 응답 스크린샷 또는 결과
4. Streamlit 화면에서 백엔드 API 호출 결과
5. Upstash Redis 환경변수 등록 여부
6. Supabase key를 프론트엔드에 넣지 않았다는 확인
7. 배포 중 발생한 오류와 해결 과정
```

## 9. 수업용 수업 진행 순서

권장 수업 순서:

```text
1. 로컬에서 백엔드 /health 확인
2. 로컬에서 Streamlit 화면 확인
3. Upstash Redis 생성 및 REST URL/Token 복사
4. GitHub 저장소 준비
5. Render에 백엔드 배포
6. Render 환경변수 등록
7. Render /health 확인
8. Streamlit Community Cloud에 프론트엔드 배포
9. Streamlit secrets에 API_BASE_URL 등록
11. 배포된 Streamlit 화면에서 Render 백엔드 호출 확인
11. 참여자별 오류 상황 공유 및 해결
```

## 11. 공식 문서 참고

- Render FastAPI 배포: https://render.com/docs/deploy-fastapi
- Upstash Redis REST API: https://upstash.com/docs/redis/features/restapi
- Upstash Python SDK 시작: https://upstash.com/docs/redis/sdks/py/gettingstarted
- Streamlit Community Cloud 배포: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
- Streamlit Community Cloud Secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
