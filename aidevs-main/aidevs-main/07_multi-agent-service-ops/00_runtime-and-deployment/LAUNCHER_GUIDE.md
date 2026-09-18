# JSON launcher 시작 안내

07 과정 최상위 폴더, 00 폴더, 각 실습 폴더의 launcher.cmd에서 동일한 JSON 메뉴를 엽니다.
빠른 실행은 [07 과정 안내](../LAUNCHER.md)를 참고하세요.

~~~powershell
.\launcher.cmd -Target 01 -Action switch
.\launcher.cmd -Target 05 -Action switch
.\launcher.cmd -Target 07 -Action switch
~~~

switch는 선택한 설정을 먼저 확인하고, 등록된 다른 앱 스택을 정지한 다음 선택한 서버를 실행합니다.
00 공용 서버와 DB 볼륨은 보존합니다. 각 앱은 8000/8501을 사용하므로 하나씩 전환합니다.
메뉴의 동작 질문에서 Enter를 누르면 앱은 switch, 문서 단계는 guide, 00은 start를 실행합니다.
open은 Frontend를 브라우저에 엽니다. start도 없는 .env를 자동 준비하고 Compose 문법 검사 후 실행합니다.

이 폴더의 **launcher.cmd를 더블클릭**하면 launcher.json의 목록을 읽습니다.
대상 ID를 입력한 뒤 guide, init, start, status, stop, check, logs 중 하나를 입력합니다.
Python 설치 없이 Windows PowerShell 5.1 또는 PowerShell 7에서 실행합니다.
Docker Desktop은 Linux containers 모드로 켜 두고, Docker Compose v2를 사용합니다.

## 처음 실행

PowerShell에서 이 파일이 있는 00_runtime-and-deployment 폴더로 이동합니다.
경로에 공백이 있으므로 Set-Location -LiteralPath '실제 폴더 전체 경로'를 사용합니다.

~~~powershell
.\launcher.cmd -Action list
.\launcher.cmd -Target 07 -Action guide
.\launcher.cmd -Target 07 -Action init
notepad .\07_integrated-bedrock-mcp\.env
.\launcher.cmd -Target 07 -Action check
.\launcher.cmd -Target 07 -Action start
.\launcher.cmd -Target 07 -Action status
~~~

.env에 OpenAI 또는 Gemini 키를 하나 설정한 뒤 http://localhost:8501 을 엽니다.
init은 기존 .env를 덮어쓰지 않습니다. 키는 launcher.json에 넣지 않습니다.
앱의 상태 점검 성공과 실제 LLM 호출 성공은 별개입니다.

~~~powershell
.\launcher.cmd -Target 07 -Action logs
.\launcher.cmd -Target 07 -Action stop
.\launcher.cmd -Target 07 -Action start -DryRun
~~~

stop은 컨테이너를 정지하고 DB 볼륨을 보존합니다.
06·07은 인프라 → 앱 순서로 시작하고 앱 → 인프라 순서로 정지합니다.
도중 실패하면 뒤 명령은 실행하지 않으며 이미 시작된 서비스는 남을 수 있습니다.
status와 logs로 확인한 뒤 필요하면 stop을 실행합니다.
DryRun은 Docker 실행과 파일 복사 없이 실행 계획만 출력합니다.
launcher.cmd의 Bypass는 해당 PowerShell 프로세스에만 적용하며 시스템 정책을 바꾸지 않습니다.

## 메뉴와 가이드

| ID | 내용 | 연결 안내 |
| --- | --- | --- |
| 00 | 공용 DB·Redis | [연결](00_local-services/doc/ConnectGuide.md) |
| 01 | Compose 원본 | [연결](01_simple-multi-llm-compose/doc/ConnectGuide.md) |
| 01-2 | Compose 2 | [연결](01_simple-multi-llm-compose2/doc/ConnectGuide.md) |
| 01-3 | Compose 3 | [연결](01_simple-multi-llm-compose3/doc/ConnectGuide.md) |
| 02 | GitHub Actions CI | [첫 실행부터](02_github-actions-ci/doc/ConnectGuide.md) |
| 03 | EC2 | [SSH 연결](03_aws-ec2/doc/ConnectGuide.md) |
| 04 | GitHub Actions CD | [배포 연결](04_github-actions-aws-deploy/doc/ConnectGuide.md) |
| 05 | Weather MCP | [연결](05_weather-mcp-deployment-project/doc/ConnectGuide.md) |
| 06 | DB 포함 Weather MCP | [연결](06_weather-mcp-stateful-deployment/doc/ConnectGuide.md) |
| 07 | 통합 + OIDC/SSM | [연결](07_integrated-bedrock-mcp/doc/ConnectGuide.md) |

02·03·04는 guide만 제공합니다. GitHub 작업이나 EC2 연결은 가이드에서 직접 진행합니다.
각 앱은 8000/8501 포트를 공유하므로 **한 번에 하나만 실행**합니다.
01·01-2·01-3은 기존 Compose 프로젝트 이름과 볼륨도 공유합니다.
변형을 바꾸면 기존 DB 데이터가 보일 수 있으며 별도 신규 DB로 취급하면 안 됩니다.
00은 공용 개발 서비스, 01 launcher는 독립 full-stack이므로 00을 먼저 켤 필요가 없습니다.

## JSON 구조

version: 1과 targets 목록을 사용합니다. 각 항목은 id, title, directory, guide,
compose(실행 순서대로 파일명 배열), envExample, url을 가집니다.
경로는 launcher.json이 있는 폴더 기준입니다. 빈 compose 배열은 문서 전용입니다.
지원 동작은 launcher.ps1에 고정되어 있고 JSON에 임의 셸 명령이나 비밀값을 넣지 않습니다.
루트의 project-player.json은 수업 진행용이므로 이 실행 설정과 별개입니다.

## 권장 학습 순서

01 또는 07 로컬 실행 → **02 CI 초록색 성공** → 03 EC2 수동 연결 →
04의 CI/CD 차이 확인 → 07 OIDC/SSM 수동 배포 → 필요할 때 main 자동 배포.
GitHub에 올리기 전 .env, PEM, API 키가 변경 목록에 없는지 확인합니다.

## 가상환경 설치와 테스트

~~~powershell
.\launcher.cmd -Target 01 -Action setup -Python python
.\launcher.cmd -Target 07 -Action setup -Python python
.\launcher.cmd -Target 01 -Action test
.\launcher.cmd -Target 07 -Action test
~~~

-Python에는 설치된 Python 3.11 이상 실행 파일의 전체 경로도 전달할 수 있습니다.
이미 설치된 환경에서는 test를 바로 실행합니다.
두 가상환경은 .venvs/compose(01 계열·00 도구), .venvs/weather(05~07)에 있습니다.
JSON의 pythonGroup이 사용할 가상환경을 선택합니다.
01 계열과 05~07의 google-genai 버전 조건이 달라 하나로 합치지 않습니다.
setup은 각 원본 requirements를 참조한 통합 requirements를 설치하고 pip check를 실행합니다.
기존 가상환경이 있으면 재사용합니다. 로컬 앱 패키지는 컨테이너 설치와 별개입니다.

전체 실습 테스트는 다음 한 번으로 실행할 수 있습니다. 실습별로 별도 Python 프로세스를 사용해
app.py 모듈 이름이 겹치지 않게 합니다.

~~~powershell
powershell -NoProfile -File .\test-python.ps1
~~~

launcher 자체의 오프라인 검증:

~~~powershell
.\.venvs\compose\Scripts\python.exe -m unittest discover -s .\tests -v
~~~

Docker 없이 서버 실행을 확인하려면 아래 연결 검사를 사용할 수 있습니다.

~~~powershell
.\.venvs\weather\Scripts\python.exe .\smoke-python.py
~~~

05의 MCP·Backend·Streamlit을 임시 로컬 포트로 띄워 서버 health와 실제 MCP tools/list 연결을
확인한 뒤 해당 프로세스만 종료합니다. DB·날씨 API·LLM은 호출하지 않습니다.
이 검사는 화면의 클릭 동작이나 Docker Build 검증을 대신하지 않습니다.

