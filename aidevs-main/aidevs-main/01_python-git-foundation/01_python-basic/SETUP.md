# SETUP

`01_python-basic` 단원 실행 환경 안내입니다.

이 단원은 `01_python-git-foundation` 과정 안에 포함된 하위 단원입니다. 따라서 `01_python-basic` 폴더 안에 `.venv`를 새로 만들지 않습니다. 이미 `01_python-git-foundation` 최상위에 만든 `.venv`를 그대로 사용합니다.

```text
사용하는 가상환경 위치:
C:\aidev\01_python-git-foundation\.venv
```

## 1. 상위 과정 폴더로 이동

```powershell
cd C:\aidev\01_python-git-foundation
```

## 2. 기존 가상환경 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell 줄 앞에 `(.venv)`가 보이면 활성화된 상태입니다.

## 3. Python 확인

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

권장 버전:

```text
Python 3.11 이상
```

## 4. 패키지 설치 기준

`01_python-basic`은 Python 표준 라이브러리만 사용합니다. 따라서 이 하위 폴더에는 별도의 `requirements.txt`를 두지 않습니다.

공통 패키지 설치는 `01_python-git-foundation` 최상위 폴더의 `requirements.txt`에서 관리합니다. 이미 상위 과정 설정에서 설치했다면 여기서 추가로 설치할 것은 없습니다.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

이미 설치했다면 다시 설치하지 않아도 됩니다.

## 5. 예제 실행

상위 과정 폴더에서 아래 명령을 실행합니다.

```powershell
python .\01_python-basic\01_python-start\01_hello_python.py
```

## 6. 자주 만나는 문제

### 스크립트 실행 권한 오류

PowerShell에서 `Activate.ps1` 실행이 막히면 아래 명령을 한 번 실행합니다.

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### python 명령을 찾을 수 없음

Python이 설치되어 있는지 확인하고, 설치 시 `Add python.exe to PATH`가 선택되어 있는지 확인합니다.
