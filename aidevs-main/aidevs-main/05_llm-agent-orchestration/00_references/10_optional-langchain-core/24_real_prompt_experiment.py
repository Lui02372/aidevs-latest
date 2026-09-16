"""같은 모델·입력으로 zero-shot과 few-shot prompt를 실제 비교합니다."""

import os
from time import perf_counter

from langchain_core.output_parsers import StrOutputParser

from provider_factory import create_chat_model
from 14_zero_shot_and_few_shot import few_shot_prompt, zero_shot_prompt


def run(name, prompt, request: str, model) -> None:
    started = perf_counter()
    result = (prompt | model | StrOutputParser()).invoke({"request": request})
    latency_ms = round((perf_counter() - started) * 1000)
    print(f"\n[{name}] {latency_ms}ms\n{result}")


if __name__ == "__main__":
    provider = os.getenv("LANGCHAIN_PROVIDER", "openai")
    model = create_chat_model(provider)
    request = "강릉 1박 2일로 가는데 비용은 정하지 않았어요"
    run("zero-shot", zero_shot_prompt, request, model)
    run("few-shot", few_shot_prompt, request, model)
