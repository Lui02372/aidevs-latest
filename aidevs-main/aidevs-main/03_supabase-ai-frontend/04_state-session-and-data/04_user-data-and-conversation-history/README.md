# 04_user-data-and-conversation-history

로그인된 사용자의 정보와 대화 이력을 조회하고 저장하는 방법을 학습합니다.

이 단원은 Supabase 테이블을 프론트엔드에서 직접 조회하는 수업이 아닙니다. 백엔드 API가 Supabase와 통신하고, Streamlit은 Authorization header를 붙여 백엔드 API를 호출합니다.

## 학습 목표

- Authorization header가 필요한 API를 호출할 수 있다.
- 현재 사용자 정보를 조회할 수 있다.
- 사용자별 대화 이력을 채팅 UI로 표시할 수 있다.
- 새 사용자 메시지와 assistant 메시지를 백엔드 API로 저장하는 흐름을 이해할 수 있다.
- 사용자 데이터 요약 화면을 만들 수 있다.
- 04 단원의 대화 이력 미리보기를 실제 백엔드 저장 이력으로 확장할 수 있다.

## 예제 파일

```text
01_current-user-page.py
02_conversation-history-api.py
03_save-conversation-message.py
04_user-data-dashboard.py
```

## 백엔드 연결 기준

실제 수업에서는 다음 백엔드 단원과 연결합니다.

```text
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\04_supabase-auth-and-rls
C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\05_conversation-history-and-service-logs
C:\aidev\02_supabase-ai-backend\99_final-backend-project
```

API 서버 실행 예시는 다음과 같습니다.

```powershell
cd C:\aidev\02_supabase-ai-backend\03_supabase-db-and-auth\03_fastapi-supabase-integration
..\..\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 보조 샘플 백엔드 실행

상태 관리와 화면 표시 흐름만 빠르게 확인할 때는 아래 샘플을 사용할 수 있습니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\04_state-session-and-data\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 프론트엔드 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\04_state-session-and-data\04_user-data-and-conversation-history\02_conversation-history-api.py
```

## 확인 내용

- 백엔드 서버가 실행 중일 때 사용자 정보가 조회되는가?
- `Bearer sample-access-token` 또는 실제 로그인 token 형식의 인증 header가 사용되는가?
- 대화 이력이 user/assistant 역할에 맞게 표시되는가?
- 메시지 저장 후 다시 조회했을 때 목록이 변경되는가?
- 사용자별 데이터가 섞이지 않는 구조를 설명할 수 있는가?

## 핵심 요약

- 사용자별 데이터 접근 제어는 백엔드와 Supabase RLS가 담당합니다.
- Streamlit은 token을 보관하고 API를 호출하는 화면 역할을 담당합니다.
- Docker와 배포 환경은 `07_multi-agent-service-ops`에서 별도로 학습합니다.
