# 05 장애 실습

한 번에 한 Container만 중단하고 `docker compose -f compose.full-stack.yml ps`와 로그로
영향 범위를 확인합니다.

## Backend 중단

```bash
docker compose -f compose.full-stack.yml stop backend
docker compose -f compose.full-stack.yml ps
```

Frontend는 열릴 수 있지만 Health·메모·Chat API는 연결 실패해야 합니다. 복구합니다.

```bash
docker compose -f compose.full-stack.yml start backend
curl --fail http://127.0.0.1:8000/health/ready
```

## Redis 중단

```bash
docker compose -f compose.full-stack.yml stop redis
```

Redis 통계와 현재 Session 오류를 확인합니다. PostgreSQL Container와 기존 영구 이력은
별도로 남아 있는지 비교한 뒤 복구합니다.

```bash
docker compose -f compose.full-stack.yml start redis
```

## PostgreSQL 중단

```bash
docker compose -f compose.full-stack.yml stop database
```

메모와 Chat 영구 이력 오류를 확인합니다. 복구 후 Volume의 기존 메모가 남았는지
확인합니다.

```bash
docker compose -f compose.full-stack.yml start database
```

## 서비스 주소 실수

Frontend Container의 올바른 Backend 주소는 `http://backend:8000`입니다.
`http://localhost:8000`은 Frontend Container 자기 자신을 뜻합니다.

## 로그

```bash
docker compose -f compose.full-stack.yml logs --tail=100 frontend
docker compose -f compose.full-stack.yml logs --tail=100 backend
docker compose -f compose.full-stack.yml logs --tail=100 redis
docker compose -f compose.full-stack.yml logs --tail=100 database
```

```text
[ ] 실패한 첫 서비스를 찾았다.
[ ] 영향받지 않은 저장소를 구분했다.
[ ] 오류를 성공으로 숨기지 않음을 확인했다.
[ ] 복구 후 Health와 데이터 유지 여부를 확인했다.
```

