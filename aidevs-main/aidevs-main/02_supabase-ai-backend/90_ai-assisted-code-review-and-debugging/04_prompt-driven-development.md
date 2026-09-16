# 04. Prompt-driven Development

이 문서는 프롬프트만으로 작은 백엔드 프로젝트를 단계적으로 만드는 전략을 설명합니다.

핵심은 "한 번에 전체 프로젝트를 만들어줘"가 아닙니다. 요구사항 정리, API 설계, mock 구현, 테스트, 외부 서비스 연결, 리뷰를 나누어 요청합니다.

## 나쁜 방식

```text
FastAPI, Supabase, Redis, Gemini를 모두 쓰는 AI 백엔드 프로젝트를 만들어줘.
```

이 방식은 파일이 한꺼번에 많이 생기고, 실행이 안 될 때 어디서부터 고쳐야 할지 알기 어렵습니다.

## 좋은 방식

```text
요구사항 정리
-> API 목록
-> 데이터 모델
-> 폴더 구조
-> mock-first 구현
-> 테스트
-> Supabase/Auth/Redis/Gemini 연결
-> 코드 리뷰
-> README 작성
```

## 예제 주제: 미니 상품 Q&A API

처음에는 외부 서비스를 쓰지 않고 memory 저장소로 시작합니다.

필수 endpoint:

```text
GET /health
POST /products
GET /products
POST /products/{product_id}/questions
GET /products/{product_id}/questions
```

선택 확장:

```text
Supabase에 상품과 질문 저장
Bearer token으로 사용자 구분
Redis에 자주 묻는 질문 캐시
Gemini로 질문 답변 초안 생성
```

## Step 1. 요구사항을 API 목록으로 바꾸기

```text
미니 상품 Q&A API를 만들고 싶습니다.
아직 코드는 작성하지 말고, 필요한 endpoint 목록과 요청/응답 예시만 제안해주세요.
초보자 수업용이므로 기능은 5개 이하로 제한해주세요.
```

## Step 2. 폴더 구조 설계

```text
위 API를 FastAPI router/schema/service 구조로 만들려고 합니다.
폴더 구조와 파일별 역할을 제안해주세요.
아직 코드는 작성하지 말아주세요.
```

## Step 3. mock-first 구현

```text
외부 DB 없이 memory list를 사용해서 먼저 동작하는 FastAPI 코드를 만들어주세요.
파일은 app/main.py 하나로 시작하고, 실행 명령도 함께 알려주세요.
```

## Step 4. Pydantic 모델 분리

```text
현재 main.py 코드를 schema와 service로 나누고 싶습니다.
관련 없는 기능 추가는 하지 말고, 요청/응답 모델과 저장 로직만 분리해주세요.
수정 후 실행 명령과 테스트할 endpoint 순서도 알려주세요.
```

## Step 5. 테스트 추가

```text
이 FastAPI 앱에 pytest TestClient 테스트를 추가해주세요.
실제 서버를 띄우지 않고 /health, POST /products, GET /products를 확인하는 테스트만 작성해주세요.
```

## Step 6. Supabase 연결

```text
memory 저장소를 Supabase 저장소로 바꾸는 계획을 세워주세요.
먼저 schema.sql과 필요한 환경변수 목록만 제안해주세요.
service role key는 서버 .env에만 둔다는 보안 기준도 함께 적어주세요.
아직 코드는 수정하지 마세요.
```

## Step 7. Auth, Redis, Gemini 선택 확장

```text
현재 프로젝트에 Auth, Redis, Gemini 중 무엇을 먼저 붙이는 것이 좋은지 우선순위를 제안해주세요.
초보자 수업 기준으로 난이도와 실패 가능성을 함께 설명해주세요.
```

## Step 8. 코드 리뷰와 보안 점검

```text
이 프로젝트를 제출 전 리뷰해주세요.
FastAPI 구조, Pydantic 검증, .env 보안, service role key 노출, 테스트, README 실행 가이드 기준으로 문제를 찾아주세요.
아직 파일은 수정하지 마세요.
```

## 운영 원칙

- 한 프롬프트에는 한 목표만 담습니다.
- 계획을 먼저 받고, 코드는 그 다음에 요청합니다.
- mock으로 먼저 실행되게 만듭니다.
- 외부 서비스 연결은 마지막에 붙입니다.
- `.env`에는 실제 값을 넣지만, 프롬프트와 문서에는 절대 노출하지 않습니다.
- 수정 후에는 항상 실행 명령과 테스트 명령을 확인합니다.
