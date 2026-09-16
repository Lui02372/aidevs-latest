# 03. VS Code 확장 프로그램 설치 가이드

VS Code 확장 프로그램은 Python 코드 작성, Markdown 문서 작성, GitHub 협업, AI 보조 개발을 편하게 해 줍니다.

## 1. 확장 프로그램 화면 열기

VS Code 왼쪽 메뉴에서 Extensions 아이콘을 클릭합니다.

단축키:

```text
Ctrl + Shift + X
```

검색창에 확장 이름을 입력하고 `Install`을 누릅니다.

## 2. 필수 확장 프로그램

| 확장 | 검색 이름 | 필요한 이유 |
| --- | --- | --- |
| Python | `Python` | Python 파일 실행, 인터프리터 선택, 디버깅에 필요합니다. |
| Pylance | `Pylance` | 타입 힌트, 자동 완성, 오류 표시를 도와줍니다. |
| Jupyter | `Jupyter` | 노트북 파일을 사용할 때 필요합니다. 필수는 아니지만 설치를 권장합니다. |
| GitHub Pull Requests | `GitHub Pull Requests and Issues` | VS Code에서 Pull Request를 확인할 때 사용합니다. |
| Markdown All in One | `Markdown All in One` | Markdown 작성과 미리보기에 도움이 됩니다. |

## 3. 선택 확장 프로그램

| 확장 | 검색 이름 | 언제 사용하나요? |
| --- | --- | --- |
| GitHub Copilot | `GitHub Copilot` | AI 코드 자동완성 기능을 사용할 때 선택합니다. |
| GitHub Copilot Chat | `GitHub Copilot Chat` | VS Code 안에서 AI에게 질문할 때 선택합니다. |
| Material Icon Theme | `Material Icon Theme` | 파일 종류별 아이콘을 보기 좋게 표시합니다. |
| Docker | `Docker` | Docker 컨테이너와 이미지를 VS Code에서 확인할 때 사용합니다. |
| YAML | `YAML` | GitHub Actions, Docker Compose YAML 파일 작성에 도움이 됩니다. |

## 4. 터미널 명령으로 설치하는 방법

`code` 명령이 동작한다면 PowerShell에서도 설치할 수 있습니다.

```powershell
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension GitHub.vscode-pull-request-github
code --install-extension yzhang.markdown-all-in-one
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension PKief.material-icon-theme
code --install-extension ms-azuretools.vscode-docker
code --install-extension redhat.vscode-yaml
```

## 5. Python 확장 설치 확인

VS Code에서 `.py` 파일을 엽니다.

오른쪽 아래 또는 Command Palette에서 Python interpreter를 선택할 수 있어야 합니다.

확인할 것:

```text
[ ] Python 파일을 열었을 때 색상이 적용된다.
[ ] import 오류가 노란색/빨간색 줄로 표시된다.
[ ] 오른쪽 아래 Python 버전 또는 interpreter 정보가 보인다.
```

## 6. Markdown 미리보기

Markdown 파일을 열고 아래 단축키를 누릅니다.

```text
Ctrl + Shift + V
```

또는:

```text
마우스 오른쪽 클릭
-> Open Preview
```

## 7. GitHub Copilot 사용 주의

GitHub Copilot은 계정과 플랜이 필요할 수 있습니다.

수업에서 사용한다면:

```text
1. GitHub 계정으로 VS Code에 로그인합니다.
2. Copilot 사용 가능 여부를 확인합니다.
3. 생성된 코드를 그대로 믿지 말고 실행과 테스트로 확인합니다.
4. API key나 개인정보를 Copilot Chat에 붙여넣지 않습니다.
```

## 8. 체크리스트

```text
[ ] Python 확장을 설치했다.
[ ] Pylance를 설치했다.
[ ] Markdown 미리보기가 된다.
[ ] GitHub Pull Requests 확장을 설치했다.
[ ] 선택적으로 Copilot/Copilot Chat을 설치했다.
```

