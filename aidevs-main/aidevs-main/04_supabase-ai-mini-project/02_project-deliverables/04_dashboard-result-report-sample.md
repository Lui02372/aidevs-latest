# 04. 대시보드 구현 결과물 샘플

프로젝트명: AI 서비스 로그 분석 및 운영 대시보드 구축

## 구현 요약

| 항목 | 구현 내용 |
| --- | --- |
| backend | FastAPI로 로그 생성, 조회, 요약, SSE endpoint 구현 |
| DB | Supabase `realtime_service_logs`, `ai_answer_feedback` 테이블 사용 |
| Redis | 새 로그 이벤트 publish/subscribe |
| frontend | Streamlit으로 실시간 로그, 최근 로그, level별 차트 표시 |
| 배포 | 선택 적용. Render, Upstash, Streamlit Community Cloud 기준 |

## 실행 방법

backend:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\backend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

frontend는 선택한 구조에 맞게 실행합니다.

왼쪽 메뉴 방식:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_multipage
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

탭 방식:

```powershell
cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_tabs
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

## 시연 시나리오

1. 백엔드 `/health` 상태를 확인합니다.
2. Streamlit 화면에서 로그를 생성합니다.
3. 최근 로그 테이블에 새 로그가 표시되는지 확인합니다.
4. 실시간 로그 영역에서 SSE 이벤트가 표시되는지 확인합니다.
5. level별 차트가 갱신되는지 확인합니다.
6. 피드백을 저장하고 개선 메모를 작성합니다.

## 핵심 기능 결과

| 기능 | 결과 | 확인 방법 |
| --- | --- | --- |
| 로그 수집 | 완료 | POST `/logs` |
| 로그 조회 | 완료 | GET `/logs` |
| 로그 시각화 | 완료 | Streamlit 테이블/차트 |
| 실시간 표시 | 완료 | GET `/stream/logs` |
| 피드백 기록 | 완료 | POST `/feedback` |

## 로그 기반 개선 내용

| 발견한 문제 | 근거 로그 | 개선 방법 |
| --- | --- | --- |
| 예: LLM 응답 시간이 길다 | `latency_ms` 평균 증가 | 프롬프트 축소 또는 캐시 적용 |
| 예: error 로그가 반복된다 | `level=error` 증가 | 예외 처리와 사용자 안내 메시지 보강 |

## 체크리스트

- [ ] 구현된 대시보드가 실행 환경에서 동작한다.
- [ ] 로그 수집, 조회, 시각화가 시연 가능하다.
- [ ] 실시간 로그 스트림이 화면에 표시된다.
- [ ] 피드백 데이터가 저장된다.
- [ ] 서비스 품질 개선 또는 운영 최적화 근거가 작성되었다.
- [ ] 배포를 진행했다면 배포 URL을 기록했다.
