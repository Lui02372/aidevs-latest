# Team Branch Workflow Guide

이 문서는 팀 프로젝트에서 여러 명이 GitHub 저장소를 함께 사용하는 흐름을 설명합니다.

이번 과정에서는 명령어보다 VS Code와 GitHub 웹 화면을 중심으로 진행합니다.

## 1. 왜 branch를 사용할까요?

팀원 여러 명이 모두 `main`을 직접 수정하면 서로의 작업이 섞이기 쉽습니다.

그래서 팀원은 각자 branch를 만들어 작업하고, 작업이 끝나면 Pull Request로 main에 합쳐 달라고 요청합니다.

```text
main:
  팀 프로젝트의 기준 코드입니다.

팀원 branch:
  각 팀원이 자기 작업을 하는 별도 공간입니다.

Pull Request:
  내 branch 작업을 main에 합쳐 달라고 요청하는 과정입니다.

main 관리자:
  Pull Request를 확인하고 main에 merge하는 담당자입니다.
```

## 2. 역할 나누기

### main 관리자

main 관리자는 팀의 기준 코드를 관리합니다.

해야 할 일:

```text
1. GitHub 저장소를 준비합니다.
2. 팀원을 Collaborator로 초대합니다.
3. 팀원의 Pull Request를 확인합니다.
4. 변경 파일과 README 링크를 확인합니다.
5. .env, API key, token이 포함되지 않았는지 확인합니다.
6. 충돌이 없는지 확인합니다.
7. 문제가 없으면 Merge pull request를 누릅니다.
8. merge 후 팀원에게 최신 main을 받으라고 안내합니다.
```

### 팀원

팀원은 main을 직접 수정하지 않고 자기 branch에서 작업합니다.

해야 할 일:

```text
1. 최신 main을 받습니다.
2. 새 branch를 만듭니다.
3. 자기 담당 파일을 수정합니다.
4. 테스트하거나 README를 확인합니다.
5. VS Code에서 stage와 commit을 합니다.
6. branch를 GitHub에 push합니다.
7. GitHub에서 Pull Request를 만듭니다.
8. main 관리자의 리뷰를 기다립니다.
9. merge가 끝나면 main으로 돌아와 최신 코드를 받습니다.
```

## 3. 팀 프로젝트 전체 흐름

```text
main 관리자 저장소 준비
-> 팀원 초대
-> 팀원 최신 main 받기
-> 팀원 branch 만들기
-> 팀원 작업
-> 팀원 commit
-> 팀원 branch push
-> 팀원 Pull Request 생성
-> main 관리자 변경 확인
-> main 관리자 merge
-> 팀원 최신 main 받기
-> 다음 작업은 새 branch에서 시작
```

## 4. VS Code에서 팀원이 branch 만들기

1. VS Code에서 프로젝트 폴더를 엽니다.
2. 왼쪽 아래 branch 이름을 클릭합니다.
3. `Create new branch`를 선택합니다.
4. branch 이름을 입력합니다.

branch 이름 예시:

```text
feature/team-a-readme
feature/add-test-main
docs/update-project-guide
fix/readme-image-path
```

초보자는 branch 이름에 공백을 넣지 않습니다.

## 5. 팀원이 작업하고 commit하기

1. 담당 파일을 수정합니다.
2. Source Control을 엽니다.
3. 변경 파일을 클릭해 diff를 확인합니다.
4. 파일 오른쪽 `+` 버튼으로 stage합니다.
5. commit message를 작성합니다.
6. Commit 버튼을 누릅니다.

commit message 예시:

```text
docs: add team A project notes
test: add add function test
fix: correct README image path
```

## 6. 팀원이 branch를 GitHub에 올리기

commit 후 Source Control에서 아래 버튼 중 하나를 누릅니다.

```text
Publish Branch
Push
Sync Changes
```

처음 만든 branch라면 보통 `Publish Branch`가 보입니다.

## 7. 팀원이 Pull Request 만들기

GitHub 웹사이트에서 저장소를 엽니다.

보통 branch를 push하면 GitHub 상단에 Pull Request를 만들 수 있는 안내가 보입니다.

흐름:

```text
Compare & pull request
-> 제목 작성
-> 설명 작성
-> 변경 내용 확인
-> Create pull request
```

PR 제목 예시:

```text
docs: add team A README section
```

PR 설명 예시:

```markdown
## 작업 내용

- 팀 A 소개 문서를 추가했습니다.
- README에 팀 A 문서 링크를 추가했습니다.

## 확인한 내용

- [ ] README 링크를 확인했습니다.
- [ ] 실제 API key가 없습니다.
- [ ] .env 파일을 올리지 않았습니다.
```

## 8. main 관리자가 Pull Request 확인하기

main 관리자는 Pull Request에서 아래 탭을 확인합니다.

```text
Conversation:
  팀원이 작성한 설명과 체크리스트를 확인합니다.

Commits:
  어떤 commit이 들어왔는지 확인합니다.

Files changed:
  실제 변경 파일과 변경 줄을 확인합니다.
```

main 관리자의 확인 기준:

```text
[ ] 담당 파일만 수정했나요?
[ ] README 링크가 깨지지 않았나요?
[ ] 테스트 파일이 있다면 테스트가 통과했나요?
[ ] .env, .venv, __pycache__가 포함되지 않았나요?
[ ] 실제 API key나 token이 포함되지 않았나요?
[ ] commit message가 이해 가능한가요?
[ ] 충돌 표시가 없나요?
```

## 9. main 관리자가 merge하기

문제가 없으면 GitHub에서 아래 버튼을 누릅니다.

```text
Merge pull request
-> Confirm merge
```

merge가 끝나면 팀원의 branch 내용이 main에 합쳐집니다.

## 10. 팀원이 최신 main 받기

merge가 끝났다고 해서 팀원 PC가 자동으로 최신 상태가 되는 것은 아닙니다.

팀원은 VS Code에서 main으로 이동한 뒤 최신 내용을 받아야 합니다.

VS Code 흐름:

```text
1. 왼쪽 아래 branch 이름 클릭
2. main 선택
3. Source Control에서 Pull 또는 Sync Changes 클릭
4. 최신 파일이 들어왔는지 확인
```

확인용 명령어:

```powershell
git branch
git status
git log --oneline -5
```

## 11. 다음 작업을 시작하는 방법

항상 최신 main에서 새 branch를 만들어 시작합니다.

```text
main 최신화
-> 새 branch 생성
-> 작업
-> commit
-> push
-> Pull Request
```

이 습관을 지키면 충돌을 줄일 수 있습니다.

## 12. 초보자가 자주 하는 실수

| 실수 | 왜 문제인가요? | 해결 |
| --- | --- | --- |
| main에서 직접 작업 | 팀 기준 코드에 바로 영향이 갑니다. | 새 branch를 만들어 작업합니다. |
| 오래된 main에서 branch 생성 | 이미 merge된 다른 팀원 작업이 빠질 수 있습니다. | 먼저 Pull 또는 Sync를 합니다. |
| .env를 push | key가 노출될 수 있습니다. | `.gitignore`를 확인합니다. |
| PR 설명 없이 요청 | main 관리자가 변경 의도를 알기 어렵습니다. | 작업 내용과 확인 항목을 씁니다. |
| merge 후 최신 main을 받지 않음 | 다음 작업에서 충돌이 날 수 있습니다. | main으로 이동해 Pull 또는 Sync합니다. |
