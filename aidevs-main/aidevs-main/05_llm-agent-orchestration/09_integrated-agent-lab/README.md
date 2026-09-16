# 09 Integrated Agent Lab

09는 08의 평가용 애플리케이션을 확장하는 장이 아닙니다. 01~08에서 배운 구성 요소를 별도의 통합 Mini Project로 조립하는 후속 실습입니다.

```text
01~05 Model·Prompt·Tool·RAG·Memory
→ 06 Agent Workflow
→ 07 Human Approval과 Safety
→ 08 기존 06·07 Agent 평가와 Trace
→ 09 별도 통합 Mini Project
```

현재 저장소에는 통합 Backend와 Frontend 구현을 복제하지 않습니다. 따라서 `C:\mini_agent_st\mini_agent_08_evaluation`을 전제로 한 실행 절차도 사용하지 않습니다. 통합 프로젝트의 위치와 실행 계약이 확정되면 이 장에 별도로 연결합니다.

## 통합 시 유지할 평가 계약

통합 Agent를 만들더라도 08의 평가 원리는 그대로 재사용합니다.

- 정상·정보 부족·Tool 오류 Scenario
- Tool 선택과 실행 순서
- 반복 및 종료 조건
- 승인 전 변경 금지와 승인 후 최대 한 번 실행
- 상태, 종료 이유와 Trace
- 기능 회귀 통과율과 Safety Gate

## 필수 확장

- 허용된 Mock Tool 하나 추가
- 정책 문서 하나 추가
- 정상 Scenario와 실패 Scenario 각각 하나 추가
- 추가한 기능의 Trace에서 실행 순서 설명

확장 전후에는 [최종 리뷰와 디버깅 체크리스트](./review-checklist.md)로 권한·근거·Trace·회귀 여부를 점검합니다.

## 제외 범위

- 실제 예약·결제·환불
- LLM Judge와 외부 평가 플랫폼
- Docker Compose와 AWS 배포
- Multi-Agent

Docker Compose와 AWS EC2 배포는 후속 운영 과정에서 진행합니다.
