# 06 연결 가이드

## 1. 어디에서 실행하나요?

아래 명령은 **Windows PowerShell, 00_runtime-and-deployment 폴더**에서 실행합니다.
Docker Desktop을 먼저 켜고 Linux containers 모드인지 확인합니다.
PowerShell 7에서는 pwsh, Windows 기본 터미널에서는 powershell을 사용할 수 있습니다.

~~~powershell
docker version
docker compose version
.\launcher.cmd -Target 06 -Action init
notepad .\06_weather-mcp-stateful-deployment\.env
.\launcher.cmd -Target 06 -Action check
.\launcher.cmd -Target 06 -Action start
.\launcher.cmd -Target 06 -Action status
~~~

init은 예제 설정만 복사하고 기존 .env는 보존합니다.
OPENAI_API_KEY 또는 GEMINI_API_KEY를 설정하고 실제 계정에서 사용할 수 있는 모델명을 입력합니다.
키를 JSON·문서·GitHub 커밋에 넣지 않습니다. 기본 DB 암호는 로컬 학습용입니다.
01 계열의 Ollama는 선택 사항입니다. OpenAI/Gemini로 실습할 때 OLLAMA_ENABLED=false로 두세요.
launcher의 기본 시작 명령은 Ollama 프로필과 모델 다운로드를 포함하지 않습니다.

## 2. 정상 동작 확인

http://localhost:8501 에서 화면을 열고, http://localhost:8000/health/ready 가 성공하는지 확인합니다. status에서 backend가 healthy인지 확인한 뒤 실제 요청을 한 번 보내세요.

~~~powershell
.\launcher.cmd -Target 06 -Action logs
.\launcher.cmd -Target 06 -Action stop
~~~

다른 실습이 8000/8501을 사용한다면 그 실습의 stop부터 실행합니다.
stop은 DB 데이터를 보존합니다. start를 다시 실행하면 기존 데이터로 재시작합니다.

## 3. PostgreSQL 연결

이 구성은 PostgreSQL을 컨테이너 내부에만 노출합니다. Windows의 localhost:5432로 직접 접속하지 않습니다.
아래는 해당 실습 폴더로 이동한 뒤 컨테이너 안의 psql을 실행하는 명령입니다.

~~~powershell
Set-Location .\06_weather-mcp-stateful-deployment
docker compose -f compose.infrastructure.yml exec database psql -U agent_user -d agent_db
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
powershell -NoProfile -File .\setup-python.ps1 -Group weather -Python python
.\.venvs\weather\Scripts\python.exe -m pytest .\06_weather-mcp-stateful-deployment\backend -q
~~~

테스트는 가짜 클라이언트 기반이며 실제 LLM·DB 연결 성공을 대신하지 않습니다.
00 공용 인프라에는 앱 테스트가 없으며 DB init 도구가 필요할 때 compose 가상환경을 사용합니다.

## 5. EC2와 GitHub Actions 연결

CI를 처음 설정한다면 [02 ConnectGuide](../../02_github-actions-ci/doc/ConnectGuide.md)의
workflow 복사 → 커밋 → Actions 실행 → 첫 빨간 Step 확인 순서대로 진행합니다.
EC2는 [03 ConnectGuide](../../03_aws-ec2/doc/ConnectGuide.md),
CD는 [04 ConnectGuide](../../04_github-actions-aws-deploy/doc/ConnectGuide.md)를 따릅니다.
이 단계에서 로컬의 .env나 .venvs를 서버로 복사하지 않습니다.

기존 서버 배포 준비와 Secret 설정은 [deploy/README.md](../deploy/README.md)에 있습니다. 07용 SSM workflow를 05·06용으로 그대로 복사하면 안 됩니다.

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
