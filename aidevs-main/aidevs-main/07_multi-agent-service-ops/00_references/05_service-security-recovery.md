# 서비스·보안·복구

```text
Frontend → Backend → Redis Queue → Worker → Agent·Tool
                                      ↓
                               PostgreSQL Trace
```

- Backend는 인증·검증·Task 접수를 담당합니다.
- Worker는 Multi-Agent Workflow를 실행합니다.
- Redis는 짧은 Task 상태와 Queue를 담당합니다.
- PostgreSQL은 실행 이력과 Handoff를 보존합니다.
- Tool 실행 전 allowlist와 사용자 승인을 검사합니다.
- 복구 후 Health Check를 통과해야 성공으로 기록합니다.

