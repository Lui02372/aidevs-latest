# 04 배포와 Health 확인

## 1. 현재 위치 확인

```bash
pwd
ls
```

현재 폴더에 `backend`, `frontend`, `database`, `compose.full-stack.yml`, `.env`가 있어야 합니다.

## 2. Compose 검사

```bash
docker compose -f compose.full-stack.yml config --quiet
```

오류가 있으면 Build 전에 경로와 YAML을 수정합니다.

## 3. Image Build와 백그라운드 실행

```bash
docker compose -f compose.full-stack.yml up --build -d
```

`-d`는 SSH 터미널을 계속 점유하지 않고 백그라운드로 실행합니다.

## 4. Container 상태

```bash
docker compose -f compose.full-stack.yml ps
```

기대 서비스:

```text
backend
frontend
redis
database
```

Backend는 Health Check를 통과해야 하고 Frontend는 실행 상태여야 합니다.

## 5. EC2 내부 Health 확인

```bash
curl --fail http://127.0.0.1:8000/health/ready
```

기대 응답:

```json
{"status":"ok","checks":{"backend":true,"redis":true,"database":true,"database_schema":true,"providers":{...}}}
```

Frontend가 응답하는지 확인합니다.

```bash
curl -I http://127.0.0.1:8501
```

## 6. 브라우저 확인

로컬 브라우저에서 다음 주소를 엽니다.

```text
http://<EC2_PUBLIC_IPV4>:8501
```

화면에서 메모 저장과 Multi-LLM 여행 Chat 응답을 확인합니다.

Backend 주소 8000은 Security Group에 공개하지 않았으므로 다음 주소는 외부
브라우저에서 접근되지 않아야 합니다.

```text
http://<EC2_PUBLIC_IPV4>:8000
```

## 7. 로그 확인

전체 로그:

```bash
docker compose -f compose.full-stack.yml logs
```

최근 Backend 로그:

```bash
docker compose -f compose.full-stack.yml logs --tail=50 backend
```

최근 Frontend 로그:

```bash
docker compose -f compose.full-stack.yml logs --tail=50 frontend
```

Redis와 PostgreSQL 로그:

```bash
docker compose -f compose.full-stack.yml logs --tail=50 redis
docker compose -f compose.full-stack.yml logs --tail=50 database
```

실시간 로그를 중단할 때는 Container를 중단하지 말고 `Ctrl+C`로 로그 보기만
종료합니다.

## 8. 재부팅 후 주의

EC2를 중지·시작하면 Public IPv4가 바뀔 수 있습니다. Elastic IP를 사용하지 않는
이번 실습에서는 Console에서 새 주소를 확인합니다. Compose 서비스의 자동 시작
정책은 이번 최소 실습 범위에 포함하지 않으므로 재부팅 후 필요하면 다시
실행합니다.

```bash
cd ~/simple-compose
docker compose -f compose.full-stack.yml up -d
```


