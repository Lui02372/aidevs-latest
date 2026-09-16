"""사용자 범위 PostgreSQL Memory를 제공하는 Streamable HTTP MCP Server입니다."""

import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from memory_store import PostgresMemoryStore


load_dotenv()
HOST = os.getenv("MEMORY_MCP_HOST", "127.0.0.1")
PORT = int(os.getenv("MEMORY_MCP_PORT", "8012"))
AUTHENTICATED_USER_ID = os.getenv("MCP_DEMO_USER_ID", "student-01")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://agent_user:agent_password@127.0.0.1:5433/agent_db",
)

store = PostgresMemoryStore(DATABASE_URL, AUTHENTICATED_USER_ID)
mcp = FastMCP(
    "PostgreSQL Memory Learning Server",
    instructions=(
        "이 서버는 인증 계층이 확인했다고 가정한 한 사용자의 Memory만 관리합니다. "
        "Tool 인자로 user_id를 받지 않습니다. 민감정보를 저장하지 말고, 답변에는 "
        "find_relevant_memories가 반환한 관련 Memory만 사용하세요."
    ),
    host=HOST,
    port=PORT,
    json_response=True,
    stateless_http=True,
)


@mcp.tool()
def list_memories() -> dict:
    """현재 인증된 사용자의 저장된 Memory를 조회합니다."""
    return {"user_scope": store.user_id, "items": store.list()}


@mcp.tool()
def save_memory(key: str, value: str) -> dict:
    """현재 인증된 사용자의 허용된 선호를 저장하거나 수정합니다."""
    return {"user_scope": store.user_id, "item": store.save(key, value)}


@mcp.tool()
def delete_memory(memory_id: str) -> dict:
    """현재 인증된 사용자의 Memory ID가 일치할 때만 삭제합니다."""
    return {"user_scope": store.user_id, "deleted": store.delete(memory_id)}


@mcp.tool()
def find_relevant_memories(question: str) -> dict:
    """질문과 관련 있는 현재 사용자의 Memory만 선택합니다."""
    return {
        "user_scope": store.user_id,
        "question": question,
        "items": store.relevant(question),
    }


if __name__ == "__main__":
    print(f"PostgreSQL Memory MCP: http://{HOST}:{PORT}/mcp")
    print("교육용 사용자 범위:", AUTHENTICATED_USER_ID)
    mcp.run(transport="streamable-http")
