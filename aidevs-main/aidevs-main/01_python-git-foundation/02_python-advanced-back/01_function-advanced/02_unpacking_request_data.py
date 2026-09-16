"""리스트와 딕셔너리를 함수 인자로 풀어서 전달하는 예제입니다."""


def create_user_request(name: str, email: str, role: str) -> dict[str, str]:
    """사용자 생성 요청 데이터를 만듭니다."""

    # FastAPI나 Supabase로 보내기 전에 필요한 데이터를 dict로 정리하는 상황을 가정합니다.
    return {
        "name": name,
        "email": email,
        "role": role,
    }


# 리스트는 순서대로 인자를 전달할 때 사용할 수 있습니다.
user_values = ["Mina", "mina@example.com", "student"]

# *user_values는 리스트 값을 순서대로 풀어서 함수에 전달합니다.
request_from_list = create_user_request(*user_values)

# 딕셔너리는 key 이름을 함수 인자 이름과 맞춰서 전달할 수 있습니다.
user_fields = {
    "name": "Joon",
    "email": "joon@example.com",
    "role": "mentor",
}

# **user_fields는 dict의 key/value를 함수 인자로 풀어서 전달합니다.
request_from_dict = create_user_request(**user_fields)

print("리스트 언패킹 요청:", request_from_list)
print("딕셔너리 언패킹 요청:", request_from_dict)
