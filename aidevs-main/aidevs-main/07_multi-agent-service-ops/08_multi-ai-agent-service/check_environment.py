"""08 서비스 실행 전 Redis와 PostgreSQL 연결·Schema를 확인합니다."""

from app.repositories import PostgresHistory, RedisTasks


for name, repository in (("Redis", RedisTasks()), ("PostgreSQL", PostgresHistory())):
    try:
        print("OK  ", name, repository.ping())
    except Exception as error:
        print("FAIL", name, f"{type(error).__name__}: {error}")
