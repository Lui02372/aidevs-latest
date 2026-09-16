"""partial variables로 공통 정책을 고정하고 도메인 입력만 교체합니다."""

from datetime import date

from langchain_core.prompts import ChatPromptTemplate


base_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "기준일은 {today}입니다. 정책: {policy}"),
        ("human", "도메인: {domain}\n요청: {request}"),
    ]
).partial(
    today=lambda: date.today().isoformat(),
    policy="확인되지 않은 사실은 단정하지 말고 실제 변경 작업은 실행하지 않습니다.",
)


if __name__ == "__main__":
    for domain in ("여행", "교육 상담"):
        value = base_prompt.invoke({"domain": domain, "request": "추천안을 만들어 주세요."})
        print(f"\n[{domain}]\n{value.to_string()}")
