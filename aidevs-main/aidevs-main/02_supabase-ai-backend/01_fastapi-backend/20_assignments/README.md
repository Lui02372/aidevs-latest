# 20_assignments

이 폴더는 `01_fastapi-backend` 단원의 제출 과제 모음입니다.

수업 중 실습인 `10_labs`가 단계별 연습이라면, 이 폴더의 과제는 같은 내용을 스스로 정리해 제출하는 용도입니다. 대부분의 과제는 앞 단원에서 정리한 **메모 API 흐름**을 기준으로 구성합니다.

마지막 `assignment-100_product-api-structure-refactor`는 `lab-100_project-structure-refactor`에서 배운 구조 분리를 다른 주제인 **상품 API**에 적용하는 과제입니다.

## 과제 목록

| 순서 | 폴더 | 연결 단원 | 제출 주제 |
| --- | --- | --- | --- |
| 1 | `assignment-01_memo-health-and-routing` | `01~02` | 서버 상태 확인, 메모 목록/단건 조회, 검색 |
| 2 | `assignment-02_memo-crud-api` | `02_routing-and-request` | 메모 생성, 수정, 삭제 |
| 3 | `assignment-03_memo-validation-response` | `03_pydantic-and-response` | 요청 검증, 응답 모델, 표준 응답 구조 |
| 4 | `assignment-04_async-external-context` | `04_async-and-external-api` | 비동기 외부 API 호출, 메모 컨텍스트 결합 |
| 99 | `assignment-99_fastapi-memo-mini-project` | `01_fastapi-backend 마무리` | 작은 메모 API 서버 완성 |
| 100 | `assignment-100_product-api-structure-refactor` | `10_labs/lab-100` 이후 | 상품 등록/조회 API를 프로젝트 구조로 분리 |

## 공통 제출 파일

각 과제 폴더 안에 아래 파일을 제출합니다.

```text
main.py
README.md
```

`starter.py`는 시작용 참고 파일입니다. 제출할 때는 완성한 코드를 `main.py`로 정리합니다.

단, `assignment-100_product-api-structure-refactor`는 구조 분리 과제이므로 아래 구조를 유지합니다.

```text
app/
  main.py
  routers/
  schemas/
  services/
tests/
README.md
```

## 공통 README 작성 기준

제출 README에는 다음 내용을 포함합니다.

```text
1. 과제 목표
2. 실행 방법
3. 구현한 API 목록
4. 요청 예시
5. 응답 예시
6. Swagger UI 테스트 결과
7. 어려웠던 점과 해결 방법
```

## 실행 기준

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

각 과제 폴더에서 실행합니다.

```powershell
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

구조 분리 과제인 `assignment-100_product-api-structure-refactor`는 아래처럼 실행합니다.

```powershell
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
python -m pytest -s
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 평가 기준

```text
실행 가능성:
  uvicorn main:app --reload로 실행되는가?
  # 위 명령에서 오류가 나면 아래처럼 실행합니다.
  python -m uvicorn main:app --reload로 실행되는가?

API 설계:
  URL과 HTTP Method가 의미에 맞게 사용되었는가?

요청 검증:
  Pydantic 모델로 잘못된 요청을 막는가?

응답 구조:
  프론트엔드가 처리하기 쉬운 일관된 응답 구조를 사용하는가?

오류 처리:
  없는 데이터 조회, 외부 API 실패 등을 HTTPException으로 처리하는가?

문서화:
  README만 보고 실행과 테스트가 가능한가?
```
