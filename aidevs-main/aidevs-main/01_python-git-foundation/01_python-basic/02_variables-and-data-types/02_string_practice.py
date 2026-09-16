"""문자열 기초 예제입니다.

문자열은 글자들의 모음입니다.
Python에서는 문자열의 특정 위치를 가져오거나, 일부만 잘라내거나,
대소문자를 바꾸는 작업을 쉽게 할 수 있습니다.
"""

# message 변수에 문자열을 저장합니다.
message: str = "Python Basic"


print("전체 문자열:", message)
print("문자열 길이:", len(message))
print(f"안녕하세요\t{message}\n입니다.!")  # len()은 문자열 길이를 확인하는 함수입니다.

# 문자열의 위치 번호는 0부터 시작합니다.
# message[0]은 첫 번째 글자인 "P"를 의미합니다.
print("첫 글자:", message[0])

# message[:6]은 처음부터 6번째 위치 전까지 잘라냅니다.
# "Python Basic"에서 앞 6글자는 "Python"입니다.
# 0부터 시작 
# 4번째 에서
# 6번째 전까지 잘라냅니다.
print("앞 6글자1:", message[7:9])
print("앞 6글자2:", message[7:])
print("앞 6글자3:", message)
new_message = message[7:]
print("앞 6글자4:", new_message)

# 음수 인덱스는 뒤에서부터 위치를 셉니다.
# message[-5:]는 뒤에서 5글자를 가져옵니다.
print("뒤 5글자:", message[-5:])

# lower()는 모든 영문자를 소문자로 바꿉니다.
print("소문자:", message.lower())

# upper()는 모든 영문자를 대문자로 바꿉니다.
print("대문자:", message.upper())

name = "Jean"
score = 95

# f-string은 문자열 안에 변수 값을 넣을 때 사용하는 편리한 문법입니다.
# 문자열 앞에 f를 붙이고, 중괄호 { } 안에 변수 이름을 넣습니다.
# () 소
# {} 중
# [] 대
print(f"{name}님의 점수는\t{score}점입니다.")
