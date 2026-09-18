# 01 연결 가이드

## 1. 어디에서 실행하나요?

아래 명령은 **Windows PowerShell, 00_runtime-and-deployment 폴더**에서 실행합니다.
Docker Desktop을 먼저 켜고 Linux containers 모드인지 확인합니다.
PowerShell 7에서는 pwsh, Windows 기본 터미널에서는 powershell을 사용할 수 있습니다.

~~~powershell
docker version
docker compose version
.\launcher.cmd -Target 01 -Action init
notepad .\01_simple-multi-llm-compose\.env
.\launcher.cmd -Target 01 -Action check
.\launcher.cmd -Target 01 -Action start
.\launcher.cmd -Target 01 -Action status
~~~

init은 예제 설정만 복사하고 기존 .env는 보존합니다.
OPENAI_API_KEY 또는 GEMINI_API_KEY를 설정하고 실제 계정에서 사용할 수 있는 모델명을 입력합니다.
키를 JSON·문서·GitHub 커밋에 넣지 않습니다. 기본 DB 암호는 로컬 학습용입니다.
01 계열의 Ollama는 선택 사항입니다. OpenAI/Gemini로 실습할 때 OLLAMA_ENABLED=false로 두세요.
launcher의 기본 시작 명령은 Ollama 프로필과 모델 다운로드를 포함하지 않습니다.

## 2. 정상 동작 확인

http://localhost:8501 에서 화면을 열고, http://localhost:8000/health/ready 가 성공하는지 확인합니다. status에서 backend가 healthy인지 확인한 뒤 실제 요청을 한 번 보내세요.

~~~powershell
.\launcher.cmd -Target 01 -Action logs
.\launcher.cmd -Target 01 -Action stop
~~~

다른 실습이 8000/8501을 사용한다면 그 실습의 stop부터 실행합니다.
stop은 DB 데이터를 보존합니다. start를 다시 실행하면 기존 데이터로 재시작합니다.

## 3. PostgreSQL 연결

이 구성은 PostgreSQL을 컨테이너 내부에만 노출합니다. Windows의 localhost:5432로 직접 접속하지 않습니다.
아래는 해당 실습 폴더로 이동한 뒤 컨테이너 안의 psql을 실행하는 명령입니다.

~~~powershell
Set-Location .\01_simple-multi-llm-compose
docker compose -f compose.full-stack.yml exec database psql -U agent_user -d agent_db
~~~

사용자와 DB명을 바꿨다면 .env와 동일하게 수정합니다. psql에서 다음을 확인합니다.

~~~sql
SELECT current_database(), current_user;
\dt
\q
~~~

앱 컨테이너의 주소는 database:5432, Redis 주소는 redis:6379입니다.
DB를 인터넷에 공개할 필요는 없습니다.

## 4. Python venv와 requirements

Docker 실행은 Dockerfile이 패키지를 설치합니다. 로컬 테스트용 가상환경은 별개입니다.
상위 폴더의 setup-python.ps1이 requirements-compose.txt / requirements-weather.txt를 설치합니다.
01 계열은 google-genai 2.x, 05~07은 1.x를 요구하므로 두 가상환경으로 분리했습니다.
Activate.ps1 실행 없이 가상환경의 python.exe를 직접 사용하면 실행 정책 문제를 피할 수 있습니다.

~~~powershell
powershell -NoProfile -File .\setup-python.ps1 -Group compose -Python python
.\.venvs\compose\Scripts\python.exe -m pytest .\01_simple-multi-llm-compose\backend -q
~~~

테스트는 가짜 클라이언트 기반이며 실제 LLM·DB 연결 성공을 대신하지 않습니다.
00 공용 인프라에는 앱 테스트가 없으며 DB init 도구가 필요할 때 compose 가상환경을 사용합니다.

## 5. EC2와 GitHub Actions 연결

CI를 처음 설정한다면 [02 ConnectGuide](../../02_github-actions-ci/doc/ConnectGuide.md)의
workflow 복사 → 커밋 → Actions 실행 → 첫 빨간 Step 확인 순서대로 진행합니다.
EC2는 [03 ConnectGuide](../../03_aws-ec2/doc/ConnectGuide.md),
CD는 [04 ConnectGuide](../../04_github-actions-aws-deploy/doc/ConnectGuide.md)를 따릅니다.
이 단계에서 로컬의 .env나 .venvs를 서버로 복사하지 않습니다.



## 6. 오류를 어디에서 고치나요?

| 증상 | 확인할 곳 |
| --- | --- |
| docker를 찾을 수 없음 | Docker Desktop 설치 및 터미널 재시작 |
| Docker daemon 연결 실패 | Docker Desktop 시작, Linux engine 상태 |
| port is already allocated | 다른 실습의 launcher stop, 점유 프로세스 확인 |
| database does not exist / password 실패 | 기존 DB 볼륨의 초기 사용자·DB와 .env 일치 여부 |
| health 실패 | launcher logs에서 최초 backend 오류 |
| LLM 401/403 | 현재 프로젝트 .env의 키와 Provider 권한 |
| PowerShell 명령을 EC2에서 실행함 | Windows는 PowerShell, SSH 접속 후에는 Linux bash |

DB 초기화 SQL은 빈 볼륨을 처음 만들 때 실행됩니다. .env의 DB 암호만 바꿔도 기존 DB 암호는
변경되지 않습니다. 학습 데이터가 필요하면 볼륨을 삭제하지 말고 DB 사용자 설정을 수정합니다.

## 01 폴더에서 launcher 실행하기

현재 폴더가 01_simple-multi-llm-compose라면 이 폴더에 추가한 launcher.cmd로 실행할 수 있습니다.
상위 공통 launcher에 전달하는 파일이며 실행 설정은 상위 launcher.json을 그대로 사용합니다.

~~~powershell
.\launcher.cmd -Target 01 -Action init
notepad .\.env
.\launcher.cmd -Target 01 -Action start
~~~

공통 launcher를 직접 지정하는 방법은 다음과 같습니다.

~~~powershell
..\launcher.cmd -Target 01 -Action init
~~~

init은 .env 준비만 합니다. PostgreSQL 실행과 초기 생성은 start 때 이루어집니다.

## 세 YAML과 PostgreSQL 초기화의 관계

| 파일 | Backend·Frontend | DB·Redis |
| --- | --- | --- |
| compose.yml | 현재 소스로 Build | 기존 공용 서비스에 연결 |
| compose.full-stack.yml | 현재 소스로 Build | 같은 Compose에서 함께 실행 |
| compose.release.yml | Registry의 완성 이미지 사용 | 기존 공용 서비스에 연결 |

세 파일은 선택하는 실행 구성입니다. 순서대로 모두 실행하거나 합칠 필요가 없습니다.
launcher의 01 start는 full-stack을 선택합니다.
파일 옵션 없이 docker compose up을 실행하면 compose.yml을 사용하므로 동작이 다릅니다.

full-stack에서는 01/.env의 POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB를
compose.full-stack.yml의 database.environment가 PostgreSQL 컨테이너에 전달합니다.
최초 빈 DB 데이터 디렉터리를 초기화할 때 PostgreSQL 이미지가 사용자·암호·DB를 준비하고,
database/init.sql이 simple_multi_llm 스키마와 notes·chat_messages 테이블을 생성합니다.
Backend의 DATABASE_URL도 동일한 세 값으로 조립됩니다.

사용자와 DB를 init.sql에 중복 등록할 필요가 없습니다.
기존 DB 볼륨이 있으면 초기화가 재실행되지 않습니다. .env 수정만으로 기존 DB 암호는 변경되지 않습니다.

기본/release 구성에서 00 공용 DB를 사용한다면 생성 설정은 00_local-services/.env에 있습니다.
01/.env의 DATABASE_URL·HOST_DATABASE_URL을 실제 공용 DB 계정과 맞춰야 합니다.
공용 DB에 이 앱의 스키마·테이블을 준비하려면 01 폴더에서 다음 명령을 사용합니다.

~~~powershell
..\.venvs\compose\Scripts\python.exe .\init_database.py
~~~

init_database.py는 이미 존재하는 사용자와 DB에 접속해 database/init.sql을 실행합니다.
사용자나 DB 자체를 생성하는 프로그램은 아닙니다.
별도 설치한 PostgreSQL을 쓰는 경우 그 서버의 관리자 계정으로 사용자·DB를 먼저 생성해야 합니다.
