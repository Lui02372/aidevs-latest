# Lab 02. API 연결 오류 분석

이 실습은 Streamlit 화면에서 백엔드 API를 호출할 때 자주 만나는 연결 오류를 점검합니다.

## 실행

먼저 샘플 백엔드를 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

새 터미널에서 문제 예제를 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-02_api-connection-error\broken_api_client.py
```

## 해야 할 일

1. 화면에 표시되는 연결 실패 메시지를 확인합니다.
2. 백엔드 실행 주소와 `API_BASE_URL` 값을 비교합니다.
3. timeout, status code, 예외 처리가 적절한지 리뷰합니다.
4. 수정 후 `/health` 응답이 화면에 표시되는지 확인합니다.

## Codex 요청 예시

```text
이 Streamlit 파일의 API 연결 실패 원인을 분석해주세요.

확인할 것:
1. API_BASE_URL이 실제 백엔드 주소와 같은가?
2. 백엔드가 켜져 있지 않을 때 어떤 메시지를 보여 주는가?
3. timeout과 예외 처리가 초보자에게 충분히 친절한가?

아직 코드는 수정하지 말고 문제점만 알려주세요.
```
