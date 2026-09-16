import os

from dotenv import load_dotenv


load_dotenv()


def create_chat_model(provider: str):
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        )
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            google_api_key=os.environ["GEMINI_API_KEY"],
            model=os.environ["GEMINI_MODEL"],
        )
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
        )
    raise ValueError("provider는 openai, gemini, ollama 중 하나여야 합니다.")
