# Assignment 07 - Integrated DB Auth Cache Plan

`00`~`06`에서 배운 Supabase DB, Supabase Auth, Upstash Redis TTL 캐시를 하나의 AI 백엔드 흐름으로 연결해 보는 통합 설계 과제입니다.

## 목표

- 환경변수, DB 저장, Auth/JWT, 로그 저장, Redis 캐시를 하나의 흐름으로 설명할 수 있습니다.
- Supabase와 Redis의 역할을 겹치지 않게 나눌 수 있습니다.
- 사용자 요청이 들어왔을 때 어떤 순서로 기능이 실행되는지 설계할 수 있습니다.

## 제출물

아래 내용을 포함해 작성합니다.

```text
1. 전체 아키텍처 설명
2. 필요한 환경변수 목록
3. 사용자 요청 처리 순서
4. Supabase Auth 역할
5. JWT/Bearer token 전달 방식
6. Supabase DB 역할
7. simple_chat_logs 저장 흐름
8. Upstash Redis TTL 캐시 역할
9. FastAPI endpoint 목록
10. 보안상 주의할 점
11. 예상 오류와 대응 방법
```

## 요청 처리 흐름 예시

```text
1. 사용자가 로그인한다.
2. 프론트엔드가 access token을 백엔드에 보낸다.
3. 백엔드는 Bearer token으로 현재 사용자를 확인한다.
4. Redis에서 같은 질문에 대한 임시 캐시가 있는지 확인한다.
5. 캐시가 없으면 mock 응답 또는 Gemini SDK 응답을 생성한다.
6. 응답을 simple_chat_logs에 저장한다.
7. 필요하면 응답을 Redis에 TTL과 함께 저장한다.
8. 사용자에게 JSON 응답을 반환한다.
```

## 확인 기준

- Supabase와 Redis의 역할이 겹치지 않습니다.
- 보안 key의 사용 위치가 올바릅니다.
- JWT/Bearer token 흐름이 포함되어 있습니다.
- `simple_chat_logs` 저장 기준이 포함되어 있습니다.
- 오류 상황을 최소 3개 이상 정리했습니다.
