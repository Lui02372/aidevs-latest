r"""Gemini SDK로 가장 작게 실행해 보는 싱글턴 호출 예제입니다.

이 파일은 예외 처리, key placeholder 검사, 자세한 오류 안내를 일부러 넣지 않습니다.
Gemini SDK 호출이 어떤 모양인지 가장 단순한 코드로 먼저 확인하기 위한 예제입니다.

주의:
    이 파일은 GEMINI_API_KEY가 설정되어 있으면 실제 Gemini API를 호출합니다.
    실제 호출은 무료 한도, quota, billing 상태에 따라 비용 또는 제한의 영향을 받을 수 있습니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\02_llm-api-integration\03_single-turn-call\02_gemini_sdk_single_turn_small.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# .env 파일은 02_supabase-ai-backend 폴더에 있습니다.
# 이 파일 위치에서 두 단계 위로 올라가면 02_supabase-ai-backend 폴더입니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


# .env에서 Gemini API key와 모델 이름을 읽습니다.
# GEMINI_MODEL이 없으면 수업 기본 모델을 사용합니다.
api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


# Google Gen AI SDK 클라이언트를 만듭니다.
# 여기서 api_key가 비어 있거나 잘못되어 있으면 실제 호출 시 오류가 날 수 있습니다.
client = genai.Client(api_key=api_key)

while(True):

    # 싱글턴 호출은 "현재 질문 1개 -> 모델 응답 1개" 흐름입니다.
    prompt = input("질문하세요: ")


    # Gemini 모델에 prompt를 보내고 응답을 받습니다.
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )


    # SDK는 응답 텍스트를 response.text로 꺼낼 수 있습니다.
    # print("1.----------------------------------------")
    # print(type(response))
    # print("2.----------------------------------------")
    # print(response)
    # print("3.----------------------------------------")
    print(response.text)
