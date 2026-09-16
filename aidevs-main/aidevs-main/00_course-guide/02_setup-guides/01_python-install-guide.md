# 01. Python 설치 가이드

이 과정은 Windows와 Python 3.12 계열을 기준으로 진행합니다.

Python은 `.py` 파일을 실행하고, `.venv` 가상환경을 만들고, FastAPI/Streamlit/LangGraph 같은 패키지를 설치할 때 필요합니다.

공식 사이트:

```text
https://www.python.org/downloads/
https://www.python.org/downloads/windows/
```

## 1. 이미 설치되어 있는지 확인

PowerShell을 열고 아래 명령을 실행합니다.

```powershell
python --version
py --version
pip --version
```

정상 예시:

```text
Python 3.12.x
Python 3.12.x
pip xx.x from ...
```

정상이라면 Python 설치는 끝난 상태입니다.

## 2. Python 다운로드

브라우저에서 아래 주소로 이동합니다.

```text
https://www.python.org/downloads/
```

Windows용 다운로드 버튼을 클릭합니다.

수업 기준은 Python 3.12 계열입니다. 이미 3.12 계열이 설치되어 있다면 새로 설치하지 않아도 됩니다.

## 3. 설치할 때 가장 중요한 체크

설치 첫 화면에서 반드시 아래 항목을 체크합니다.

```text
Add python.exe to PATH
```

이 항목을 체크해야 PowerShell에서 `python` 명령을 바로 사용할 수 있습니다.

그 다음 `Install Now`를 눌러 설치합니다.

## 4. 설치 후 확인

설치가 끝나면 기존 PowerShell을 닫고 새 PowerShell을 엽니다.

```powershell
python --version
py --version
pip --version
```

버전이 출력되면 정상입니다.

## 5. Python 실행 위치 확인

어떤 Python을 사용하는지 확인합니다.

```powershell
python -c "import sys; print(sys.executable)"
```

예시:

```text
C:\Users\사용자명\AppData\Local\Programs\Python\Python312\python.exe
```

과정별 `.venv`를 활성화한 뒤에는 이 경로가 각 과정의 `.venv\Scripts\python.exe`로 바뀌어야 합니다.

## 6. 자주 나는 문제

### python 명령을 찾을 수 없음

가능한 원인:

```text
1. 설치할 때 Add python.exe to PATH를 체크하지 않았습니다.
2. 설치 후 PowerShell을 새로 열지 않았습니다.
3. Python이 설치되지 않았습니다.
```

해결:

```text
1. PowerShell을 새로 엽니다.
2. py --version을 실행해 봅니다.
3. 그래도 안 되면 Python을 다시 설치하면서 Add python.exe to PATH를 체크합니다.
```

### pip 명령이 안 됨

아래처럼 실행합니다.

```powershell
python -m pip --version
python -m pip install --upgrade pip
```

## 7. 설치 체크리스트

```text
[ ] python --version이 출력된다.
[ ] py --version이 출력된다.
[ ] pip --version 또는 python -m pip --version이 출력된다.
[ ] python -c "import sys; print(sys.executable)"로 Python 경로를 확인했다.
```

