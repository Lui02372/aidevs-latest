# 00_references

`03_supabase-ai-frontend`를 시작하기 전에 읽는 참고 자료입니다.

이 폴더는 별도 수업 단원이 아니라, Streamlit 프론트엔드 수업 전체에서 반복해서 확인하는 기준 문서 모음입니다.

## 문서 목록

```text
frontend-course-map.md
frontend-security-and-deployment-notes.md
streamlit-usage-guide.md
streamlit-theme-guide.md
```

| 문서 | 설명 |
| --- | --- |
| [frontend-course-map.md](./frontend-course-map.md) | 03 과정 전체 흐름과 단원 역할을 확인합니다. |
| [frontend-security-and-deployment-notes.md](./frontend-security-and-deployment-notes.md) | 프론트엔드 보안 기준과 배포 시 주의점을 확인합니다. |
| [streamlit-usage-guide.md](./streamlit-usage-guide.md) | Streamlit 설치, 실행, widget, session state, form, layout, API 호출, secrets 기준을 공식 문서 기반으로 정리한 참고 문서입니다. |
| [streamlit-theme-guide.md](./streamlit-theme-guide.md) | Streamlit 테마 설정 파일 위치, 색상 옵션, 예제 실행 기준을 확인합니다. |

## 먼저 확인할 내용

- 이 과정의 기본 UI 도구는 Streamlit입니다.
- React는 필수 실습이 아니라 진도와 난이도에 따라 선택적으로 소개합니다.
- Streamlit은 Supabase DB에 직접 접속하지 않고 FastAPI API를 호출합니다.
- 초반에는 `03_api-integration/00_sample_backend`로 API 호출을 연습합니다.
- 실제 백엔드 흐름은 `02_supabase-ai-backend`와 연결합니다.
- `99_final-frontend-project`에서는 필수 실습용 `backend_mock`과 선택/심화용 `backend_service`를 구분합니다.
- 기본 단원 실습의 프론트엔드 `.env`에는 `API_BASE_URL`만 둡니다.
- `99_final-frontend-project`도 기본적으로 03 과정 최상위 `.env`의 `API_BASE_URL`을 사용합니다.
- Supabase `service_role` key, Upstash token, LLM API key는 실제 서비스용 프론트엔드에 두지 않습니다.
- `05_ai-chatbot-interface`에서는 mock 응답과 백엔드 chat API 호출을 기준으로 챗봇 화면을 구성합니다.
- SSE 기반 실시간 응답 스트리밍은 `04_supabase-ai-mini-project`에서 백엔드, 프론트엔드, Supabase 저장 흐름을 함께 연결해 다룹니다.

## 환경변수 기준

```text
기본 단원 실습:
C:\aidev\03_supabase-ai-frontend\.env

최종 프론트엔드 프로젝트:
C:\aidev\03_supabase-ai-frontend\.env

최종 프로젝트 실제 backend_service:
C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\backend_service\.env
```

수업 중 프론트엔드는 한 과정 폴더의 `.env` 하나를 기준으로 진행합니다. `backend_service`의 Supabase/Gemini/Upstash key는 별도 backend `.env`에 둡니다. 배포를 선택 실습으로 진행할 때만 Streamlit Secrets에서 `API_BASE_URL`을 따로 설정합니다.

## 확인 질문

```text
Streamlit은 전체 서비스에서 어떤 역할을 하나요?
프론트엔드에 service role key를 두면 왜 위험한가요?
API_BASE_URL은 어디에 사용되나요?
03 과정의 .env는 어디에 있나요?
backend_mock과 backend_service는 언제 다르게 사용하나요?
SSE는 왜 04 미니 프로젝트에서 다루나요?
```
