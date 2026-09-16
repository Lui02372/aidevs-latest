"""set 기초 예제입니다.

set은 중복을 허용하지 않는 자료구조입니다.

특징:
1. 같은 값은 한 번만 저장됩니다.
2. 순서가 중요하지 않습니다.
3. 중복 제거와 집합 연산에 자주 사용합니다.

실제 개발에서는 태그 목록, 중복 사용자 제거, 권한 목록 비교 등에
set을 사용할 수 있습니다.
"""

# 중괄호 { }를 사용해 set을 만들 수 있습니다.
tags = {"python", "fastapi", "python", "supabase", "python "}

print("태그 목록:", tags)
print("자료형:", type(tags))

# "python"을 두 번 넣었지만 set에는 한 번만 저장됩니다.
print("태그 개수:", len(tags))

# add()는 set에 값을 추가합니다.
tags.add("streamlit")
print("추가 후:", tags)

# discard()는 값을 제거합니다.
# 값이 없어도 오류가 나지 않습니다.
tags.discard("fastapi")
print("삭제 후:", tags)

# in을 사용해 특정 값이 있는지 확인할 수 있습니다.
print("python 태그가 있나요?", "python" in tags)

if "fastapi" in tags:
    print("fastapi 태그가 있습니다.")

# set은 집합 연산을 할 수 있습니다.
backend_tags = {"python", "fastapi", "supabase"}
frontend_tags = {"python", "streamlit", "ui"}

print("\n합집합:", backend_tags | frontend_tags)
print("교집합:", backend_tags & frontend_tags)
print("차집합:", backend_tags - frontend_tags)
