"""직접 만든 모듈에서 필요한 함수만 가져오는 예제입니다."""

# math_tools 모듈에서 add 함수와 subtract 함수만 가져옵니다.
# 이렇게 가져오면 math_tools.add()가 아니라 add()라고 바로 호출할 수 있습니다.
from math_tools import add, subtract

# 가져온 함수를 바로 호출합니다.
add_result = add(10, 5)
subtract_result = subtract(10, 5)

# 결과를 출력합니다.
print("10 + 5 =", add_result)
print("10 - 5 =", subtract_result)

# 필요한 함수만 가져오면 코드가 짧아집니다.
# 하지만 어디에서 온 함수인지 헷갈릴 수 있으므로 이름을 명확하게 쓰는 것이 좋습니다.
