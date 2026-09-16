# 00_references

`04_supabase-ai-mini-project`의 참고 자료입니다.

이 폴더는 별도 실습 단원이 아니라, 프로젝트를 진행하면서 반복해서 확인하는 기준 문서 모음입니다.

## 문서 목록

```text
01_project-overview.md
02_sse-redis-db-guide.md
03_deployment-guide.md
04_reference-structure.md
```

## 먼저 확인할 내용

- 04 과정의 주제는 **AI 서비스 로그 분석 및 운영 대시보드 구축**입니다.
- DB, Redis, SSE는 역할이 다릅니다.
- DB는 로그와 피드백의 영구 저장소입니다.
- Redis는 새 로그 이벤트를 빠르게 전달하는 실시간 이벤트 통로입니다.
- SSE는 FastAPI가 프론트엔드로 실시간 이벤트를 보내는 방식입니다.
- 전체 프로젝트 구조는 `03_supabase-ai-frontend/99_final-frontend-project`의 backend/frontend 분리 구조를 참고합니다.
- 배포는 선택 적용이지만, 배포 가능한 구조를 염두에 두고 환경변수와 보안을 정리합니다.

## 확인 질문

```text
서비스 로그는 왜 저장해야 하나요?
DB와 Redis는 각각 어떤 역할을 하나요?
SSE는 WebSocket과 무엇이 다른가요?
프론트엔드는 Supabase service role key를 직접 가져도 되나요?
최종 산출물 4종은 무엇인가요?
```
