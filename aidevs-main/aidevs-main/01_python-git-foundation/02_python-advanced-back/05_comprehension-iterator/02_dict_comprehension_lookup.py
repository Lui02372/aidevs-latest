"""딕셔너리 컴프리헨션으로 id 기반 조회 구조를 만드는 예제입니다."""

# 여러 사용자 정보를 리스트로 준비합니다.
users = [
    {"id": "u1", "name": "Mina", "role": "student"},
    {"id": "u2", "name": "Joon", "role": "mentor"},
    {"id": "u3", "name": "Sora", "role": "student"},
]

# id를 key로, 사용자 dict를 value로 하는 딕셔너리를 만듭니다.
# 이렇게 바꾸면 user_by_id["u2"]처럼 빠르게 조회할 수 있습니다.
user_by_id = {user["id"]: user for user in users}

# 역할별 이름 목록도 만들 수 있습니다.
student_names = [user["name"] for user in users if user["role"] == "student"]

# 결과를 출력합니다.
print("id 기반 사용자 조회:", user_by_id)
print("u2 사용자:", user_by_id["u2"])
print("student 이름 목록:", student_names)
