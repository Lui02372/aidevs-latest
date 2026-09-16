# 10_labs

수업 중 함께 진행하는 API 연동 실습입니다.

이 실습은 샘플 FastAPI 백엔드를 실행한 뒤, Streamlit 화면에서 API를 호출하고 정상 응답과 오류 상황을 모두 확인하는 방식으로 진행합니다.

## 실습 목록

```text
lab-01-health-check-page.py
lab-02-message-client-page.py
lab-03-error-handling-page.py
```

## 사전 준비

샘플 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\03_api-integration\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 실행 예시

다른 PowerShell에서 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\03_api-integration\10_labs\lab-01-health-check-page.py
```

## 실습 기준

- FastAPI 서버를 먼저 실행합니다.
- Streamlit 앱에서 API 호출 버튼을 누릅니다.
- 정상 응답과 오류 상황을 모두 확인합니다.
- 오류 메시지가 사용자에게 이해 가능한 문장인지 확인합니다.
- 응답 JSON에서 실제 화면에 필요한 key만 골라 표시합니다.

## 완료 기준

- health check 결과를 화면에서 확인할 수 있습니다.
- POST 요청으로 입력값을 백엔드에 전달할 수 있습니다.
- 서버 연결 실패 상황을 화면에서 안내할 수 있습니다.
