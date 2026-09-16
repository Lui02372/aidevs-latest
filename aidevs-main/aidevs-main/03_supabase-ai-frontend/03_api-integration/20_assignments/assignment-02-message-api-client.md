# Assignment 02: Message API Client

## 목표

Streamlit 입력값을 FastAPI POST API로 전송하는 앱을 만듭니다.

이 과제의 목적은 사용자가 입력한 값을 JSON payload로 만들고, 백엔드 응답을 다시 화면에 표시하는 흐름을 익히는 것입니다.

## 요구사항

- 이름과 메시지를 입력받습니다.
- 입력값을 JSON으로 만들어 `/api/message`에 POST 요청을 보냅니다.
- 백엔드 응답의 `reply` 값을 화면에 표시합니다.
- 빈 입력값과 API 실패 상황을 처리합니다.
- 응답 전체 JSON도 `st.json`으로 확인할 수 있어야 합니다.

## 사전 준비

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\03_api-integration\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 제출 파일 예시

```text
assignment-02-message-api-client.py
```

## 확인 기준

- 이름과 메시지를 입력한 뒤 POST 요청이 성공합니다.
- `reply` 값이 화면에 표시됩니다.
- 이름 또는 메시지가 비어 있을 때 안내 메시지를 표시합니다.
- API 실패 상황을 `st.error` 또는 `st.warning`으로 처리합니다.
