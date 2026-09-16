# 02 Agent Architecture Guide

에이전트 아키텍처 설계서는 구현 전에 Agent의 판단 흐름을 문서로 정리하는 산출물입니다.

## 권장 StateGraph 흐름

```text
START
-> analyze_request
-> decide_tool
-> call_tool
-> review_result
-> reflect_or_answer
-> END
```

## Node 역할 예시

| Node | 역할 |
| --- | --- |
| `analyze_request` | 사용자 요청에서 참석자, 날짜 범위, 회의 길이, 제약 조건을 추출합니다. |
| `decide_tool` | 현재 State를 보고 어떤 Tool이 필요한지 결정합니다. |
| `call_tool` | 선택된 Tool을 실행하고 결과를 State에 저장합니다. |
| `review_result` | Tool 결과가 충분한지, 최종 답변과 충돌하지 않는지 검증합니다. |
| `reflect_or_answer` | 오류가 있으면 수정 전략을 고르고, 충분하면 최종 응답을 만듭니다. |

## State 필드 예시

| 필드 | 타입 예시 | 설명 |
| --- | --- | --- |
| `messages` | `list[dict]` | 사용자와 Agent의 대화 기록입니다. |
| `user_request` | `str` | 현재 처리할 사용자 요청입니다. |
| `participants` | `list[str]` | 일정 조정 대상자입니다. |
| `date_range` | `str` | 사용자가 요청한 날짜 범위입니다. |
| `required_tools` | `list[str]` | 필요하다고 판단한 Tool 목록입니다. |
| `tools_called` | `list[str]` | 실제 호출한 Tool 목록입니다. |
| `tool_results` | `dict` | Tool 실행 결과입니다. |
| `error_count` | `int` | 오류 또는 재시도 횟수입니다. |
| `iteration` | `int` | Agent 반복 실행 횟수입니다. |
| `reflection_notes` | `list[str]` | 자기 성찰 결과입니다. |
| `final_answer` | `str` | 사용자에게 보여줄 최종 응답입니다. |

## 분기 조건 예시

| 조건 | 다음 흐름 |
| --- | --- |
| 참석자 또는 날짜가 없음 | 추가 질문 생성 |
| 일정 조회가 필요함 | `call_tool` |
| Tool 결과가 비어 있음 | fallback 또는 대체 날짜 제안 |
| Tool 결과와 답변이 불일치함 | `reflect_or_answer`에서 수정 |
| 오류 횟수가 기준 이상임 | 안전한 fallback 응답 후 종료 |

## 설계서에 반드시 넣을 내용

- StateGraph Node와 Edge 목록
- 각 Node의 입력과 출력
- 분기 조건과 fallback 기준
- Tool 호출 흐름
- 단기 기억과 장기 기억을 사용할 경우의 연결 방식
- State 필드의 타입과 역할
