"""프로젝트 폴더의 .env 파일을 읽습니다."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)
