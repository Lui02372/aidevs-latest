# Docker Desktop 설치 가이드

Docker는 내 컴퓨터 안에서 작은 실행 환경인 컨테이너를 띄우는 도구입니다. 05 과정 이후에는 PostgreSQL, pgvector, Redis, Agent 서비스 같은 여러 구성 요소를 로컬에서 실행할 때 Docker를 사용합니다.

공식 문서:

- [Docker Desktop for Windows 설치](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Compose 문서](https://docs.docker.com/compose/)

## 1. 언제 필요한가

처음 01~04 과정에서는 Docker를 필수로 사용하지 않습니다.

Docker는 주로 아래 과정에서 필요합니다.

| 과정 | Docker 사용 이유 |
| --- | --- |
| 05_llm-agent-orchestration | 로컬 실행 환경, PostgreSQL, pgvector, 선택형 도구 실습 |
| 07_multi-agent-service-ops | Docker Compose, 컨테이너 기반 배포, 운영 실습 |
| 08_multi-agent-service-mini-project | 멀티 컨테이너 서비스, 장애 복구, 배포 검증 |

## 2. 설치 순서

1. [Docker Desktop for Windows 설치 페이지](https://docs.docker.com/desktop/setup/install/windows-install/)에 접속합니다.
2. `Download Docker Desktop for Windows`를 선택합니다.
3. 설치 파일을 실행합니다.
4. 설치 중 `Use WSL 2 instead of Hyper-V`와 비슷한 선택지가 보이면 기본값으로 둡니다.
5. 설치가 끝나면 컴퓨터를 재시작합니다.
6. Docker Desktop을 실행합니다.

Docker Desktop은 처음 실행될 때 WSL 2 업데이트나 추가 설치를 요청할 수 있습니다. 화면 안내에 따라 진행하면 됩니다.

## 3. 설치 확인

PowerShell을 열고 아래 명령을 실행합니다.

```powershell
docker --version
docker compose version
docker ps
```

정상이라면 Docker 버전과 실행 중인 컨테이너 목록이 보입니다.

처음에는 실행 중인 컨테이너가 없으므로 `docker ps` 결과가 비어 있어도 괜찮습니다.

## 4. 테스트 실행

아래 명령으로 Docker가 실제로 컨테이너를 실행할 수 있는지 확인합니다.

```powershell
docker run hello-world
```

정상이라면 Docker가 테스트 이미지를 내려받고 성공 메시지를 출력합니다.

## 5. 자주 쓰는 명령

| 명령 | 의미 |
| --- | --- |
| `docker ps` | 현재 실행 중인 컨테이너 확인 |
| `docker ps -a` | 종료된 컨테이너까지 모두 확인 |
| `docker images` | 내려받은 이미지 확인 |
| `docker compose up` | `docker-compose.yml` 기준으로 서비스 실행 |
| `docker compose up -d` | 백그라운드로 서비스 실행 |
| `docker compose down` | compose로 실행한 서비스 중지와 정리 |
| `docker logs 컨테이너명` | 컨테이너 로그 확인 |

## 6. 포트 충돌 확인

Docker 컨테이너도 FastAPI처럼 포트를 사용합니다. 이미 사용 중인 포트를 다시 쓰면 실행에 실패합니다.

자주 쓰는 포트 예시는 다음과 같습니다.

| 포트 | 주로 사용하는 서비스 |
| --- | --- |
| 8000 | FastAPI |
| 8501 | Streamlit |
| 5432 또는 5433 | PostgreSQL |
| 6379 | Redis |
| 11434 | Ollama |

포트 충돌이 나면 실행 명령이나 `docker-compose.yml`에서 외부 포트를 바꿔야 합니다.

## 7. Docker와 `.env`

Docker Compose 실습에서는 `.env` 파일을 함께 사용하는 경우가 많습니다.

예:

```env
POSTGRES_DB=agent_db
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=change-me
```

주의할 점:

```text
.env 파일은 GitHub에 올리지 않습니다.
.env.example에는 실제 비밀번호 대신 예시 값만 넣습니다.
Docker Compose가 어떤 .env를 읽는지 항상 현재 폴더를 확인합니다.
```

## 8. 체크리스트

```text
[ ] Docker Desktop을 설치했다.
[ ] Docker Desktop이 실행 중이다.
[ ] docker --version이 동작한다.
[ ] docker compose version이 동작한다.
[ ] docker run hello-world가 성공했다.
[ ] Docker 실습 전에 포트 충돌 가능성을 확인할 수 있다.
```
