# 01. Project Overview

## 주제

```text
에러 자가 치유(Auto Healing) 워크플로우
```

08 프로젝트는 운영 중인 AI 서비스에서 장애가 발생했다고 가정하고, 여러 Agent가 협업하여 장애를 분류하고 복구 전략을 선택하며, 복구 결과를 검증하는 구조를 만드는 미니 프로젝트입니다.

## 필수 목표

1. 에이전트 협업 시나리오 및 구조 설계
2. 장애 유형별 복구 로직 및 자동화 파이프라인 구현
3. 헬스체크, 재시도, 대체 경로 기반 장애 대응 흐름 구현
4. 서비스 배포 및 결과 검증

## 최소 구현 범위

| 영역 | 구현 내용 |
| --- | --- |
| backend | 장애 이벤트 접수, Health Check, 복구 결과 조회 API |
| worker | 장애 유형 분류, 복구 전략 선택, 복구 실행 또는 시뮬레이션 |
| frontend | 장애 이벤트 입력, 결과 확인 화면 |
| monitor | 운영 로그, 복구 상태, 파이프라인 상태 확인 화면 |
| docker | Dockerfile, Docker Compose 실행 구조 |
| ci/cd | GitHub Actions 기반 테스트와 빌드 검증 |
| deploy | AWS 배포 결과와 리소스 정리 기록 |

## 예시 장애 시나리오

| 장애 유형 | 예시 | 복구 전략 |
| --- | --- | --- |
| 네트워크 장애 | API timeout, 연결 끊김 | retry, timeout 조정, fallback endpoint |
| DB 장애 | 연결 실패, slow query | reconnect, connection pool 점검, read-only fallback |
| API 장애 | 5xx, rate limit | retry with backoff, cached response, 대체 API |
| LLM 장애 | 토큰 초과, 응답 불일치 | 프롬프트 축소, 모델 변경, 응답 검증 |
| 프롬프트 보안 | injection, jailbreak | 입력 필터링, tool 권한 제한, policy validation |

## 프로젝트 성공 기준

- 장애 이벤트를 입력하면 Agent 협업 흐름이 실행됩니다.
- Agent 역할과 Handoff Context가 문서화되어 있습니다.
- 장애 유형별 감지 기준과 복구 전략이 정리되어 있습니다.
- Docker Compose로 전체 서비스가 실행됩니다.
- GitHub Actions로 테스트와 빌드 검증이 수행됩니다.
- AWS 배포 결과, 로그 확인, 리소스 삭제 결과가 보고서에 남습니다.
