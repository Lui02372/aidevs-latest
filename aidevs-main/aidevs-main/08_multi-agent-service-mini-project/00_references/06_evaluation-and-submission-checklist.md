# 06. Evaluation And Submission Checklist

최종 제출 전 아래 항목을 확인합니다.

## 멀티 에이전트 아키텍처 설계서

- [ ] 아키텍처 구조가 응답 속도, 결정 일관성, 장애 격리 기준에 맞게 선택되었다.
- [ ] Planner/Supervisor, Executor, Critic/Validation, Memory/Reporter 등 Agent 역할과 책임이 명확하다.
- [ ] Agent 간 Handoff 시 상태, 메모리, 중간 결과가 누락 없이 전달된다.
- [ ] 공유 상태 객체의 필드가 문서화되어 있다.
- [ ] 예외 흐름과 fallback 흐름이 표현되어 있다.

## 배포 및 장애 복구 보고서

- [ ] Docker Compose 기반 멀티 서비스 구조가 작성되어 있다.
- [ ] 서비스 디스커버리, 포트, 환경변수, secret 관리 방식이 정리되어 있다.
- [ ] 네트워크, DB, API, LLM, 프롬프트 보안 장애 유형별 감지 기준이 있다.
- [ ] 장애 유형별 자동 복구 전략이 구현 또는 시뮬레이션되어 있다.
- [ ] Health Check 결과와 복구 성공/실패 결과가 기록되어 있다.
- [ ] AWS 배포 결과와 CloudWatch 로그 확인 결과가 포함되어 있다.
- [ ] 실습 후 리소스 삭제 결과가 기록되어 있다.

## 파이프라인 구현 결과 보고서

- [ ] code commit, build, test, deploy 단계가 다이어그램으로 표현되어 있다.
- [ ] 단위/통합 테스트 기준이 명시되어 있다.
- [ ] 테스트 실패 시 배포를 차단하는 정책이 있다.
- [ ] GitHub Actions 실행 결과가 첨부되어 있다.
- [ ] 알림 또는 에스컬레이션 구조가 정의되어 있다.

## 보안 점검

- [ ] `.env`가 GitHub에 올라가지 않았다.
- [ ] API Key, AWS Access Key, 비밀번호가 문서에 노출되지 않았다.
- [ ] 위험한 복구 명령이 Guardrail 기준으로 제한되어 있다.
- [ ] GitHub Actions 로그에 secret이 출력되지 않는다.
