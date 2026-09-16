# Runtime and Deployment 학습 요약

작성 기준: 2026-09-16, 이 폴더의 실제 Compose와 Docker 실행 상태.

## 1. 이번 오류와 해결

`docker compose up -d`가 올바른 명령이다. `-d`는 백그라운드 실행이다.
`Bind for 0.0.0.0:6379 failed: port is already allocated`는 PC의 6379 포트를 이미 다른 컨테이너가 사용한다는 뜻이다. 이미지 다운로드 실패가 아니다.

확인한 점유자는 `mini_agent_09_integrated_llm_lab-redis-1`이다. 기존 `ollama`도 11434를 사용한다. 기존 프로젝트의 Redis를 중지하면 그 프로젝트가 고장 날 수 있어 수업용 Redis의 PC 포트만 분리했다.

| 대상 | 현재 연결 | 처리 |
| --- | --- | --- |
| 기존 Mini Agent Redis | PC 6379 | 유지 |
| 수업용 `multi-agent-redis` | PC 6380 → 컨테이너 6379 | `.env`에서 설정 |
| 수업용 `multi-agent-postgres` | PC 5433 → 컨테이너 5432 | 유지 |
| 기존 `ollama` | PC 11434 | 기존 서버 사용 |
| 중복 `multi-agent-ollama` | 생성만 됨, 실행 실패 | 컨테이너만 제거, 이미지·볼륨 보존 |

`docker-compose.yml`의 Redis 공개 포트를 `${REDIS_HOST_PORT:-6379}:6379`로 바꾸었다. 이 PC의 `.env`에는 `REDIS_HOST_PORT=6380`, `REDIS_URL=redis://127.0.0.1:6380/0`을 적용했다. 다른 PC에서 변수를 지정하지 않으면 원래 6379를 사용한다.

Ollama에는 선택 profile을 적용했다. 이제 기본 `up -d`는 Redis·PostgreSQL만 실행한다. 기존 Ollama가 있는 이 PC에서는 `up -d ollama`를 실행하지 않는다. 기존 서버가 없는 PC에서는 서비스를 명시해서 실행할 수 있다.

## 2. 먼저 실행할 명령

PowerShell에서 경로는 공백이 있으므로 따옴표로 감싼다. 실제 폴더명은 `07_multi-agent-service-ops`와 `00_runtime-and-deployment`이다.

```powershell
cd 'C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\00_local-services'
docker compose config --quiet
docker compose up -d redis postgres
docker compose ps
docker compose exec redis redis-cli ping
docker compose exec postgres pg_isready -U agent_user -d agent_db
```

정상 기준: 두 서비스 `healthy`, Redis `PONG`, PostgreSQL `accepting connections`. DB 사용자·DB 이름을 별도로 변경했다면 검사 명령도 그 값으로 맞춘다. 컨테이너가 생성되었다는 출력만으로 전체 실행 성공을 판단하지 않는다.

```powershell
# 실패 원인 확인
docker compose logs --tail=100 redis postgres
# 기존 모델 확인: 다운로드·삭제하지 않는다
docker exec ollama ollama list
# 데이터 유지하고 일시 중지 / 재개
docker compose stop
docker compose start
```

기존 `.env`를 `.env.example`로 덮어쓰면 이번 6380 설정이 사라진다. 예제 복사는 `.env`가 없을 때만 한다.

## 3. 폴더별 배울 내용

### PostgreSQL 18과 예제 16, pgAdmin의 관계

이 PC의 pgAdmin 기존 등록에는 Windows PostgreSQL 18(5432), VectorDB(15432)가 있다.
수업용 Docker PostgreSQL은 별도 서버인 16.15(5433)이다. 버전이 달라도 포트와 데이터 위치가 분리되어 공존한다.
PostgreSQL 18에 포함된 pgAdmin 4는 관리 도구이며, 수업용 PostgreSQL 16에도 접속할 수 있다.
이번에는 버전 변경이나 기존 DB 마이그레이션을 하지 않았다.

수업용 pgAdmin 등록 파일은 `00_local-services/pgadmin-servers.json`이다.
표시 이름은 `AIDevs Course → Course 00 - Docker PostgreSQL 16`, 주소는 `127.0.0.1:5433`, DB는 `agent_db`, 사용자는 `agent_user`다.
가져오기 파일에는 비밀번호를 저장하지 않았다. 접속 시 DB 비밀번호를 물으면 예제의 `agent_pwd`를 입력한다.
pgAdmin의 Master Password를 물으면 사용자 본인이 설정한 pgAdmin 마스터 비밀번호이며 DB 비밀번호와 별개다.

`init_database.py` 실행을 완료했고 pgvector 확장 및 `task_runs`, `task_events`, `handoff_events`, `learning_runs`, `learning_events` 테이블을 확인했다.
pgAdmin에서 `agent_db → Schemas → public → Tables`를 펼치면 된다.

| 폴더·파일 | 이해할 내용 | 진행 시점 |
| --- | --- | --- |
| `00_windows-docker-setup.md` | Windows Docker 실행 환경과 설치 확인 | 처음 |
| `00_local-services` | 공용 PostgreSQL·Redis, 선택 Ollama와 볼륨 | 지금 |
| `01_simple-multi-llm-compose` | Streamlit → FastAPI → LLM·저장소 연결 | 저장소 확인 후 |
| `01_simple-multi-llm-compose2` | 유사한 앱 구성과 배포 파일 비교 | 선택 참고 |
| `01_simple-multi-llm-compose3` | 유사한 full-stack·release 구성 비교 | 선택 참고 |
| `02_github-actions-ci` | 테스트·빌드·설정 검사를 자동 실행하는 CI | 앱 동작 이해 후 |
| `03_aws-ec2` | 원격 서버 준비, 수동 배포, 장애 확인·정리 | 로컬 성공 후 |
| `04_github-actions-aws-deploy` | CI 이후 원격 배포 자동화 | 수동 배포 후 |
| `05_weather-mcp-deployment-project` | Frontend·Backend·Weather MCP 연결과 배포 | 확장 실습 |
| `06_weather-mcp-stateful-deployment` | 저장소와 애플리케이션의 배포 수명 분리 | 데이터 유지 학습 |
| `05_local-or-managed-cloud.md` | 실행 위치별 선택지 비교 | 참고 |
| `06_to-integrated-operations.md` | 09 통합 운영으로 연결 | 후반 |
| `LEARNING_SEQUENCE.md` | 과정 전체에서 Docker·CI/CD를 배울 순서 | 전체 안내 |

`01...`, `01...2`, `01...3`을 동시에 실행할 필요는 없다. 특히 일부 프로젝트 이름·공개 포트가 겹친다. `compose3`에는 실제로 기본 `compose.yml`이 없고 full-stack·release 파일이 있으므로 README의 기본 명령을 그대로 실행하지 말고 실제 파일을 확인한다.

첫날에는 저장소 준비까지 하면 된다. 이 폴더 자체가 완성된 Multi-Agent 시스템은 아니다. 이후 과정에서 Agent·Orchestration을 배우고 08의 서비스, 09의 운영으로 확장한다.

## 4. Docker에서 반드시 구분할 것

| 용어 | 의미 | 이 실습의 예 |
| --- | --- | --- |
| Image | 실행 파일·의존성을 묶은 재사용 원본 | `redis:7-alpine` |
| Container | 이미지를 실행하는 개별 인스턴스 | `multi-agent-redis` |
| Volume | 컨테이너 교체 후에도 남기는 데이터 | PostgreSQL 데이터·Ollama 모델 |
| Network | 컨테이너 사이 통신 공간 | Compose 기본 네트워크 |
| Compose | 여러 서비스의 이미지·포트·볼륨·환경 변수를 선언 | `docker-compose.yml` |
| Dockerfile | 앱 이미지를 만드는 방법 | `backend/Dockerfile` |

포트 `6380:6379`에서 왼쪽은 **PC 포트**, 오른쪽은 **컨테이너 포트**다. 같은 PC 포트를 두 서비스가 동시에 차지할 수 없다. 서로 다른 컨테이너의 내부 6379는 공존할 수 있다.

```text
PC에서 실행하는 Python → 127.0.0.1:6380 → 수업용 Redis:6379
다른 Compose의 Backend → host.docker.internal:6380 → 수업용 Redis:6379
같은 Compose 네트워크의 서비스 → redis:6379
```

컨테이너 안의 `localhost`는 그 컨테이너 자신이다. 다른 프로젝트의 Redis를 서비스 이름 `redis`만으로 찾을 수 있다고 가정하지 않는다.

## 5. 다음 앱 실습에 연결하기

`01_simple-multi-llm-compose/compose.yml`은 기본적으로 **Frontend·Backend만** 만들고 PC의 공용 저장소를 사용한다. 반면 `compose.full-stack.yml`은 저장소까지 별도로 만든다. 상위 README의 '01은 독립 네 Container' 설명보다 실행할 실제 Compose 파일을 기준으로 판단한다.

기본 앱을 실행할 때 해당 앱 폴더의 `.env`에 다음 Redis 주소를 설정한다. `00_local-services/.env`가 다른 폴더에 자동 전달되지는 않는다.

```dotenv
REDIS_URL=redis://host.docker.internal:6380/0
```

다른 과정의 Python을 PC에서 실행하면 그 과정의 `.env`에는 `redis://127.0.0.1:6380/0`을 사용한다. DB는 5433, 기존 Ollama는 11434를 사용한다. API 키·DB 자격 증명은 해당 앱의 안내에 따라 준비한다.

```powershell
# 00_local-services에서 이동
cd '..\01_simple-multi-llm-compose'
# 해당 앱의 .env 준비 후
docker compose config --quiet
docker compose up -d --build
docker compose ps
```

이 폴더의 실제 기본 화면 포트는 PC `80`이며 Backend는 `8000`이다. full-stack의 화면은 `8501`이다. 이번 작업에서는 앱 전체를 실행하거나 LLM 응답까지 검증하지 않았다.

`00_local-services/start-local-services.ps1`은 `aidevs-*`라는 다른 컨테이너를 `docker run`으로 만들고 포트 6379·5433·11434를 사용한다. 현재 Compose와 섞어 실행하면 충돌하므로 이번에는 Compose 명령만 사용한다.

## 6. 삭제가 안 되는 이유와 이번 정리 판단

이미지는 실행 중이거나 중지된 컨테이너가 참조하면 삭제가 막힐 수 있다. 중지된 컨테이너도 참조 관계가 남는다. 실행 중 컨테이너는 일반 `docker rm`으로 삭제되지 않는다. 볼륨은 컨테이너에 연결되어 있으면 삭제가 막힐 수 있다. 이번에 사용자가 본 삭제 오류 원문은 없으므로 개별 삭제 실패 이유는 확정하지 않았다.

| 확인한 항목 | 판단 |
| --- | --- |
| `educator-customer-lab-*` 컨테이너·이미지 | 중지 상태여도 사용자 프로젝트이므로 보존 |
| `educator-go:1.27.1`, `educator-typescript:7.0.2` | 컨테이너 참조는 없어도 교육 환경이 다시 사용할 수 있어 보존 |
| Mini Agent API·Redis, `vect-postgres`, 기존 `ollama` | 실행 중이므로 보존 |
| `simple-multi-llm-full-stack-*`, `project-player-course07-*` | 기존 실습과 데이터 연결이 있어 보존 |
| `trusting_archimedes` | 이름은 임의 이름이지만 실제로 기존 Streamlit 이미지 사용, 보존 |
| Docker Desktop·Kubernetes 이미지 | 플랫폼에서 사용하는 이미지이므로 보존 |
| 이번 생성 실패의 `multi-agent-ollama` | 한 번도 시작하지 못한 중복 컨테이너만 제거 |
| 모든 볼륨·이미지·빌드 캐시 | 이번에는 삭제하지 않음 |

조회 당시 이미지는 약 14.43GB, 볼륨은 7.26GB, 빌드 캐시는 2.547GB였다. 이미지 회수 가능 1.794GB는 educator 이미지에 해당하므로 '회수 가능 = 필요 없음'이 아니다. dangling 이미지도 없었다. Docker 내부 사용량 감소와 Windows 디스크 파일 크기 감소는 같지 않을 수 있다.

점검 명령은 읽기 전용이다.

```powershell
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker image ls
docker system df
docker ps --filter publish=6379
```

개별 항목을 지울 때는 소유 프로젝트 → 데이터·볼륨 → 재사용 여부 → 중지 → 컨테이너 제거 → 이미지 제거 순서로 판단한다. 컨테이너의 볼륨 밖 파일은 컨테이너를 지우면 사라진다. 현재는 불필요함이 확인되지 않은 대상을 추가로 삭제하지 않는다.

`docker system prune -a`, 전체 컨테이너 삭제, `docker compose down -v`, `docker volume prune -a`는 이 사용 목적에 맞지 않는다. 일반 `docker compose down`도 현재 프로젝트의 컨테이너를 제거하므로 일시 중지에는 `stop`을 사용한다.

Docker 공식 근거: [이미지 삭제와 컨테이너 참조](https://docs.docker.com/desktop/use-desktop/images/), [prune의 삭제 범위](https://docs.docker.com/engine/manage-resources/pruning/).
