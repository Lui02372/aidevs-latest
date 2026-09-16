# 06 Deployment Guide

06 과정의 배포는 선택입니다. 우선 로컬에서 Agent 흐름과 산출물을 완성한 뒤, 시간이 남을 때 무료 배포 서비스를 사용합니다.

## 선택 배포 구조

```text
Streamlit UI
-> FastAPI backend
-> LangGraph Agent
-> Mock data 또는 외부 API
```

## 추천 서비스

| 대상 | 서비스 |
| --- | --- |
| FastAPI backend | Render |
| Streamlit frontend | Streamlit Community Cloud |
| 환경 변수 | 각 서비스의 Environment Variables |

## 배포 전에 확인할 것

- `.env` 파일을 업로드하지 않았는가?
- API Key를 코드에 직접 작성하지 않았는가?
- 로컬에서 backend와 frontend가 실행되는가?
- `/health` 같은 상태 확인 endpoint가 있는가?
- Mock data 또는 실제 API 연결 방식이 README에 설명되어 있는가?

## 07 과정으로 넘기는 내용

다음 내용은 07 과정에서 본격적으로 다룹니다.

```text
Dockerfile
Docker Compose
AWS 배포
GitHub Actions
서비스 장애 복구
멀티 에이전트 운영
모니터링과 알림
```

06 과정에서는 배포 자체보다 Agent 설계, Tool 흐름, Self-Reflection, 시험 결과 문서화를 더 중요하게 봅니다.
