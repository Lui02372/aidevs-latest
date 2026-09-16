# 00 Course Guide

이 폴더는 전체 AI 개발 과정을 처음 이해하고, 필요한 공통 기준을 빠르게 확인하기 위한 안내서입니다.

상세한 실습은 각 과정 폴더의 `README.md`와 `SETUP.md`에서 진행합니다. 이곳에서는 전체 과정 흐름, 설치와 계정 준비, 막혔을 때 확인할 공통 기준만 봅니다.

## 구성

| 폴더 | 역할 |
| --- | --- |
| [01_course-overview](./01_course-overview/README.md) | 01~08 과정의 순서, 목표, 큰 흐름 |
| [02_setup-guides](./02_setup-guides/README.md) | 설치, 계정 생성, 로그인, 공통 개발 환경 준비 |
| [03_learning-support](./03_learning-support/README.md) | 처음 시작 순서, 문서 읽는 법, 공통 오류 해결 기준 |

강사용 운영 자료는 로컬 전용 `04_instructor-guide`에 둘 수 있습니다. 이 폴더는 Git에 올리지 않도록 `.gitignore`에 등록되어 있으며, 학생 배포본에는 포함하지 않습니다.

## 처음 보는 순서

1. [과정 순서](./01_course-overview/course-sequence.md)를 보고 전체 학습 흐름을 확인합니다.
2. [과정 지도](./01_course-overview/course-map.md)에서 각 과정의 역할을 확인합니다.
3. [설치 가이드](./02_setup-guides/README.md)에서 GitHub 계정, VS Code, Python, Git, `.venv`, `.env` 준비를 진행합니다.
4. [시작 가이드](./03_learning-support/getting-started.md)를 따라 첫 실행 전 체크리스트를 확인합니다.
5. 각 과정 폴더의 `README.md`와 `SETUP.md`를 열어 해당 과정의 실행 방법을 따릅니다.
6. 막히면 [트러블슈팅 가이드](./03_learning-support/troubleshooting.md)를 먼저 봅니다.

## 핵심 기준

- `01`은 Python/Git 기초를 분리해서 초반 병목을 줄입니다.
- `02`~`04`는 Supabase 기반 AI 웹 서비스 흐름을 다룹니다.
- `05`~`06`은 LLM Agent, Tool Use, RAG, LangGraph를 다룹니다.
- `07`~`08`은 Docker Compose, 운영 자동화, 멀티 에이전트 서비스 프로젝트를 다룹니다.
- `01`~`04`, `06`~`08`은 과정 최상위 `.venv` 하나를 기본으로 사용합니다.
- `05`는 단원별 의존성이 달라질 수 있어 단원별 `.venv` 방식을 우선 권장합니다.
- `.env`, API Key, token, password는 제출하거나 GitHub에 올리지 않습니다.

## 설치 문서 빠른 링크

처음 설치하는 수강생은 아래 문서를 순서대로 확인합니다.

| 준비 항목 | 문서 |
| --- | --- |
| Python 설치 | [01_python-install-guide.md](./02_setup-guides/01_python-install-guide.md) |
| GitHub 계정 생성과 VS Code 설치 | [02_vscode-install-guide.md](./02_setup-guides/02_vscode-install-guide.md) |
| VS Code 확장 프로그램 | [03_vscode-extensions-guide.md](./02_setup-guides/03_vscode-extensions-guide.md) |
| Git/GitHub 기본 설정 | [04_git-github-setup-guide.md](./02_setup-guides/04_git-github-setup-guide.md) |
| PowerShell과 터미널 | [05_powershell-and-terminal-guide.md](./02_setup-guides/05_powershell-and-terminal-guide.md) |
| `.venv`, `pip`, `requirements.txt` | [06_venv-pip-requirements-guide.md](./02_setup-guides/06_venv-pip-requirements-guide.md) |
| `.env`와 secret 보안 | [07_env-and-secret-guide.md](./02_setup-guides/07_env-and-secret-guide.md) |
| Gemini/OpenAI 계정과 비용 | [08_gemini-openai-account-guide.md](./02_setup-guides/08_gemini-openai-account-guide.md) |
| Supabase | [09_supabase-account-guide.md](./02_setup-guides/09_supabase-account-guide.md) |
| Upstash Redis | [10_upstash-redis-guide.md](./02_setup-guides/10_upstash-redis-guide.md) |
| Streamlit | [11_streamlit-guide.md](./02_setup-guides/11_streamlit-guide.md) |
| Postman | [12_postman-guide.md](./02_setup-guides/12_postman-guide.md) |
| Render, Streamlit Cloud 등 무료 배포 | [13_free-deployment-services-guide.md](./02_setup-guides/13_free-deployment-services-guide.md) |
| Docker Desktop | [14_docker-desktop-guide.md](./02_setup-guides/14_docker-desktop-guide.md) |
| AWS 계정과 비용 관리 | [15_aws-account-and-cost-guide.md](./02_setup-guides/15_aws-account-and-cost-guide.md) |
| GitHub Actions | [16_github-actions-guide.md](./02_setup-guides/16_github-actions-guide.md) |
| Codex와 ChatGPT 사용 준비 | [17_codex-chatgpt-guide.md](./02_setup-guides/17_codex-chatgpt-guide.md) |
