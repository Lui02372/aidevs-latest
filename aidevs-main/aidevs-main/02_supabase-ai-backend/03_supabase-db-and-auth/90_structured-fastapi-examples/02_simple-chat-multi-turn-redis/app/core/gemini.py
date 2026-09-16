"""Gemini client를 만듭니다."""

import os

from fastapi import HTTPException

import app.core.config  # .env 파일을 읽습니다.


def get_gemini_client():
    """GEMINI_API_KEY를 사용하는 Gemini client를 만듭니다."""

    from google import genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(500, "GEMINI_API_KEY가 없습니다. .env 파일을 확인하세요.")

    return genai.Client(api_key=api_key)
