"""Lab 01 starter: LLM 메시지와 파라미터 구조 만들기."""

from pprint import pprint


# TODO: 사용자가 남긴 메모 내용을 한 문장으로 적어 보세요.
memo_context = ""

# TODO: AI에게 물어볼 질문을 적어 보세요.
user_question = ""


# system 메시지는 AI가 어떤 역할로 답해야 하는지 알려주는 기본 지시문입니다.
system_message = {
    "role": "system",
    "content": "너는 사용자의 메모를 바탕으로 짧고 친절하게 답변하는 AI 비서입니다.",
}

# user 메시지는 실제 사용자의 요청입니다.
# 메모 컨텍스트와 질문을 함께 넣으면 AI가 더 구체적인 답을 만들 수 있습니다.
user_message = {
    "role": "user",
    "content": f"메모 내용: {memo_context}\n질문: {user_question}",
}

# TODO: messages 리스트에 system_message와 user_message를 순서대로 넣어 보세요.
messages = []


# LLM 호출에 함께 전달할 주요 옵션입니다.
# 실제 API를 호출하지는 않지만, 이런 값들이 요청에 들어간다는 점을 확인합니다.
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
