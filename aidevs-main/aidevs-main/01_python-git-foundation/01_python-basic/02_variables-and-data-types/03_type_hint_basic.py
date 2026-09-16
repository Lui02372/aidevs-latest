r"""타입 힌트 기초 예제입니다.

실행:
    cd C:\aidev\01_python-git-foundation
    .\.venv\Scripts\Activate.ps1
    python .\01_python-basic\02_variables-and-data-types\03_type_hint_basic.py

타입 힌트는 변수가 어떤 종류의 값을 사용할 예정인지 표시하는 문법입니다.
Python은 기본적으로 실행 중에 타입 힌트를 강제로 검사하지는 않습니다.
하지만 VS Code가 코드를 이해하고, 잘못된 값을 넣었을 때 미리 알려 주는 데 도움이 됩니다.

함수에 타입 힌트를 붙이는 방법은 나중에 06_function-basic에서 다시 다룹니다.
"""

# 타입 힌트를 붙인 변수 선언입니다.
# name: str = "kim"은 name 변수에 문자열(str)을 넣어 사용할 예정이라는 뜻입니다.
name: str = "kim"
age: int = 20
height: float = 175.5
is_student: bool = True

print("이름:", name)
print("나이:", age)
print("키:", height)
print("학생인가요?", is_student)
print(f"타입 힌트 예시: {name}, {age}, {height}, {is_student}")

msg = "     1000    "
num = int(msg)
print(f"입력{num}입니다")
print(f"입력{msg.strip()}입니다")


msg2: str = "12,000,000"
num2 = int(msg2.replace(",", ""))
print(f"입력{num2}입니다")


# jmlee@tonesol.com  에서
# id 변수에 jmlee 입력
# domain 변수에 tonesol 입력
# id 와 domain을 출력 하시오
# "ID는 id이고, 도메인은 domain입니다." 

data: str = "jmlee@tonesol.com"
id: str = data[:data.index("@")]
domain: str = data[data.index("@")+1:data.index(".")]
print(f"ID는 {id}이고, 도메인은 {domain}입니다