# Launcher 구현·설치 검증 결과

검증일: 2026-09-17

## 목표

00_runtime-and-deployment 안의 실습을 JSON 기반 Windows launcher로 실행하고,
각 단계의 doc/ConnectGuide.md에서 PowerShell·PostgreSQL·EC2·GitHub Actions 연결을 안내한다.

## 구현

- launcher.json: 00, 01, 01-2, 01-3, 02, 03, 04, 05, 06, 07 총 10개 항목
- launcher.cmd / launcher.ps1: 메뉴, guide, init, setup, test, start, status, stop, check, logs, DryRun
- 각 실습 doc/ConnectGuide.md 10개와 공통 LAUNCHER_GUIDE.md
- GitHub Actions CI 예제: 6개 프로젝트를 별도 Runner에서 테스트·Build
- setup-python.ps1: 기존 requirements를 참조해 호환되는 두 그룹별 가상환경 설치
- test-python.ps1: 실습별 별도 프로세스로 테스트
- smoke-python.py: 실제 05 MCP·Backend·Streamlit 기동 및 health 확인 후 프로세스 종료

## 검증 결과

| 검사 | 판정 | 근거 |
| --- | --- | --- |
| 변경 범위 | PASS | 구현·문서·가상환경은 00 폴더 내부 |
| JSON 경로·ID | PASS | 10개 항목의 guide·Compose·env 예제 경로 검사 |
| launcher 회귀 검사 | PASS | tests/test_launcher.py 6개 통과 |
| .env 보존 | PASS | 기존 값 보존, 없는 파일만 예제에서 생성 |
| 실행 순서 | PASS | 인프라→앱 시작, 앱→인프라 정지, 실패 후 다음 Compose 미실행 |
| Windows 호환 | PASS | PowerShell 7 및 Windows PowerShell 5.1 실행 계획, cmd 메뉴 |
| 문서 링크 | PASS | 가이드 11개 내부 파일 링크 검사 |
| CI YAML | PASS | YAML 파싱 및 6개 matrix 프로젝트 requirements 경로 검사 |
| compose 가상환경 | PASS | Python 3.12.14, requirements-compose.txt 설치, pip check 통과 |
| weather 가상환경 | PASS | Python 3.12.14, requirements-weather.txt 설치, pip check 통과 |
| 01 / 01-2 / 01-3 | PASS | 각각 Backend 테스트 3개 통과 |
| 05 / 06 | PASS | 각각 Backend 테스트 2개 통과 |
| 07 | PASS | Backend 테스트 11개 통과 |
| 실제 로컬 연결 | PASS | MCP health, Backend의 실제 MCP tools/list, Streamlit health |
| 프로세스 정리 | PASS | Windows 하위 프로세스 트리 종료 방식 수정 후 정상 종료 |
| Docker Build·컨테이너 실행 | WARN | 이 PC에 Docker CLI/Desktop을 찾지 못해 미실행 |
| GitHub Actions 실제 실행·AWS 배포 | WARN | workflow 활성화·Push·계정 연결·배포는 미수행, 가이드와 템플릿 제공 |

Backend 테스트 24개 + launcher 테스트 6개 통과.
실제 연결 검사는 별도로 실행했으며 종료 후 테스트 서버를 계속 켜 두지 않았다.
외부 날씨 API·실제 LLM·실제 PostgreSQL 연결은 이번 검사에서 호출하지 않았다.
FastAPI/Starlette 의존성의 deprecation 경고가 있으나 테스트 실패나 pip 의존성 충돌은 없었다.
샌드박스에서는 taskkill의 트리 종료가 제한되어 실제 Windows 종료 검사는 승인된 실행 환경에서 재확인했다.

## 재현

00_runtime-and-deployment에서 실행한다.

~~~powershell
.\launcher.cmd -Action list
.\launcher.cmd -Target 07 -Action test
powershell -NoProfile -File .\test-python.ps1
.\.venvs\compose\Scripts\python.exe -m unittest discover -s .\tests -v
.\.venvs\weather\Scripts\python.exe .\smoke-python.py
~~~

Docker가 준비된 뒤에는 launcher의 check → start → status를 실행한다.
GitHub Actions는 02/doc/ConnectGuide.md를 먼저 읽고, CD는 04/doc/ConnectGuide.md 순서로 연결한다.

## JSON 서버 전환 추가 검증

- 07 최상위와 00 내부의 10개 실습 폴더에 공통 launcher 진입점 연결.
- JSON에 실제 Compose 서비스 목록과 Backend 주소 추가.
- start: 없는 .env 준비 → 전체 Compose 설정 검사 → 순서대로 up --wait.
- switch: 선택한 구성 검사 → 다른 등록 앱 정지 → 선택한 앱 시작. 00 공용 인프라·볼륨 보존.
- open: 선택한 Frontend 주소를 브라우저에 열기.
- launcher 테스트 9개 통과: 전환 순서, 검사 실패 시 기존 앱 미중지, 환경 파일 보존 포함.
- 10개 JSON 항목의 서비스 목록, Compose YAML, Build의 Dockerfile 경로 대조 통과.
- 07 최상위 cmd 메뉴, 07 switch DryRun, Windows PowerShell 5.1 전환 계획 확인.
- 실제 start는 Docker CLI 미설치로 실패 메시지를 확인함. 실제 Docker Build/기동 성공을 의미하지 않음.
