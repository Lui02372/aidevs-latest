# VS Code Redis 노란 밑줄과 Python 환경

requirements-compose.txt / requirements-weather.txt 설치와 두 환경의 import redis 및 pip check를 확인했습니다.
Redis Python 패키지 설치와 Redis 서버 실행은 별개입니다.

## 실습에 맞는 Python 선택

| 실습 | 인터프리터 |
| --- | --- |
| 00 도구, 01 / 01-2 / 01-3 | 00_runtime-and-deployment/.venvs/compose/Scripts/python.exe |
| 05 / 06 / 07 | 00_runtime-and-deployment/.venvs/weather/Scripts/python.exe |

07 과정 최상위와 00 폴더의 기본 Python은 현재 학습 중인 01 계열의 compose 환경입니다.
각 실습 폴더를 직접 열면 그 폴더의 .vscode/settings.json에서 해당 환경을 선택합니다.
모든 실습을 함께 열 때는 이 폴더의 runtime.code-workspace를 VS Code로 열면 폴더별 설정을 사용합니다.
Gemini SDK 버전 조건이 달라 두 환경을 하나로 합치지 않습니다.

VS Code가 이미 다른 Python을 선택해 둔 상태라면 defaultInterpreterPath만 바꿔도 기존 선택이 바뀌지 않을 수 있습니다.
그때는 해당 Python 파일을 열고 Ctrl+Shift+P → Python: Select Interpreter → Enter interpreter path에서
위 python.exe를 직접 선택합니다. 필요하면 Developer: Reload Window를 실행합니다.
경고를 숨기는 설정은 추가하지 않았습니다.

## 설치와 확인 재실행

00_runtime-and-deployment 폴더에서:

~~~powershell
powershell -NoProfile -File .\setup-python.ps1
.\.venvs\compose\Scripts\python.exe -c "import redis; print(redis.__version__)"
.\.venvs\weather\Scripts\python.exe -c "import redis; print(redis.__version__)"
~~~

## Docker 화면이나 앱의 Redis 상태가 노란 경우

편집기의 import 밑줄과 다른 문제입니다. Python 패키지만 설치해도 Redis 서버가 실행되지는 않습니다.
Docker Desktop을 실행한 뒤 launcher로 해당 서비스를 시작하고 로그를 확인합니다.

~~~powershell
.\launcher.cmd -Target 01 -Action start
.\launcher.cmd -Target 01 -Action status
.\launcher.cmd -Target 01 -Action logs
~~~

01 폴더에서 서버 응답을 확인하는 명령:

~~~powershell
docker compose -f compose.full-stack.yml exec redis redis-cli ping
~~~

정상 응답은 PONG입니다. 현재 점검한 PC에서는 Docker 실행 파일을 찾지 못했으므로 서버 연결은 미검증입니다.
