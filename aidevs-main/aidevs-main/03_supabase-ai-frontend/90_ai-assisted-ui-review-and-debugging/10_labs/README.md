# 10_labs

앞 단원에서 자주 만나는 Streamlit/UI/API 오류를 직접 실행하고 AI와 함께 고치는 실습입니다.

각 lab은 다음 흐름으로 진행합니다.

```text
문제 예제 실행
-> 오류 또는 불편한 UI 확인
-> Codex에게 원인 분석 요청
-> 수정 방향 검토
-> 코드 수정
-> 재실행
-> solution_notes.md 형식으로 기록
```

| Lab | 주제 |
| --- | --- |
| `lab-01_streamlit-run-error` | Streamlit 실행 오류와 import 순서 확인 |
| `lab-02_api-connection-error` | `API_BASE_URL`, 백엔드 실행, 포트 확인 |
| `lab-03_session-state-token-error` | `st.session_state`, token, Authorization header 점검 |
| `lab-04_ui-review-and-refactor` | 실행은 되지만 아쉬운 UI 코드 리뷰와 리팩토링 |

## 실행 전 준비

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
streamlit --version
```

Lab 02와 Lab 03은 샘플 백엔드가 필요합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
