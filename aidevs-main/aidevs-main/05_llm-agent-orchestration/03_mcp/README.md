# 03 MCP (Model Context Protocol)

MCP는 Tool과 Context를 특정 Agent 코드에 직접 묶지 않고, Client가 발견하고 호출할
수 있는 공통 규약으로 제공합니다. 이 단원은 기존 `03_tool-use`의 여행 Tool을 작은
MCP Server로 옮기며 차이를 확인합니다.

```text
Tool Use: Agent → Python 함수 직접 호출
MCP:      Host/Client → MCP Server 발견 → Tool 호출 → 결과 사용
```

## Tool Use와 MCP stdio 구분

Tool은 날씨 조회나 호텔 검색처럼 **실제로 수행할 기능**입니다. MCP는 Tool 그 자체가
아니라 Tool·Resource·Prompt를 Client에 제공하고 호출하기 위한 **통신 규약**입니다.
`stdio`는 MCP Client와 Server가 그 규약의 메시지를 주고받는 **전송 방식**입니다.

```text
Tool  = 무엇을 실행할 것인가
MCP   = 기능을 어떻게 설명·발견·호출할 것인가
stdio = MCP 메시지를 어떤 통로로 주고받을 것인가
```

따라서 `get_current_weather()` 함수는 Tool이고, `tools/list`와 `tools/call`은 MCP가
정한 호출 방식이며, `stdin`과 `stdout`은 이 예제에서 선택한 전송 통로입니다.

| 구분 | 기존 Tool Use | MCP + stdio |
| --- | --- | --- |
| 기능 구현 | Python 함수 | 동일한 Python 함수 |
| Tool 위치 | Agent 또는 Backend 코드 내부 | 별도 MCP Server 프로세스 |
| Tool 등록 | Agent 코드가 Schema를 직접 보유 | Server가 Tool과 Schema를 공개 |
| Tool 발견 | 미리 작성한 목록 사용 | Client가 `tools/list` 요청 |
| Tool 실행 | Python 함수 직접 호출 | Client가 `tools/call` 요청 |
| 통신 | 같은 프로세스의 함수 호출 | JSON-RPC 메시지를 stdin/stdout으로 교환 |
| 서버 실행 | 별도 서버 없음 | Client가 자식 프로세스로 자동 실행 |
| 포트 | 사용하지 않음 | 사용하지 않음 |
| 수명 | Backend와 같음 | Client 연결이 끝나면 자식 프로세스도 종료 |
| 재사용 범위 | 해당 애플리케이션에 결합 | MCP Client를 지원하는 Host에서 재사용 가능 |
| Context 제공 | 애플리케이션마다 직접 구현 | Resources·Prompts라는 공통 기능 사용 가능 |

두 방식 모두 LLM이 함수를 직접 실행하는 것은 아닙니다. LLM은 Tool 이름과
arguments를 제안하고, 실제 실행 여부와 권한은 Backend 또는 MCP Server가
검증합니다.

### stdio 실행 흐름

```text
사용자 질문
→ Host가 사용할 Tool 판단
→ MCP Client가 Python Server 프로세스 실행
→ initialize로 기능 협상
→ tools/list로 Tool과 Schema 발견
→ tools/call로 이름과 arguments 전달
→ MCP Server가 검증 후 Python Tool 실행
→ Tool Result 반환
→ Host가 최종 답변 생성
→ Client 종료와 함께 Server 프로세스 종료
```

stdio는 설치된 로컬 Tool을 연결하기 단순하고 네트워크 포트를 열지 않는다는 장점이
있습니다. 반면 Client마다 Server 프로세스를 실행하므로 여러 Backend가 하나의 원격
서버를 공유하거나 독립적으로 배포하는 구조에는 적합하지 않습니다. 그런 경우에는
다음 Mini Agent 프로젝트처럼 Streamable HTTP를 사용합니다.

## 핵심 구성

| 파일 | 확인할 내용 |
| --- | --- |
| `01_first_mcp_server.py` | Tool과 Resource를 제공하는 stdio MCP Server |
| `02_list_and_call_tools.py` | 서버 자동 실행, 초기화, Tool 발견과 호출 |
| `03_read_resource.py` | Tool이 아닌 읽기 전용 Context 조회 |
| `04_validation_and_errors.py` | Schema 검증 오류가 Tool Result로 돌아오는 과정 |
| `05_mcp_tool_loop.py` | GPT → 여러 MCP Tool 선택·호출 → LLM 최종 답변 |

이 예제에서 MCP Server는 별도 터미널이나 포트를 요구하지 않습니다. Client가 Python
자식 프로세스로 서버를 실행하고 `stdin`/`stdout`으로 JSON-RPC 메시지를 교환합니다.
Client가 종료되면 서버 프로세스도 함께 종료됩니다.

## 준비

과정 루트에서 가상환경을 활성화하고 의존성을 설치합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

MCP Python SDK는 안정적인 v1 API를 사용하도록 `mcp>=1.27,<2`로 제한합니다.

## 실행

서버 파일을 단독 실행하면 stdio 입력을 기다리므로 화면에 아무것도 출력되지 않는
것이 정상입니다. 학습할 때는 Client 예제를 실행합니다.

```powershell
python .\03_mcp\02_list_and_call_tools.py
python .\03_mcp\03_read_resource.py
python .\03_mcp\04_validation_and_errors.py
python .\03_mcp\05_mcp_tool_loop.py
```

`05_mcp_tool_loop.py`는 OpenAI Responses API를 사용합니다. 과정 루트의 `.env`에
API Key와 Function Calling 지원 모델을 설정합니다.

```env
OPENAI_API_KEY=발급받은_API_KEY
OPENAI_MODEL=gpt-4.1-mini
```

05번의 실제 실행 흐름은 다음과 같습니다.

```text
MCP tools/list
→ MCP Tool Schema를 OpenAI Function Tool 형식으로 변환
→ OpenAI Responses API
→ GPT가 Tool 이름과 arguments 제안
→ 허용된 MCP Tool인지 검사
→ MCP tools/call
→ function_call_output을 call_id와 함께 GPT에 전달
→ 두 번째 GPT 호출에서 Tool 없이 최종 답변 생성
```

교육용 여행 데이터가 지원하는 도시는 `부산`, `서울`입니다. MCP Tool의 `city`
Schema도 두 값의 enum으로 제한해 GPT가 다른 도시를 제안하면 Server 검증에서
거부합니다. 출력 Trace의 `tool`, `arguments`, `is_error`를 함께 확인합니다.

## Tool과 Resource

| 구분 | 용도 | 이 예제 |
| --- | --- | --- |
| Tool | 계산, 조회, 변경처럼 실행이 필요한 기능 | `get_current_weather`, `search_hotels` |
| Resource | URI로 식별하는 읽기 전용 Context | `travel://policy/baggage` |

Tool 설명과 arguments Schema는 서버가 제공하고 Client는 `list_tools()`로 발견합니다.
Client는 서버의 Python 함수를 직접 import하지 않고 `call_tool()`로 실행합니다.

## 안전 경계

- Tool arguments는 서버의 타입 힌트에서 만들어진 Schema로 검증합니다.
- Client가 보내는 Tool 이름과 arguments를 신뢰하지 않습니다.
- stdio 서버는 표준 출력에 임의 로그를 쓰지 않습니다. 로그는 프로토콜 메시지와
  충돌할 수 있습니다.
- API Key 같은 환경변수는 필요한 값만 MCP 자식 프로세스에 전달합니다.
- 실제 예약·결제처럼 상태를 바꾸는 Tool은 사용자 확인 단계를 별도로 둡니다.

## 다음 단계

`C:\mini_agent_st\mini_agent_03_mcp`에서는 같은 서버를 FastAPI Backend의 MCP
Server와 분리해 `8010/mcp`에서 실행합니다. Backend는 Streamable HTTP로 연결하고,
Frontend에서 발견된 Tool·arguments·결과 Trace를 확인합니다.

## 공식 문서

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP Resources](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)
