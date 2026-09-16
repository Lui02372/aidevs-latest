# Assignment 02 - Schema Design And SQL

Supabase SQL Editor에서 사용할 필수 테이블 구조를 이해하고 설명하는 과제입니다.

현재 필수 범위는 `learning_notes`와 `simple_chat_logs`입니다. `conversations`, `messages`, `service_logs`는 이후 확장 구조로만 간단히 언급합니다.

## 목표

- `learning_notes` 테이블이 CRUD 실습에 왜 필요한지 설명할 수 있습니다.
- `simple_chat_logs` 테이블이 AI 질문/답변 저장에 왜 필요한지 설명할 수 있습니다.
- 테이블 컬럼과 Python/FastAPI 코드의 연결을 설명할 수 있습니다.

## 제출물

아래 내용을 포함한 설계 문서를 작성합니다.

```text
1. learning_notes 테이블 목적
2. learning_notes 컬럼 목록과 의미
3. simple_chat_logs 테이블 목적
4. simple_chat_logs 컬럼 목록과 의미
5. SQL Editor 실행 결과 요약
6. Supabase Table Editor에서 확인한 테이블 목록
7. conversations/messages/service_logs를 나중에 확장할 때 사용하는 이유
8. 테이블이 없을 때 발생할 수 있는 오류 예시
```

## 참고 SQL

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\00_references\supabase-schema.sql
```

## 확인 기준

- 필수 테이블 2개의 역할을 구분했습니다.
- 각 컬럼의 의미를 코드 흐름과 연결했습니다.
- 확장 참고 테이블을 필수 구현으로 착각하지 않았습니다.
- SQL 파일이나 제출 문서에 실제 API key를 넣지 않았습니다.
