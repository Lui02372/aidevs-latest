# 04_supabase-ai-mini-project

`04_supabase-ai-mini-project`는 02 백엔드 과정과 03 프론트엔드 과정에서 배운 내용을 묶어 진행하는 24시간 단위 프로젝트입니다.

주제는 **AI 서비스 로그 분석 및 운영 대시보드 구축**입니다. FastAPI backend, Supabase DB, Upstash Redis 이벤트 전달, SSE 스트리밍, Streamlit 대시보드를 연결해 실시간 로그 대시보드 인터페이스를 구현합니다.

## 프로젝트 목표

```text
1. 백엔드, DB, UI 통합 아키텍처 구현 및 배포 흐름 이해
2. 사용자 로그 및 서비스 데이터 수집, 저장 구조 구현
3. Upstash Redis와 SSE 기반 실시간 데이터 시각화 대시보드 구현
4. 로그 기반 서비스 품질 개선 및 운영 최적화 기준 정리
```

## 전체 구조

```text
04_supabase-ai-mini-project
├─ README.md
├─ SETUP.md
├─ 00_references
├─ 01_realtime-log-dashboard-practice
├─ 02_project-deliverables
└─ 03_project_structure
```

## 폴더 역할

| 폴더 | 역할 |
| --- | --- |
| `00_references` | 프로젝트 개요, DB/Upstash Redis/SSE 역할, 배포 가이드, 참고 구조를 정리합니다. |
| `01_realtime-log-dashboard-practice` | Supabase DB 저장, Upstash Redis 이벤트 전달, SSE 화면 표시를 작은 예제로 실행합니다. |
| `02_project-deliverables` | API 설계서, 화면 설계서, DB 설계서, 대시보드 결과 보고서 샘플을 제공합니다. |
| `03_project_structure` | 최종 프로젝트를 시작할 때 사용할 backend/frontend/database/docs starter 구조입니다. |

## 필수 구현 범위

| 항목 | 기준 |
| --- | --- |
| Supabase DB 저장 | 서비스 로그와 피드백 데이터를 테이블에 저장합니다. |
| Upstash Redis 이벤트 전달 | 새 로그 이벤트를 Upstash Redis로 publish하고 SSE source로 사용합니다. |
| FastAPI SSE endpoint | `/stream/logs`에서 실시간 로그 이벤트를 전송합니다. |
| Streamlit 대시보드 | 실시간 로그 영역, 최근 로그 테이블, 간단한 차트를 표시합니다. |
| 산출물 작성 | API 설계 문서, 화면 설계서, 데이터베이스 설계서, 대시보드 구현 결과물을 작성합니다. |

## 선택 구현 범위

| 항목 | 설명 |
| --- | --- |
| 실제 배포 | FastAPI -> Render, Upstash Redis -> Upstash, Streamlit -> Streamlit Community Cloud 흐름을 적용합니다. |
| AI 로그 요약 | 로그 목록을 기반으로 운영 원인 또는 개선 포인트를 요약합니다. |
| 고급 Redis Stream | Pub/Sub 대신 Redis Stream으로 이벤트를 보존합니다. |
| 사용자별 권한 | Supabase Auth/RLS를 적용해 사용자별 로그 조회를 제한합니다. |

## Upstash Redis 실행 기준

04 프로젝트의 기본 실습 기준은 Upstash Redis입니다. 이번 과정에서는 로컬 Redis를 설치하지 않습니다. 다만 Upstash 계정 생성이나 URL 준비가 늦어져도 실습 흐름이 멈추지 않도록 예제 backend는 memory fallback을 제공합니다.

```text
REDIS_URL 있음 -> Upstash Redis publish/subscribe 사용
REDIS_URL 없음 -> 임시 memory fallback으로 SSE 흐름 확인
```

최종 산출물에는 Upstash Redis를 연결했는지, 또는 수업 진행상 임시 fallback으로 시연했는지를 명확히 적습니다.

## 제외 범위

```text
Grafana/Prometheus
Docker Compose 운영 환경
AWS 배포
GitHub Actions CI/CD
Auto Healing 운영 자동화
```

위 내용은 `07_multi-agent-service-ops`에서 더 깊게 다룹니다.

## 진행 순서

1. [SETUP.md](./SETUP.md)를 보고 `.venv`, `.env`, 패키지를 준비합니다.
2. [00_references](./00_references/README.md)에서 프로젝트 목표와 DB/Upstash Redis/SSE 역할을 확인합니다.
3. [01_realtime-log-dashboard-practice](./01_realtime-log-dashboard-practice/README.md)에서 작은 실시간 로그 예제를 실행합니다.
4. [02_project-deliverables](./02_project-deliverables/README.md)에서 필수 산출물 기준을 확인합니다.
5. [03_project_structure](./03_project_structure/README.md)를 복사하거나 참고해 최종 프로젝트를 구현합니다.

## 다음 과정 연결

04 과정은 로컬 또는 무료 배포 수준의 단위 프로젝트입니다. 이후 05~07 과정에서는 LangGraph, 멀티 에이전트, Docker, AWS, GitHub Actions, 운영 자동화로 확장합니다.
