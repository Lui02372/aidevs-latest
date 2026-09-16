# Lab 04. 코드 리뷰와 리팩토링

## 목표

동작은 하지만 구조가 지저분한 FastAPI 코드를 리뷰하고, router/schema/service 구조로 나누는 계획을 세웁니다.

이 lab의 `messy_product_api.py`는 일부러 다음 문제가 있습니다.

- 모든 코드가 한 파일에 있음
- 전역 list를 직접 조작함
- 요청/응답 모델이 부족함
- 오류 응답이 일관되지 않음
- 테스트는 있지만 구조 개선 여지가 큼

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\90_ai-assisted-code-review-and-debugging\10_labs\lab-04_code-review-and-refactor
..\..\..\.venv\Scripts\Activate.ps1
python -m uvicorn messy_product_api:app --reload --host 127.0.0.1 --port 8094
```

테스트:

```powershell
python -m pytest tests
```

## 1차 프롬프트

```text
아래 FastAPI 코드를 리뷰해주세요.
아직 수정하지 말고 문제점을 치명도 순서로 알려주세요.
검토 관점은 endpoint 설계, Pydantic 모델, 오류 처리, 전역 상태, 테스트 가능성, router/schema/service 분리입니다.
```

## 2차 프롬프트

```text
이 코드를 router/schema/service 구조로 나누는 리팩토링 계획을 세워주세요.
한 번에 모든 코드를 바꾸지 말고 단계별 수정 순서를 제안해주세요.
```

## 3차 프롬프트

```text
계획 중 1단계만 최소 수정으로 반영해주세요.
수정 후 python -m pytest tests가 통과해야 합니다.
```
