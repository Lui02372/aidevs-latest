"""Local Docker와 Cloud Provider 환경을 한 번에 확인합니다."""

import os
import socket

import httpx
import psycopg
import redis
from dotenv import load_dotenv


load_dotenv()


def check_port(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False


def check_ollama() -> tuple[bool, str]:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    try:
        response = httpx.get(f"{base_url.rstrip('/')}/api/tags", timeout=3)
        response.raise_for_status()
        models = [item["name"] for item in response.json().get("models", [])]
        return True, ", ".join(models) if models else "모델이 없습니다."
    except Exception as error:
        return False, str(error)


def check_postgres() -> tuple[bool, str]:
    try:
        with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=3) as connection:
            version = connection.execute(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            ).fetchone()
        return bool(version), f"pgvector={version[0]}" if version else "pgvector 미설치"
    except Exception as error:
        return False, str(error)


def check_redis() -> tuple[bool, str]:
    try:
        client = redis.from_url(os.environ["REDIS_URL"], socket_connect_timeout=3)
        return bool(client.ping()), "PONG"
    except Exception as error:
        return False, str(error)


def show(name: str, result: tuple[bool, str]) -> None:
    success, detail = result
    print(f"{name:<24} {'OK' if success else 'FAIL'}  {detail}")


if __name__ == "__main__":
    print("Local ports")
    print(f"{'Ollama 11434':<24} {'OPEN' if check_port('127.0.0.1', 11434) else 'CLOSED'}")
    print(f"{'PostgreSQL 5433':<24} {'OPEN' if check_port('127.0.0.1', 5433) else 'CLOSED'}")
    print(f"{'Redis 6379':<24} {'OPEN' if check_port('127.0.0.1', 6379) else 'CLOSED'}")
    print("\nConnections")
    show("Ollama", check_ollama())
    show("PostgreSQL/pgvector", check_postgres())
    show("Redis", check_redis())
    print("\nCloud keys")
    print(f"{'OPENAI_API_KEY':<24} {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
    print(f"{'GEMINI_API_KEY':<24} {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")
