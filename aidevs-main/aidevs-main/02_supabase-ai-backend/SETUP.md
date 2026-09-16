# SETUP

`02_supabase-ai-backend` 과정의 개발 환경 설정 문서입니다.

이 문서는 처음 실행할 때 그대로 따라 할 수 있도록 작성했습니다. 이 과정은 FastAPI, Supabase, Gemini API, Upstash Redis를 사용해 AI 백엔드의 기본 구조를 학습합니다. Python과 Git/GitHub 기초는 앞 과정인 `01_python-git-foundation`에서 먼저 다룹니다.

중요한 기준은 다음과 같습니다.

- 데이터베이스와 인증은 Supabase를 기준으로 진행합니다.
- LLM API 실습은 Gemini API를 기본으로 진행합니다.
- OpenAI API 관련 예제 파일은 선택/비교 강의용으로 그대로 유지합니다.
- Redis는 로컬 설치나 Docker 실행이 아니라 Upstash Redis를 사용합니다.
- Docker, Docker Compose, 로컬 PostgreSQL/Redis 운영, AWS 배포는 `C:\aidev\07_multi-agent-service-ops`에서 다룹니다.

## 공통 개발 환경 안내 문서

이 `SETUP.md`는 `02_supabase-ai-backend` 과정을 바로 실행하기 위한 순서를 중심으로 정리한 문서입니다. Python 설치, VS Code 설치, 확장 프로그램, PowerShell 사용법, `.venv`, `pip`, Markdown 문서 보기, Codex 로그인처럼 더 구체적인 준비 방법은 아래 공통 안내 문서를 참고합니다.

| 필요한 내용 | 참고 문서 |
| --- | --- |
| Python 설치와 버전 확인 | [`../00_course-guide/02_setup-guides/01_python-install-guide.md`](../00_course-guide/02_setup-guides/01_python-install-guide.md) |
| VS Code 설치 | [`../00_course-guide/02_setup-guides/02_vscode-install-guide.md`](../00_course-guide/02_setup-guides/02_vscode-install-guide.md) |
| VS Code 확장 프로그램 설치 | [`../00_course-guide/02_setup-guides/03_vscode-extensions-guide.md`](../00_course-guide/02_setup-guides/03_vscode-extensions-guide.md) |
| PowerShell 기본 사용법 | [`../00_course-guide/02_setup-guides/05_powershell-and-terminal-guide.md`](../00_course-guide/02_setup-guides/05_powershell-and-terminal-guide.md) |
| `.venv`, `pip`, `requirements.txt` 사용법 | [`../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md`](../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md) |
| Markdown 미리보기와 문서 작성법 | [`../00_course-guide/03_learning-support/getting-started.md`](../00_course-guide/03_learning-support/getting-started.md) |
| 첫 실행 전 점검표 | [`../00_course-guide/03_learning-support/getting-started.md`](../00_course-guide/03_learning-support/getting-started.md) |
| Gemini 계정, API Key, 결제/쿼터 안내 | [`../00_course-guide/02_setup-guides/08_gemini-openai-account-guide.md`](../00_course-guide/02_setup-guides/08_gemini-openai-account-guide.md) |
| OpenAI 계정과 결제 안내 | [`../00_course-guide/02_setup-guides/08_gemini-openai-account-guide.md`](../00_course-guide/02_setup-guides/08_gemini-openai-account-guide.md) |
| Supabase 계정과 프로젝트 | [`../00_course-guide/02_setup-guides/09_supabase-account-guide.md`](../00_course-guide/02_setup-guides/09_supabase-account-guide.md) |
| Upstash Redis 계정과 REST API 정보 | [`../00_course-guide/02_setup-guides/10_upstash-redis-guide.md`](../00_course-guide/02_setup-guides/10_upstash-redis-guide.md) |
| Codex와 ChatGPT 사용 준비 | [`../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md`](../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md) |

## Python/Git 선행 과정 확인

이 과정에 들어오기 전에 `01_python-git-foundation`에서 Python 기본 문법과 Git/GitHub 사용 흐름을 먼저 확인합니다. 여기서는 GitHub 계정 생성과 Git 명령을 길게 반복하지 않고, 백엔드 실습에 필요한 상태만 점검합니다.

처음 시작하기 전에 아래 항목을 확인합니다.

```text
1. 01_python-git-foundation의 Python 기본 예제를 실행해 보았는가?
2. 01_python-git-foundation의 pytest 예제를 실행해 보았는가?
3. GitHub 계정과 Git 설치를 확인했는가?
4. VS Code Source Control에서 변경 파일을 확인해 보았는가?
5. `.env`, API key, token 같은 민감정보를 GitHub에 올리지 않는 기준을 이해했는가?
```

Git 설치 여부는 PowerShell에서 확인합니다.

```powershell
git --version
```

정상 예시:

```text
git version 2.x.x
```

GitHub 계정 생성, 커밋, 브랜치, push, VS Code Source Control 사용법은 아래 선행 과정에서 단계적으로 실습합니다.

```text
..\01_python-git-foundation\03_git-github
```

VS Code 화면에서 Git을 사용하는 자세한 방법은 아래 문서를 참고합니다.

```text
..\01_python-git-foundation\03_git-github\00_references\vscode-source-control-guide.md
```

## 1. 작업 위치로 이동

PowerShell을 열고 과정 폴더로 이동합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
```

현재 위치를 확인합니다.

```powershell
Get-Location
```

결과가 아래와 비슷하면 됩니다.

```text
C:\aidev\02_supabase-ai-backend
```

## 2. Python 가상환경 만들기

가상환경은 이 과정에서 사용할 Python 패키지를 따로 보관하는 공간입니다. 이 과정은 `C:\aidev\02_supabase-ai-backend` 폴더 안의 `.venv` 하나를 사용합니다.

```powershell
C:\Users\jeanm\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv
```

이미 `.venv` 폴더가 있으면 다시 만들 필요는 없습니다.

## 3. 가상환경 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell 줄 앞에 `(.venv)`가 보이면 활성화된 상태입니다.

수업에서는 VS Code로 `C:\aidev\02_supabase-ai-backend` 폴더를 직접 열어 진행합니다. 이 폴더를 열면 `.vscode/settings.json` 설정에 따라 새 터미널에서 `.venv`가 자동 활성화됩니다. 새 터미널을 열 때마다 아래 확인 명령으로 현재 Python 경로가 이 과정의 `.venv`를 가리키는지 확인합니다.

확인 명령:

```powershell
echo $env:VIRTUAL_ENV
python -c "import sys; print(sys.executable)"
python --version
pip --version
```

정상이라면 위 두 경로가 아래처럼 `02_supabase-ai-backend\.venv`를 가리켜야 합니다.

```text
C:\aidev\02_supabase-ai-backend\.venv
C:\aidev\02_supabase-ai-backend\.venv\Scripts\python.exe
```

가상환경을 처음 만들었거나 패키지를 설치하기 전에는 `pip`를 최신 버전으로 올립니다. `python -m pip` 형태로 실행하면 현재 활성화된 가상환경의 `pip`를 확실하게 사용합니다.

```powershell
python -m pip install --upgrade pip
pip --version
```

PowerShell 실행 정책 오류가 나오면 다음 명령을 한 번 실행한 뒤 다시 활성화합니다.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 4. 패키지 설치

FastAPI, Supabase client, HTTP 요청, 환경변수 로딩에 필요한 패키지를 설치합니다.

```powershell
pip install -r requirements.txt
```

설치 확인:

```powershell
python -c "import fastapi, supabase, httpx; print('packages ok')"
```

## 5. Supabase 프로젝트 준비

Supabase는 이 과정에서 데이터베이스, 인증, API 기능을 제공하는 관리형 백엔드 서비스입니다.

### 5.1 Supabase 접속

브라우저에서 Supabase에 접속합니다.

```text
https://supabase.com
```

진행 순서:

```text
1. Supabase 사이트 접속
2. Sign in 또는 Start your project 클릭
3. GitHub 계정 또는 이메일로 로그인
4. Dashboard로 이동
```

### 5.2 프로젝트 생성

Dashboard에서 새 프로젝트를 만듭니다.

추천 이름:

```text
supabase-ai-backend-practice
```

Database Password는 Supabase의 PostgreSQL 데이터베이스 관리자 비밀번호입니다. 화면 공유나 문서에 적지 말고 개인적으로 보관합니다.

Region은 가능하면 가까운 지역을 선택합니다. 실제 선택 가능한 리전 이름은 Supabase 화면 기준으로 확인합니다.

프로젝트 생성 후 준비가 완료될 때까지 몇 분 정도 걸릴 수 있습니다.

### 5.3 Project URL과 API Key 확인

Supabase Dashboard에서 아래 메뉴로 이동합니다.

```text
Project Settings
-> API
```

여기에서 아래 값을 확인합니다.

| 항목 | `.env` 변수명 | 설명 |
| --- | --- | --- |
| Project URL | `SUPABASE_URL` | FastAPI 코드가 Supabase 프로젝트에 접속할 때 사용하는 주소입니다. |
| anon public key | `SUPABASE_ANON_KEY` | 브라우저나 일반 클라이언트에서 사용할 수 있는 공개용 key입니다. |
| service_role key | `SUPABASE_SERVICE_ROLE_KEY` | 서버에서만 사용하는 강한 권한의 key입니다. 절대 공개하면 안 됩니다. |

초보자는 `service_role key`를 특히 조심해야 합니다. 이 값은 GitHub, README, 과제 문서, 화면 캡처에 올리면 안 됩니다.

## 6. Upstash Redis 준비

Upstash Redis는 관리형 Redis 서비스입니다. 이 과정에서는 Docker로 Redis를 직접 실행하지 않고, Upstash Redis의 REST API를 사용합니다.

### 6.1 Upstash 접속

브라우저에서 Upstash에 접속합니다.

```text
https://upstash.com
```

진행 순서:

```text
1. Upstash 사이트 접속
2. Sign in 또는 Get Started 클릭
3. GitHub 또는 이메일로 로그인
4. Console 또는 Dashboard로 이동
```

### 6.2 Redis database 생성

Dashboard에서 Redis database를 생성합니다.

추천 이름:

```text
backend-practice-cache
```

이 과정에서는 캐시와 TTL만 최소 예제로 사용합니다. 요청 횟수 제한, 세션 저장, 고급 운영 설정은 뒤 과정에서 다룹니다.

### 6.3 REST API 정보 확인

Redis database 상세 화면에서 REST API 정보를 확인합니다.

| 항목 | `.env` 변수명 | 설명 |
| --- | --- | --- |
| REST URL | `UPSTASH_REDIS_REST_URL` | Python/FastAPI 코드가 Upstash Redis에 요청을 보낼 주소입니다. |
| REST Token | `UPSTASH_REDIS_REST_TOKEN` | Upstash Redis REST API 호출에 사용하는 token입니다. |

REST Token은 비밀번호처럼 다룹니다. GitHub, README, 과제 문서, 화면 캡처에 올리면 안 됩니다.

## 7. 환경변수 파일 만들기

`.env.example`을 복사해 `.env` 파일을 만듭니다.

```powershell
Copy-Item .env.example .env
```

이 실습에서는 아래 위치의 `.env` 파일을 사용합니다.

```text
C:\aidev\02_supabase-ai-backend\.env
```

즉, `C:\aidev\.env`나 다른 과정 폴더의 `.env`를 사용하는 구조가 아닙니다. 과정마다 필요한 환경변수가 다르기 때문에, `02_supabase-ai-backend`는 자기 폴더 안의 `.env`를 기준으로 실행합니다.

`.env` 파일을 열고 Supabase와 Upstash 값을 입력합니다.

```env
APP_NAME=02_supabase-ai-backend
APP_ENV=local

SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

UPSTASH_REDIS_REST_URL=https://your-upstash-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-upstash-redis-rest-token

GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite

OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
```

`GEMINI_API_KEY`는 02~04 과정에서 실제 LLM API 호출을 진행할 때 기본으로 사용합니다. Gemini의 무료 범위와 호출 제한은 진행 시점의 공식 화면에서 반드시 다시 확인합니다.

`OPENAI_API_KEY`는 필수가 아닙니다. 기존 OpenAI 예제 파일을 활용해 모델 공급자 차이를 비교하거나 추가 강의를 진행할 때만 설정합니다.

Python 기초, FastAPI 기본, Supabase CRUD, Upstash Redis 기본 실습만 할 때는 LLM API key가 당장 필요하지 않을 수 있습니다.

## 8. 환경변수 보안 기준

반드시 지켜야 할 기준입니다.

```text
.env 파일은 GitHub에 올리지 않습니다.
.env 파일은 과제로 제출하지 않습니다.
SUPABASE_SERVICE_ROLE_KEY는 서버에서만 사용합니다.
UPSTASH_REDIS_REST_TOKEN은 서버에서만 사용합니다.
화면 공유 중 key와 token 값이 보이지 않게 주의합니다.
```

`.env.example`에는 실제 key를 적지 않고 예시 값만 남깁니다.

## 9. 환경변수 확인

PowerShell에서 `.env` 파일이 있는지 확인합니다.

```powershell
dir .env
```

파일이 보이면 준비된 상태입니다.

단, `.env` 내용을 터미널에 그대로 출력하지 않는 것이 좋습니다. key와 token이 화면에 노출될 수 있기 때문입니다.

Supabase 환경변수 확인:

```powershell
dir .env
```

`.env` 파일을 VS Code에서 열어 `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`가 실제 값으로 입력되어 있는지 확인합니다. key 전체 값은 터미널이나 문서에 출력하지 않습니다.

Upstash Redis 환경변수는 아래 예제를 실행하면서 함께 확인합니다.

```powershell
python .\03_supabase-db-and-auth\06_upstash-redis-cache-and-session\01_redis_set_get_ttl.py
```

## 10. Supabase에서 테이블 만들기 기본 흐름

실습에서 데이터를 저장하려면 Supabase에 테이블이 필요합니다.

Dashboard에서 테이블을 만드는 기본 흐름은 다음과 같습니다.

```text
1. Supabase Dashboard 접속
2. 프로젝트 선택
3. 왼쪽 메뉴에서 Table Editor 선택
4. Create a new table 클릭
5. 테이블 이름 입력
6. 컬럼 이름과 타입 입력
7. Save 클릭
```

기본 실습 SQL은 아래 파일에서 확인합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

단원별 실습에서는 필요한 SQL이나 테이블 구조를 각 README에서 다시 안내합니다.

## 11. Supabase Auth와 RLS 기본 개념

Supabase Auth는 회원가입, 로그인, 사용자 식별을 담당합니다.

RLS는 Row Level Security의 줄임말입니다. 테이블의 각 행에 대해 누가 읽고 쓸 수 있는지 제어하는 보안 기능입니다.

초보자는 아래처럼 이해하면 됩니다.

```text
Auth
-> 이 사용자가 누구인지 확인

RLS
-> 이 사용자가 이 데이터에 접근해도 되는지 확인
```

처음에는 단순 CRUD를 먼저 실습하고, 이후 `03_supabase-db-and-auth/04_supabase-auth-and-rls`에서 Auth와 RLS를 자세히 다룹니다.

## 12. Upstash Redis 기본 개념

Redis는 빠른 임시 저장소입니다. Supabase처럼 오래 보관해야 하는 데이터의 중심 저장소로 쓰기보다, 빠르게 쓰고 일정 시간이 지나면 사라져도 되는 데이터에 사용합니다. 이 과정에서는 시간상 TTL 기반 캐시만 최소 예제로 확인합니다.

이 과정에서는 아래 기준으로 설명합니다.

```text
Supabase
-> 오래 보관할 데이터
-> 사용자 정보, 대화 이력, 서비스 로그, 피드백

Upstash Redis
-> 짧게 보관할 임시 데이터
-> 캐시, TTL
-> 중복 요청 방지, 요청 횟수 제한, 임시 세션 상태는 뒤 과정에서 확장
```

Upstash Redis TTL 예제 실행:

```powershell
python .\03_supabase-db-and-auth\06_upstash-redis-cache-and-session\01_redis_set_get_ttl.py
```

FastAPI Redis 캐시 예제 실행:

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\06_upstash-redis-cache-and-session
..\..\.venv\Scripts\Activate.ps1
uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_fastapi_redis_cache:app --reload --host 127.0.0.1 --port 8004
```

## 13. FastAPI 실행 기본형

FastAPI 예제는 보통 예제 파일이 있는 폴더에서 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-01_fastapi-health-check
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

브라우저에서 확인:

```text
http://127.0.0.1:8000/docs
```

서버를 멈출 때는 PowerShell에서 `Ctrl + C`를 누릅니다.

## 14. 자주 만나는 오류

### python 명령을 찾을 수 없는 경우

```powershell
py --version
python --version
```

Python이 설치되어 있지만 `python` 명령이 안 될 수 있습니다. 이 경우 설치 경로를 직접 사용하거나 Python 설치 옵션에서 PATH 추가 여부를 확인합니다.

### 패키지 import 오류

가상환경이 활성화되어 있는지 확인한 뒤 다시 설치합니다.

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Supabase 연결 오류

확인할 것:

```text
1. SUPABASE_URL이 https:// 로 시작하는가?
2. SUPABASE_URL 끝에 불필요한 공백이 없는가?
3. SUPABASE_ANON_KEY 또는 SUPABASE_SERVICE_ROLE_KEY를 잘못 복사하지 않았는가?
4. 서버 전용 코드에서 service role key가 필요한데 anon key를 넣은 것은 아닌가?
5. `.env` 파일이 현재 실행 위치에서 읽히는가?
6. python-dotenv 또는 설정 로딩 코드가 있는가?
```

### Upstash Redis 연결 오류

확인할 것:

```text
1. UPSTASH_REDIS_REST_URL이 https:// 로 시작하는가?
2. UPSTASH_REDIS_REST_TOKEN을 잘못 복사하지 않았는가?
3. URL 또는 token 앞뒤에 공백이 들어가지 않았는가?
4. Upstash Redis database가 활성 상태인가?
5. `.env` 파일이 현재 실행 위치에서 읽히는가?
```

### FastAPI 포트 충돌

기본 포트 `8000`을 이미 다른 서버가 사용 중이면 포트를 바꿔 실행합니다.

```powershell
uvicorn solution:app --reload --port 8001
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload --port 8001
```

## 15. Docker 학습 범위 안내

`02_supabase-ai-backend`에서는 Docker로 PostgreSQL이나 Redis를 직접 실행하지 않습니다.

이 과정의 DB/인증/대화 이력/로그 저장은 Supabase를 기준으로 진행합니다. Redis가 필요한 캐시, TTL, 요청 제한은 Upstash Redis를 사용합니다.

Docker, Docker Compose, 로컬 PostgreSQL 운영, 로컬 Redis 운영, AWS 배포는 아래 과정에서 본격적으로 다룹니다.

```text
C:\aidev\07_multi-agent-service-ops
```
