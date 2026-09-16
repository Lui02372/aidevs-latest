# assignment-100_product-api-structure-refactor

`lab-100_project-structure-refactor`에서 연습한 구조 분리를 메모가 아닌 **상품(Product) API** 주제로 직접 적용합니다.

이 과제는 단일 `main.py`에 모든 코드를 넣는 방식에서 벗어나 `routers`, `schemas`, `services`로 역할을 나누는 연습입니다.

## 목표

```text
starter/app/main.py:
  FastAPI 앱 생성과 router 연결

starter/app/routers/product_router.py:
  API 경로와 HTTP Method 정의

starter/app/schemas/product_schema.py:
  요청/응답 Pydantic 모델 정의

starter/app/services/product_service.py:
  상품 데이터 조회, 검색, 생성 로직

starter/tests/test_product_api.py:
  TestClient로 API 동작 검증
```

## 폴더 구조

```text
assignment-100_product-api-structure-refactor
├─ README.md
├─ starter
│  ├─ app
│  └─ tests
└─ solution
   ├─ app
   └─ tests
```

먼저 `starter` 폴더의 TODO를 완성합니다. 수업 후 또는 복습할 때 `solution` 폴더와 비교합니다.

## 실행 방법

과정 가상환경을 활성화합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

starter 폴더로 이동해 서버를 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\20_assignments\assignment-100_product-api-structure-refactor\starter
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 테스트 실행

```powershell
python -m pytest -s
```

처음에는 TODO가 남아 있어 테스트가 실패할 수 있습니다. 실패 메시지를 보고 `app/services`, `app/routers`, `app/schemas`를 하나씩 완성합니다.

solution을 확인하려면 아래처럼 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\20_assignments\assignment-100_product-api-structure-refactor\solution
python -m pytest -s
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

## 구현 요구사항

1. `GET /health`는 `{"status": "ok"}`를 반환합니다.
2. `GET /products`는 전체 상품 목록과 개수를 반환합니다.
3. `GET /products/search?keyword=...`는 상품명 또는 설명에 keyword가 포함된 상품을 반환합니다.
4. `GET /products/{product_id}`는 상품 1개를 반환합니다.
5. 없는 상품 id를 조회하면 404를 반환합니다.
6. `POST /products`는 새 상품을 생성하고 201 상태 코드를 반환합니다.
7. 새 상품의 `name`, `description`은 빈 문자열을 허용하지 않습니다.
8. 새 상품의 `price`는 0보다 커야 합니다.

## 제출 기준

아래 항목을 README에 정리합니다.

```text
1. 실행 명령
2. 구현한 API 목록
3. 요청/응답 예시
4. 테스트 실행 결과
5. 구조를 나누면서 이해한 점
```

## 점검 질문

```text
구조:
  app/main.py는 router 연결만 담당하는가?

Router:
  API 경로와 HTTP Method가 product_router.py에 모여 있는가?

Schema:
  요청 모델과 응답 모델이 product_schema.py에 분리되어 있는가?

Service:
  데이터 조회, 검색, 생성 로직이 product_service.py에 분리되어 있는가?

Test:
  python -m pytest -s로 테스트가 통과하는가?
```
