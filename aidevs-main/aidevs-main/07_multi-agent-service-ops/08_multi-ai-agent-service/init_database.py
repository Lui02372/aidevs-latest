"""PostgreSQL에 Mini Multi-Agent 08 실행·Trace Schema를 준비합니다."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
database_url = os.getenv(
    "DATABASE_URL",
    "postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db",
)
sql = (ROOT / "schema.sql").read_text(encoding="utf-8")

with psycopg.connect(database_url) as database:
    database.execute(sql)

print("mini_multi_agent_08 실행·Trace Schema가 준비되었습니다.")
