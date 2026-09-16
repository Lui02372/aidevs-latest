# 99_final-backend-project

이 단원은 `02_supabase-ai-backend`의 최종 프로젝트 안내입니다.

새로운 대규모 예제를 추가로 배우는 단원이 아니라, `01_fastapi-backend`, `02_llm-api-integration`, `03_supabase-db-and-auth`에서 배운 내용을 작은 백엔드 서비스 하나로 정리합니다.

## 프로젝트 목표

수강생은 아래 흐름을 설명하고 실행할 수 있어야 합니다.

```text
사용자 요청
-> FastAPI endpoint
-> Pydantic 검증
-> mock 또는 Gemini 응답 생성
-> Supabase 저장
-> Swagger UI 테스트
-> 오류/보안 점검 기록
```

## 추천 주제

시간이 부족한 초보자 과정이므로 주제는 단순하게 잡습니다.

```text
AI 학습 메모 백엔드
AI 질문 답변 기록 API
상품 설명 생성 API
간단한 상담 로그 API
```

## 필수 포함 요소

| 항목 | 기준 |
| --- | --- |
| FastAPI | 서버가 실행되고 `GET /health`가 동작합니다. |
| endpoint | 최소 3개 이상의 API가 있습니다. |
| Pydantic | 요청 Body를 모델로 검증합니다. |
| LLM 흐름 | mock 응답 또는 Gemini SDK 응답 중 하나를 사용합니다. |
| Supabase | 최소 1개 테이블에 데이터를 저장하거나 조회합니다. |
| 로그 | 요청/응답 또는 오류 기록을 남깁니다. |
| Swagger 결과 | `/docs`에서 실행한 결과를 문서에 정리합니다. |
| 보안 | `.env`는 제출하지 않고, `.env.example`만 제공합니다. |

## 선택 포함 요소

| 항목 | 설명 |
| --- | --- |
| Gemini 실제 호출 | API key와 비용 제한을 확인한 뒤 적용합니다. |
| Upstash Redis | 같은 질문에 대한 짧은 TTL 캐시를 적용합니다. |
| Auth/JWT/RLS | 로그인 사용자별 데이터 접근 제어를 적용합니다. |
| 구조 분리 | `app/main.py`, `app/schemas.py`, `app/repository.py`처럼 파일을 나눕니다. |
| pytest | 핵심 API에 대한 테스트를 추가합니다. |

## 권장 endpoint 예시

```text
GET /health
POST /items
GET /items
POST /ai/answer
GET /logs
```

주제가 상품 설명 생성 API라면 예시는 이렇게 바꿀 수 있습니다.

```text
GET /health
POST /products
GET /products
POST /products/{product_id}/ai-description
GET /service-logs
```

## 제출 폴더 예시

```text
my-final-backend-project
├─ README.md
├─ .env.example
├─ requirements.txt
├─ app
│  └─ main.py
└─ docs
   ├─ 01_project-plan.md
   ├─ 02_api-design.md
   ├─ 03_db-design.md
   ├─ 04_env-security-checklist.md
   ├─ 05_swagger-test-result.md
   └─ 06_troubleshooting-log.md
```

처음에는 `app/main.py` 하나로 시작해도 됩니다. 시간이 남거나 코드가 길어질 때만 구조 분리를 선택 확장으로 진행합니다.

## 진행 순서

1. `templates/01_project-plan.md`로 주제와 필수 기능을 정합니다.
2. `templates/02_api-design.md`로 endpoint와 요청/응답 예시를 적습니다.
3. `templates/03_db-design.md`로 Supabase 테이블을 정리합니다.
4. `starter/app/main.py`를 복사해 `GET /health`부터 실행합니다.
5. mock 응답으로 API 흐름을 먼저 완성합니다.
6. 필요하면 Gemini SDK 호출을 연결합니다.
7. Supabase 저장을 연결합니다.
8. Swagger UI에서 실행 결과를 캡처하거나 문서로 정리합니다.
9. `90_ai-assisted-code-review-and-debugging` 체크리스트로 리뷰합니다.
10. `.env`가 제출되지 않는지 마지막으로 확인합니다.

## 참고 solution

막혔을 때는 `solution` 폴더를 참고합니다. `solution`은 정답을 그대로 제출하라는 의미가 아니라, 작은 최종 프로젝트를 어떤 구조와 흐름으로 끝까지 연결할 수 있는지 보여 주는 기준 구현입니다.

```text
solution
├─ README.md
├─ schema.sql
└─ app
   ├─ core
   ├─ routers
   ├─ schemas
   ├─ services
   └─ main.py
```

## 최종 프로젝트 체크리스트

제출 전에는 [checklist/final-project-checklist.md](./checklist/final-project-checklist.md)를 보면서 전체 프로젝트가 실행, API 설계, DB 연결, 보안, 문서화 기준을 충족하는지 확인합니다.

핵심은 기능을 많이 넣는 것이 아니라, 작은 백엔드 서비스를 끝까지 설명하고 실행할 수 있는 것입니다.
