# Lab 01. VS Code Source Control 흐름

이 실습에서는 VS Code Source Control 화면을 사용해 변경 파일을 확인하고 commit하는 흐름을 연습합니다.

명령어를 많이 입력하지 않습니다. 대부분 VS Code 화면에서 진행합니다.

## 실습 목표

```text
1. VS Code에서 과정 폴더를 열 수 있습니다.
2. Source Control 화면을 열 수 있습니다.
3. 변경 파일을 클릭해 diff를 볼 수 있습니다.
4. 변경 파일을 stage할 수 있습니다.
5. commit message를 작성하고 commit할 수 있습니다.
```

## 실습 대상 프로젝트

아래 폴더를 사용합니다.

```text
03_git-github/10_labs/practice-files/git-practice-project
```

폴더 구조:

```text
git-practice-project
├─ README.md
├─ main.py
└─ test_main.py
```

## 1. VS Code에서 폴더 열기

VS Code에서 아래 폴더를 엽니다.

```text
C:\aidev\01_python-git-foundation
```

파일 하나만 열지 말고 폴더 전체를 열어야 Source Control이 정상적으로 보입니다.

## 2. 테스트 프로젝트 확인

아래 파일을 엽니다.

```text
03_git-github/10_labs/practice-files/git-practice-project/main.py
```

`add` 함수가 있는지 확인합니다.

## 3. 파일 수정하기

`main.py`에 아래 함수를 추가합니다.

```python
def multiply(a: int, b: int) -> int:
    return a * b
```

저장합니다.

## 4. Source Control에서 변경 확인

VS Code 왼쪽의 Source Control 아이콘을 클릭합니다.

확인할 내용:

```text
Changes 영역에 main.py가 보이나요?
main.py를 클릭하면 변경 전후가 보이나요?
초록색으로 추가된 줄이 보이나요?
```

## 5. Stage 하기

`main.py` 오른쪽의 `+` 버튼을 클릭합니다.

파일이 아래 영역으로 이동해야 합니다.

```text
Staged Changes
```

## 6. Commit Message 작성

Source Control 상단 메시지 입력 칸에 아래처럼 씁니다.

```text
feat: add multiply function
```

## 7. Commit 하기

Commit 버튼을 누릅니다.

commit 후 Source Control에 변경 파일이 사라지면 정상입니다.

## 8. 확인용 명령어

필요하면 PowerShell에서 아래 명령만 확인합니다.

```powershell
git status
git log --oneline -5
```

## 정리 질문

```text
1. 파일 저장과 commit은 무엇이 다른가요?
2. stage는 왜 필요한가요?
3. diff 화면에서 초록색 줄은 무엇을 의미하나요?
4. 좋은 commit message는 어떤 특징이 있나요?
```
