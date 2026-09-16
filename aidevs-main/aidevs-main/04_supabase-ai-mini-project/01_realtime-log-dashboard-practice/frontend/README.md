# Frontend

Streamlit으로 실시간 로그 대시보드를 확인하는 작은 예제입니다.

## 화면 구성

```text
frontend
├─ app.py
├─ frontend_common.py
└─ pages
   ├─ 00_overview.py
   ├─ 01_log_input_and_query.py
   ├─ 02_sse_timed_receive.py
   └─ 03_sse_continuous_receive.py
```

| 파일 | 역할 |
| --- | --- |
| `app.py` | 왼쪽 메뉴 이름 정의와 화면 실행 |
| `frontend_common.py` | API 주소, JSON 요청, SSE 파싱 공통 함수 |
| `pages/00_overview.py` | 화면 설명, 저장/실시간 수신 차이, fallback 설명 |
| `pages/01_log_input_and_query.py` | REST API로 로그 생성/조회 |
| `pages/02_sse_timed_receive.py` | 정해진 시간 동안 SSE 이벤트 수신, 표/그래프 표시 |
| `pages/03_sse_continuous_receive.py` | 화면 진입 시 SSE 3분 자동 수신, 표/그래프 표시 |

## 실행

```powershell
cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\frontend
C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

실행 후 왼쪽 메뉴에서 화면을 선택합니다.

```text
화면설명
1. 로그입력.조회
2. SSE 시간 설정 수신
3. SSE 3분 자동 수신
```

## 확인 순서

1. `화면설명`에서 전체 구조와 fallback 의미를 확인합니다.
2. `1. 로그입력.조회` 화면에서 `POST /logs`로 로그를 생성합니다.
3. 같은 화면에서 `GET /logs`로 저장된 로그를 조회합니다.
4. `2. SSE 시간 설정 수신` 화면을 열고 수신 버튼을 누릅니다.
5. 다른 탭에서 새 로그를 생성해 SSE 이벤트가 들어오는지 확인합니다.
6. 2번 화면에서 수신된 이벤트가 표와 level별 그래프로 표시되는지 확인합니다.
7. `3. SSE 3분 자동 수신` 화면을 열면 바로 실시간 수신이 시작됩니다. 약 3분 동안 새 이벤트를 받고, 수신된 이벤트는 최근 이벤트 표와 level별 그래프로 함께 표시됩니다.

## SSE 연결 오류가 날 때

2번과 3번 화면은 모두 Python `httpx.stream()` 방식으로 `GET /stream/logs`를 호출합니다.

연결 오류가 계속 나오면 아래를 확인합니다.

SSE 연결이 오래 열려 있어도 끊기지 않도록 backend는 10초마다 `event: heartbeat`를 보냅니다. 이 heartbeat는 연결 유지용 신호라서 2번/3번 화면의 log 표와 그래프 집계에는 포함하지 않습니다.

1. FastAPI backend가 실행 중인가?
2. `http://127.0.0.1:8000/health`가 열리는가?
3. `http://127.0.0.1:8000/stream/logs`를 직접 열면 `event: connected`가 보이는가?
4. backend를 수정한 뒤 기존 터미널을 끄고 다시 실행했는가?
