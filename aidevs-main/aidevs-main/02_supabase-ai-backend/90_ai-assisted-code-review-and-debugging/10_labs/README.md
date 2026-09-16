# 10_labs

이 폴더는 앞 단원에서 자주 나오는 오류를 직접 재현하고, Codex에게 단계적으로 질문해 수정하는 실습입니다.

| Lab | 주제 |
| --- | --- |
| `lab-01_import-env-fastapi-error` | import, 가상환경, 실행 위치, `.env` 문제 |
| `lab-02_api-debugging-404-422` | FastAPI 404, 405, 422와 Swagger 호출 |
| `lab-03_supabase-auth-redis-error` | Supabase table, Bearer token, RLS, Redis TTL |
| `lab-04_code-review-and-refactor` | 코드 리뷰와 router/schema/service 리팩토링 |

실습 목적은 오류를 모두 외우는 것이 아니라, 오류를 재현하고 정보를 정리해서 좋은 질문을 만드는 습관을 만드는 것입니다.

각 lab은 아래 순서로 진행합니다.

```text
1. broken 또는 messy 코드 실행
2. 오류 또는 문제점 기록
3. README의 1차 프롬프트를 Codex에게 전송
4. 원인 분석을 검토
5. 2차 프롬프트로 최소 수정 요청
6. 다시 실행하거나 테스트
7. solution_notes.md와 비교
```
