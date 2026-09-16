"""직접 만든 모듈 전체를 import해서 사용하는 예제입니다."""

# 같은 폴더에 있는 math_tools.py 파일을 모듈로 가져옵니다.
# import math_tools라고 쓰면 math_tools.py 안의 함수를 사용할 수 있습니다.
import math_tools

# 모듈 전체를 import했기 때문에 함수 앞에 모듈 이름을 붙입니다.
add_result = math_tools.add(3, 4)
multiply_result = math_tools.multiply(3, 4)

# 결과를 출력합니다.
print("3 + 4 =", add_result)
print("3 * 4 =", multiply_result)
