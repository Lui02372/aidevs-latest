# Docker 첫 사용 가이드

이 문서는 Docker를 처음 사용하는 학생을 위한 준비 단계입니다. 목표는 Docker를
모두 배우는 것이 아니라, 이 과정의 Ollama·PostgreSQL·Redis를 안전하게
시작하고 상태를 확인할 수 있는 정도까지 익히는 것입니다.

## 1. 무엇을 설치하나요?

Windows에는 **Docker Desktop 하나만 설치**합니다. Ollama, PostgreSQL, Redis는
Windows 프로그램으로 각각 설치하지 않고 Linux Container로 실행합니다.

1. [Docker Desktop Windows 설치 안내](https://docs.docker.com/desktop/setup/install/windows-install/)를 확인합니다.
2. PowerShell에서 `wsl --version`을 실행해 WSL 상태를 확인합니다.
3. WSL 업데이트가 필요하면 관리자 PowerShell에서 `wsl --update`를 실행합니다.
4. Docker Desktop을 설치하고 직접 실행합니다.
5. Docker Desktop이 Linux Container를 사용하고 있는지 확인합니다.

교육장 PC에서 가상화나 관리자 권한이 제한되어 설치할 수 없다면 Mock 예제를 먼저
진행합니다. Docker 설치 문제 때문에 `01`~`03`의 핵심 학습을 멈출 필요는 없습니다.

## 2. Image와 Container를 비유로 이해하기

```text
Image       실행 환경을 만드는 설계도
Container   설계도로 만든 실제 실행 공간
Port        Windows와 Container를 잇는 출입구
Volume      Container를 교체해도 남는 데이터 보관함
```

Image 하나로 여러 Container를 만들 수 있습니다. Container를 중지하는 것은
프로그램을 끄는 것과 비슷하며, Container나 Volume을 삭제하는 것과 다릅니다.

## 3. `docker run` 한 줄 읽기

이 과정에서 사용할 Redis 명령을 예로 봅니다.

```powershell
docker run -d `
  --name aidevs-redis `
  -p 6379:6379 `
  -v aidevs-redis-data:/data `
  redis:7 `
  redis-server --appendonly yes
```

| 부분 | 의미 |
| --- | --- |
| `docker run` | Image로 새 Container를 만들고 시작 |
| `-d` | 터미널 뒤에서 실행 |
| `--name aidevs-redis` | 사람이 읽기 쉬운 Container 이름 지정 |
| `-p 6379:6379` | `Windows Port:Container Port` 연결 |
| `-v aidevs-redis-data:/data` | Named Volume을 Container의 데이터 폴더에 연결 |
| `redis:7` | 사용할 Image와 Tag |
| 마지막 부분 | Container 안에서 실행할 명령 |

PowerShell의 줄 끝 `` ` ``은 다음 줄까지 하나의 명령이라는 뜻입니다. 뒤에 공백을
붙이면 줄 연결이 실패할 수 있으므로, 문제가 생기면 README의 명령을 다시 복사합니다.

## 4. Container의 생애주기

`docker run`은 **처음 한 번만** 사용합니다. 같은 이름의 Container가 이미 있으면
새로 만들지 말고 다시 시작합니다.

```powershell
docker ps
docker ps -a
docker stop aidevs-redis
docker start aidevs-redis
docker logs aidevs-redis
```

```text
docker run → 생성 + 시작
docker stop → 중지
docker start → 기존 Container 재시작
docker rm → Container 삭제
```

`docker ps`는 실행 중인 것만, `docker ps -a`는 중지된 Container까지 보여 줍니다.
명령이 실패하면 바로 삭제하지 말고 `docker ps -a`와 `docker logs`부터 확인합니다.

## 5. 무엇을 지워도 되나요?

| 명령 | 결과 | 이 과정의 기본 사용 |
| --- | --- | --- |
| `docker stop <이름>` | 실행만 중지, 데이터 유지 | 사용함 |
| `docker start <이름>` | 기존 Container 재시작 | 사용함 |
| `docker rm <이름>` | Container 삭제 | 원인을 확인한 뒤 사용 |
| `docker volume rm <이름>` | 저장 데이터 삭제 | 일반 실습에서는 사용하지 않음 |
| `docker system prune` | 여러 미사용 자원을 한꺼번에 정리 | 수업에서는 사용하지 않음 |

Container를 삭제해도 Named Volume이 남아 있으면 데이터를 다시 연결할 수 있습니다.
하지만 Volume을 삭제하면 PostgreSQL 데이터와 다운로드한 Ollama 모델 등이 사라질 수
있습니다. 삭제 명령은 이름과 보존할 데이터를 확인한 뒤 실행합니다.

## 6. 이번 과정과 다음 과정의 경계

```text
현재 05 과정
docker run → Container 하나씩 이해 → Python에서 연결

후속 운영 과정
Dockerfile → Docker Compose → 여러 서비스 연결 → AWS EC2 배포
```

이번 과정에서 Docker Compose를 먼저 외울 필요는 없습니다. Image, Container,
Port, Volume, 로그를 이해하면 나중에 Compose 파일이 여러 `docker run` 설정을
한곳에 기록한 것이라는 점을 자연스럽게 이해할 수 있습니다.

## 다음 단계

[Docker 상태 확인](./01_docker-health-check.md)을 진행한 뒤 가장 가벼운 Redis부터
직접 실행합니다.
