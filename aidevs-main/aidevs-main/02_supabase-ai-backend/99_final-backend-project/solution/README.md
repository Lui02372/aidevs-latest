# Solution

이 폴더는 `99_final-backend-project`의 참고용 solution입니다.

주제는 **상품 설명 생성 API**입니다. 초보자가 최종 프로젝트에서 꼭 보여 주어야 하는 흐름을 작게 묶었습니다.

```text
FastAPI
-> Pydantic 요청 검증
-> routers/services/schemas 구조 분리
-> mock AI 설명 생성
-> 상품 목록과 서비스 로그 저장
-> Swagger UI 테스트
```

## 폴더 구조

```text
solution
├─ README.md
├─ .env.example
├─ requirements.txt
├─ pytest.ini
├─ schema.sql
├─ app
│  ├─ core
│  │  └─ config.py
│  ├─ routers
│  │  └─ product_router.py
│  ├─ schemas
│  │  └─ product_schema.py
│  ├─ services
│  │  ├─ ai_service.py
│  │  └─ storage_service.py
│  └─ main.py
└─ tests
   └─ test_app_routes.py
```

## 실행 방법

처음 실행할 때 필요한 패키지가 없다면 아래 명령으로 설치합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r .\99_final-backend-project\solution\requirements.txt
```

서버 실행은 solution 폴더에서 진행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\99_final-backend-project\solution
..\..\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

확인 주소:

```text
http://127.0.0.1:8000/docs
```

## 제공 API

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/health` | 서버 상태 확인 |
| POST | `/products` | 상품 등록 |
| GET | `/products` | 상품 목록 조회 |
| POST | `/products/{product_id}/ai-description` | mock AI 상품 설명 생성 |
| GET | `/service-logs` | 서비스 로그 조회 |

## 기본 실행 기준

Supabase 환경변수가 없으면 메모리에 데이터를 저장합니다. 그래서 수강생은 Supabase 연결 전에 FastAPI와 Swagger 흐름부터 바로 확인할 수 있습니다.

## Supabase 선택 연결

Supabase까지 연결하려면 `schema.sql`을 Supabase SQL Editor에서 실행한 뒤, `02_supabase-ai-backend\.env`에 아래 값을 설정합니다.
값의 예시는 `.env.example`에서 확인할 수 있습니다.

```text
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

주의:

- `SUPABASE_SERVICE_ROLE_KEY`는 백엔드에서만 사용합니다.
- 이 값을 프론트엔드, README, 제출 문서, 화면 캡처에 노출하지 않습니다.

## 수강생에게 설명할 포인트

- 처음에는 메모리 저장으로 API 흐름을 확인합니다.
- 이후 Supabase 환경변수를 넣으면 같은 API가 Supabase 테이블을 사용할 수 있습니다.
- 실제 LLM 호출은 필수가 아닙니다. 이 solution은 비용이 들지 않도록 mock AI 응답을 사용합니다.
- Gemini 실제 호출은 선택 확장으로만 연결합니다.
- 구조가 길어졌을 때 `router`, `schema`, `service`로 나누는 기준을 확인할 수 있습니다.
