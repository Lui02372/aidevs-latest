# SETUP

`02_python-advanced` 단원을 시작하기 전에 개발 환경을 다시 확인하는 문서입니다.

이 단원은 `01_python-git-foundation` 과정 안에 포함되어 있습니다. 따라서 `02_python-advanced` 폴더 안에 `.venv`를 새로 만들지 않습니다.

```text
사용하는 가상환경 위치:
C:\aidev\01_python-git-foundation\.venv
```

## 1. 작업 위치로 이동

PowerShell에서 상위 과정 폴더로 이동합니다.

```powershell
cd C:\aidev\01_python-git-foundation
Get-Location
```

정상 위치:

```text
C:\aidev\01_python-git-foundation
```

## 2. 기존 가상환경 활성화

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

정상이라면 Python 경로가 아래처럼 `01_python-git-foundation\.venv`를 가리켜야 합니다.

```text
C:\aidev\01_python-git-foundation\.venv\Scripts\python.exe
```

## 3. 패키지 설치 확인

이 단원에서는 테스트 예제를 위해 `pytest`를 사용합니다.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest --version
```

## 4. 첫 예제 실행

```powershell
python .\02_python-advanced\01_function-and-import\01_function_basic_review.py
```

## 5. JSON 예제 실행

```powershell
python .\02_python-advanced\02_exception-debugging\03_read_json_safely.py
```

## 6. 테스트 실행

```powershell
python -m pytest .\02_python-advanced\03_testing-basic
```

## 7. 프로젝트 구조 예제 실행

```powershell
python .\02_python-advanced\04_project-structure\01_simple_chat_project\main.py
python -m pytest .\02_python-advanced\04_project-structure\01_simple_chat_project

python .\02_python-advanced\04_project-structure\02_simple_chat_project\main.py
python -m pytest .\02_python-advanced\04_project-structure\02_simple_chat_project
```

## 시작 전 체크리스트

```text
[ ] 현재 위치가 C:\aidev\01_python-git-foundation 인가?
[ ] PowerShell 앞에 (.venv)가 보이는가?
[ ] python 실행 경로가 01_python-git-foundation\.venv 아래인가?
[ ] pytest 버전 확인이 되는가?
[ ] 02_python-advanced 안에 .venv를 새로 만들지 않았는가?
```

## 자주 헷갈리는 부분

### 02_python-advanced 폴더로 이동해서 실행해도 되나요?

가능은 하지만 이 과정에서는 권장하지 않습니다. 모든 예제 실행은 `01_python-git-foundation` 최상위 폴더에서 하는 것으로 통일합니다.

### 왜 02_python-advanced 안에 requirements.txt가 없나요?

필요한 패키지는 `01_python-git-foundation` 최상위 `requirements.txt`에서 함께 관리합니다. 같은 `.venv`를 사용하므로 단원마다 requirements를 나누지 않습니다.

### object를 깊게 배우지 않아도 되나요?

이 단원에서는 object를 “관련 데이터를 하나로 묶은 것” 정도로만 다룹니다. FastAPI의 Pydantic 모델을 이해하기 위한 준비로 `dataclass`를 짧게 확인합니다.
