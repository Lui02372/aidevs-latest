# 05. PowerShell과 터미널 기본 가이드

PowerShell은 Windows에서 명령어를 실행하는 터미널입니다.

이 과정에서는 Python 실행, `.venv` 활성화, FastAPI 서버 실행, Streamlit 실행, Docker 실행을 PowerShell에서 진행합니다.

## 1. PowerShell 열기

방법 1:

```text
Windows 시작 메뉴
-> PowerShell 검색
-> Windows PowerShell 실행
```

방법 2:

```text
VS Code
-> Terminal
-> New Terminal
```

## 2. 현재 위치 확인

```powershell
Get-Location
```

짧게는 아래 명령도 사용할 수 있습니다.

```powershell
pwd
```

## 3. 폴더 이동

```powershell
cd C:\aidev
cd C:\aidev\01_python-git-foundation
```

한 단계 위로 이동:

```powershell
cd ..
```

## 4. 파일과 폴더 목록 보기

```powershell
dir
```

또는:

```powershell
Get-ChildItem
```

## 5. 가상환경 활성화

각 과정 폴더에서 실행합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

정상이라면 PowerShell 앞에 `(.venv)`가 보입니다.

## 6. 실행 정책 오류 해결

가상환경 활성화 때 오류가 나면 아래 명령을 한 번 실행합니다.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

그 다음 PowerShell을 새로 열고 다시 활성화합니다.

## 7. 현재 Python 확인

```powershell
python -c "import sys; print(sys.executable)"
```

각 과정의 `.venv\Scripts\python.exe`가 출력되어야 합니다.

## 8. 서버 실행 후 중지

FastAPI나 Streamlit 서버를 실행하면 터미널이 계속 실행 중인 상태가 됩니다.

중지:

```text
Ctrl + C
```

## 9. 자주 쓰는 명령

| 명령 | 의미 |
| --- | --- |
| `cd 경로` | 폴더 이동 |
| `dir` | 파일 목록 보기 |
| `python --version` | Python 버전 확인 |
| `pip --version` | pip 버전 확인 |
| `python -m pip install -r requirements.txt` | 패키지 설치 |
| `Ctrl + C` | 실행 중인 서버 중지 |

