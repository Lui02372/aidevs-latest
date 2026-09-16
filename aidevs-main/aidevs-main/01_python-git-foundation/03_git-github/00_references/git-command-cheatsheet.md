# Git Command Cheatsheet

이 문서는 실습 중 상태가 헷갈릴 때 확인하는 최소 Git 명령어 모음입니다.

이번 과정에서는 대부분 VS Code Source Control로 진행합니다. 아래 명령어는 “확인용”으로만 사용합니다.

## Git 설치 확인

```powershell
git --version
```

Git이 설치되어 있으면 버전이 출력됩니다.

버전이 출력되지 않으면 Git이 아직 설치되지 않았거나 PowerShell에서 Git을 찾지 못하는 상태입니다.

먼저 공통 설치 문서의 Git 설치 안내를 확인합니다.

```text
../../../../00_course-guide/02_setup-guides/04_git-github-setup-guide.md
```

## 현재 상태 확인

```powershell
git status
```

확인할 수 있는 것:

```text
현재 branch
수정된 파일
새로 생긴 파일
stage된 파일
commit할 내용이 있는지
```

## 현재 branch 확인

```powershell
git branch
```

`*` 표시가 붙은 branch가 현재 작업 중인 branch입니다.

## 최근 commit 확인

```powershell
git log --oneline -5
```

최근 commit 5개를 한 줄씩 확인합니다.

## GitHub 원격 저장소 확인

```powershell
git remote -v
```

GitHub 저장소 주소가 연결되어 있는지 확인합니다.

## 변경 내용 확인

```powershell
git diff
```

VS Code에서는 변경 파일을 클릭하면 같은 내용을 화면으로 볼 수 있습니다.

## 꼭 기억할 것

```text
git status:
  지금 상태를 봅니다.

git branch:
  지금 어느 branch인지 봅니다.

git log --oneline -5:
  최근 commit을 봅니다.

git remote -v:
  GitHub와 연결되어 있는지 봅니다.
```

명령어로 바로 해결하려고 하기보다, 먼저 VS Code Source Control 화면에서 변경 파일과 branch를 확인합니다.
