# 03_api-integration

Streamlit 프론트엔드에서 HTTP 요청을 보내고 FastAPI 백엔드 응답을 화면에 표시하는 단원입니다.

이 단원부터는 화면만 만드는 것을 넘어, 사용자의 입력을 API 요청으로 보내고 JSON 응답을 처리하는 흐름을 학습합니다. 기본 실습은 이 폴더의 `00_sample_backend`를 사용해 가볍게 진행하고, 실제 Supabase 저장과 인증 흐름은 `02_supabase-ai-backend`와 연결해 확인합니다.

Gemini SDK와 Supabase 저장은 이 단원에서 깊게 다루지 않습니다. 여기서는 “프론트엔드가 백엔드를 호출하고 응답을 화면에 표시한다”는 연결 흐름에 집중합니다. 챗봇 응답을 화면에 표시하는 흐름은 `05_ai-chatbot-interface`, 응답을 대화 이력에 누적하는 흐름은 `04_state-session-and-data`에서 다룹니다.

## 학습 목표

- HTTP 요청과 JSON 응답의 기본 흐름을 이해합니다.
- `httpx`를 사용해 GET, POST 요청을 보낼 수 있습니다.
- Streamlit 화면에서 FastAPI 백엔드 API를 호출할 수 있습니다.
- API 응답 JSON 중 필요한 값을 화면에 표시할 수 있습니다.
- API 호출 중 로딩 상태를 표시할 수 있습니다.
- 서버 연결 실패, timeout, status code 오류, 잘못된 응답 구조를 화면에서 처리할 수 있습니다.

## 학습 순서

```text
00_sample_backend
-> 01_httpx-api-call
-> 02_fastapi-backend-connect
-> 03_error-loading-and-response-handling
-> 04_xxx
-> 05_weather_df
-> 10_labs
-> 20_assignments
```

## 폴더 구성

```text
03_api-integration
├─ README.md
├─ 00_references
├─ 00_sample_backend
├─ 01_httpx-api-call
├─ 02_fastapi-backend-connect
├─ 03_error-loading-and-response-handling
├─ 04_xxx
├─ 05_weather_df
├─ 10_labs
└─ 20_assignments
```

## 1단계: 샘플 백엔드 실행

PowerShell을 하나 열고 샘플 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\03_api-integration\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

정상 실행 확인:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 2단계: Streamlit 프론트엔드 실행

PowerShell을 하나 더 열고 Streamlit 예제를 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\03_api-integration\02_fastapi-backend-connect\01_fastapi-health-check.py
```

## 실제 01 백엔드와 연결하는 기준

이 단원의 샘플 백엔드는 API 호출 흐름을 배우기 위한 보조 서버입니다. 실제 Supabase 데이터 저장, 인증, RLS, 서비스 로그 저장은 `02_supabase-ai-backend`의 FastAPI 서버를 기준으로 확인합니다.

```text
샘플 백엔드
-> API 호출 구조 학습
-> health/message/course/score-feedback 확인

02_supabase-ai-backend
-> Supabase 저장
-> 사용자 인증
-> 대화 이력과 서비스 로그 관리
```

## 실행 확인 기준

- FastAPI 서버가 `http://127.0.0.1:8000`에서 실행 중입니다.
- Streamlit 화면에서 API 호출 버튼을 누르면 JSON 응답이 표시됩니다.
- POST 요청에서 입력값이 백엔드로 전달됩니다.
- 서버가 꺼져 있을 때 오류 메시지가 표시됩니다.
- 로딩 상태와 응답 검증 메시지가 화면에 표시됩니다.

## 필수와 선택 기준

| 구분 | 내용 |
| --- | --- |
| 필수 | `API_BASE_URL`, GET/POST 요청, JSON 응답 표시, timeout/status code 오류 처리, 로딩 상태 표시 |
| 선택 | 샘플 백엔드 대신 02 백엔드 전체 연결, 응답 데이터 표/차트 확장 |
| 제외 | Supabase DB 직접 접속, SSE 스트리밍, 배포 |

## 직접 꼭 구분해야 할 것

- Streamlit은 화면을 담당합니다.
- FastAPI는 요청을 받고 JSON 응답을 반환합니다.
- Supabase는 사용자, 대화, 로그 같은 오래 보관할 데이터를 저장합니다.
- 이 단원의 샘플 백엔드는 Supabase에 저장하지 않습니다.
- Docker 실행은 이 단원에서 하지 않고 `07_multi-agent-service-ops`에서 배웁니다.
- 이 단원에서의 실시간 표시는 로딩, 상태 메시지, 응답 검증 중심입니다. SSE 기반 응답 스트리밍은 `04_supabase-ai-mini-project`에서 통합 실습으로 다룹니다.
