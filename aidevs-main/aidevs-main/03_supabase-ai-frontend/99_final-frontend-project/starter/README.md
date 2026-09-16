# Starter

최종 프론트엔드 프로젝트를 시작할 때 사용하는 최소 Streamlit 앱입니다.

## 실행 방법

```powershell
cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\starter
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

먼저 제공용 `backend_mock`을 실행하고, `API_BASE_URL`과 백엔드 `/health` 연결을 확인합니다. 이후 회원가입, 로그인, 챗봇, 대화 기록, 서비스 로그 화면을 하나씩 추가합니다.

실제 Supabase/Gemini/Redis 연결은 `backend_service`를 실행한 뒤 같은 Streamlit 앱의 `API_BASE_URL`만 바꿔 확인합니다.
