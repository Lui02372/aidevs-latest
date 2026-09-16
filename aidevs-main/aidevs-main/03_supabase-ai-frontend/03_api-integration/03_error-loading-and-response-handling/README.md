# 03_error-loading-and-response-handling

API 호출 중 발생할 수 있는 로딩, 오류, 응답 검증을 Streamlit 화면에서 처리하는 방법을 학습합니다.

이 챕터의 실시간 표시는 SSE 스트리밍이 아니라, 사용자가 기다리는 동안 화면이 멈춘 것처럼 보이지 않게 만드는 기초 UI 처리입니다. `st.spinner`, `st.status`, 상태 메시지, 오류 안내 문구를 먼저 익힌 뒤, SSE 기반 응답 스트리밍은 `04_supabase-ai-mini-project`에서 통합 실습으로 다룹니다.

## 학습 목표

- API 호출 중 로딩 메시지를 표시할 수 있습니다.
- timeout 상황을 사용자에게 이해 가능한 문장으로 안내할 수 있습니다.
- status code에 따라 성공과 실패 메시지를 나눌 수 있습니다.
- 응답 JSON에 필요한 key가 있는지 검증할 수 있습니다.

## 예제 파일

```text
01_loading-spinner.py
02_timeout-error-handling.py
03_status-code-handling.py
04_response-validation.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\03_api-integration\03_error-loading-and-response-handling\02_timeout-error-handling.py
```

## 확인할 내용

- API 호출 중 spinner가 표시되는가?
- 처리 단계가 길어질 때 상태 메시지를 표시할 수 있는가?
- 서버가 꺼져 있을 때 오류 메시지가 표시되는가?
- status code별로 다른 메시지를 표시할 수 있는가?
- 응답 JSON에 필요한 key가 있는지 확인할 수 있는가?

## 이후 과정과 연결

```text
03_api-integration
-> 로딩, 오류, 응답 검증

05_ai-chatbot-interface
-> mock/Gemini 응답을 화면에 표시

04_state-session-and-data
-> 응답 결과와 오류 상태를 대화 이력과 로그에 누적
```
