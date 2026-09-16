# 02. Code Review Checklist

최종 프로젝트로 넘어가기 전에 아래 항목을 빠르게 점검합니다.

## FastAPI

- endpoint URL이 리소스 중심으로 정리되어 있는가?
- HTTP Method가 의미에 맞는가?
- `GET /health` 같은 기본 확인 API가 있는가?
- 오류가 났을 때 초보자가 이해할 수 있는 메시지를 반환하는가?
- Swagger에서 테스트 순서를 설명할 수 있는가?
- `python -m uvicorn ...` 실행 명령이 README에 있는가?

## Pydantic

- 요청 Body 모델이 너무 느슨하지 않은가?
- 필수 값과 선택 값이 구분되어 있는가?
- 응답 형식이 예제마다 크게 흔들리지 않는가?
- `Field(min_length=...)`, 예시값, 타입 힌트가 적절한가?
- 중첩 JSON이 필요하다면 nested model로 분리되어 있는가?

## LLM API

- mock 호출과 실제 Gemini 호출이 구분되어 있는가?
- 모델명, provider, 실제 호출 여부를 기록하는가?
- API key를 코드에 직접 적지 않았는가?
- 비용이 커질 수 있는 무제한 반복 호출이 없는가?

## Supabase

- 테이블명과 컬럼명이 SQL 문서와 일치하는가?
- insert/select/update/delete 결과를 확인하는가?
- update/delete에는 조건이 있는가?
- service role key가 프론트엔드나 문서에 노출되지 않았는가?
- `SUPABASE_ANON_KEY`와 `SUPABASE_SERVICE_ROLE_KEY`의 역할이 구분되어 있는가?
- `schema.sql`을 언제 실행해야 하는지 README에 적혀 있는가?

## Auth/JWT/RLS

- 로그인 후 받은 access token을 Bearer token으로 보내는 흐름을 설명할 수 있는가?
- RLS를 켠 테이블은 어떤 사용자가 어떤 행을 볼 수 있는지 기준이 있는가?
- 초보자에게 너무 어려운 SQL은 선택 확장으로 분리되어 있는가?
- Swagger `Authorize`를 쓰는지, 직접 `Authorization` 헤더를 입력하는지 명확한가?
- `auth.uid() = user_id` 같은 정책의 의미가 문서화되어 있는가?

## Redis

- Redis는 영구 저장소가 아니라 캐시/TTL 용도라는 점이 드러나는가?
- key 이름이 충돌하지 않도록 설계되어 있는가?
- TTL이 필요한 데이터에 만료 시간이 설정되어 있는가?
- Upstash Data Browser에서 key를 확인하는 방법을 설명할 수 있는가?
- Redis가 없을 때 fallback이 있는지, 아니면 필수인지 명확한가?

## 보안

- `.env`는 Git에 올라가지 않는가?
- `.env.example`에는 예시 값만 있는가?
- 로그에 API key, JWT, 비밀번호, 개인정보가 들어가지 않는가?
- AI에게 질문하기 전에 key/token을 `***`로 마스킹했는가?
- service role key를 프론트엔드 코드에 넣지 않았는가?

## 테스트와 문서

- `python -m pytest tests` 실행이 가능한가?
- 실패하는 테스트가 있다면 의도적으로 실패하는 lab인지 명시되어 있는가?
- README의 실행 경로가 실제 폴더 구조와 맞는가?
- 수정 전/후 기록이 남아 있는가?
