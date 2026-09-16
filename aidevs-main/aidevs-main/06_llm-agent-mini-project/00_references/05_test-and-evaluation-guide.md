# 05 Test And Evaluation Guide

에이전트 시험 결과 보고서는 Agent가 실제로 안정적으로 동작하는지 보여주는 문서입니다.

## 필수 테스트 시나리오

| 시나리오 | 입력 예시 | 기대 결과 |
| --- | --- | --- |
| 정상 일정 요청 | "민수, 지영과 내일 30분 회의 잡아줘" | 가능한 시간 제안 |
| 정보 부족 | "회의 잡아줘" | 참석자나 날짜를 추가 질문 |
| 일정 충돌 | 모든 참석자가 가능한 시간이 없음 | 대체 날짜 또는 시간 축소 제안 |
| Tool 오류 | 일정 조회 Tool 실패 | 재시도 또는 fallback |
| 응답 불일치 | Tool 결과와 답변이 다름 | Self-Reflection 후 수정 |

## 평가 지표 예시

| 지표 | 의미 |
| --- | --- |
| task_completion_rate | 요청을 끝까지 처리한 비율 |
| tool_selection_accuracy | 필요한 Tool을 올바르게 선택한 비율 |
| response_consistency_score | Tool 결과와 최종 응답이 일치하는 정도 |
| average_retry_count | 평균 재시도 횟수 |
| fallback_rate | fallback으로 종료된 비율 |

## 비교 방식

Self-Reflection 적용 전후를 비교합니다.

| 버전 | 설명 |
| --- | --- |
| v1 | 기본 Tool 호출만 있는 버전 |
| v2 | 오류 감지와 재시도 추가 |
| v3 | Self-Reflection과 fallback 추가 |

보고서에는 완벽한 수치보다 **어떤 오류가 있었고, 어떻게 수정했고, 결과가 어떻게 좋아졌는지**가 드러나는 것이 중요합니다.
