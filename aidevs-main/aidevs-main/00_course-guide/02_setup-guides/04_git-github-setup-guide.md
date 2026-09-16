# 04. Git/GitHub 기본 설정 가이드

Git은 내 컴퓨터에서 변경 이력을 관리하는 도구이고, GitHub는 Git 저장소를 인터넷에서 관리하고 팀원과 공유하는 서비스입니다.

공식 사이트:

```text
Git 다운로드: https://git-scm.com/download/win
GitHub: https://github.com/
GitHub 회원가입: https://github.com/signup
```

## 1. Git 설치 확인

PowerShell에서 실행합니다.

```powershell
git --version
```

정상 예시:

```text
git version 2.xx.x.windows.x
```

## 2. Git 설치

Git이 없다면 아래 공식 사이트에서 Git for Windows를 설치합니다.

```text
https://git-scm.com/download/win
```

설치 중 초보자는 대부분 기본값으로 진행해도 됩니다.

권장 기준:

```text
1. 기본 editor 선택 화면에서 VS Code가 보이면 VS Code를 선택합니다.
2. PATH 관련 선택은 Git from the command line and also from 3rd-party software를 사용합니다.
3. 나머지는 기본값으로 진행합니다.
```

설치 후 PowerShell을 새로 열고 다시 확인합니다.

```powershell
git --version
```

## 3. Git 사용자 이름과 이메일 설정

commit에는 누가 작업했는지 기록됩니다.

```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

예시:

```powershell
git config --global user.name "Kim Student"
git config --global user.email "kim@example.com"
```

설정 확인:

```powershell
git config --global user.name
git config --global user.email
```

## 4. GitHub 계정 확인

브라우저에서 GitHub에 로그인합니다.

```text
https://github.com/login
```

아직 계정이 없다면:

```text
https://github.com/signup
```

이메일 인증을 완료해야 저장소 생성과 협업 기능을 원활하게 사용할 수 있습니다.

## 5. VS Code에서 GitHub 로그인

VS Code 왼쪽 아래 Accounts 아이콘을 클릭합니다.

```text
Accounts
-> Sign in with GitHub
-> 브라우저 로그인
-> Authorize Visual Studio Code
```

로그인 후 VS Code에 GitHub 계정이 표시되면 정상입니다.

## 6. 최소 확인 명령어

```powershell
git status
git branch
git log --oneline -5
git remote -v
```

이 과정에서는 Git 명령어를 많이 외우기보다 VS Code Source Control 화면으로 변경 내용을 확인합니다.

## 7. 체크리스트

```text
[ ] git --version이 출력된다.
[ ] git config user.name을 설정했다.
[ ] git config user.email을 설정했다.
[ ] GitHub 계정에 로그인할 수 있다.
[ ] VS Code에서 GitHub 계정으로 로그인했다.
[ ] VS Code Source Control 아이콘을 찾을 수 있다.
```

