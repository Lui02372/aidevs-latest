# 05 과정 환경 준비

## 1. 기본 환경

- Python 3.11 이상 권장
- VS Code
- Git
- 선택 실연동: Docker Desktop
- GPT·이미지·TTS 실습: OpenAI API Key
- Gemini 비교 실습: Gemini API Key

모든 필수 예제는 `APP_MODE=mock`으로 실행할 수 있습니다.

## 1.1 권장 학습 경로

Docker가 처음이라면 모든 환경을 한 번에 설치하지 않습니다.

| 시점 | 실행 모드 | 필요한 환경 |
| --- | --- | --- |
| `01`~`05` 기본 예제 | Mock | Python과 `.venv` |
| `04` pgvector 확장 | Local Database | Docker Desktop, PostgreSQL/pgvector |
| `05` Memory 확장 | Local Cache/Database | Docker Desktop, Redis, PostgreSQL |
| Provider 비교 | Real 또는 Local LLM | API Key 또는 Docker Ollama |
| `08` 평가와 Trace | 저장 Fixture부터 시작 | 선택 실습에서 Mini Agent 06·07 Backend 사용 |
| `09` 통합 Lab | 별도 과정 | 별도 통합 Mini Project에서 구성 |

먼저 Mock으로 Agent의 계약과 흐름을 이해한 뒤 필요한 서비스만 추가합니다.
Docker가 설치되지 않았다는 이유로 초반 단원 학습을 중단할 필요는 없습니다.

## 1.2 이전 Cloud 환경과의 관계

- Supabase 대신 로컬 PostgreSQL을 사용해 DB와 pgvector의 내부 동작을 확인합니다.
- Upstash 대신 로컬 Redis를 사용해 Key, TTL, 재시작을 직접 관찰합니다.
- Render 대신 내 PC에서 Container의 Port와 실행 상태를 관리해 봅니다.
- Streamlit은 계속 Frontend로 사용하며 연결 대상만 두 Agent Backend로 바뀝니다.
- OpenAI·Gemini와 별도로 Ollama를 실행해 Cloud LLM과 Local LLM을 비교합니다.

로컬 서비스는 Cloud 서비스보다 우수해서 선택하는 것이 아니라 학습자가 시작,
중지, 데이터, 로그, 장애를 모두 통제할 수 있기 때문에 사용합니다. 운영 환경에서는
관리 편의성, 비용, 보안, 가용성을 검토해 관리형 서비스 사용 여부를 결정합니다.

## 2. 가상환경과 패키지

```powershell
cd C:\aidevs\05_llm-agent-orchestration
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Python 경로를 확인합니다.

```powershell
python -c "import sys; print(sys.executable)"
```

## 3. 환경 변수

```powershell
Copy-Item .env.example .env
```

기본값:

```dotenv
APP_MODE=mock
LLM_PROVIDER=mock
OPENAI_MODEL=gpt-4.1-mini
OPENAI_VISION_MODEL=gpt-4.1-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=coral
MAX_IMAGE_SIZE_MB=5
PYTHON_AGENT_API_URL=http://127.0.0.1:8000
LANGGRAPH_AGENT_API_URL=http://127.0.0.1:8001
```

실제 OpenAI 연결을 선택하는 경우에만 `OPENAI_API_KEY`를 설정합니다. `.env`는 Git에 올리지 않습니다.

## 4. Local Docker 환경

Docker Desktop만 Windows에 설치하고, Ollama·PostgreSQL·Redis는 각각 Docker
Container로 격리해 실행합니다. 자세한 개념과 명령은
[00_local-runtime](./00_local-runtime/README.md)에서 확인합니다.

Docker를 처음 사용한다면 먼저
[Docker 첫 사용 가이드](./00_local-runtime/00_docker-first-guide.md)에서 설치,
WSL, 명령 읽기, 중지와 삭제의 차이를 확인합니다. 수업에서는 개별 Container를
한 번씩 직접 실행한 뒤 반복 실행용 스크립트를 사용합니다.

[00_local-runtime](./00_local-runtime/README.md)의 순서로 다음 컨테이너를 준비합니다.

```text
Ollama/Llama          http://127.0.0.1:11434
PostgreSQL/pgvector   127.0.0.1:5433
Redis                 127.0.0.1:6379
```

Docker 상태와 연결을 확인합니다.

```powershell
docker ps
python .\00_local-runtime\05_environment_diagnostics.py
```

## 5. 단위 예제

```powershell
python .\01_llm-to-agent\01_concept_example.py
python .\01_llm-to-agent\02_travel_example.py
```

각 단원의 README에 실행 순서가 있습니다.

## 6. 08 평가와 Trace

08은 별도 Mini Agent 애플리케이션이 아닙니다. 다음 두 Backend를 각각 실행하고 Live 평가합니다.

```text
C:\mini_agent_st\mini_agent_06_agent_workflow
C:\mini_agent_st\mini_agent_07_human_approval
```

```powershell
cd C:\aidevs\05_llm-agent-orchestration\08_agent-evaluation-and-tracing
python .\01_evaluate_live_agent_06.py
python .\02_evaluate_live_agent_07.py
```

06과 07이 같은 기본 Port를 사용하므로 한 번에 하나씩 실행합니다. 별도의 `mini_agent_08_evaluation` Backend나 Frontend는 사용하지 않습니다.

## 7. 테스트

각 Mini Agent 프로젝트의 Backend Test를 먼저 통과시킨 뒤 08의 Live 평가를 실행합니다.

## 8. 실행 모드

Mock:

```dotenv
APP_MODE=mock
LLM_PROVIDER=mock
STORAGE_MODE=memory
```

GPT와 Docker 저장소:

```dotenv
APP_MODE=real
LLM_PROVIDER=openai
STORAGE_MODE=postgres
```

Gemini 또는 Ollama 비교:

```dotenv
LLM_PROVIDER=gemini
```

```dotenv
LLM_PROVIDER=ollama
```

08의 필수 평가는 저장 Fixture로 실행합니다. 실제 06·07 Agent 반복 평가는
각 Mini Agent의 실행 모드와 Provider 비용을 확인한 뒤 선택적으로 진행합니다.

## 9. 선택 환경

pgvector, Redis, Ollama는 해당 단원의 확장 실습에서만 사용합니다. Dockerfile과 Docker Compose 운영은 `07_multi-agent-service-ops`에서 학습합니다.

후속 `07_multi-agent-service-ops`에서는 다음 순서로 확장합니다.

```text
Dockerfile 작성
→ Docker Compose로 Frontend와 Backend 연결
→ Worker·Redis·PostgreSQL·Ollama 통합
→ GitHub Actions에서 Test·Compose 검사·Image Build
→ AWS EC2에서 Simple Compose 수동 배포
→ 비용이 발생하는 EC2·EBS·Security Group 정리
```

Docker Compose 파일 자체가 AWS의 모든 운영 문제를 해결하는 것은 아닙니다.
후속 과정에서는 학습 범위를 명확히 하기 위해 EC2 한 대에서 수동 Compose 배포를
먼저 경험하고, 완전한 CI/CD와 관리형 Container 운영은 선택 확장으로 구분합니다.

## 10. 자주 발생하는 문제

| 증상 | 확인 |
| --- | --- |
| 모듈을 찾지 못함 | 가상환경과 현재 폴더 확인 |
| API Key 오류 | `APP_MODE=mock`으로 먼저 실행 |
| Backend 연결 실패 | 두 Uvicorn 포트와 `PYTHON_AGENT_API_URL`, `LANGGRAPH_AGENT_API_URL` 확인 |
| 날짜 검증 오류 | ISO 날짜 `YYYY-MM-DD` 사용 |
| Streamlit 상태 초기화 | `st.session_state` key 확인 |
| LangGraph 재개 실패 | 동일한 `thread_id` 사용 여부 확인 |
| Docker Engine 연결 오류 | Docker Desktop 실행 후 `docker info` 확인 |
| Container 이름 충돌 | `docker ps -a` 확인 후 기존 Container를 `docker start` |
| Docker Port 충돌 | 실행 중인 `aidevs-*`와 `mini-agent-*` 중 한 환경만 사용 |
| `xxhash` DLL 차단 | 교육장 PC의 애플리케이션 제어 정책 확인 또는 허용된 개발 컨테이너/WSL 사용 |

일부 Windows 교육장 PC는 가상환경 내부의 네이티브 DLL을 차단할 수 있습니다.
이 경우 Python Workflow와 Mock/API 실습은 계속할 수 있지만 LangGraph import는
실패할 수 있습니다. 이는 예제 로직이 아니라 PC 보안 정책 문제입니다.
