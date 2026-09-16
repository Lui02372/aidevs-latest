# 공식 문서

라이브러리 API는 변경될 수 있으므로 수업 전 다음 공식 문서를 확인합니다.

## OpenAI

- [Developer Quickstart](https://developers.openai.com/api/docs/quickstart)
- [Responses API 전환 가이드](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Images and Vision](https://developers.openai.com/api/docs/guides/images-vision)
- [Text to Speech](https://developers.openai.com/api/docs/guides/text-to-speech)

## Gemini

- [Gemini API](https://ai.google.dev/gemini-api/docs)
- [Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)

## Ollama

- [API](https://docs.ollama.com/api/introduction)
- [Tool Calling](https://docs.ollama.com/capabilities/tool-calling)

## LangChain

- [LangChain Overview](https://docs.langchain.com/oss/python/langchain/overview)
- [Models](https://docs.langchain.com/oss/python/langchain/models)
- [Tools](https://docs.langchain.com/oss/python/langchain/tools)
- [Structured Output](https://docs.langchain.com/oss/python/langchain/structured-output)

## LangGraph

- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

## Backend와 Schema

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [psycopg 3](https://www.psycopg.org/psycopg3/docs/)

## Local Runtime과 Data

- [Docker Desktop Windows 설치](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Desktop WSL 2](https://docs.docker.com/desktop/features/wsl/)
- [Docker Container 기초](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [Docker `run`](https://docs.docker.com/reference/cli/docker/container/run/)
- [Docker Volume](https://docs.docker.com/engine/storage/volumes/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL](https://www.postgresql.org/docs/current/)
- [pgvector](https://github.com/pgvector/pgvector)
- [Redis](https://redis.io/docs/latest/)

## Frontend

- [Streamlit](https://docs.streamlit.io/)

## 확인 기준

- 설치된 패키지 버전과 문서 버전
- Import 경로
- State와 Checkpointer 사용법
- `interrupt`와 `Command(resume=...)`
- Provider의 Structured Output 지원 여부
- 이미지·TTS처럼 Provider별로 다른 기능의 지원 범위
- Docker Image Tag와 PostgreSQL·Redis 버전
- Host Port와 Container 내부 Port
- Pydantic 1과 2의 API 차이

공식 문서의 최신 예제가 현재 설치된 패키지보다 새로운 API를 사용할 수 있습니다.
문서만 보고 Import 경로를 즉시 바꾸지 말고, 먼저 가상환경에서 설치 버전을
확인한 뒤 예제와 함께 검증합니다.
