# Assignment 99 - Supabase DB Auth Mini Design

`03_supabase-db-and-auth`의 `00`~`06`에서 배운 내용을 바탕으로 작은 AI 백엔드 서비스 설계안을 작성하는 최종 과제입니다.

## 목표

- Supabase DB, Supabase Auth/JWT, Upstash Redis TTL 캐시를 하나의 서비스 설계로 통합할 수 있습니다.
- LLM 응답 생성 흐름을 mock-first와 Gemini SDK 실제 호출 구조로 구분해 설계할 수 있습니다.
- 이후 `90_ai-assisted-code-review-and-debugging`의 리뷰와 `99_final-backend-project`의 최종 프로젝트로 이어질 수 있는 설계 문서를 작성합니다.

## 프로젝트 주제 예시

아래 중 하나를 선택하거나 비슷한 난이도의 주제를 직접 정할 수 있습니다.

```text
1. 개인 학습 메모 AI 챗봇
2. 고객 문의 기록 챗봇
3. 회의록 요약 저장 서비스
4. 문서 기반 Q&A 기록 서비스
5. 서비스 로그 조회 API
```

## 제출물

아래 내용을 포함해 작성합니다.

```text
1. 프로젝트 주제
2. 사용자가 해결하려는 문제
3. 필요한 환경변수 목록
4. Supabase 테이블 구조
5. FastAPI endpoint 목록
6. Auth/JWT/Bearer token 적용 계획
7. simple_chat_logs 또는 확장 테이블 저장 흐름
8. Upstash Redis TTL 캐시 설계
9. mock 응답과 Gemini SDK 응답을 구분하는 기록 기준
10. 예상 오류와 대응 방법
11. 이후 확장할 기능
```

## 제출 문서 권장 구조

```text
# 프로젝트명

## 1. 서비스 개요
## 2. 사용자 흐름
## 3. 환경변수와 보안 기준
## 4. 데이터베이스 설계
## 5. API 설계
## 6. Auth/JWT/Bearer Token 흐름
## 7. Redis TTL 캐시 설계
## 8. LLM 호출과 응답 저장
## 9. 오류 처리와 검증 계획
```

## 확인 기준

- 서비스 주제가 명확합니다.
- 데이터 저장 위치가 Supabase와 Redis로 구분되어 있습니다.
- JWT/Bearer token 기반 보호 API 계획이 포함되어 있습니다.
- 구현 가능한 수준의 API 목록이 작성되어 있습니다.
- `simple_chat_logs` 또는 확장 테이블 저장 기준이 포함되어 있습니다.
- `actual_api_called=false`인 mock 응답과 실제 Gemini SDK 응답 저장 기준이 포함되어 있습니다.
