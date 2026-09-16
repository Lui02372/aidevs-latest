# 02_fastapi-backend-connect

Streamlit 화면에서 FastAPI 백엔드를 호출하는 방법을 학습합니다.

이 폴더에서는 `00_sample_backend`를 기본 연결 대상으로 사용합니다. 프론트엔드는 데이터베이스나 AI 모델에 직접 연결하지 않고, 백엔드 API 주소를 호출합니다. 이 기준은 이후 Supabase 연동 백엔드와 연결할 때도 같습니다.

## 학습 목표

- Streamlit 버튼을 API 호출 시점으로 사용할 수 있습니다.
- 입력값을 JSON payload로 만들어 POST 요청을 보낼 수 있습니다.
- 백엔드 응답 JSON을 화면에 표시할 수 있습니다.
- 백엔드에서 받은 리스트를 DataFrame으로 변환해 표로 표시할 수 있습니다.
- API 기본 주소를 변수로 분리해 관리할 수 있습니다.

## 예제 파일

```text
01_fastapi-health-check.py
02_fastapi-message-client.py
03_fastapi-course-list.py
04_fastapi-score-feedback.py
```

## 기본 백엔드 실행

PowerShell을 하나 더 열고 샘플 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\03_api-integration\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

정상 실행 확인:

```text
http://127.0.0.1:8000/docs
```

## 프론트엔드 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\03_api-integration\02_fastapi-backend-connect\02_fastapi-message-client.py
```

## 확인할 내용

- Streamlit 버튼이 API 호출 시점으로 동작하는가?
- 입력값이 JSON으로 백엔드에 전달되는가?
- 백엔드 응답이 화면에 표시되는가?
- 과정 목록이 DataFrame 표로 표시되는가?
- 백엔드가 꺼졌을 때 오류 메시지를 확인할 수 있는가?

## 실제 백엔드 연결 기준

샘플 백엔드로 흐름을 익힌 뒤에는 `02_supabase-ai-backend`에서 만든 FastAPI 서버로 `API_BASE_URL`만 바꿔 연결할 수 있습니다. 이때 Supabase 저장과 인증은 백엔드가 담당하고, Streamlit은 화면과 API 호출만 담당합니다.

## 수업 메모

Docker 실행은 이 챕터에서 하지 않습니다. Docker, Docker Compose, AWS 배포는 `07_multi-agent-service-ops`에서 학습합니다.
