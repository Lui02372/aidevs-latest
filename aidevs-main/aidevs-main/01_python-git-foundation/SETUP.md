# SETUP

`01_python-git-foundation` 과정의 개발 환경 설정 문서입니다.

이 과정은 Python 기초와 Git/GitHub 실습을 위한 독립 선행 과정입니다. Supabase, Gemini API, FastAPI, Redis 설정은 다음 과정인 `02_supabase-ai-backend`부터 진행합니다.

## 공통 개발 환경 안내 문서

Python 설치, VS Code 설치, 확장 프로그램, PowerShell 사용법, Markdown 문서 보기처럼 더 구체적인 준비 방법은 아래 공통 안내 문서를 참고합니다.

| 필요한 내용 | 참고 문서 |
| --- | --- |
| Python 설치와 버전 확인 | [`../00_course-guide/02_setup-guides/01_python-install-guide.md`](../00_course-guide/02_setup-guides/01_python-install-guide.md) |
| VS Code 설치 | [`../00_course-guide/02_setup-guides/02_vscode-install-guide.md`](../00_course-guide/02_setup-guides/02_vscode-install-guide.md) |
| VS Code 확장 프로그램 설치 | [`../00_course-guide/02_setup-guides/03_vscode-extensions-guide.md`](../00_course-guide/02_setup-guides/03_vscode-extensions-guide.md) |
| Git 설치와 버전 확인 | [`../00_course-guide/02_setup-guides/04_git-github-setup-guide.md`](../00_course-guide/02_setup-guides/04_git-github-setup-guide.md) |
| PowerShell 기본 사용법 | [`../00_course-guide/02_setup-guides/05_powershell-and-terminal-guide.md`](../00_course-guide/02_setup-guides/05_powershell-and-terminal-guide.md) |
| `.venv`, `pip`, `requirements.txt` 사용법 | [`../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md`](../00_course-guide/02_setup-guides/06_venv-pip-requirements-guide.md) |
| Markdown 미리보기와 문서 작성법 | [`../00_course-guide/03_learning-support/getting-started.md`](../00_course-guide/03_learning-support/getting-started.md) |
| 첫 실행 전 점검표 | [`../00_course-guide/03_learning-support/getting-started.md`](../00_course-guide/03_learning-support/getting-started.md) |
| Codex와 ChatGPT 사용 준비 | [`../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md`](../00_course-guide/02_setup-guides/17_codex-chatgpt-guide.md) |

## 1. 작업 위치로 이동

PowerShell을 열고 과정 폴더로 이동합니다.

```powershell
cd C:\aidev\01_python-git-foundation
```

현재 위치를 확인합니다.

```powershell
Get-Location
```

결과가 아래와 비슷하면 됩니다.

```text
C:\aidev\01_python-git-foundation
```

## 2. Python 가상환경 만들기

이 과정에서는 `01_python-git-foundation` 최상위의 `.venv` 하나를 사용합니다. `01_python-basic`, `02_python-advanced`, `03_git-github` 하위 폴더 안에는 별도 `.venv`를 만들지 않습니다.

```powershell
python -m venv .venv
```

이미 `.venv` 폴더가 있으면 다시 만들 필요는 없습니다.

## 3. 가상환경 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell 줄 앞에 `(.venv)`가 보이면 활성화된 상태입니다.

확인 명령:

```powershell
echo $env:VIRTUAL_ENV
python -c "import sys; print(sys.executable)"
python --version
pip --version
```

정상이라면 위 두 경로가 아래처럼 `01_python-git-foundation\.venv`를 가리켜야 합니다.

```text
C:\aidev\01_python-git-foundation\.venv
C:\aidev\01_python-git-foundation\.venv\Scripts\python.exe
```

PowerShell 실행 정책 오류가 나오면 다음 명령을 한 번 실행한 뒤 다시 활성화합니다.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 4. VS Code 터미널 자동 활성화 설정

`01_python-git-foundation`에는 `.vscode/settings.json` 파일이 포함되어 있습니다. 이 파일은 VS Code의 새 PowerShell 터미널을 열 때 아래 명령을 자동으로 실행하도록 설정합니다.

```powershell
& '.\.venv\Scripts\Activate.ps1'
```

이 설정을 사용하면 VS Code에서 터미널을 새로 열 때마다 직접 `.\.venv\Scripts\Activate.ps1`을 입력하지 않아도 됩니다.

중요한 기준:

```text
1. 먼저 .venv를 만들어 둡니다.
2. VS Code에서 C:\aidev\01_python-git-foundation 폴더 자체를 엽니다.
3. 새 터미널을 열었을 때 PowerShell 앞에 (.venv)가 보이는지 확인합니다.
```

`C:\aidev` 전체 폴더를 VS Code로 열어 수업을 진행할 때는 루트 `.vscode/settings.json`에서 Python 확장의 자동 가상환경 활성화를 끕니다. 따라서 새 터미널을 연 뒤에는 위 확인 명령으로 현재 Python 경로가 이 과정의 `.venv`를 가리키는지 먼저 확인합니다.

## 5. 패키지 설치

기초 실습과 테스트에 필요한 패키지를 설치합니다.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

설치 확인:

```powershell
python -c "import pytest; print('packages ok')"
```

## 6. 예제 실행

```powershell
python .\01_python-basic\01_python-start\01_hello_python.py
python .\02_python-advanced\01_function-advanced\01_args_kwargs_api_options.py
python -m pytest .\02_python-advanced\08_testing-code-quality
```

## 7. Git/GitHub 준비

Git 설치 여부를 확인합니다.

```powershell
git --version
```

버전이 출력되지 않으면 공통 환경 문서의 Git 설치 안내를 먼저 진행합니다.

```text
../00_course-guide/02_setup-guides/04_git-github-setup-guide.md
```

GitHub 계정 준비와 VS Code Source Control 사용법은 `03_git-github`에서 단계적으로 실습합니다.

```text
03_git-github
```

## 체크리스트

```text
[ ] 01_python-git-foundation 최상위에서 .venv를 만들었는가?
[ ] .venv가 활성화된 상태에서 pip install -r requirements.txt를 실행했는가?
[ ] 01_python-basic 예제가 실행되는가?
[ ] 02_python-advanced 테스트가 실행되는가?
[ ] git --version으로 Git 설치를 확인했는가?
```
