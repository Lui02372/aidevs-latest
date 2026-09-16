# 01. Project Overview

## 교과목 단위 프로젝트

| 항목 | 내용 |
| --- | --- |
| 교과목 | 웹 서비스 기초 및 AI 백엔드 개발 |
| 단위 프로젝트 | 실시간 로그 대시보드 인터페이스 |
| 주제 | AI 서비스 로그 분석 및 운영 대시보드 구축 |
| 권장 시간 | 24시간 |

## 프로젝트 목표

```text
1. 백엔드, DB, UI 통합 아키텍처 구현 및 배포
2. 사용자 로그 및 서비스 데이터 수집, 저장 구조 구현
3. 실시간 데이터 시각화 및 운영 대시보드 구현
4. 로그 기반 서비스 품질 개선 및 운영 최적화
```

## 필수 기능

| 기능 | 설명 |
| --- | --- |
| 로그 생성 API | 사용자의 요청, AI 응답, 오류, 응답 시간 같은 이벤트를 저장합니다. |
| 로그 조회 API | Supabase DB에 저장된 최근 로그와 요약 데이터를 조회합니다. |
| Upstash Redis 이벤트 전달 | 새 로그가 생성될 때 Upstash Redis로 이벤트를 전달합니다. |
| SSE 스트리밍 | Upstash Redis 이벤트를 FastAPI SSE endpoint로 프론트엔드에 전달합니다. |
| Streamlit 대시보드 | 실시간 로그, 최근 로그 테이블, level별 차트를 표시합니다. |
| 피드백 기록 | 사용자 피드백을 저장하고 AI 답변 품질 개선 기준을 정리합니다. |

## 필수 산출물

| 산출물 | 파일 예시 |
| --- | --- |
| API 설계 문서 | `02_project-deliverables/01_api-design-sample.md` |
| 화면 설계서 | `02_project-deliverables/02_screen-design-sample.md` |
| 데이터베이스 설계서 | `02_project-deliverables/03_database-design-sample.md` |
| 대시보드 구현 결과물 | `02_project-deliverables/04_dashboard-result-report-sample.md` |

## 수업 운영 기준

`01_realtime-log-dashboard-practice`는 작게 실행해 보는 실습입니다. `03_project_structure`는 최종 프로젝트를 시작하기 위한 starter 구조입니다.

```text
01 = 작게 실행해서 개념 확인
02 = 산출물 기준 확인
03 = 최종 프로젝트 구조 작성
```
