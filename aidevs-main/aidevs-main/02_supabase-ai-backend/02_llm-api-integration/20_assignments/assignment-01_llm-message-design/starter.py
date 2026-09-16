"""Assignment 01 starter: LLM 메시지 구조 설계."""

from pprint import pprint


# TODO: 사용자가 저장한 메모 내용을 작성하세요.
memo_context = ""

# TODO: AI에게 물어볼 질문을 작성하세요.
user_question = ""


# system 메시지는 AI의 역할과 답변 기준을 정합니다.
system_message = {
    "role": "system",
    "content": "너는 사용자의 메모를 바탕으로 핵심을 정리하는 AI 비서입니다.",
}

# TODO: user_message에 메모와 질문을 함께 담아 보세요.
user_message = {
    "role": "user",
    "content": "",
}

# TODO: messages에 system_message와 user_message를 순서대로 넣으세요.
messages = []


# TODO: 아래 요청 옵션을 완성하세요.
request_options = {
    "provider": "gemini",
    "model": "gemini-2.5-flash-lite",
    "temperature": 0.3,
    "top_p": 0.9,
    "max_tokens": 300,
    "actual_api_called": False,
}


print("[LLM messages]")
pprint(messages, width=100)

print("\n[request options]")
pprint(request_options, width=100)
