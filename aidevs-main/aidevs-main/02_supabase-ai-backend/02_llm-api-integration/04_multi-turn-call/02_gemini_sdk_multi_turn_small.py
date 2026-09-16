r"""Gemini SDK로 가장 작게 실행해 보는 멀티턴 호출 예제입니다.

이 파일은 예외 처리, key placeholder 검사, 자세한 오류 안내를 일부러 넣지 않습니다.
Gemini SDK로 이전 대화 이력을 함께 보내는 최소 구조를 먼저 확인하기 위한 예제입니다.

주의:
    이 파일은 GEMINI_API_KEY가 설정되어 있으면 실제 Gemini API를 호출합니다.
    실제 호출은 무료 한도, quota, billing 상태에 따라 비용 또는 제한의 영향을 받을 수 있습니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\04_multi-turn-call\02_gemini_sdk_multi_turn_small.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# .env 파일은 02_supabase-ai-backend 폴더에 있습니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

client = genai.Client(api_key=api_key)


# 멀티턴 호출의 핵심은 이전 user/model 메시지를 함께 보내는 것입니다.
# Gemini에서는 이전 AI 답변을 role="model"로 표현합니다.
contents = [
    {
        "role": "user",
        "parts": [{"text": "이제부터 너의 이름은 지니야"}],
    },
    {
        "role": "model",
        "parts": [{"text": "내 제 이름은 지금부토 지니 입니다."}],
    },
    {
        "role": "user",
        "parts": [{"text": "너의 이름은 뭐야?"}],
    },
]

response = client.models.generate_content(
    model=model,
    contents=contents,
)

print(response.text)
