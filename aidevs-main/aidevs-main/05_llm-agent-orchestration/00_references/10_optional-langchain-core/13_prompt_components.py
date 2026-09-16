"""Role, Instruction, Context, Constraint를 분리해 ChatPromptTemplate을 만듭니다."""

from langchain_core.prompts import ChatPromptTemplate


ROLE = "당신은 여행 요청을 정리하는 분석가입니다."
INSTRUCTION = "요청에서 목적지, 기간, 인원, 예산을 추출하세요."
CONSTRAINT = "추측하지 말고 모르는 값은 '확인 필요'로 표시하세요."

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "[Role]\n{role}\n\n[Instruction]\n{instruction}\n\n[Constraint]\n{constraint}"),
        ("human", "[Context]\n{request}"),
    ]
).partial(role=ROLE, instruction=INSTRUCTION, constraint=CONSTRAINT)


if __name__ == "__main__":
    value = prompt.invoke({"request": "가을에 부모님과 제주에 가고 싶어요."})
    for message in value.to_messages():
        print(f"[{message.type}]\n{message.content}\n")
