# 기존 EC2 + PostgreSQL + GitHub Actions 실습

EC2 주소: `15.165.231.208`, SSH 사용자: `ec2-user`, OS: Amazon Linux 2023 x86_64.
SSH는 AWS 계정 ID가 아니라 서버 Linux 사용자명으로 로그인합니다.
키 위치: `C:\수업 보관소\aws Save\multi-agent-course.pem` (키 내용은 Git에 넣지 않습니다).
실제 확인한 DB는 EC2의 PostgreSQL 17 컨테이너, DB `agent_db`, 사용자 `agent_user`입니다.
pgAdmin에 보이는 `127.0.0.1:5432`는 Windows PC의 별도 DB입니다.
API/Worker/화면/MCP와 Redis만 배포합니다. 기존 PostgreSQL을 생성·삭제·교체하지 않습니다.

```text
GitHub push → 테스트 DB/Redis로 CI → 이미지 빌드 → SSH 전송 → EC2 앱 교체
내 PC → SSH 터널 → EC2 화면 → API → Redis → Worker → 실제 LLM/MCP
                              └──── 기존 PostgreSQL 작업/Trace 이력
```

## 1. EC2 최초 준비

Linux x86_64 서버, Docker Engine, Compose v2(`up --wait` 지원), Bash/curl/flock이 필요합니다.
SSH 사용자로 `docker ps`, `docker compose version`, `uname -m`을 실행해 권한과 아키텍처를 확인합니다.
기존 앱의 8000/8501 포트를 유지하고 09 API/화면은 localhost의 18000/18501을 사용합니다.

```bash
mkdir -p ~/multi-agent-09/shared
chmod 700 ~/multi-agent-09/shared
```

이 폴더의 `.env.example`을 EC2 `~/multi-agent-09/shared/app.env`로 복사하고 실제 DB URL과
OPENAI_API_KEY, 사용 가능한 모델을 입력합니다. `chmod 600 ~/multi-agent-09/shared/app.env`를 실행합니다.
비밀값은 EC2에만 보관합니다. 기본 Agent는 전부 OpenAI이며 Ollama 서버는 배포하지 않습니다.

| 기존 DB 위치 | DATABASE_URL의 호스트 |
| --- | --- |
| RDS/다른 EC2 | 접근 가능한 private DNS/IP. TLS 필요 시 sslmode=require 추가 |
| 같은 EC2 호스트/호스트 포트를 공개한 DB 컨테이너 | host.docker.internal:호스트포트 |
| 내 PC | localhost 사용 불가. VPN/사설 연결 또는 EC2/RDS로 데이터 이전 필요 |

컨테이너의 localhost는 앱 자신입니다. 같은 EC2 DB가 127.0.0.1에만 바인딩되어 있으면 Docker에서
접근할 수 없습니다. PostgreSQL listen_addresses/pg_hba.conf와 방화벽에서 실제 Docker 대역을 허용합니다.
RDS는 EC2 보안 그룹에서 DB 포트에 접근하도록 설정합니다. DB를 전체 인터넷에 공개하지 않습니다.
비밀번호의 @/:/#/% 등은 URL 인코딩합니다. 기존 DB명·계정을 사용합니다.

이 EC2에서는 DB 포트를 호스트에 공개하지 않고 기존 Docker 네트워크로 접속합니다.
`compose.existing-db.example.yaml`을 `~/multi-agent-09/shared/compose.override.yaml`로 두면
deploy.sh가 자동 반영합니다. DATABASE_URL의 호스트는 기존 네트워크의 `database`, 포트는 5432입니다.
기존 DB 컨테이너와 네트워크를 제거하면 09도 연결되지 않습니다.

`08_multi-ai-agent-service/schema.sql`을 DB 도구(psql/DBeaver 등)에서 대상 DB에 최초 한 번 실행합니다.
전용 mini_multi_agent_08 스키마·테이블·인덱스를 IF NOT EXISTS로 추가하며 기존 행을 지우지 않습니다.
기존 테이블 구조를 바꾸는 마이그레이션은 아닙니다. 앱 계정에 스키마·테이블·sequence 접근 권한을 줍니다.
DB 백업은 별도로 유지합니다. 매 배포에서는 스키마를 수정하지 않고 연결/쓰기/읽기만 검사합니다.

## 2. GitHub 활성화

Git 저장소 루트는 현재 수업 폴더보다 세 단계 위입니다. GitHub는 저장소 루트의
`.github/workflows/*.yml`만 실행합니다. `deploy/github/ec2-ci-cd.yml`을 루트의
`.github/workflows/09-ec2-ci-cd.yml`로 복사합니다. COURSE는 현재 저장소 구조인
`aidevs-main/aidevs-main/07_multi-agent-service-ops`이며 폴더 구조가 바뀌면 수정합니다.

Settings → Environments → `ec2-learning`에서 설정합니다.

| 종류 | 이름 | 값 |
| --- | --- | --- |
| Variable | EC2_HOST | 15.165.231.208 |
| Variable | EC2_USER | 실제 SSH 사용자. Ubuntu는 보통 ubuntu, Amazon Linux는 ec2-user |
| Secret | EC2_SSH_KEY | SSH 개인키 전체. 채팅/커밋에 넣지 않음 |
| Secret | EC2_KNOWN_HOSTS | 검증한 서버 SSH 공개 호스트키 라인 |

ssh-keyscan 결과는 수집용입니다. EC2 콘솔 등 신뢰할 수 있는 경로의
`ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` 지문과 비교한 뒤 known_hosts를 등록합니다.
GitHub runner에서 EC2 SSH 포트에 접근할 수 있어야 합니다. IP 제한이 있으면 고정 출구 IP runner/VPN을
준비합니다. 내 PC에서 SSH 된다고 runner에서도 된다는 뜻은 아닙니다.

PR은 CI만 실행합니다. main push는 CI 후 자동 배포합니다. 준비 중에는 Environment 승인자를 설정합니다.
Actions → `09 EC2 CI CD` → Run workflow에서 deploy를 끄면 CI만, main에서 켜면 배포까지 실행합니다.
로컬 파일만으로 활성화되지 않습니다. workflow를 GitHub에 push한 뒤 Actions에 표시되는지 확인합니다.

## 3. 학습 순서

1. CI를 실행하고 테스트용 실제 PostgreSQL/Redis에 API가 작업과 Trace를 저장·조회하는지 확인합니다.
2. EC2 app.env와 DB 스키마를 준비하고 수동 배포를 실행합니다.
3. 내 PC에서 실제 키 경로와 SSH 사용자로 터널을 엽니다.

```powershell
ssh -i "C:\수업 보관소\aws Save\multi-agent-course.pem" -L 18501:127.0.0.1:18501 -L 18000:127.0.0.1:18000 ec2-user@15.165.231.208
```

화면은 http://127.0.0.1:18501, API 문서는 http://127.0.0.1:18000/docs 입니다.
화면에서 여행 요청을 실행하고 DB에서 결과를 확인합니다.

```sql
SELECT task_id, user_id, status, created_at
FROM mini_multi_agent_08.travel_task_runs ORDER BY created_at DESC LIMIT 10;
SELECT task_id, actor, action, status
FROM mini_multi_agent_08.travel_trace_events ORDER BY event_id DESC LIMIT 20;
```

4. 작은 변경을 main에 push하고 Actions 성공, EC2의 `cat ~/multi-agent-09/shared/current`,
   기존 DB 행 보존을 확인합니다. Redis 상태는 TTL 후 사라질 수 있지만 PostgreSQL 이력은 남습니다.
5. 테스트 브랜치의 assertion을 일부러 실패시켜 CI 실패를 확인하고 복구합니다. 실제 DB를 끊을 필요는 없습니다.

CI는 실제 LLM을 호출하지 않습니다. LLM 성공은 API Key를 넣고 화면에서 별도로 확인합니다.
DB probe는 rollback하여 행을 남기지 않지만 sequence 번호는 증가할 수 있습니다.

## 4. 운영과 복구

EC2에서 다음을 실행합니다.

```bash
cd ~/multi-agent-09
export APP_ENV_FILE="$HOME/multi-agent-09/shared/app.env"
sha=$(cat shared/current)
export APP_IMAGE="multi-agent-09:$sha"
docker compose -p multi-agent-09 -f "releases/$sha/compose.yaml" -f shared/compose.override.yaml ps
docker compose -p multi-agent-09 -f "releases/$sha/compose.yaml" -f shared/compose.override.yaml logs --tail 80 worker
# 이전 성공 SHA로 수동 복구:
bash releases/PREVIOUS_FULL_SHA/deploy.sh PREVIOUS_FULL_SHA
```

DB 사전 검사 실패는 기존 앱을 유지합니다. 앱 교체 후 readiness/화면/DB 검사 실패는 이전 성공 이미지와
Compose로 복구를 시도하며 Actions는 실패로 남습니다. 첫 배포에는 복구할 이전 버전이 없습니다.
앱 복구는 DB 데이터를 되돌리지 않습니다. Worker/MCP는 프로세스 기동만 검사하며 실제 작업은 화면에서 확인합니다.
실행 중 작업의 무중단 처리는 보장하지 않으므로 큐가 비었을 때 배포합니다.
Redis 볼륨을 삭제하는 down -v는 사용하지 않습니다. 이미지/releases가 쌓이므로 이전 성공 버전을 보존하며 디스크를 관리합니다.
이 실습의 user_id는 인증이 아닙니다. localhost 바인딩과 SSH 터널을 유지하고 공개 서비스는 인증/TLS를 별도 구성합니다.
