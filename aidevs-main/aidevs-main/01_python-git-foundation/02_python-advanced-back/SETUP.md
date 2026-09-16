# SETUP

`02_python-advanced` 단원을 시작하기 전에 개발 환경을 다시 확인하는 복습용 안내입니다.

이 단원은 `01_python-git-foundation` 과정 안에 포함된 하위 단원입니다. 따라서 `02_python-advanced` 폴더 안에 `.venv`를 새로 만들지 않습니다. 이미 `01_python-git-foundation` 최상위에 만든 `.venv`를 그대로 사용합니다.

```text
사용하는 가상환경 위치:
C:\aidev\01_python-git-foundation\.venv
```

## 이 문서를 다시 보는 이유

`01_python-basic`을 마친 뒤 `02_python-advanced`로 넘어오면 함수, 모듈, 예외 처리, 테스트처럼 조금 더 구조적인 내용을 다룹니다. 이때 실행 위치나 가상환경이 헷갈리면 예제 코드가 정상이어도 실행 오류가 날 수 있습니다.

그래서 이 문서는 새 환경을 만드는 문서가 아니라, 이미 만든 환경을 다시 확인하는 복습 문서입니다.

핵심 기준은 아래와 같습니다.

```text
1. 작업 위치는 C:\aidev\01_python-git-foundation 입니다.
2. 가상환경은 C:\aidev\01_python-git-foundation\.venv 하나만 사용합니다.
3. 02_python-advanced 안에는 .venv를 만들지 않습니다.
4. 02_python-advanced 안에는 별도 requirements.txt를 두지 않습니다.
5. 필요한 패키지는 01_python-git-foundation 최상위 requirements.txt에서 관리합니다.
```

## 1. 상위 과정 폴더로 이동

PowerShell에서 `01_python-git-foundation` 폴더로 이동합니다.

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

## 2. 기존 가상환경 활성화

이미 01 과정 시작 단계에서 만든 `.venv`를 활성화합니다.

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

## 3. pip 업그레이드

패키지를 설치하기 전에 현재 가상환경의 `pip`를 최신 버전으로 올립니다.

```powershell
python -m pip install --upgrade pip
```

## 4. 패키지 설치 확인

`02_python-advanced`에서는 테스트 예제를 위해 `pytest`를 사용합니다.

이 패키지는 `01_python-git-foundation` 최상위의 `requirements.txt`에서 함께 관리합니다. 상위 과정의 공통 패키지가 아직 설치되지 않았다면 아래 명령으로 설치합니다.

```powershell
pip install -r requirements.txt
```

설치 확인:

```powershell
python -c "import pytest; print('advanced packages ok')"
```

## 5. 02_python-advanced에서 사용하는 외부 패키지

`02_python-advanced` 하위 폴더에는 별도의 `requirements.txt`가 없지만, 테스트 단원에서 사용하는 외부 패키지는 있습니다. 해당 패키지는 이미 `01_python-git-foundation` 최상위 `requirements.txt`에 포함되어 있으므로, 아래 명령을 이전에 실행했다면 추가 설치하지 않아도 됩니다.

```powershell
pip install -r requirements.txt
```

이번 단원에서 직접 사용하는 주요 외부 패키지는 아래와 같습니다.

| 패키지 | 사용하는 위치 | 왜 필요한가 |
| --- | --- | --- |
| `pytest` | `08_testing-code-quality`, `20_assignments` | 함수가 예상대로 동작하는지 자동으로 검사하는 테스트 도구입니다. `test_*.py` 파일을 실행해 코드 품질을 확인합니다. |

### pytest

`pytest`는 Python 테스트 도구입니다. 직접 프로그램을 실행해 눈으로 확인하는 대신, 함수의 입력과 출력이 맞는지 자동으로 검사할 수 있습니다.

이 과정에서는 다음 내용을 연습합니다.

```text
1. 테스트 파일 이름 규칙 이해하기
2. assert로 결과 검증하기
3. 함수 단위로 코드가 맞는지 확인하기
4. 리팩토링 후 기존 기능이 깨지지 않았는지 확인하기
```

설치 확인:

```powershell
python -m pytest --version
```

정리하면, `02_python-advanced`에서 새 `requirements.txt`를 만들 필요는 없습니다. 필요한 패키지는 최상위 `requirements.txt`에 이미 포함되어 있고, 같은 `.venv` 안에 설치됩니다.

## 6. 첫 예제 실행

상위 과정 폴더에서 아래 명령을 실행합니다.

```powershell
python .\02_python-advanced\01_function-advanced\01_args_kwargs_api_options.py
```

## 7. 테스트 실행

`pytest`가 설치되어 있으면 테스트 예제를 실행할 수 있습니다.

```powershell
python -m pytest .\02_python-advanced\08_testing-code-quality
```

## 8. 시작 전 체크리스트

```text
[ ] 현재 위치가 C:\aidev\01_python-git-foundation 인가?
[ ] PowerShell 앞에 (.venv)가 보이는가?
[ ] python -c "import sys; print(sys.executable)" 결과가 01_python-git-foundation\.venv\Scripts\python.exe인가?
[ ] python --version과 pip --version이 정상 출력되는가?
[ ] pytest import 확인이 되는가?
[ ] 02_python-advanced 안에 .venv를 새로 만들지 않았는가?
```

## 9. 자주 헷갈리는 부분

### 02_python-advanced 폴더로 이동해서 실행해도 되나요?

가능은 하지만 이 과정에서는 권장하지 않습니다. 모든 예제 실행은 `01_python-git-foundation` 최상위 폴더에서 하는 것으로 통일합니다.

### 02_python-advanced 안에 requirements.txt가 없는데 괜찮나요?

괜찮습니다. 필요한 패키지는 `01_python-git-foundation` 최상위 `requirements.txt`에서 함께 관리합니다.

### .venv를 다시 만들면 안 되나요?

이 과정에서는 다시 만들지 않습니다. 단원마다 `.venv`를 만들면 어떤 패키지가 어느 환경에 설치되었는지 헷갈릴 수 있습니다. `01_python-git-foundation\.venv` 하나를 계속 사용합니다.
