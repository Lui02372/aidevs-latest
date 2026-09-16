# 02. VS Code 설치와 GitHub 로그인 가이드

이 문서는 수업에서 사용할 GitHub 계정과 VS Code 설치, VS Code 안에서 GitHub 계정으로 로그인하는 방법을 설명합니다.

수업에서는 GitHub 계정을 여러 곳에서 공통 로그인 계정으로 사용할 예정입니다.

예시:

```text
GitHub
VS Code
Render
Streamlit Community Cloud
GitHub Pull Request
GitHub Actions
```

그래서 **VS Code 설치보다 먼저 GitHub 계정을 준비**합니다.

공식 사이트:

| 항목 | 공식 링크 |
| --- | --- |
| GitHub | https://github.com/ |
| GitHub 회원가입 | https://github.com/signup |
| GitHub 계정 생성 안내 | https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github |
| VS Code 다운로드 | https://code.visualstudio.com/download |
| VS Code Windows 설치 안내 | https://code.visualstudio.com/docs/setup/windows |
| VS Code Settings Sync | https://code.visualstudio.com/docs/configure/settings-sync |

## 1. 왜 GitHub 계정을 먼저 만들까요?

GitHub는 코드를 인터넷에 저장하고 팀원과 협업하는 서비스입니다.

수업에서는 GitHub 계정을 아래 용도로 사용합니다.

```text
1. 수업 프로젝트를 GitHub 저장소에 올립니다.
2. VS Code에서 GitHub 계정으로 로그인합니다.
3. 팀 프로젝트에서 Pull Request를 만듭니다.
4. Render, Streamlit Community Cloud 같은 배포 서비스에 GitHub 계정으로 로그인합니다.
5. 배포 서비스가 GitHub 저장소의 코드를 가져가서 실행합니다.
```

즉, GitHub 계정은 단순히 Git 수업에서만 쓰는 계정이 아니라, 이후 백엔드, 프론트엔드, 미니 프로젝트, 배포 실습까지 계속 사용하는 기본 계정입니다.

## 2. GitHub 계정 만들기

브라우저에서 아래 주소로 이동합니다.

```text
https://github.com/signup
```

또는 GitHub 메인 페이지에서 `Sign up`을 클릭합니다.

```text
https://github.com/
```

가입할 때 보통 아래 정보를 입력합니다.

```text
이메일 주소
비밀번호
사용자 이름(username)
이메일 인증 코드
```

초보자가 주의할 점:

```text
1. username은 GitHub 주소에 사용될 수 있습니다.
2. 공개 저장소에서는 username이 다른 사람에게 보일 수 있습니다.
3. 이메일 인증을 완료해야 저장소 생성 같은 기본 기능을 원활하게 사용할 수 있습니다.
4. 비밀번호는 다른 서비스와 같은 것을 사용하지 않는 것이 좋습니다.
```

GitHub 공식 문서에서도 계정 생성 후 이메일 인증이 필요할 수 있다고 안내합니다.

## 3. GitHub 로그인 확인

계정을 만든 뒤 아래 주소로 이동합니다.

```text
https://github.com/login
```

로그인 후 오른쪽 위에 본인 프로필 아이콘이 보이면 정상입니다.

확인할 내용:

```text
[ ] GitHub에 로그인할 수 있다.
[ ] 오른쪽 위 프로필 아이콘이 보인다.
[ ] 이메일 인증을 완료했다.
[ ] username을 기억한다.
```

## 4. VS Code 다운로드

브라우저에서 아래 주소로 이동합니다.

```text
https://code.visualstudio.com/download
```

Windows 사용자는 보통 아래 항목을 선택합니다.

```text
Windows User Installer x64
```

VS Code 공식 Windows 설치 안내에서는 User Installer가 대부분의 사용자에게 권장됩니다. 관리자 권한 없이 설치할 수 있고 자동 업데이트도 편하게 사용할 수 있기 때문입니다.

## 5. VS Code 설치

다운로드한 설치 파일을 실행합니다.

설치 중 선택 화면이 나오면 초보자는 아래 기준으로 진행합니다.

```text
1. 사용권 계약에 동의합니다.
2. 설치 위치는 기본값을 사용합니다.
3. 시작 메뉴 폴더도 기본값을 사용합니다.
4. 추가 작업 선택 화면에서 가능하면 아래 항목을 체크합니다.
```

추천 체크 항목:

```text
Add "Open with Code" action to Windows Explorer file context menu
Add "Open with Code" action to Windows Explorer directory context menu
Register Code as an editor for supported file types
Add to PATH
```

특히 `Add to PATH`를 체크하면 PowerShell에서 아래 명령으로 VS Code를 열 수 있습니다.

```powershell
code .
```

설치 후 VS Code를 실행합니다.

## 6. VS Code 설치 확인

PowerShell을 새로 열고 아래 명령을 실행합니다.

```powershell
code --version
```

정상이라면 VS Code 버전이 출력됩니다.

만약 아래처럼 `code` 명령을 찾을 수 없다고 나오면:

```text
code : 'code' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프로그램 이름으로 인식되지 않습니다.
```

다음 중 하나를 확인합니다.

```text
1. VS Code 설치 시 Add to PATH를 체크했는지 확인합니다.
2. PowerShell을 완전히 닫고 새로 엽니다.
3. VS Code를 실행한 뒤 Command Palette에서 Shell Command 관련 설정을 확인합니다.
4. 그래도 안 되면 VS Code를 다시 설치하면서 Add to PATH를 체크합니다.
```

## 7. VS Code에서 폴더 열기

수업에서는 파일 하나만 열지 않고, 과정 폴더 전체를 엽니다.

예시:

```text
C:\aidev\01_python-git-foundation
```

VS Code 메뉴:

```text
File
-> Open Folder
-> C:\aidev\01_python-git-foundation 선택
```

PowerShell에서 열 수도 있습니다.

```powershell
code C:\aidev\01_python-git-foundation
```

주의:

```text
README.md 파일 하나만 열면 안 됩니다.
과정 폴더 전체를 열어야 .vscode 설정, 터미널, Git 상태를 제대로 사용할 수 있습니다.
```

## 8. VS Code에서 GitHub 계정으로 로그인

VS Code를 실행한 뒤 왼쪽 아래의 사람 모양 아이콘 또는 Accounts 아이콘을 클릭합니다.

진행 흐름:

```text
1. VS Code 왼쪽 아래 Accounts 아이콘을 클릭합니다.
2. Sign in with GitHub 또는 Turn on Settings Sync를 선택합니다.
3. 브라우저가 열리면 GitHub 계정으로 로그인합니다.
4. Visual Studio Code 권한 요청 화면에서 Authorize를 누릅니다.
5. 브라우저에서 VS Code로 돌아가라는 안내가 나오면 허용합니다.
6. VS Code 왼쪽 아래 Accounts 아이콘에서 GitHub 계정이 보이는지 확인합니다.
```

VS Code Settings Sync는 GitHub 계정 또는 Microsoft 계정으로 로그인할 수 있습니다. 이 과정에서는 여러 서비스 로그인을 GitHub로 맞추기 위해 GitHub 로그인을 우선 사용합니다.

## 9. Settings Sync는 켜야 하나요?

Settings Sync는 VS Code 설정, 단축키, 확장 프로그램 목록 등을 다른 PC와 동기화하는 기능입니다.

수업용 PC가 한 대라면 꼭 켤 필요는 없습니다.

여러 PC에서 같은 환경을 쓰고 싶다면 켜도 됩니다.

추천 기준:

```text
처음 수업을 시작하는 초보자:
  꼭 켜지 않아도 됩니다.

집 PC와 강의장 PC를 함께 사용하는 수강생:
  켜면 확장 프로그램과 설정을 맞추는 데 도움이 됩니다.

공용 PC를 사용하는 경우:
  수업이 끝난 뒤 GitHub 로그아웃 여부를 확인합니다.
```

## 10. GitHub 로그인이 필요한 순간

VS Code에서 GitHub 로그인이 필요한 순간은 다음과 같습니다.

```text
1. GitHub 저장소를 clone할 때
2. GitHub 저장소로 push할 때
3. VS Code에서 Pull Request를 확인할 때
4. GitHub Pull Requests 확장을 사용할 때
5. Settings Sync를 GitHub 계정으로 사용할 때
```

Git commit 자체는 내 컴퓨터에서 만드는 것이므로 GitHub 로그인 없이도 가능합니다.

하지만 GitHub에 코드를 올리는 push는 GitHub 인증이 필요합니다.

## 11. 설치 후 확인 체크리스트

```text
[ ] GitHub 계정을 만들었다.
[ ] GitHub 이메일 인증을 완료했다.
[ ] GitHub에 로그인할 수 있다.
[ ] VS Code를 설치했다.
[ ] PowerShell에서 code --version이 출력된다.
[ ] VS Code에서 과정 폴더를 열 수 있다.
[ ] VS Code Accounts에서 GitHub 계정으로 로그인했다.
[ ] VS Code Source Control 아이콘을 찾을 수 있다.
```

## 12. 자주 만나는 문제

### GitHub 로그인 브라우저가 열리지 않습니다

확인할 것:

```text
기본 브라우저가 정상 실행되는가?
회사/학교 네트워크에서 GitHub 접속이 막히지 않았는가?
VS Code를 관리자 권한이 아닌 일반 권한으로 실행해도 같은가?
```

### VS Code에서 GitHub 로그인이 계속 실패합니다

확인할 것:

```text
브라우저에 다른 GitHub 계정이 로그인되어 있지 않은가?
GitHub 이메일 인증이 완료되었는가?
VS Code를 완전히 종료한 뒤 다시 실행했는가?
```

### code 명령이 동작하지 않습니다

확인할 것:

```text
VS Code 설치 시 Add to PATH를 선택했는가?
PowerShell을 새로 열었는가?
code --version을 다시 실행했는가?
```

### 과정 폴더를 열었는데 터미널 자동 활성화가 안 됩니다

확인할 것:

```text
C:\aidev 루트가 아니라 현재 과정 폴더 자체를 열었는가?
예: C:\aidev\01_python-git-foundation
.vscode/settings.json 파일이 과정 폴더 안에 있는가?
이미 .venv를 만든 상태인가?
```

## 13. 다음 단계

VS Code 설치와 GitHub 로그인이 끝났다면 다음 문서를 진행합니다.

```text
03_vscode-extensions-guide.md
04_git-github-setup-guide.md
```

아직 위 문서가 분리되어 있지 않다면 각 과정의 `SETUP.md` 안내를 따라 진행합니다.

