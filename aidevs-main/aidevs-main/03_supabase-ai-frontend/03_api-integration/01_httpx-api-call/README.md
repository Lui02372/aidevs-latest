# 01_httpx-api-call

`httpx`를 사용해 Python 코드에서 HTTP 요청을 보내는 기본 흐름을 학습합니다.

이 폴더는 Streamlit 화면을 붙이기 전에, Python 코드만으로 백엔드 API를 호출해 보는 단계입니다. 먼저 터미널에서 GET, POST 요청과 JSON 응답을 확인하면 이후 Streamlit 화면에서 같은 요청을 보내는 흐름을 이해하기 쉽습니다.

## 학습 목표

- GET 요청과 POST 요청의 차이를 설명할 수 있습니다.
- 응답 status code와 JSON 데이터를 확인할 수 있습니다.
- API 주소를 변수로 분리할 수 있습니다.
- 요청 payload가 백엔드 Pydantic 모델과 맞아야 한다는 점을 이해합니다.

## 예제 파일

```text
01_get-request.py
02_post-request.py
03_api-base-url.py
```

## 사전 준비

먼저 샘플 백엔드를 실행합니다.

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
python .\03_api-integration\01_httpx-api-call\01_get-request.py
```

## 확인할 내용

- GET 요청과 POST 요청의 차이를 설명할 수 있는가?
- 응답 status code와 JSON 데이터를 확인할 수 있는가?
- API 주소를 변수로 분리할 수 있는가?
- 서버가 꺼져 있으면 어떤 오류가 나는지 확인했는가?
