# 11. Streamlit 준비 가이드

Streamlit은 Python 코드로 빠르게 웹 화면을 만드는 도구입니다.

03 과정부터 Streamlit으로 챗봇 UI, 로그 화면, 대시보드 화면을 만듭니다.

공식 사이트:

```text
Streamlit: https://streamlit.io/
Streamlit Docs: https://docs.streamlit.io/
Streamlit Community Cloud: https://streamlit.io/cloud
```

## 1. 설치

각 과정의 `.venv`를 활성화한 뒤 `requirements.txt`로 설치합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

직접 설치해야 한다면:

```powershell
pip install streamlit
```

## 2. 설치 확인

```powershell
streamlit --version
```

## 3. 앱 실행

```powershell
streamlit run app.py
```

예시:

```powershell
streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

실행 후 브라우저에서 보통 아래 주소가 열립니다.

```text
http://localhost:8501
```

## 4. 백엔드 연결 기준

프론트엔드는 Supabase나 LLM API key를 직접 가지지 않습니다.

```text
Streamlit 화면
-> API_BASE_URL 기준 FastAPI 호출
-> FastAPI backend
-> Supabase/Gemini/Redis 처리
```

`.env` 예시:

```env
API_BASE_URL=http://127.0.0.1:8000
```

## 5. Community Cloud 배포 준비

Streamlit Community Cloud는 GitHub 저장소의 Streamlit 앱을 배포할 수 있습니다.

기본 흐름:

```text
1. https://streamlit.io/cloud 접속
2. GitHub 계정으로 로그인
3. New app 선택
4. GitHub repository 선택
5. branch 선택
6. main file path 지정
7. secrets가 필요하면 설정
8. Deploy 클릭
```

## 6. 체크리스트

```text
[ ] streamlit --version이 출력된다.
[ ] streamlit run으로 예제를 실행할 수 있다.
[ ] API_BASE_URL 역할을 설명할 수 있다.
[ ] 프론트엔드에 service role key나 LLM API key를 넣으면 안 된다는 점을 이해했다.
```

