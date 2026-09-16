# VS Code Source Control Guide

이 문서는 VS Code 화면에서 Git 작업을 진행하는 방법을 설명합니다.

이번 과정에서는 Git 명령어를 많이 입력하지 않습니다. 파일 변경 확인, stage, commit, push는 대부분 VS Code의 **Source Control** 화면에서 진행합니다.

## 전체 흐름

```text
폴더 열기
-> 파일 수정
-> Source Control 열기
-> 변경 파일 확인
-> diff 확인
-> stage
-> commit message 작성
-> commit
-> push 또는 sync
-> GitHub에서 확인
```

## 1. VS Code에서 과정 폴더 열기

VS Code에서는 파일 하나만 여는 것이 아니라 폴더 전체를 열어야 합니다.

올바른 위치:

```text
C:\aidev\01_python-git-foundation
```

PowerShell에서 열 수 있습니다.

```powershell
code C:\aidev\01_python-git-foundation
```

`code` 명령이 동작하지 않으면 VS Code를 직접 실행한 뒤 아래 메뉴를 사용합니다.

```text
File
-> Open Folder
-> C:\aidev\01_python-git-foundation 선택
```

## 2. Source Control 화면 열기

VS Code 왼쪽 메뉴에서 가지 모양 아이콘을 클릭합니다.

```text
Source Control
```

단축키:

```text
Ctrl + Shift + G
```

## 3. Source Control 화면에서 보이는 말

| 화면 문구 | 의미 | 무엇을 하면 되나요? |
| --- | --- | --- |
| No changes | 수정된 파일이 없습니다. | 파일을 수정한 뒤 다시 확인합니다. |
| Changes | 수정되었지만 아직 commit 준비는 안 된 파일입니다. | 파일을 클릭해 diff를 확인합니다. |
| Staged Changes | 다음 commit에 포함하기로 선택한 파일입니다. | 메시지를 작성하고 commit합니다. |
| Initialize Repository | 현재 폴더가 Git 저장소가 아닙니다. | 안내에 따라 저장소를 초기화합니다. |
| Publish Branch | 현재 branch를 GitHub에 처음 올릴 수 있습니다. | GitHub에 처음 올릴 때 사용합니다. |
| Sync Changes | GitHub와 내 PC의 변경 내용을 동기화합니다. | pull/push가 필요할 때 사용합니다. |

## 4. 파일 수정 후 변경 확인

예를 들어 `README.md`를 수정하면 Source Control 화면에 파일 이름이 나타납니다.

파일 이름을 클릭하면 변경 전후를 비교할 수 있습니다.

```text
왼쪽: 수정 전 내용
오른쪽: 수정 후 내용
초록색: 새로 추가된 줄
빨간색: 삭제된 줄
```

이 화면을 **diff**라고 부릅니다. commit하기 전에 반드시 diff를 확인합니다.

## 5. Stage 하기

stage는 “이 파일을 다음 commit에 포함하겠다”고 선택하는 단계입니다.

VS Code에서는 파일 이름 오른쪽의 `+` 버튼을 누릅니다.

```text
Changes
-> 파일 오른쪽 + 클릭
-> Staged Changes로 이동
```

초보자는 한 번에 모든 파일을 stage하기보다, 먼저 파일을 클릭해서 diff를 확인한 뒤 stage합니다.

## 6. Commit Message 작성

Source Control 상단의 메시지 입력 칸에 commit message를 작성합니다.

예시:

```text
docs: add Git practice README
test: add simple function test
fix: correct README image path
```

좋지 않은 예:

```text
수정
작업
final
update
```

왜 좋지 않을까요?

```text
나중에 봤을 때 무엇을 수정했는지 알 수 없기 때문입니다.
```

## 7. Commit 하기

메시지를 작성한 뒤 Commit 버튼을 누릅니다.

commit은 GitHub에 올리는 것이 아닙니다.

```text
commit:
  내 컴퓨터의 Git 이력에 저장합니다.

push:
  내 컴퓨터의 commit을 GitHub에 올립니다.
```

## 8. GitHub로 Push 하기

commit 후 GitHub로 올릴 때는 아래 버튼 중 하나가 보일 수 있습니다.

| 버튼 | 의미 |
| --- | --- |
| Publish Branch | 이 branch를 GitHub에 처음 올립니다. |
| Push | 내 commit을 GitHub에 올립니다. |
| Sync Changes | GitHub 최신 내용을 받고, 내 commit도 올립니다. |

혼자 실습할 때는 `Sync Changes`를 사용해도 괜찮습니다.

팀 프로젝트에서는 무조건 Sync를 누르기보다, 먼저 현재 branch와 변경 파일을 확인합니다.

## 9. GitHub에서 확인하기

push 후 GitHub 웹사이트에서 아래를 확인합니다.

```text
README가 잘 보이나요?
이미지 링크가 깨지지 않았나요?
표가 깨지지 않았나요?
Mermaid 도표가 보이나요?
최근 commit message가 보이나요?
실제 key나 .env 파일이 올라가지 않았나요?
```

## 10. 문제가 생겼을 때 최소 확인 명령어

VS Code 화면이 헷갈릴 때만 PowerShell에서 아래 명령어를 사용합니다.

```powershell
git status
git branch
git log --oneline -5
git remote -v
```

각 명령어의 의미:

| 명령어 | 의미 |
| --- | --- |
| `git status` | 현재 변경 파일과 branch 상태를 확인합니다. |
| `git branch` | 현재 어느 branch에 있는지 확인합니다. |
| `git log --oneline -5` | 최근 commit 5개를 확인합니다. |
| `git remote -v` | GitHub 원격 저장소가 연결되어 있는지 확인합니다. |

## 11. 커밋 전 체크리스트

commit 버튼을 누르기 전에 아래를 확인합니다.

```text
[ ] 변경 파일을 클릭해 diff를 확인했습니다.
[ ] .env 파일이 포함되지 않았습니다.
[ ] .venv 폴더가 포함되지 않았습니다.
[ ] 실제 API key나 token이 README나 코드에 없습니다.
[ ] commit message가 무엇을 바꿨는지 설명합니다.
[ ] 실수로 생성된 __pycache__나 .pyc 파일이 없습니다.
```

## 12. 초보자가 기억할 한 문장

```text
파일 저장은 VS Code 저장이고, commit은 Git 저장이며, push는 GitHub 업로드입니다.
```
