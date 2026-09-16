# 03 MCP Labs

## Lab 01 · 새로운 Tool 공개

`01_first_mcp_server.py`에 `get_exchange_rate(base, quote)` Tool을 추가하고
`02_list_and_call_tools.py`에서 발견·호출되는지 확인합니다. 결과는 고정된 교육용
환율 데이터로 만들어 API Key 없이 반복 실행할 수 있게 합니다.

## Lab 02 · Resource 추가

`travel://policy/refund` Resource를 추가하고 Client에서 읽습니다. 같은 정보를 Tool로
제공할 때와 Resource로 제공할 때 호출 의도가 어떻게 다른지 설명합니다.

## Lab 03 · 두 MCP Server와 순차 Tool Loop

`03_weather_mcp_server.py`와 `03_hotel_mcp_server.py`를 각각 stdio Server로
실행하고 `03_multi_server_tool_loop.py`에서 동시에 연결합니다.

연결할 Server 목록은 `mcp_servers.json`에서 관리합니다. 새 Server를 추가할 때는
Client 코드를 수정하지 않고 다음처럼 설정만 추가합니다. `command`를 생략하면 현재
Python 실행 파일을 사용하며, 상대 경로인 Python 파일은 이 Lab 디렉터리를 기준으로
찾습니다.

```json
{
  "weather": { "args": ["03_weather_mcp_server.py"] },
  "hotel": { "args": ["03_hotel_mcp_server.py"] },
  "restaurant": { "args": ["03_restaurant_mcp_server.py"] }
}
```

```text
질문
→ 부산의 현재 날씨와 내일 예보를 확인하고, 15만 원 이하 호텔을 찾은 뒤
  검색된 호텔의 취소 규정을 알려줘.
```

Weather Server는 `get_current_weather`, `get_weather_forecast`를 제공하고 Hotel
Server는 `search_hotels`, `get_cancellation_policy`를 제공합니다. Client는 두
Server의 Tool 이름 앞에 `weather__`, `hotel__`을 붙여 GPT에 전달하고, 라우팅
테이블을 이용해 GPT가 선택한 Tool을 원래 Server에서 실행합니다.

```text
Weather MCP Server ─ get_current_weather
                   └ get_weather_forecast

Hotel MCP Server   ─ search_hotels
                   └ get_cancellation_policy
```

`parallel_tool_calls=False`이므로 GPT는 응답 한 번에 Tool 하나를 선택합니다.
Tool 결과는 `function_call_output`으로 다시 GPT에 전달되며, 더 이상 Function
Call이 없을 때까지 Agent Loop를 반복합니다. 특히 `get_cancellation_policy`의
`hotel_id`는 `search_hotels` 결과에서 얻어야 하므로 두 호출은 반드시 순서대로
진행되어야 합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
python .\03_mcp\10_labs\03_multi_server_tool_loop.py
```

예상되는 핵심 호출은 다음과 같습니다. 독립적인 날씨 호출과 호텔 호출의 실제
순서는 GPT의 판단에 따라 달라질 수 있습니다.

```text
weather__get_current_weather(city="부산")
weather__get_weather_forecast(city="부산", days=1)
hotel__search_hotels(city="부산", max_price=150000)
hotel__get_cancellation_policy(hotel_id="hotel-busan-001")
최종 답변
```

## 완료 기준

- Client가 Tool 이름을 코드에 등록하지 않아도 `list_tools()`에서 발견합니다.
- 정상 arguments와 잘못된 arguments의 결과를 모두 확인합니다.
- 서버는 표준 출력에 디버그 문장을 출력하지 않습니다.
- Lab 03의 Trace에서 두 Server의 Tool이 올바른 Server로 라우팅됩니다.
- 호텔 취소 규정은 호텔 검색 결과의 `hotel_id`로 조회됩니다.
