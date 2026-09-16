# Docker Redis

## 실행

```powershell
docker run -d `
  --name aidevs-redis `
  -p 6379:6379 `
  redis:7 `
  redis-server --appendonly yes
```

다음 수업부터는 새로 만들지 않고 기존 Container를 시작합니다.

```powershell
docker start aidevs-redis
docker ps --filter "name=aidevs-redis"
```

## 연결 확인

```powershell
docker exec -it aidevs-redis redis-cli PING
```

예상 결과:

```text
PONG
```

## TTL 실습

```powershell
docker exec -it aidevs-redis redis-cli SETEX agent:session:demo 60 active
docker exec -it aidevs-redis redis-cli TTL agent:session:demo
docker exec -it aidevs-redis redis-cli GET agent:session:demo
```

`SETEX`의 `60`은 60초 뒤 Key가 자동 삭제된다는 뜻입니다. `TTL`은 남은 시간을
초 단위로 보여 주며, `-2`는 Key가 없고 `-1`은 만료 시간이 없다는 뜻입니다.

## 중지와 데이터 유지 확인

```powershell
docker exec -it aidevs-redis redis-cli SET course:persist-demo saved
docker stop aidevs-redis
docker start aidevs-redis
docker exec -it aidevs-redis redis-cli GET course:persist-demo
```

예상 결과가 `saved`라면 AOF 설정과 `aidevs-redis-data` Volume을 통해 데이터가
유지된 것입니다. 학습을 마치면 테스트 Key만 삭제합니다.

```powershell
docker exec -it aidevs-redis redis-cli DEL course:persist-demo
```

## Key 규칙

```text
agent:session:{user_id}:{session_id}
agent:run:{run_id}
agent:cache:{provider}:{prompt_hash}
```

사용자별 Prefix와 TTL을 적용합니다. Redis를 장기 보존이 필요한 사용자 데이터의 유일한 저장소로 사용하지 않습니다.

이 설정에는 비밀번호가 없으므로 로컬 학습용으로만 사용하고 외부 네트워크에
공개하지 않습니다.
