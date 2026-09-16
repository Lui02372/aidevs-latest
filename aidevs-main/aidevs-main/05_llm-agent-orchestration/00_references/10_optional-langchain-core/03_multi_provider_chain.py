"""같은 PromptTemplate을 GPT, Gemini, Ollama/Llama에 적용합니다."""

from time import perf_counter

from langchain_core.prompts import ChatPromptTemplate

from provider_factory import create_chat_model


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 초보자를 돕는 친절한 여행 도우미입니다."),
        ("human", "{message}"),
    ]
)

message = "부산에서 대중교통으로 즐기는 2박 3일 여행을 제안해 주세요."
for provider_name in ("openai", "gemini", "ollama"):
    try:
        chain = prompt | create_chat_model(provider_name)
        started = perf_counter()
        result = chain.invoke({"message": message})
        latency_ms = round((perf_counter() - started) * 1000)
        print(f"\n[{provider_name}] {latency_ms}ms")
        print(result.content)
    except Exception as error:
        print(f"\n[{provider_name}] 실행 실패: {error}")
