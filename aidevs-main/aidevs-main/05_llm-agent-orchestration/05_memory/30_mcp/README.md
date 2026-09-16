# 30 · PostgreSQL HTTP MCP Memory

기존 PostgreSQL 장기 Memory를 Agent가 호출할 수 있는 MCP Tool로 노출합니다. 실제 PostgreSQL만 사용하며 기본 주소는 `http://127.0.0.1:8012/mcp`입니다.

```text
MCP Client
→ Streamable HTTP :8012/mcp
→ 인증된 사용자 범위
→ PostgreSQL user_memories
```

## Tool

| Tool | 역할 | 변경 여부 |
| --- | --- | --- |
| `list_memories` | 현재 사용자 Memory 조회 | 읽기 |
| `save_memory` | 허용된 선호 저장·수정 | 쓰기 |
| `delete_memory` | Memory ID로 삭제 | 쓰기 |
| `find_relevant_memories` | 질문 관련 Memory 선택 | 읽기 |

Tool 인자에는 `user_id`가 없습니다. Server가 `MCP_DEMO_USER_ID`를 인증 계층에서 확인된 사용자라고 가정하고 모든 SQL에 같은 사용자 범위를 적용합니다.

## 실행

먼저 `00_local-runtime`의 PostgreSQL과 `user_memories` Schema를 준비합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\.venv\Scripts\Activate.ps1
$env:DATABASE_URL="postgresql://agent_user:agent_password@127.0.0.1:5433/agent_db"
$env:MCP_DEMO_USER_ID="student-01"
python .\05_memory\30_mcp\memory_mcp_server.py
```

새 Terminal에서 Client를 실행합니다.

```powershell
python .\05_memory\30_mcp\memory_mcp_client.py
```

DB 연결 없이 저장 허용·민감정보·관련성 정책만 검사할 수 있습니다.

```powershell
python .\05_memory\30_mcp\test_memory_policy.py
```

## Codex 연결

```toml
[mcp_servers.memory_demo]
url = "http://127.0.0.1:8012/mcp"
enabled_tools = ["list_memories", "save_memory", "delete_memory", "find_relevant_memories"]
default_tools_approval_mode = "writes"
```

이 예제의 환경 변수 사용자 범위는 localhost 수업용입니다. 운영 환경에서는 OAuth 또는 Bearer Token을 검증한 결과로 사용자 범위를 정해야 합니다.
