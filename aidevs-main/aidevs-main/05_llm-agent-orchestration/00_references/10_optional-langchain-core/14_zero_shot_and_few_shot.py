"""Zero-shot과 Few-shot prompt의 구조를 비교합니다.

이 예제는 prompt만 출력합니다. 품질 차이는 `24_real_prompt_experiment.py`에서 같은
Provider와 설정으로 측정해야 합니다.
"""

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


examples = [
    {"request": "부산 2박, 예산은 아직 몰라요", "label": "missing_budget"},
    {"request": "제주 3박 4일, 2명, 80만원", "label": "complete"},
    {"request": "내일 당장 해외여행 예약해 줘", "label": "needs_confirmation"},
]

example_prompt = ChatPromptTemplate.from_messages(
    [("human", "요청: {request}"), ("ai", "분류: {label}")]
)
few_shot = FewShotChatMessagePromptTemplate(examples=examples, example_prompt=example_prompt)

zero_shot_prompt = ChatPromptTemplate.from_messages(
    [("system", "여행 요청을 complete, missing_budget, needs_confirmation 중 하나로 분류하세요."),
     ("human", "요청: {request}")]
)
few_shot_prompt = ChatPromptTemplate.from_messages(
    [("system", "예시의 판단 기준을 따라 여행 요청을 분류하세요."), few_shot,
     ("human", "요청: {request}")]
)


if __name__ == "__main__":
    data = {"request": "강릉 1박 2일로 가는데 비용은 정하지 않았어요"}
    for name, template in (("zero-shot", zero_shot_prompt), ("few-shot", few_shot_prompt)):
        print(f"\n[{name}]")
        for message in template.invoke(data).to_messages():
            print(f"{message.type}: {message.content}")
