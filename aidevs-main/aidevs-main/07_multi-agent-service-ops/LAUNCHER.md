# 07 과정 JSON Launcher

이 폴더의 **launcher.cmd를 더블클릭**합니다.
실행 목록은 [00의 launcher.json](00_runtime-and-deployment/launcher.json)에서 관리합니다.

1. 목록에서 01, 01-2, 01-3, 05, 06, 07 중 하나를 입력합니다.
2. 동작 질문에서 Enter를 누르면 switch로 해당 실습으로 전환합니다.
3. 다른 등록 실습의 앱/인프라를 정지하고, 선택한 실습의 DB·Backend·Frontend를 실행합니다.
4. Frontend http://localhost:8501, Backend 문서 http://localhost:8000/docs 를 엽니다.

00은 PostgreSQL·Redis 공용 서버입니다. 02·03·04는 서버 코드가 없는 CI·EC2·CD 연결 가이드입니다.
이 번호들은 메뉴에서 Enter를 누르면 가이드를 엽니다(00은 서버 시작).
01 계열은 full-stack이므로 00을 별도로 먼저 실행하지 않아도 됩니다.

## PowerShell에서 한 단계씩 실행

명령은 현재 07_multi-agent-service-ops 폴더 기준입니다.
00 폴더와 그 안의 각 실습 폴더에도 launcher.cmd가 있어 같은 명령을 사용할 수 있습니다.

~~~powershell
.\launcher.cmd -Action list
.\launcher.cmd -Target 01 -Action switch
.\launcher.cmd -Target 01 -Action status
.\launcher.cmd -Target 01 -Action open
.\launcher.cmd -Target 01 -Action logs
.\launcher.cmd -Target 05 -Action switch
.\launcher.cmd -Target 05 -Action stop
~~~

switch는 등록된 다른 로컬 앱 스택을 정지합니다. DB 볼륨은 삭제하지 않습니다.
00 공용 서버는 switch 정지 대상에서 제외합니다.
start는 다른 실습을 정지하지 않고 선택한 실습만 시작하므로 공용 8000/8501 포트 충돌에 주의합니다.
init은 .env 준비만, start/switch는 서버 실행입니다.

## 서버 구성

| ID | 실행 서비스 |
| --- | --- |
| 00 | PostgreSQL + Redis |
| 01 / 01-2 / 01-3 | Frontend + Backend + PostgreSQL + Redis |
| 05 | Frontend + Backend + Weather MCP |
| 06 / 07 | Frontend + Backend + Weather MCP + PostgreSQL + Redis |

01 계열의 Ollama는 기본 실행에 포함하지 않습니다. OpenAI 또는 Gemini를 사용합니다.
06/07은 인프라 Compose가 healthy가 된 다음 앱 Compose를 시작합니다.
시작 전에 모든 Compose 설정을 검사하고, 오류가 나면 다음 단계를 실행하지 않습니다.
Build가 실패하면 이전 앱을 자동으로 다시 켜지는 않으므로 logs 확인 후 재실행합니다.

## 최초 준비

Docker Desktop의 Linux engine과 Compose v2가 필요합니다.
앱별 .env가 없으면 예제를 자동 복사하며, 기존 .env는 보존합니다.
실제 LLM 응답을 받으려면 사용할 실습의 .env에 OpenAI 또는 Gemini 키를 설정합니다.
키를 입력한 뒤 start 또는 switch를 다시 실행해 컨테이너에 반영합니다.
Dockerfile이 Backend·Frontend 패키지를 설치하므로 Docker 실행에 호스트 venv 활성화는 필요 없습니다.

01·01-2·01-3은 기존 Compose 프로젝트 이름과 DB 볼륨을 공유합니다.
이전 실습 데이터를 보존하기 위해 프로젝트 이름을 바꾸지 않았습니다.
다른 01 변형으로 전환해도 같은 DB 데이터가 보일 수 있습니다.

실행 전 명령만 확인할 수 있습니다.

~~~powershell
.\launcher.cmd -Target 07 -Action switch -DryRun
~~~

자세한 [사용법](00_runtime-and-deployment/LAUNCHER_GUIDE.md),
[CI 처음 설정](00_runtime-and-deployment/02_github-actions-ci/doc/ConnectGuide.md),
[EC2/CD 연결](00_runtime-and-deployment/04_github-actions-aws-deploy/doc/ConnectGuide.md).
