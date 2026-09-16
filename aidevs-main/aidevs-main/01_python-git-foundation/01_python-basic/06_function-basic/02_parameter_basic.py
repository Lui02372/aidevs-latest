"""매개변수(parameter) 기초 예제입니다.

매개변수는 함수가 실행될 때 외부에서 값을 받아오기 위한 이름입니다.

함수를 호출할 때 넣는 실제 값을 인자(argument)라고 부릅니다.
처음에는 둘을 엄격히 구분하기보다,
"함수에 값을 넣어 실행한다"는 흐름을 이해하면 됩니다.
"""

# argument
def greet(name: str):
    print(name, "님, 안녕하세요.")


def print_score(name: str, score: float):
    print(name, "님의 점수는", score, "점입니다.")


# "Jean"은 greet 함수의 name 매개변수로 전달됩니다.
greet("Jean")
greet("Mina")

# print_score 함수는 값을 두 개 받습니다.
print_score("Jean", 95)
print_score("Mina", 82)

# 매개변수를 사용하면 같은 함수로 여러 값을 처리할 수 있습니다.
