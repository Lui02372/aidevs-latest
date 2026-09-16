"""print 확인과 assert 확인의 차이를 보여 주는 예제입니다.

실행:
    cd C:\aidev\01_python-git-foundation
    python .\02_python-advanced\08_testing-code-quality\02_print_vs_assert.py

핵심:
    print는 결과를 보여 주는 도구입니다.
    assert는 결과가 맞는지 자동으로 검사하는 도구입니다.

초보자는 처음에 print로 값을 확인하는 것이 자연스럽습니다.
하지만 코드가 많아지면 모든 출력 결과를 사람이 매번 확인하기 어렵습니다.
그래서 중요한 규칙은 assert나 pytest 테스트로 남겨 두는 것이 좋습니다.
"""


def calculate_total(price: int, quantity: int) -> int:
    """상품 가격과 수량을 받아 총액을 계산합니다."""

    return price * quantity


# print는 결과를 화면에 보여 줍니다.
# 하지만 이 값이 맞는지 틀린지는 사람이 직접 봐야 합니다.
print("print 확인:", calculate_total(3000, 2))

# assert는 예상값과 실제값을 코드가 직접 비교합니다.
# 3000원 상품 2개의 총액은 6000이어야 합니다.
assert calculate_total(3000, 2) == 6000

# 아래 줄의 주석을 풀면 일부러 실패하는 assert를 확인할 수 있습니다.
# AssertionError가 발생하면 "예상과 실제가 다르다"는 뜻입니다.
# assert calculate_total(3000, 2) == 5000

print("assert 검사 통과")
