# 03. Prompt Recipes

Codex에게 요청할 때는 한 번에 모든 것을 맡기지 않습니다. 원인 분석, 수정 계획, 최소 수정, 검증을 나누어 요청합니다.

## 공통 입력 형식

```text
상황:

파일:
C:\aidev\02_supabase-ai-backend\...

실행 위치:
C:\aidev\02_supabase-ai-backend\...

실행 명령:
...

기대 결과:
...

실제 결과:
...

오류 메시지:
...

요청:
1. 가능한 원인을 우선순위로 정리해주세요.
2. 아직 파일은 수정하지 마세요.
3. 먼저 확인할 명령과 파일을 알려주세요.
```

## 1. 원인 분석만 요청

```text
아래 오류를 분석해주세요.
아직 코드는 수정하지 말고, 가능한 원인과 확인 순서만 알려주세요.
초보자가 이해할 수 있도록 실행 위치, 가상환경, 파일 경로 관점으로 설명해주세요.
```

## 2. 최소 수정 요청

```text
위 원인 분석을 바탕으로 최소 범위만 수정해주세요.
관련 없는 리팩토링은 하지 말아주세요.
수정한 파일 목록과 수정 후 실행할 검증 명령을 함께 알려주세요.
```

## 3. FastAPI 404, 405, 422 분석

```text
FastAPI에서 아래 응답이 나왔습니다.
404, 405, 422 중 어떤 유형인지 구분하고 원인을 설명해주세요.
Swagger에서 어떤 Method와 Body로 다시 호출해야 하는지도 알려주세요.
아직 코드는 수정하지 마세요.
```

## 4. .env와 API key 오류 분석

```text
.env 또는 API key 관련 오류를 분석해주세요.
실제 key는 모두 ***로 가렸습니다.
어느 폴더의 .env를 읽고 있는지, 환경변수 이름이 맞는지, placeholder 값인지 확인하는 순서를 알려주세요.
```

## 5. Supabase 테이블/RLS 오류 분석

```text
Supabase 요청이 실패했습니다.
테이블명, 컬럼명, schema.sql 실행 여부, anon key/service role key 구분, RLS 정책 순서로 원인을 점검해주세요.
아직 SQL이나 Python 파일은 수정하지 마세요.
```

## 6. Bearer token 인증 오류 분석

```text
Authorization Bearer token 관련 오류를 분석해주세요.
로그인 응답에서 access_token을 받았는지, Swagger Authorize에 넣었는지,
FastAPI가 token을 어떻게 읽고 Supabase Auth에 확인하는지 순서대로 설명해주세요.
```

## 7. Redis 캐시/TTL 오류 분석

```text
Redis 캐시가 기대대로 동작하지 않습니다.
Upstash REST URL/token, Redis key 이름, TTL 만료, 같은 질문 재호출 여부를 기준으로 확인 순서를 알려주세요.
Data Browser에서 어떤 key를 찾아야 하는지도 설명해주세요.
```

## 8. 코드 리뷰 요청

```text
아래 코드를 리뷰해주세요.
문제점은 치명도 순서로 먼저 알려주고, 수정 제안은 그 다음에 알려주세요.
검토 관점은 FastAPI endpoint, Pydantic 모델, 환경변수, key 보안, Supabase/RLS, Redis, 테스트입니다.
아직 파일은 수정하지 마세요.
```

## 9. 리팩토링 계획 요청

```text
이 단일 파일 FastAPI 코드를 router/schema/service 구조로 나누고 싶습니다.
먼저 새 폴더 구조와 파일별 역할만 제안해주세요.
아직 코드는 만들지 마세요.
초보자가 따라 할 수 있도록 단계별로 나누어 주세요.
```

## 10. 수정 후 검증 요청

```text
방금 수정한 내용이 제대로 동작하는지 검증 계획을 세워주세요.
실행 명령, Swagger 호출 순서, pytest 명령, 확인해야 할 응답 값을 체크리스트로 정리해주세요.
```
