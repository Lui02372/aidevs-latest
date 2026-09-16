# 90_ai-assisted-ui-review-and-debugging

이 단원은 `01_streamlit-basic`부터 `07_streamlit-tabs-app`까지 만든 Streamlit 코드를 AI 보조 도구와 함께 점검하는 마무리 단원입니다.

새로운 큰 기능을 많이 추가하는 단원이 아니라, 실행 오류, API 연결 실패, session state 문제, UI 사용성, 보안 키 노출 위험을 정리하고 고치는 방법을 연습합니다.

백엔드 과정의 `90_ai-assisted-code-review-and-debugging`과 같은 방식으로 진행합니다. 즉, 설명만 읽지 않고 일부러 문제가 있는 예제를 실행한 뒤 AI와 함께 원인을 분석하고, 수정하고, 수정 전후 기록을 남깁니다.

## 학습 목표

- Streamlit 오류 메시지를 실행 명령, 파일 위치, 기대 결과와 함께 정리할 수 있습니다.
- Codex에게 바로 수정을 맡기기 전에 원인 분석을 요청할 수 있습니다.
- `API_BASE_URL`, 백엔드 실행 여부, 요청 URL, HTTP status code를 확인할 수 있습니다.
- `st.session_state` 초기화 문제와 token 저장 흐름을 점검할 수 있습니다.
- 프론트엔드 코드에 민감 정보가 들어가지 않았는지 확인할 수 있습니다.
- 프롬프트만으로 작은 Streamlit UI를 단계적으로 설계하고 개선할 수 있습니다.
- 최종 프로젝트 제출 전 UI 리뷰 기록을 남길 수 있습니다.

## 진행 순서

```text
01_streamlit-debugging-playbook.md
-> 02_ui-review-checklist.md
-> 03_prompt-recipes.md
-> 04_prompt-driven-ui-development.md
-> 10_labs
-> templates
```

## 가장 중요한 원칙

Codex에게 질문할 때 실제 token, API key, 비밀번호를 붙여 넣지 않습니다.

```text
Authorization: Bearer ***
API_BASE_URL=http://127.0.0.1:8000
SUPABASE_SERVICE_ROLE_KEY=절대 프론트엔드에 넣지 않음
```

## 단원별 점검 관점

| 앞 단원 | 점검할 내용 |
| --- | --- |
| `01_streamlit-basic` | 실행 명령, 파일 경로, Streamlit 화면 표시 |
| `02_streamlit-ui-components` | 입력값 반영, 폼 submit, 표/차트 표시 |
| `03_api-integration` | 백엔드 실행 여부, `API_BASE_URL`, GET/POST, timeout, status code |
| `04_state-session-and-data` | `st.session_state`, 로그인 token, Authorization header, 대화 이력/로그 조회 |
| `05_ai-chatbot-interface` | chat UI, mock 응답, 백엔드 chat API 연결, LLM key 노출 여부 |
| `06_streamlit-multipage-app` | `st.Page`, `st.navigation()` 구조, `app.py` 실행 기준, `frontend_common.py` 공통 코드, page 간 `session_state` 공유, 팀 개발 파일 분리 |
| `07_streamlit-tabs-app` | `st.tabs()` 구조, `tab_pages` 파일 분리, 탭 간 `session_state` 공유, 한 화면 안의 대시보드 구성 |
| `99_final-frontend-project` | 최종 앱 실행, 테스트 결과, 보안 점검, 제출 문서 |

## 제출 산출물

필수:

```text
1. 오류 분석 기록 1개
2. UI 리뷰 체크리스트 1개
3. 수정 후 재실행 결과 1개
4. 프롬프트 기반 UI 개선 기록 1개
```

선택:

```text
리팩토링 전후 비교
최종 프로젝트 사전 리뷰 기록
보안 키 노출 점검표
```

## 템플릿

| 파일 | 용도 |
| --- | --- |
| `templates/error-report-template.md` | 실행 오류를 정리해 Codex에게 전달할 때 사용합니다. |
| `templates/ui-debugging-session-template.md` | 오류 분석, 원인, 수정, 재실행 결과를 한 번에 기록합니다. |
| `templates/ui-review-request-template.md` | UI 리뷰를 요청할 때 관점과 요청 문장을 정리합니다. |
| `templates/before-after-ui-fix-template.md` | 수정 전후 차이를 제출 기록으로 남깁니다. |
| `templates/prompt-driven-ui-plan-template.md` | 프롬프트만으로 UI를 단계적으로 만들 때 사용합니다. |
| `templates/security-redaction-checklist.md` | token, API key, 비밀번호 노출 여부를 확인합니다. |
