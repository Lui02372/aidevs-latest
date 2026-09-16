"""중첩된 API 응답에서 필요한 값만 추출하는 예제입니다."""

# 실제 API 응답은 보통 dict 안에 list가 들어 있는 구조가 많습니다.
api_response = {
    "items": [
        {"id": 1, "message": {"role": "user", "content": "FastAPI란?"}},
        {"id": 2, "message": {"role": "assistant", "content": "API 서버 프레임워크입니다."}},
        {"id": 3, "message": {"role": "user", "content": "Supabase란?"}},
    ]
}

# items 목록만 먼저 꺼냅니다.
items = api_response["items"]

# 사용자 메시지만 고르고, 화면 출력에 필요한 형태로 바꿉니다.
user_messages = [
    {
        "id": item["id"],
        "content": item["message"]["content"],
    }
    for item in items
    if item["message"]["role"] == "user"
]

# 결과를 출력합니다.
print("사용자 메시지 목록:", user_messages)
