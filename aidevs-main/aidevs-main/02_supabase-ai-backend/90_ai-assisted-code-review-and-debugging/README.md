# 90_ai-assisted-code-review-and-debugging

이 단원은 02 백엔드 과정의 마무리 실습입니다.

목표는 Codex에게 정답을 맡기는 것이 아니라, 오류를 재현하고 정보를 정리한 뒤 AI의 도움을 받아 원인을 좁히고 작은 단위로 수정하는 개발 흐름을 연습하는 것입니다.

## 핵심 루프

```text
오류 재현
-> 실행 위치, 명령어, 기대 결과, 실제 결과 기록
-> 민감 정보 마스킹
-> 1차 프롬프트: 원인 분석만 요청
-> 2차 프롬프트: 수정 계획 요청
-> 3차 프롬프트: 최소 수정 요청
-> 재실행과 테스트
-> 수정 전/후 기록
```

처음부터 "고쳐줘"라고 요청하지 않습니다. 먼저 원인을 설명하게 하고, 확인 명령을 받은 뒤, 필요한 범위만 수정합니다.

## 학습 목표

- Traceback, HTTP 오류, Supabase/RLS 오류를 재현하고 정리할 수 있습니다.
- Codex에게 원인 분석, 수정 계획, 최소 수정, 검증 요청을 단계별로 나눠 보낼 수 있습니다.
- FastAPI 404/405/422, `.env`, API key, Bearer token, RLS, Redis TTL 오류를 구분할 수 있습니다.
- 코드 리뷰 체크리스트를 사용해 보안, 비용, 구조, 테스트 관점에서 백엔드 코드를 점검할 수 있습니다.
- 프롬프트만으로 작은 백엔드 프로젝트를 단계적으로 설계, 생성, 검증, 수정할 수 있습니다.

## 진행 순서

```text
01_debugging-playbook.md
-> 02_code-review-checklist.md
-> 03_prompt-recipes.md
-> 04_prompt-driven-development.md
-> 10_labs
-> templates
```

## 실습 구성

| 구분 | 주제 | 핵심 활동 |
|---|---|---|
| Lab 01 | 실행 환경 문제 | import, venv, 실행 위치, `.env` 오류를 분석합니다. |
| Lab 02 | FastAPI/API 호출 문제 | 404, 405, 422를 Swagger와 요청 Body 기준으로 구분합니다. |
| Lab 03 | 외부 서비스 문제 | Supabase table, Bearer token, RLS, Redis TTL 오류를 정리합니다. |
| Lab 04 | 코드 리뷰와 리팩토링 | 지저분한 단일 파일 API를 리뷰하고 구조 개선 계획을 세웁니다. |
| 별도 문서 | 프롬프트 기반 프로젝트 생성 | 작은 백엔드 프로젝트를 단계별 프롬프트로 만들어 봅니다. |

## 민감 정보 원칙

Codex에게 오류를 물어볼 때 실제 API key, JWT, service role key, Redis token, 비밀번호를 붙여 넣지 않습니다.

```text
GEMINI_API_KEY=***
SUPABASE_SERVICE_ROLE_KEY=***
Authorization: Bearer ***
UPSTASH_REDIS_REST_TOKEN=***
```

## 필수 산출물

```text
1. 오류 분석 기록 1개
2. AI에게 보낸 프롬프트와 응답 요약 1개
3. 수정 전/후 비교 1개
4. 재실행 또는 테스트 검증 결과 1개
5. 보안 마스킹 체크 1개
```

제출 기록은 `templates/ai-debugging-session-template.md`와 `templates/before-after-fix-template.md`를 사용합니다.
