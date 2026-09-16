# 01_python-git-foundation

Python 기초, Python 심화, Git/GitHub를 먼저 분리해서 학습하는 선행 과정입니다.

이 과정은 이후 `02_supabase-ai-backend`, `03_supabase-ai-frontend`, `04_supabase-ai-mini-project`를 진행하기 전에 필요한 공통 기반을 다집니다. Supabase, Gemini API, FastAPI 서버 구현은 다음 과정부터 본격적으로 다룹니다.

## 과정 목표

- Python 기본 문법, 자료형, 조건문, 반복문, 함수를 이해합니다.
- 파일/JSON 처리, 함수 심화, 모듈/패키지, 예외 처리, OOP, 테스트를 익힙니다.
- Git/GitHub로 변경 이력을 관리하고 VS Code Source Control을 사용할 수 있습니다.
- README 작성, `.gitignore`, `.env`와 API key 보안 기준을 이해합니다.
- 이후 백엔드 과정에서 코드를 읽고 실행할 수 있는 최소 개발 습관을 만듭니다.

## 처음 시작하는 순서

1. [SETUP.md](./SETUP.md)를 보고 `01_python-git-foundation` 폴더에 `.venv`를 만듭니다.
2. PowerShell에서 `.venv`를 활성화합니다.
3. 선택 사항으로 VS Code 터미널 자동 활성화 설정을 확인합니다.
4. `pip install -r requirements.txt`로 기초 실습 패키지를 설치합니다.
5. `01_python-basic`부터 예제를 실행합니다.
6. `02_python-advanced`에서 함수, 모듈, 예외 처리, 테스트를 확장합니다.
7. `03_git-github`에서 Git/GitHub와 VS Code Source Control을 실습합니다.

이 과정에서는 단원별 `.venv`를 만들지 않고, `01_python-git-foundation` 최상위의 `.venv` 하나를 사용합니다.

VS Code에서 `01_python-git-foundation` 폴더 자체를 열면 `.vscode/settings.json` 설정에 따라 새 터미널을 열 때 `.venv`가 자동 활성화됩니다. `C:\aidev` 전체 폴더를 열면 하위 과정의 `.vscode` 설정은 자동 적용되지 않으므로, 자동 활성화를 사용하려면 해당 과정 폴더를 VS Code로 여는 것이 좋습니다.

## 과정 구조

```text
01_python-git-foundation
├─ .venv
├─ requirements.txt
├─ README.md
├─ SETUP.md
├─ 01_python-basic
├─ 02_python-advanced
└─ 03_git-github
```

## 단원 요약

| 단원 | 역할 |
| --- | --- |
| `01_python-basic` | 변수, 자료형, 입출력, 조건문, 반복문, 함수, 파일/JSON 기초를 학습합니다. |
| `02_python-advanced` | 함수 심화, 모듈/패키지, 예외 처리, OOP, 테스트, 프로젝트 구조를 학습합니다. |
| `03_git-github` | Git/GitHub, 커밋/브랜치, VS Code Source Control, README/문서 작성, 민감정보 보호 기준을 학습합니다. |

## 필수 학습 흐름

이 과정은 이후 백엔드와 프론트엔드 실습을 따라가기 위한 기반 과정입니다. 모든 자료를 같은 깊이로 다루기보다, 다음 과정에서 바로 필요한 내용을 먼저 익힙니다.

```text
환경 설정과 Python 실행
-> 변수, 자료형, 타입 힌트
-> 조건문과 반복문
-> list, dict 중심의 자료구조
-> 함수와 파일/JSON 저장
-> 모듈, 예외 처리, pytest 기초
-> 프로젝트 구조 맛보기
-> Git/GitHub, .gitignore, .env 보안
```

## 선택 학습 흐름

아래 내용은 시간이 충분하거나 복습이 필요할 때 보충으로 다룹니다.

| 구분 | 내용 |
| --- | --- |
| Python 심화 | 함수 심화, 모듈/패키지, 예외 처리, JSON 처리, pytest, 프로젝트 구조 복습 |
| 선택 과제 | `02_python-advanced/20_assignments` 종합 과제 |
| Git 심화 | VS Code Source Control, README 작성, Pull Request, 팀 브랜치 협업 |

## 다음 과정으로 넘어가기 전 기준

아래 내용을 스스로 설명하고 실행할 수 있으면 `02_supabase-ai-backend`로 넘어갈 준비가 된 것입니다.

```text
python 파일을 실행할 수 있다.
.venv를 활성화하고 Python 경로를 확인할 수 있다.
변수, 조건문, 반복문, list/dict, 함수를 사용해 작은 프로그램을 만들 수 있다.
JSON 파일을 저장하고 다시 읽을 수 있다.
try/except의 기본 의미를 설명할 수 있다.
pytest를 실행해 간단한 테스트 결과를 확인할 수 있다.
git status, git diff, git add, git commit의 역할을 설명할 수 있다.
.env와 .venv를 GitHub에 올리면 안 되는 이유를 설명할 수 있다.
```

## 공통 실행 준비

자세한 환경 준비는 [SETUP.md](./SETUP.md)를 참고합니다.

```powershell
cd C:\aidev\01_python-git-foundation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 예제 실행 방법

항상 과정 최상위 폴더에서 실행하면 경로 혼선을 줄일 수 있습니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
python .\01_python-basic\01_python-start\01_hello_python.py
python .\02_python-advanced\01_function-advanced\01_args_kwargs_api_options.py
python -m pytest .\02_python-advanced\08_testing-code-quality
```

## 다음 과정과의 연결

`01_python-git-foundation`을 마친 뒤에는 [02_supabase-ai-backend](../02_supabase-ai-backend/README.md)로 이동합니다.

다음 과정에서는 Python/Git 자체를 다시 길게 설명하지 않고, FastAPI, Supabase, Gemini API, Upstash Redis를 사용해 AI 백엔드 구조를 만드는 데 집중합니다.
