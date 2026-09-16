# Getting Started

처음 시작할 때는 아래 순서만 따라가면 됩니다.

1. `C:\aidev` 폴더를 만듭니다.
2. [car1403/aidev_student](https://github.com/car1403/aidev_student) 저장소에서 수강생용 자료를 내려받습니다.
3. 내려받은 자료 안의 과정 폴더 구조를 `C:\aidev` 안에 복사합니다.
4. 루트 [README.md](../../README.md)에서 과정 순서를 봅니다.
5. [설치 가이드](../02_setup-guides/README.md)에서 필요한 프로그램과 계정을 준비합니다.
6. 각 과정 폴더의 `README.md`를 읽습니다.
7. 각 과정 폴더의 `SETUP.md`를 따라 환경을 준비합니다.
8. VS Code는 가능하면 현재 진행 중인 과정 폴더 자체를 엽니다.
9. 터미널 앞에 `(.venv)`가 보이는지 확인합니다.
10. 실습 전 `pip install -r requirements.txt`를 실행합니다.

## 수강생용 자료 준비

수강생은 기본적으로 아래 저장소를 사용합니다.

```text
https://github.com/car1403/aidev_student
```

이 저장소는 수업을 따라가기 위한 학생용 구조입니다. 처음에는 전체 코드를 완성본처럼 읽기보다, 폴더 구조와 실습 파일을 `C:\aidev`에 준비하는 용도로 사용합니다.

권장 준비 흐름:

```text
1. GitHub에서 car1403/aidev_student 저장소에 접속합니다.
2. Code 버튼을 누릅니다.
3. Download ZIP을 선택합니다.
4. 내려받은 ZIP 파일의 압축을 풉니다.
5. 압축을 푼 폴더 안의 과정 폴더와 파일을 C:\aidev 안으로 복사합니다.
6. C:\aidev\README.md가 보이는지 확인합니다.
```

준비 후 폴더는 아래와 비슷하게 보여야 합니다.

```text
C:\aidev
├─ 00_course-guide
├─ 01_python-git-foundation
├─ 02_supabase-ai-backend
├─ 03_supabase-ai-frontend
├─ 04_supabase-ai-mini-project
├─ 05_llm-agent-orchestration
├─ 06_llm-agent-mini-project
├─ 07_multi-agent-service-ops
├─ 08_multi-agent-service-mini-project
└─ README.md
```

## 전체 코드 참고 자료

전체 코드와 완성 흐름을 참고하고 싶을 때는 아래 저장소를 봅니다.

```text
https://github.com/car1403/aidev
```

이 저장소는 전체 과정의 참고 코드와 문서가 포함된 원본 자료입니다.

사용 기준:

```text
aidev_student:
  수강생이 실습을 진행할 기본 자료입니다.
  C:\aidev에 복사해서 수업 중 직접 수정합니다.

aidev:
  전체 코드, 완성 예시, 참고 구현을 확인하는 자료입니다.
  막혔을 때 비교하거나, 수업 후 복습할 때 참고합니다.
```

처음부터 `aidev`의 완성 코드를 그대로 복사하기보다는, 먼저 `aidev_student`로 실습을 진행하고 필요한 경우에만 `aidev`를 참고합니다.

## 과정 시작 전 공통 체크

```text
[ ] Python 3.12 계열이 설치되어 있다.
[ ] GitHub 계정이 있고 로그인할 수 있다.
[ ] VS Code가 설치되어 있다.
[ ] Git이 설치되어 있다.
[ ] car1403/aidev_student 자료를 내려받아 C:\aidev에 준비했다.
[ ] car1403/aidev 저장소는 전체 코드 참고용이라는 것을 이해했다.
[ ] PowerShell에서 python --version이 동작한다.
[ ] 과정 폴더에 .venv를 만들 수 있다.
[ ] README.md와 SETUP.md를 Markdown Preview로 볼 수 있다.
[ ] .env와 .env.example의 차이를 이해했다.
```

## 설치 문서 빠른 이동

| 필요한 내용 | 문서 |
| --- | --- |
| Python 설치 | [Python 설치 가이드](../02_setup-guides/01_python-install-guide.md) |
| GitHub 계정과 VS Code 설치 | [VS Code 설치 가이드](../02_setup-guides/02_vscode-install-guide.md) |
| VS Code 확장 프로그램 | [VS Code 확장 프로그램](../02_setup-guides/03_vscode-extensions-guide.md) |
| Git/GitHub 설정 | [Git/GitHub 기본 설정](../02_setup-guides/04_git-github-setup-guide.md) |
| PowerShell | [PowerShell과 터미널](../02_setup-guides/05_powershell-and-terminal-guide.md) |
| `.venv`, `pip` | [.venv, pip, requirements.txt](../02_setup-guides/06_venv-pip-requirements-guide.md) |
| `.env` 보안 | [.env와 secret 보안](../02_setup-guides/07_env-and-secret-guide.md) |

## 문서 읽는 기준

- `README.md`: 무엇을 배우는지, 어떤 순서로 볼지
- `SETUP.md`: 설치와 실행 방법
- `00_references`: 개념과 보충 설명
- `10_labs`: 수업 중 실습
- `20_assignments`: 개인 과제
- `99_*`: 미니 프로젝트 또는 팀 프로젝트
