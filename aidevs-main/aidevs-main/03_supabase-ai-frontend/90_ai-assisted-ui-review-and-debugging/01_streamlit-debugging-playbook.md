# 01. Streamlit Debugging Playbook

오류가 나면 먼저 실행 위치, 실행 명령, Python 경로, 백엔드 실행 여부를 확인합니다.

## 1. 현재 위치와 Python 확인

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
Get-Location
python -c "import sys; print(sys.executable)"
streamlit --version
```

## 2. 자주 만나는 오류

| 오류 | 먼저 확인할 것 |
| --- | --- |
| `streamlit` 명령을 찾을 수 없음 | `.venv` 활성화, `pip install -r requirements.txt` |
| `ModuleNotFoundError` | 현재 Python 경로와 패키지 설치 여부 |
| 화면은 열리지만 API 오류 | 백엔드 실행 여부, `API_BASE_URL`, 포트 번호 |
| 404 Not Found | 요청 URL이 백엔드 endpoint와 같은지 |
| 405 Method Not Allowed | GET/POST 방식이 맞는지 |
| 422 Validation Error | 요청 JSON이 백엔드 Pydantic 모델과 맞는지 |
| session 값이 사라짐 | `st.session_state` 초기화 위치 |
| 인증 API 실패 | token 저장 여부, Authorization header |

## 3. Codex에게 물어보는 형식

```text
아래 Streamlit 오류를 분석해주세요.

실행 위치:
C:\aidev\03_supabase-ai-frontend

실행 명령:
streamlit run ...

기대 결과:
버튼을 누르면 백엔드 응답이 화면에 표시되어야 합니다.

실제 결과:
...

요청:
아직 코드를 수정하지 말고 가능한 원인과 확인 순서를 초보자 기준으로 설명해주세요.
```

## 4. 수정 전 확인

- 프론트엔드와 백엔드를 각각 다른 터미널에서 실행했는가?
- `.env`의 `API_BASE_URL`이 실제 백엔드 주소인가?
- 브라우저 주소창이 아니라 Streamlit 화면에서 버튼을 눌렀는가?
- token이나 API key를 화면에 출력하고 있지 않은가?
