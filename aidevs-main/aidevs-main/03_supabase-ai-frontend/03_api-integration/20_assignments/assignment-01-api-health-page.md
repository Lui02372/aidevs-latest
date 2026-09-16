# Assignment 01: API Health Page

## 목표

Streamlit에서 FastAPI `/health` API를 호출하는 화면을 만듭니다.

이 과제의 목적은 프론트엔드 화면에서 백엔드 서버 상태를 확인하는 가장 기본적인 연결 흐름을 익히는 것입니다.

## 요구사항

- API 기본 주소를 변수로 분리합니다.
- 버튼을 누르면 `/health` API를 호출합니다.
- status code와 JSON 응답을 화면에 표시합니다.
- 서버가 꺼져 있을 때 사용자 안내 메시지를 표시합니다.
- 성공과 실패 메시지가 화면에서 구분되어야 합니다.

## 사전 준비

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\03_api-integration\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 제출 파일 예시

```text
assignment-01-api-health-page.py
```

## 확인 기준

- 백엔드가 켜져 있을 때 `status: ok`를 확인할 수 있습니다.
- 백엔드가 꺼져 있을 때 오류 안내가 표시됩니다.
- 코드에서 `API_BASE_URL`을 사용합니다.
