# Mock에서 실제 연동으로 확장하는 기준

Mock은 없애지 않습니다. Agent의 판단 과정과 API 계약을 빠르고 반복 가능하게
학습하는 기준선으로 사용합니다. 실제 연동은 같은 입력과 Schema를 유지한 채
교체하여 비용, 지연, 품질, 장애를 비교합니다.

| 학습 주제 | Mock/개념 예제 | 실제 연동 예제 | 확인할 차이 |
| --- | --- | --- | --- |
| LLM 호출 | 결정적 문자열 응답 | GPT·Gemini·Ollama | 지연, 비용, 응답 편차 |
| Structured Output | Pydantic 직접 생성 | Provider별 Schema 강제 | 검증 실패와 재시도 |
| Tool | 규칙 기반 선택 | LLM Tool Calling | 잘못된 Tool/인자 |
| RAG | 단어 기반 문서 검색 | Ollama embedding + pgvector | 검색 점수와 근거 |
| 단기 Memory | Python 객체 | Redis TTL | 만료와 복구 |
| 장기 Memory | Python 객체 | PostgreSQL | 사용자 격리와 삭제 |
| Workflow | 순차 함수 | LangGraph | 분기, 중단, 재개 |
| UI | 단위 스크립트 | FastAPI + Streamlit | 네트워크 오류와 상태 |

## 운영 규칙

1. API Key는 Backend `.env`에만 저장합니다.
2. Frontend는 Provider 이름만 전송합니다.
3. Provider 결과는 공통 Pydantic Schema로 검증합니다.
4. fallback은 기본적으로 끄고, 실습에서 명시적으로 켭니다.
5. 실제 예약·결제 Tool은 연결하지 않고 조회와 예약 초안까지만 다룹니다.
6. 정상 LLM 호출은 Provider, 모델, 지연 시간을 Trace에 기록합니다.
7. 현재 오류 응답은 FastAPI `detail` 형식이며, 실패 Trace의 Provider·모델·지연
   시간을 일관되게 기록하는 작업은 후속 확장 항목입니다.

## 실행 모드 구분

환경변수 하나가 모든 연동 방식을 결정하지 않습니다.

| 환경변수 | 역할 | 예 |
| --- | --- | --- |
| `APP_MODE` | 실제 외부 호출을 허용할지 결정 | `mock`, `real` |
| `LLM_PROVIDER` | 사용할 LLM Provider 선택 | `mock`, `openai`, `gemini`, `ollama` |
| `STORAGE_MODE` | Agent 실행과 Memory 저장소 선택 | `memory`, `postgres` |
| `LLM_FALLBACK_ENABLED` | Primary Provider 실패 시 fallback 허용 | `false`, `true` |
| `LLM_FALLBACK_PROVIDER` | fallback으로 사용할 Provider | `mock` |

예를 들어 `APP_MODE=real`만 설정해도 PostgreSQL이나 Ollama가 자동으로 실행되지는
않습니다. 선택한 Provider의 API Key 또는 Local 서비스와, 선택한 Storage의 연결
주소를 각각 준비해야 합니다.

## 권장 전환 순서

```text
APP_MODE=mock + LLM_PROVIDER=mock + STORAGE_MODE=memory
→ 실제 LLM + Memory 저장소
→ 실제 LLM + PostgreSQL
→ Primary Provider 실패 + 명시적 fallback
```

한 번에 한 축만 변경해야 실패 원인이 LLM, Database, Redis, 네트워크 중 어디에
있는지 구분할 수 있습니다.
