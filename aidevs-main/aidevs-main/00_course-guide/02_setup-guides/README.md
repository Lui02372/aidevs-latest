# 02 Setup Guides

이 폴더는 수업을 시작하기 전에 필요한 설치, 계정 생성, 로그인, 환경 설정 방법을 항목별로 정리한 설치 허브입니다.

각 과정의 `SETUP.md`에서는 설치 방법을 길게 반복하지 않고, 필요한 문서만 링크로 연결합니다.

## 먼저 볼 문서

처음 시작한다면 아래 순서대로 진행합니다.

```text
1. Python 설치
2. GitHub 계정 생성과 VS Code 설치
3. VS Code 확장 프로그램 설치
4. Git/GitHub 기본 설정
5. PowerShell과 터미널 사용법
6. .venv, pip, requirements.txt 사용법
7. .env와 secret 보안 기준
8. ChatGPT 또는 Codex 사용 준비
```

## 문서 목록

| 번호 | 문서 | 언제 필요한가 |
| --- | --- | --- |
| 01 | [Python 설치](./01_python-install-guide.md) | 모든 Python 실습 전에 필요합니다. |
| 02 | [VS Code 설치와 GitHub 로그인](./02_vscode-install-guide.md) | 모든 과정에서 사용할 기본 개발 도구입니다. |
| 03 | [VS Code 확장 프로그램](./03_vscode-extensions-guide.md) | Python, Markdown, GitHub, AI 보조 개발을 위해 필요합니다. |
| 04 | [Git/GitHub 기본 설정](./04_git-github-setup-guide.md) | GitHub 저장소, commit, push, Pull Request 실습 전에 필요합니다. |
| 05 | [PowerShell과 터미널](./05_powershell-and-terminal-guide.md) | 명령어 실행, 폴더 이동, 서버 실행 전에 필요합니다. |
| 06 | [.venv, pip, requirements.txt](./06_venv-pip-requirements-guide.md) | 과정별 Python 패키지 설치 전에 필요합니다. |
| 07 | [.env와 secret 보안](./07_env-and-secret-guide.md) | API key, Supabase key, AWS key를 다루기 전에 필요합니다. |
| 08 | [Gemini/OpenAI 계정과 비용](./08_gemini-openai-account-guide.md) | LLM API를 실제 호출하기 전에 필요합니다. |
| 09 | [Supabase 계정과 프로젝트](./09_supabase-account-guide.md) | Supabase DB/Auth/RLS 실습 전에 필요합니다. |
| 10 | [Upstash Redis](./10_upstash-redis-guide.md) | Redis 캐시, 세션, SSE 이벤트 전달 실습 전에 필요합니다. |
| 11 | [Streamlit](./11_streamlit-guide.md) | Streamlit 화면 실습과 배포 전에 필요합니다. |
| 12 | [Postman](./12_postman-guide.md) | FastAPI API를 Swagger 외부 도구로 테스트할 때 선택 사용합니다. |
| 13 | [무료 배포 서비스](./13_free-deployment-services-guide.md) | Render, Streamlit Community Cloud, Supabase Cloud, Upstash 배포 준비에 필요합니다. |
| 14 | [Docker Desktop](./14_docker-desktop-guide.md) | 05 이후 Docker 실습 전에 필요합니다. |
| 15 | [AWS 계정과 비용 관리](./15_aws-account-and-cost-guide.md) | 07~08 AWS 필수 실습 전에 필요합니다. |
| 16 | [GitHub Actions](./16_github-actions-guide.md) | CI/CD 자동 검증과 배포 파이프라인 전에 필요합니다. |
| 17 | [Codex와 ChatGPT 사용 준비](./17_codex-chatgpt-guide.md) | AI 보조 개발, 코드 리뷰, 오류 분석 실습 전에 필요합니다. |

## 중요한 기준

```text
.env 파일은 GitHub에 올리지 않습니다.
.venv 폴더는 GitHub에 올리지 않습니다.
API key, token, password는 README나 발표 자료에 적지 않습니다.
설치가 안 되면 먼저 버전 확인 명령을 실행합니다.
각 과정은 해당 과정 폴더 자체를 VS Code로 여는 것을 권장합니다.
```
