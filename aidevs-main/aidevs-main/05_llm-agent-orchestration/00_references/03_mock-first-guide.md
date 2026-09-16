# Mock First 가이드

## 목적

API Key, 네트워크, 외부 서비스 상태와 무관하게 핵심 흐름을 학습하고 테스트합니다.

## 세 단계

```text
고정 Mock 결과
→ 실제 LLM + Mock Tool
→ 실제 LLM + 선택적 실제 조회 API
```

## Mock이 필요한 대상

- LLM 응답
- 날씨·숙소·관광지 Tool
- 예약 요청
- Vector Search
- 사용자 Memory 저장소

## 규칙

- Mock 결과에도 실제 응답과 같은 Schema를 사용합니다.
- 현재 기본 예제는 결정적인 정상 Mock 결과를 제공합니다.
- timeout, 빈 결과, 잘못된 Schema는 Lab과 테스트에서 실패 Mock으로 추가합니다.
- 테스트에서는 현재 날짜나 네트워크에 의존하지 않습니다.

## 정상 Mock과 실패 Mock

| 구분 | 목적 | 현재 과정에서의 위치 |
| --- | --- | --- |
| 정상 Mock | Agent 계약과 기본 흐름을 반복 검증 | 기본 예제와 Backend |
| timeout Mock | 제한 시간과 retry·fallback 검증 | Lab·테스트 확장 |
| 빈 결과 Mock | 정보 부족과 사용자 재질문 검증 | Lab·테스트 확장 |
| 잘못된 Schema Mock | Pydantic 검증 실패와 복구 검증 | Lab·테스트 확장 |
| Tool 실패 Mock | 부분 실패와 안전한 종료 검증 | Tool·평가 Lab |

Mock은 실제 서비스가 항상 성공한다고 가정하기 위한 것이 아닙니다. 먼저 정상
기준선을 만든 뒤 실패를 한 종류씩 통제해서 재현하는 도구로 사용합니다.
