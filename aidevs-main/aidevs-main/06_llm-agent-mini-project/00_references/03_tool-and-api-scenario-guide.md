# 03 Tool And API Scenario Guide

이 프로젝트의 Tool은 Agent가 외부 기능을 사용하기 위한 Python 함수입니다. 처음에는 실제 API 대신 Mock data로 구현하고, 시간이 남으면 실제 API로 교체합니다.

## 기본 Tool 예시

| Tool | 입력 | 출력 | 실패 상황 |
| --- | --- | --- | --- |
| `check_calendar_tool` | 참석자, 날짜 범위 | 참석자별 일정 목록 | 참석자 누락, 날짜 범위 누락 |
| `find_available_slot_tool` | 일정 목록, 회의 길이 | 가능한 시간 후보 | 가능한 시간이 없음 |
| `draft_invitation_tool` | 선택 시간, 참석자 | 초대 메시지 초안 | 선택 시간이 없음 |
| `summarize_decision_tool` | Tool 결과, 제약 조건 | 결정 근거 요약 | 결과가 불충분함 |

## Mock data로 시작하는 이유

실제 Calendar API를 처음부터 연결하면 인증, API Key, 권한, 쿼터, 네트워크 오류 때문에 Agent 흐름을 이해하기 전에 막힐 수 있습니다.

따라서 프로젝트 초반에는 다음 순서로 진행합니다.

```text
Mock 일정 데이터 준비
-> Tool 함수 단독 실행
-> LangGraph Node에서 Tool 호출
-> Tool 결과를 State에 저장
-> 최종 응답 생성
-> 실제 API 연결은 선택 확장
```

## Tool 설계 질문

- 이 Tool이 없으면 Agent가 문제를 해결할 수 없는가?
- 입력값은 State에서 가져올 수 있는가?
- 출력값은 다음 Node가 바로 사용할 수 있는가?
- 실패했을 때 재시도할 것인가, fallback할 것인가?
- Tool 결과가 최종 답변에 어떻게 반영되는가?

## API 연결 선택 예시

| API | 적용 예시 |
| --- | --- |
| Google Calendar API | 실제 일정 조회 |
| Notion API | 프로젝트 일정 또는 회의록 조회 |
| 공공 API | 휴일, 날씨, 교통 정보 반영 |
| 자체 FastAPI | 팀이 만든 일정 데이터 API 연결 |

실제 API 연결은 필수가 아닙니다. 필수는 Tool 흐름과 Agent 판단 구조를 설명하고 검증하는 것입니다.
