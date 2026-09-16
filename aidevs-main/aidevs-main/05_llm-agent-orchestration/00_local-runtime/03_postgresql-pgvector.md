# Docker PostgreSQL과 pgvector

## 실행

아래 비밀번호는 외부에 공개하지 않는 **로컬 수업 전용 값**입니다. 실제 서비스는
강한 비밀번호와 Secret 관리, 접근 제어를 별도로 적용해야 합니다.

```powershell
docker run -d `
  --name aidevs-pgvector `
  -p 5433:5432 `
  -e POSTGRES_DB=agent_db `
  -e POSTGRES_USER=agent_user `
  -e POSTGRES_PASSWORD=agent_pwd `
  -v aidevs-pgvector-data:/var/lib/postgresql/data `
  pgvector/pgvector:pg16
```

다음 수업부터는 기존 Container를 시작하고 준비 상태를 확인합니다.

```powershell
docker start aidevs-pgvector
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
```

예상 결과에 `accepting connections`가 표시되면 연결할 준비가 된 것입니다.

## 연결과 Schema

먼저 pgvector extension을 만들고 확인합니다.

```powershell
docker exec -it aidevs-pgvector `
  psql -U agent_user -d agent_db `
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

```powershell
docker exec -it aidevs-pgvector `
  psql -U agent_user -d agent_db `
  -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

Python Schema 적용:

```powershell
python .\00_local-runtime\database\apply_schema.py
```

이 명령은 과정 루트의 `.env`에 있는 `DATABASE_URL`을 사용합니다. 실행 전에
가상환경, `pip install -r requirements.txt`, `.env` 복사를 완료해야 합니다.

테이블 확인:

```powershell
docker exec -it aidevs-pgvector `
  psql -U agent_user -d agent_db `
  -c "\dt"
```

## 역할

- `documents`: RAG Chunk와 Embedding
- `user_memories`: 사용자 장기 선호
- `conversation_messages`: 대화 이력
- `agent_runs`: Agent 실행 결과

서로 다른 Embedding 모델의 Vector는 같은 collection에서 비교하지 않습니다.

## Volume 확인 실습

```powershell
docker stop aidevs-pgvector
docker start aidevs-pgvector
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
```

재시작한 뒤에도 테이블이 남는 이유는 `aidevs-pgvector-data` Volume을 사용하기
때문입니다. 일반 종료 과정에서 이 Volume을 삭제하지 않습니다.
