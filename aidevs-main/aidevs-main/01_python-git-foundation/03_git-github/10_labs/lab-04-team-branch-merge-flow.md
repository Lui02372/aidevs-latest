# Lab 04. 팀 Branch와 main 관리자 Merge 흐름

이 실습에서는 팀원이 각자 branch에서 작업하고, main 관리자가 Pull Request를 확인한 뒤 merge하는 흐름을 연습합니다.

명령어보다 VS Code와 GitHub 웹 화면을 중심으로 진행합니다.

## 실습 목표

```text
1. 팀원과 main 관리자 역할을 구분할 수 있습니다.
2. 팀원이 VS Code에서 branch를 만들 수 있습니다.
3. 팀원이 자기 branch에서 작업하고 commit할 수 있습니다.
4. 팀원이 GitHub에서 Pull Request를 만들 수 있습니다.
5. main 관리자가 PR의 Files changed를 확인할 수 있습니다.
6. main 관리자가 문제가 없는 PR을 merge할 수 있습니다.
7. 팀원이 merge 후 최신 main을 받을 수 있습니다.
```

## 역할

### main 관리자

```text
팀 저장소를 관리합니다.
팀원의 Pull Request를 확인합니다.
민감정보가 없는지 확인합니다.
충돌이 없는지 확인합니다.
문제가 없으면 main branch에 merge합니다.
```

### 팀원

```text
main에서 최신 코드를 받습니다.
자기 branch를 만듭니다.
담당 파일을 수정합니다.
commit하고 branch를 push합니다.
Pull Request를 만듭니다.
merge 후 다시 최신 main을 받습니다.
```

## 실습 예시 역할 분담

```text
팀원 A:
  README에 프로젝트 소개 문단 추가

팀원 B:
  main.py에 함수 1개 추가

팀원 C:
  test_main.py에 테스트 1개 추가

main 관리자:
  각 Pull Request 확인 후 merge
```

## 1. 팀원: 최신 main 받기

VS Code에서 현재 branch가 `main`인지 확인합니다.

왼쪽 아래 branch 이름을 클릭해 `main`을 선택합니다.

그 다음 Source Control에서 `Pull` 또는 `Sync Changes`를 눌러 최신 main을 받습니다.

확인용 명령어:

```powershell
git branch
git status
```

## 2. 팀원: 새 branch 만들기

VS Code 왼쪽 아래 branch 이름을 클릭합니다.

```text
Create new branch
```

branch 이름 예시:

```text
feature/team-a-readme
feature/add-multiply-function
test/add-main-test
```

주의:

```text
branch 이름에 공백을 넣지 않습니다.
main에서 직접 작업하지 않습니다.
최신 main을 받은 뒤 새 branch를 만듭니다.
```

## 3. 팀원: 파일 수정

자기 담당 파일만 수정합니다.

예시:

```text
팀원 A:
  README.md 수정

팀원 B:
  main.py 수정

팀원 C:
  test_main.py 수정
```

## 4. 팀원: Source Control에서 diff 확인

Source Control에서 변경 파일을 클릭합니다.

확인할 내용:

```text
[ ] 내가 맡은 파일만 수정했나요?
[ ] 실수로 다른 파일을 바꾸지 않았나요?
[ ] .env나 key가 들어가지 않았나요?
[ ] README 링크가 깨지지 않았나요?
```

## 5. 팀원: Commit 하기

변경 파일을 stage하고 commit합니다.

commit message 예시:

```text
docs: add team A project intro
feat: add multiply function
test: add multiply function test
```

## 6. 팀원: Branch Push

Source Control에서 `Publish Branch` 또는 `Push`를 누릅니다.

처음 만든 branch라면 보통 `Publish Branch`가 보입니다.

## 7. 팀원: Pull Request 만들기

GitHub 웹사이트에서 저장소를 엽니다.

branch를 push하면 보통 아래 버튼이 보입니다.

```text
Compare & pull request
```

Pull Request 제목 예시:

```text
docs: add team A project intro
```

Pull Request 설명 예시:

```markdown
## 작업 내용

- README에 팀 A 프로젝트 소개를 추가했습니다.

## 확인한 내용

- [ ] 변경 파일을 확인했습니다.
- [ ] .env 파일을 올리지 않았습니다.
- [ ] 실제 API key가 없습니다.
- [ ] README가 깨지지 않습니다.
```

## 8. main 관리자: Pull Request 확인

main 관리자는 PR에서 아래 탭을 확인합니다.

```text
Conversation
Commits
Files changed
```

가장 중요한 곳은 `Files changed`입니다.

확인 기준:

```text
[ ] 담당 파일만 수정했나요?
[ ] 민감정보가 없나요?
[ ] .env, .venv, __pycache__가 없나요?
[ ] README 링크가 깨지지 않나요?
[ ] 테스트 관련 수정이면 테스트 설명이 있나요?
[ ] 충돌 표시가 없나요?
```

## 9. main 관리자: Merge 하기

문제가 없으면 아래 버튼을 누릅니다.

```text
Merge pull request
-> Confirm merge
```

merge가 끝나면 해당 branch의 변경 내용이 main에 합쳐집니다.

## 10. 팀원: 최신 main 받기

merge 후 팀원 PC가 자동으로 최신 상태가 되는 것은 아닙니다.

팀원은 다시 main으로 이동한 뒤 최신 main을 받아야 합니다.

VS Code 흐름:

```text
1. 왼쪽 아래 branch 이름 클릭
2. main 선택
3. Pull 또는 Sync Changes 클릭
4. 다른 팀원의 변경 내용이 들어왔는지 확인
```

## 11. 다음 작업 시작

다음 작업은 다시 최신 main에서 새 branch를 만들어 시작합니다.

```text
최신 main 받기
-> 새 branch 만들기
-> 작업
-> commit
-> push
-> Pull Request
-> main 관리자 merge
```

## 정리 질문

```text
1. 팀원이 main에서 직접 작업하지 않는 이유는 무엇인가요?
2. Pull Request는 왜 필요한가요?
3. main 관리자는 PR에서 무엇을 확인해야 하나요?
4. merge 후 팀원이 최신 main을 받아야 하는 이유는 무엇인가요?
5. 다음 작업을 시작할 때 왜 새 branch를 만들어야 하나요?
```
