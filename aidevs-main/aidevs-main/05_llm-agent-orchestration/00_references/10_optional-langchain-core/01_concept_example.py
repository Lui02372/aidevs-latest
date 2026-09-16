"""LangChain Runnable을 API Key 없이 학습하는 최소 예제."""

from langchain_core.runnables import RunnableLambda


def normalize_input(data: dict) -> dict:
    return {"topic": data["topic"].strip(), "audience": data.get("audience", "초보자")}


def mock_model(data: dict) -> dict:
    return {
        "title": f"{data['topic']} 입문",
        "summary": f"{data['audience']}를 위한 {data['topic']} 설명입니다.",
    }


chain = RunnableLambda(normalize_input) | RunnableLambda(mock_model)


if __name__ == "__main__":
    print(chain.invoke({"topic": " LangChain ", "audience": "Python 학습자"}))
