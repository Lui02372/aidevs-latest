# 03. Git GitHub

이 단원은 Git 명령어를 많이 외우는 시간이 아닙니다.

이번 단원의 목표는 **VS Code Source Control 화면을 사용해 내가 만든 프로젝트를 GitHub에 올리고, 팀원이 branch로 작업한 내용을 main 관리자가 확인한 뒤 merge하는 흐름**을 익히는 것입니다.

## 이 단원의 방향

```text
명령어 암기
-> VS Code 화면에서 변경 파일 확인
-> README 작성
-> Commit
-> GitHub Push
-> 팀원별 branch 작업
-> Pull Request
-> main 관리자 merge
-> 팀원들이 최신 main 받기
```

터미널 명령어는 아주 적게 사용합니다. 대부분의 작업은 VS Code 왼쪽의 **Source Control** 화면에서 진행합니다.

## 시작 전 확인

Git이 설치되어 있어야 VS Code Source Control과 GitHub 연동을 사용할 수 있습니다.

PowerShell에서 먼저 확인합니다.

```powershell
git --version
```

버전이 출력되지 않으면 아래 공통 설치 문서의 **Git 설치와 확인** 섹션을 먼저 진행합니다.

```text
../../00_course-guide/02_setup-guides/04_git-github-setup-guide.md
```

GitHub 계정도 필요합니다. 계정이 없다면 아래 사이트에서 미리 준비합니다.

```text
https://github.com/
```

## 학습 목표

- Git과 GitHub의 차이를 설명할 수 있습니다.
- VS Code Source Control에서 변경 파일과 변경 내용을 확인할 수 있습니다.
- VS Code에서 stage, commit, push, sync 흐름을 진행할 수 있습니다.
- GitHub에 올라가는 README를 Markdown으로 작성할 수 있습니다.
- README에 표, 코드 블록, 이미지 링크, Mermaid 도표를 넣을 수 있습니다.
- `.env`, `.venv`, API key 같은 민감정보를 GitHub에 올리면 안 되는 이유를 설명할 수 있습니다.
- 팀원이 각자 branch에서 작업하고 Pull Request를 만드는 흐름을 이해합니다.
- main 관리자가 Pull Request를 확인하고 merge하는 기준을 이해합니다.
- merge 후 팀원이 최신 main을 받아 다음 작업을 시작하는 흐름을 이해합니다.

## 폴더 구성

```text
03_git-github
├─ README.md
├─ 00_references
│  ├─ README.md
│  ├─ vscode-source-control-guide.md
│  ├─ markdown-readme-guide.md
│  ├─ gitignore-and-secret-guide.md
│  ├─ commit-message-guide.md
│  ├─ team-branch-workflow-guide.md
│  └─ git-command-cheatsheet.md
├─ 10_labs
│  ├─ README.md
│  ├─ lab-01-vscode-source-control-flow.md
│  ├─ lab-02-markdown-readme-writing.md
│  ├─ lab-03-github-push-and-secret-check.md
│  ├─ lab-04-team-branch-merge-flow.md
│  └─ practice-files
└─ 20_assignments
   └─ README.md
```

## 학습 순서

```text
1. Git과 GitHub 역할 이해
2. VS Code Source Control 화면 열기
3. 작은 Python 테스트 프로젝트 수정하기
4. 변경 파일과 diff 확인하기
5. Stage와 Commit 진행하기
6. README.md 작성하기
7. README에 표, 코드 블록, 이미지 링크, Mermaid 도표 넣기
8. .gitignore와 민감정보 제외 기준 확인하기
9. GitHub에 Push하기
10. GitHub 웹에서 README와 커밋 확인하기
11. 팀원이 자기 branch에서 작업하기
12. 팀원이 Pull Request 만들기
13. main 관리자가 PR 확인 후 merge하기
14. 팀원이 최신 main을 받아 다음 작업 시작하기
```

## 이 단원에서 사용하는 최소 명령어

VS Code가 중심이지만, 문제가 생겼을 때 상태를 확인하기 위해 아래 명령어는 알아둡니다.

```powershell
git --version
git status
git branch
git log --oneline -5
git remote -v
```

명령어로 commit, branch, merge를 깊게 연습하지 않습니다. 실제 작업은 VS Code와 GitHub 웹 화면에서 진행합니다.

## 핵심 개념

| 개념 | 초보자용 설명 |
| --- | --- |
| Git | 내 컴퓨터에서 파일 변경 이력을 관리하는 도구입니다. |
| GitHub | Git으로 관리한 프로젝트를 인터넷에 올리고 팀과 공유하는 서비스입니다. |
| Source Control | VS Code에서 Git 변경 파일을 보고 commit할 수 있는 화면입니다. |
| Commit | 현재 변경 내용을 하나의 저장 지점으로 남기는 것입니다. |
| Push | 내 컴퓨터의 commit을 GitHub에 올리는 것입니다. |
| Pull | GitHub의 최신 내용을 내 컴퓨터로 받는 것입니다. |
| Sync Changes | VS Code에서 Pull과 Push를 함께 처리하는 버튼입니다. |
| Branch | main과 분리된 작업 공간입니다. 팀원은 보통 자기 branch에서 작업합니다. |
| Pull Request | 내 branch 변경 내용을 main에 합쳐 달라고 요청하는 GitHub 기능입니다. |
| main 관리자 | 팀원의 Pull Request를 확인하고 main branch에 merge하는 담당자입니다. |
| Merge | branch의 변경 내용을 main에 합치는 작업입니다. |
| `.gitignore` | GitHub에 올리면 안 되는 파일을 제외하는 규칙 파일입니다. |

## 개인 실습 흐름

개인 실습에서는 `10_labs/practice-files/git-practice-project`를 사용합니다.

```text
1. main.py를 수정합니다.
2. test_main.py 테스트를 실행합니다.
3. README.md를 작성합니다.
4. VS Code Source Control에서 변경 내용을 확인합니다.
5. stage합니다.
6. commit합니다.
7. GitHub에 push합니다.
8. GitHub 웹에서 README가 잘 보이는지 확인합니다.
```

## 팀 실습 흐름

팀 실습에서는 역할을 나눕니다.

```text
main 관리자:
  GitHub 저장소를 관리합니다.
  팀원의 Pull Request를 확인합니다.
  민감정보, 충돌, README 링크, 테스트 결과를 확인합니다.
  문제가 없으면 main branch에 merge합니다.

팀원:
  최신 main을 받습니다.
  자기 branch를 만듭니다.
  VS Code에서 파일을 수정합니다.
  commit하고 branch를 GitHub에 push합니다.
  Pull Request를 만듭니다.
  merge가 끝나면 다시 최신 main을 받습니다.
```

## 실습 목록

| 실습 | 내용 |
| --- | --- |
| `10_labs/lab-01-vscode-source-control-flow.md` | VS Code Source Control로 변경 확인, stage, commit |
| `10_labs/lab-02-markdown-readme-writing.md` | README에 표, 코드 블록, 이미지, Mermaid 도표 작성 |
| `10_labs/lab-03-github-push-and-secret-check.md` | GitHub push와 `.env`, `.venv`, key 제외 확인 |
| `10_labs/lab-04-team-branch-merge-flow.md` | 팀원 branch, Pull Request, main 관리자 merge, 최신 main 받기 |

## 참고 문서

| 문서 | 용도 |
| --- | --- |
| `00_references/vscode-source-control-guide.md` | VS Code Source Control 사용법 |
| `00_references/markdown-readme-guide.md` | GitHub README 작성법 |
| `00_references/gitignore-and-secret-guide.md` | 민감정보와 제외 파일 관리 |
| `00_references/commit-message-guide.md` | 커밋 메시지 작성 기준 |
| `00_references/team-branch-workflow-guide.md` | 팀 브랜치 협업 흐름 |
| `00_references/git-command-cheatsheet.md` | 최소 Git 확인 명령어 |

## 단원 완료 기준

아래 내용을 직접 해보고 설명할 수 있으면 됩니다.

```text
VS Code Source Control에서 변경 파일을 확인할 수 있다.
변경 파일을 클릭해 diff를 볼 수 있다.
stage와 commit을 할 수 있다.
GitHub에 push할 수 있다.
README에 표, 코드 블록, 이미지 링크, Mermaid 도표를 넣을 수 있다.
.env와 .venv를 GitHub에 올리면 안 되는 이유를 설명할 수 있다.
팀원이 branch에서 작업하고 PR을 만드는 흐름을 설명할 수 있다.
main 관리자가 PR을 확인하고 merge하는 기준을 설명할 수 있다.
merge 후 팀원이 최신 main을 받는 이유를 설명할 수 있다.
```
