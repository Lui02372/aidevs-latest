"""RunnableGenerator의 chunk streaming을 API Key 없이 확인합니다."""

from collections.abc import Iterator

from langchain_core.runnables import RunnableGenerator


def mock_stream(inputs: Iterator[str]) -> Iterator[str]:
    for text in inputs:
        for token in text.split():
            yield token + " "


chain = RunnableGenerator(mock_stream)


if __name__ == "__main__":
    for chunk in chain.stream("부산 여행은 바다와 시장을 함께 즐기기 좋습니다."):
        print(chunk, end="", flush=True)
    print()
