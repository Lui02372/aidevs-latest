# 10_labs

상태 관리, 로그인 상태, 사용자별 대화 이력, 캐시, 서비스 로그 조회를 조합하는 수업 중 실습입니다.

이 실습은 `02_supabase-ai-backend`의 Supabase 기반 인증/사용자 데이터 API와 연결하는 것을 기본 방향으로 합니다. 샘플 백엔드는 백엔드 과정이 아직 준비되지 않았을 때만 사용하는 보조 자료입니다.

## 실습 목록

```text
lab-01-login-state-page.py
lab-02-user-conversation-page.py
lab-03-cached-user-dashboard.py
lab-04-service-log-dashboard.py
```

## 기본 백엔드 실행

PowerShell을 하나 더 열고 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 보조 샘플 백엔드

백엔드 인증 단원이 아직 준비되지 않았을 때는 아래 샘플을 사용합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 실습 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\04_state-session-and-data\10_labs\lab-01-login-state-page.py
```

## 실습 진행 방식

1. 로그인 상태가 저장되는지 확인합니다.
2. Authorization header가 필요한 API를 호출합니다.
3. 사용자별 대화 이력이 화면에 표시되는지 확인합니다.
4. 캐시 적용 전후로 같은 데이터를 다시 불러오는 흐름이 어떻게 달라지는지 관찰합니다.
5. 서비스 로그 조회 화면에서 API 상태와 최근 로그를 확인합니다.
6. 서버를 끄거나 token을 지워 오류 상황을 확인하고 사용자 안내 문구를 개선합니다.

## 확인 기준

- 로그인 성공 후 상태값이 유지된다.
- 보호된 API 호출에 token이 포함된다.
- 대화 이력이 표 또는 채팅 메시지로 표시된다.
- 캐시가 적용된 함수와 적용 이유를 설명할 수 있다.
- 서비스 로그 조회 화면에 백엔드 응답이 표시된다.
- Supabase 연결과 권한 검증은 백엔드에서 담당한다는 점을 설명할 수 있다.
