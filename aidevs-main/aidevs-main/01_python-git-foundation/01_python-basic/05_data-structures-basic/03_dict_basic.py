"""dict 기초 예제입니다.

dict는 key와 value를 한 쌍으로 저장하는 자료구조입니다.

특징:
1. key로 값을 찾습니다.
2. 데이터에 이름을 붙여 저장할 수 있습니다.
3. JSON 데이터와 모양이 비슷합니다.

실제 백엔드 개발에서는 사용자 정보, 설정값, API 응답 데이터 등을
dict 형태로 자주 다룹니다.
"""

# 중괄호 { }를 사용해 dict를 만듭니다.
# JSON(JavaScript Object Notation)과 모양이 비슷합니다.
# dict는 파이썬 backend에서 JSON 데이터를 다룰 때 자주 사용합니다.
# JSON은 Frontend와 Backend 사이에서 데이터를 주고받을 때 사용하는 데이터 형식입니다.
student: dict[str, object] = {
    "name": "Jean",
    "score": 95,
    "passed": True,
}

print("학생 정보:", student)
print("자료형:", type(student))

# dict는 key를 사용해 값을 꺼냅니다.
print("이름:", student["name"])
print("점수:", student["score"])

# 새로운 key와 value를 추가할 수 있습니다.
student["course"] = "Python Basic"
print("과정 추가 후:", student)

# 기존 key의 value를 수정할 수 있습니다.
student["score"] = 98
print("점수 수정 후:", student)

# get()은 key가 없을 때 오류 대신 기본값을 사용할 수 있게 해 줍니다.
email = student.get("email", )
print("이메일:", email)

print("\n[dict 전체 출력]")

# items()는 key와 value를 함께 꺼냅니다.
for key, value in student.items():
    print(key, "=", value)

# keys()는 key만 꺼냅니다.
print("\nkey 목록:", list(student.keys()))

# values()는 value만 꺼냅니다.
print("value 목록:", list(student.values()))

# keys()는 key만 꺼냅니다.
print("\nkey 목록:", tuple(student.keys()))

# values()는 value만 꺼냅니다.
print("value 목록:", tuple(student.values()))
