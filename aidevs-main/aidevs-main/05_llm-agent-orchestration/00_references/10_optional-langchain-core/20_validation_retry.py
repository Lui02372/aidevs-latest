"""구조화 결과 검증 실패를 제한된 재시도 입력으로 바꾸는 흐름입니다."""

from pydantic import BaseModel, Field, ValidationError


class BudgetResult(BaseModel):
    currency: str = Field(pattern="^(KRW|USD)$")
    amount: int = Field(gt=0)


def validate_with_feedback(candidate: dict) -> tuple[BudgetResult | None, str | None]:
    try:
        return BudgetResult.model_validate(candidate), None
    except ValidationError as error:
        feedback = "; ".join(
            f"{'.'.join(map(str, item['loc']))}: {item['msg']}" for item in error.errors()
        )
        return None, f"다음 검증 오류만 수정하세요: {feedback}"


if __name__ == "__main__":
    attempts = [{"currency": "won", "amount": -1}, {"currency": "KRW", "amount": 300000}]
    for number, candidate in enumerate(attempts, start=1):
        result, feedback = validate_with_feedback(candidate)
        print(f"시도 {number}:", result or feedback)
        if result:
            break
    print("실서비스에서는 최대 재시도 횟수와 실패 fallback을 반드시 정합니다.")
