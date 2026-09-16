"""RunnablePassthrough, RunnableParallel, RunnableBranch를 한 번에 비교합니다."""

from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)


normalize = RunnableLambda(
    lambda data: {
        "destination": data["destination"].strip(),
        "budget": int(data["budget"]),
    }
)

inspect_in_parallel = RunnableParallel(
    original=RunnablePassthrough(),
    daily_budget=RunnableLambda(lambda data: data["budget"] // 3),
    is_domestic=RunnableLambda(lambda data: data["destination"] in {"부산", "제주", "서울"}),
)

recommend_by_budget = RunnableBranch(
    (lambda data: data["daily_budget"] < 100_000, RunnableLambda(lambda _: "대중교통 중심 일정")),
    RunnableLambda(lambda _: "택시와 유료 체험을 포함한 일정"),
)

chain = normalize | inspect_in_parallel | RunnableLambda(
    lambda data: {**data, "recommendation": recommend_by_budget.invoke(data)}
)


if __name__ == "__main__":
    print(chain.invoke({"destination": " 부산 ", "budget": "240000"}))
