# 공통 오류

## 확인 순서

```text
현재 폴더
→ 가상환경
→ Python 실행 경로
→ requirements 설치
→ .env 위치
→ APP_MODE
→ Backend URL
→ 요청·응답 Schema
→ trace_id
```

## Agent가 종료되지 않을 때

- `iteration`이 증가하는지 확인합니다.
- `max_iterations`를 검사하는 분기가 있는지 확인합니다.
- 모든 조건 경로가 종료 또는 사용자 입력 대기로 연결되는지 확인합니다.

## Tool이 잘못 호출될 때

- Tool 이름과 설명이 겹치지 않는지 확인합니다.
- 입력 Schema의 필수 필드를 확인합니다.
- Tool 선택 결과와 실행 코드를 분리해 출력합니다.

## 실제 LLM 연결이 실패할 때

먼저 `APP_MODE=mock`으로 전체 흐름을 확인합니다. 그 후 API Key, 모델명, 네트워크, 사용량 제한을 확인합니다.

## Docker 서비스가 연결되지 않을 때

다음 순서로 한 단계씩 확인합니다.

```text
Docker Desktop 실행 여부
→ Linux Container 모드
→ docker info
→ docker ps -a
→ Container 상태
→ docker logs <container-name>
→ Host Port 충돌
→ Docker Volume
→ .env 연결 주소
```

```powershell
docker ps -a
docker logs aidevs-redis
docker logs aidevs-pgvector
docker logs aidevs-ollama
```

`docker ps`에는 실행 중인 Container만 표시됩니다. 중지된 Container까지 보려면
`docker ps -a`를 사용합니다. Container를 삭제하기 전에는 Volume에 보존해야 할
실습 데이터가 있는지 먼저 확인합니다.

## Docker 오류 메시지별 첫 확인

| 오류·증상 | 뜻 | 먼저 할 일 |
| --- | --- | --- |
| Docker daemon에 연결할 수 없음 | CLI는 있지만 Engine이 준비되지 않음 | Docker Desktop 실행 후 `docker info` |
| Container name이 이미 사용 중 | 같은 이름의 중지된 Container가 있음 | `docker ps -a`, 필요하면 `docker start <이름>` |
| Port가 이미 할당됨 | Host Port를 다른 프로세스가 사용 중 | 아래 Port 확인 명령 실행 |
| Container가 바로 종료됨 | 내부 서비스 시작 실패 | `docker logs <이름>` |
| Image를 가져오지 못함 | 네트워크·프록시·Registry 문제 가능 | 오류 원문과 네트워크 확인 |
| WSL 관련 오류 | WSL 또는 가상화 준비 문제 | `wsl --version`, 필요하면 `wsl --update` |

이름 충돌을 해결하려고 기존 Container부터 삭제하지 않습니다. 과정에서 만든
`aidevs-*` Container라면 대부분 `docker start <이름>`으로 다시 사용할 수 있습니다.

## `localhost`로 연결되지 않을 때

실행 위치에 따라 주소가 달라집니다.

| 호출 위치 | 연결 주소 예 |
| --- | --- |
| Windows에서 실행한 Python | `127.0.0.1:5433`, `127.0.0.1:6379` |
| 같은 Docker Compose 안의 Container | `postgres:5432`, `redis:6379` |

Container 안의 `localhost`는 Windows Host나 다른 Container가 아니라 그
Container 자신을 의미합니다. `05`의 `docker run` 실습에서는 Host Port로
연결하고, 후속 `07_multi-agent-service-ops`의 Docker Compose에서는 서비스 이름과
내부 Port로 연결합니다.

## 포트 충돌이 발생할 때

```powershell
Get-NetTCPConnection -State Listen |
    Where-Object LocalPort -In 11434,5433,6379,8000,8001,8501
```

이미 사용 중인 Port의 프로세스나 Container를 먼저 확인합니다. 원인을 모른 채
프로세스를 강제 종료하지 않습니다.

## 삭제 명령 주의

```text
docker stop             실행만 중지
docker rm               Container 삭제
docker volume rm        저장 데이터 삭제
docker system prune     여러 미사용 자원을 일괄 정리
```

수업의 정상 종료는 `docker stop`입니다. `docker volume rm`과
`docker system prune`은 데이터 범위를 설명할 수 있을 때만 사용합니다.
