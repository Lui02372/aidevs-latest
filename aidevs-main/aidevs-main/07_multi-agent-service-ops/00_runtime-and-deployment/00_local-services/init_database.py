"""
[Database 초기화 시나리오]
PostgreSQL Container는 이미 실행 중이지만 과정에서 사용할 Table과 pgvector Extension이
아직 준비되지 않았습니다. 이 프로그램은 같은 폴더의 `.env`에서 `DATABASE_URL`을 읽고
`init.sql`을 PostgreSQL에 실행합니다.

`init.sql`은 `CREATE ... IF NOT EXISTS`를 사용하므로 기존 Table을 삭제하거나 데이터를
초기화하지 않습니다. 연결 실패, 인증 실패 또는 SQL 오류는 성공으로 바꾸지 않고 그대로
출력합니다. 이 파일은 Container를 생성하거나 제거하지 않으며 Database 구조만 준비합니다.
"""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
SQL_PATH = ROOT / "init.sql"
DEFAULT_DATABASE_URL = (
    "postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db"
)


def load_database_url() -> str:
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)
        print(f"환경 설정 파일: {ENV_PATH}")
    else:
        print(".env가 없어 과정 기본 DATABASE_URL을 사용합니다.")
        print("필요하면 먼저 Copy-Item .env.example .env를 실행하세요.")
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def initialize_database(database_url: str) -> None:
    if not SQL_PATH.exists():
        raise FileNotFoundError(f"SQL 파일을 찾을 수 없습니다: {SQL_PATH}")

    sql = SQL_PATH.read_text(encoding="utf-8")
    print(f"실행할 SQL 파일: {SQL_PATH}")
    print("PostgreSQL에 연결하고 Schema를 준비합니다.")

    with psycopg.connect(database_url) as connection:
        connection.execute(sql)
        extension = connection.execute(
            "SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')"
        ).fetchone()[0]
        tables = connection.execute(
            """SELECT table_name
               FROM information_schema.tables
               WHERE table_schema = 'public'
                 AND table_name IN (
                     'task_runs', 'handoff_events', 'task_events',
                     'learning_runs', 'learning_events'
                 )
               ORDER BY table_name"""
        ).fetchall()

    print("Database 초기화가 완료되었습니다.")
    print(f"pgvector Extension: {'준비됨' if extension else '확인 필요'}")
    print("확인된 과정 Table:")
    for table in tables:
        print(f"- {table[0]}")
    print("기존 Table과 데이터는 삭제하지 않았습니다.")


def main() -> None:
    database_url = load_database_url()
    initialize_database(database_url)


if __name__ == "__main__":
    main()
