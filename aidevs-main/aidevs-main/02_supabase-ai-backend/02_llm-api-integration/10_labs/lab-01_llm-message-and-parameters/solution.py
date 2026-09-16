"""Lab 01 solution: LLM 메시지와 파라미터 구조 만들기."""

from pprint import pprint


# 메모 컨텍스트는 사용자가 이전에 입력했거나 저장해 둔 정보입니다.
# 실제 서비스에서는 이 값이 Supabase의 대화 이력이나 메모 테이블에서 올 수 있습니다.
memo_context = "오늘 FastAPI에서 POST 요청과 Pydantic 모델을 공부했다."

# 사용자의 질문은 AI가 바로 답해야 하는 현재 요청입니다.
user_question = "오늘 공부한 내용을 복습할 수 있는 짧은 퀴즈를 만들어줘."


# system 메시지는 AI의 역할, 말투, 답변 기준을 정하는 메시지입니다.
system_message = {
    "role": "system",
    "content": "너는 사용자의 메모를 바탕으로 짧고 친절하게 답변하는 AI 비서입니다.",
}

# user 메시지는 사용자의 실제 입력입니다.
# 여기서는 메모와 질문을 함께 묶어 AI가 참고할 수 있게 만듭니다.
user_message = {
    "role": "user",
    "content": f"메모 내용: {memo_context}\n질문: {user_question}",
}

# 대부분의 LLM API는 여러 메시지를 순서대로 전달받습니다.
# system 메시지를 먼저 두고 user 메시지를 뒤에 두면 역할 지시가 먼저 적용됩니다.
messages = [system_message, user_message]


# 실제 API 호출에 사용할 수 있는 설정값입니다.
# 이 실습에서는 mock 구조만 확인하므로 actual_api_called를 False로 둡니다.
request_options = {
    "provider": "gemini",
    "model": "gemini-2.5-flash-lite",
    "temperature": 0.3,
    "top_p": 0.9,
    "max_tokens": 300,
    "actual_api_called": False,
}


print("[messages]")
pprint(messages, width=100)

print("\n[request_options]")
pprint(request_options, width=100)
