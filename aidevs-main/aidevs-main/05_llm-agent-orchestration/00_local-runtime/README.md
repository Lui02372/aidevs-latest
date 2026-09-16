# 00 Local Runtime

Docker에서 Ollama/Llama, PostgreSQL/pgvector, Redis를 실행하고 Python에서 연결을 확인합니다.

이 단원에서 로컬 머신에 직접 설치하는 핵심 프로그램은 Docker Desktop입니다.
Ollama, PostgreSQL, Redis는 Windows에 각각 설치하지 않고 Docker가 관리하는
독립 Container로 실행합니다. 실습이 끝나면 Container만 중지할 수 있고, 데이터는
Docker Volume에 남길 수 있습니다.

## Cloud 서비스와 비교

| Local Docker | 이전 과정의 Cloud 서비스 | 공통 역할 | 주요 차이 |
| --- | --- | --- | --- |
| PostgreSQL/pgvector | Supabase | 관계형 데이터와 Vector 저장 | 로컬에서는 시작·Schema·Volume을 직접 관리 |
| Redis | Upstash Redis | Cache, Session, TTL | 로컬에서는 프로세스·데이터 보존·장애를 직접 확인 |
| Ollama/Llama | OpenAI·Gemini | LLM 추론 | 로컬 자원을 사용하며 모델별 기능과 성능이 다름 |
| Container 실행 | Render 배포 | Backend 실행 환경 제공 | 로컬에서는 Port와 실행 상태를 직접 관리 |

Streamlit은 인프라 서비스가 아니라 Python Frontend Framework입니다. `05`에서도
그대로 사용하며, 로컬에서 실행한 Python Agent 또는 LangGraph Agent API를
선택해 호출합니다.

## 먼저 알아둘 네 가지

| 용어 | 이 과정에서의 의미 |
| --- | --- |
| Image | Container를 만들기 위한 실행 환경의 원본 |
| Container | Image로 만든 실행 중인 독립 프로세스 |
| Port | Windows에서 Container 서비스로 접근하는 연결 번호 |
| Volume | Container를 중지·교체해도 유지할 데이터 저장 공간 |

예를 들어 `-p 5433:5432`는 Windows의 `5433`번 Port를 PostgreSQL Container의
`5432`번 Port에 연결합니다. `-v aidevs-pgvector-data:...`는 DB 데이터를
Container 밖의 Docker Volume에 보존합니다.

## 서비스 역할

| 서비스 | 역할 | Host Port |
| --- | --- | ---: |
| Ollama | Llama 로컬 실행 | `11434` |
| PostgreSQL/pgvector | RAG, 장기 Memory, 실행 이력 | `5433` |
| Redis | 단기 상태, Cache, TTL | `6379` |

## 진행 순서

1. [Docker 첫 사용 가이드](./00_docker-first-guide.md)
2. [Docker 상태 확인](./01_docker-health-check.md)
3. [Redis 실행](./04_redis.md)과 `PING` 확인
4. [PostgreSQL/pgvector 실행](./03_postgresql-pgvector.md)과 Schema 확인
5. [Ollama/Llama 실행](./02_ollama-llama.md)과 모델 다운로드
6. `05_environment_diagnostics.py` 실행

Redis는 가장 작은 명령으로 실행과 응답을 확인할 수 있어 Docker 입문 실습에
적합합니다. Ollama는 모델 다운로드와 PC 자원 사용량이 크므로 마지막에
진행합니다.

## 반복 실행용 스크립트

각 Container를 한 번씩 직접 실행해 본 뒤에는 다음 스크립트로 세 서비스를 다시
시작할 수 있습니다. **첫 Docker 실습에서는 스크립트보다 개별 문서를 먼저
따라갑니다.**

```powershell
.\00_local-runtime\scripts\start-local-services.ps1
```

모델 다운로드:

```powershell
docker exec -it aidevs-ollama ollama pull llama3.2
```

연결 점검:

```powershell
python .\00_local-runtime\05_environment_diagnostics.py
```

## 종료

```powershell
.\00_local-runtime\scripts\stop-local-services.ps1
```

종료는 컨테이너와 데이터를 삭제하지 않습니다. 컨테이너·Volume 삭제는 실습 데이터가 사라지는 작업이므로 학생이 대상을 확인한 뒤 별도로 수행합니다.

## 현재 과정과 후속 운영 과정의 경계

현재 `05_llm-agent-orchestration`에서는 각각의 인프라 도구를 `docker run`으로
실행합니다. Dockerfile, Docker Compose, 배포와 운영 자동화는 후속
`07_multi-agent-service-ops`에서 다룹니다. 현재 단원의
`07_human-approval-and-safety`와는 다른 과정입니다.

```text
05 Local Runtime
개별 Image → 개별 Container → Port → Volume → Python 연결

07 Service Ops
Dockerfile → Docker Compose → GitHub Actions → AWS EC2 Compose 배포
```

Docker Compose는 여러 Container의 설정과 네트워크를 한 파일로 묶어 같은 구성을
반복 실행하게 해 줍니다. 후속 `07_multi-agent-service-ops`에서는 먼저 로컬과
CI에서 Compose 구성을 검증한 뒤 Amazon Linux 2023 EC2 한 대에 Simple Compose를
수동 배포합니다. 수업 완료에는 비용 방지를 위한 EC2, EBS, Security Group
정리도 포함됩니다.
