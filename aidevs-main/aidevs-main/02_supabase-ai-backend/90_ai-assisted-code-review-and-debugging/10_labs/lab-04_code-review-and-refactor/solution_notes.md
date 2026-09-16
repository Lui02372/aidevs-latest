# Lab 04 Solution Notes

## 리뷰에서 나와야 할 핵심 문제

- `main.py` 역할과 router/service/schema 역할이 한 파일에 섞여 있습니다.
- 전역 list는 서버 재시작 시 데이터가 사라집니다.
- 응답 모델이 없어 Swagger 문서가 덜 명확합니다.
- 오류 응답 형식이 다른 예제와 통일되어 있지 않습니다.
- 리팩토링 전후 기능 유지 기준으로 테스트는 좋은 출발점입니다.

## 추천 리팩토링 순서

1. `schemas/product_schema.py`에 Pydantic 모델을 분리합니다.
2. `services/product_service.py`에 memory 저장 로직을 분리합니다.
3. `routers/product_router.py`에 endpoint를 분리합니다.
4. `main.py`는 app 생성과 router 연결만 남깁니다.
5. `python -m pytest tests`로 기존 기능이 유지되는지 확인합니다.

## 좋은 프롬프트 포인트

처음부터 "리팩토링해줘"라고 하지 말고, 먼저 문제점 리뷰와 단계별 계획을 요청합니다.
