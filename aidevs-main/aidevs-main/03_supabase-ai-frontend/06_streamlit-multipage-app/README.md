# 06. Streamlit Multipage App

이 단원은 Streamlit의 `st.Page`, `st.navigation()` 구조를 이용해 왼쪽 메뉴 기반 앱을 만드는 연습입니다.

`99_final-frontend-project`로 가기 전에, 화면을 파일 단위로 나누고 팀에서 각 화면을 나누어 개발하는 방식을 먼저 익힙니다.

이 예제는 실제 backend API를 호출하지 않습니다. 화면 흐름을 익히기 위한 mock 앱입니다.

따라서 이 단원만 실행할 때는 `backend`를 먼저 실행하지 않아도 되고, `.env`나 `API_BASE_URL`도 필요하지 않습니다. 실제 API 연결은 `03_api-integration`, `05_ai-chatbot-interface`, `99_final-frontend-project`에서 다룹니다.

## 학습 목표

- Streamlit 왼쪽 메뉴 기반 멀티페이지 앱 구조를 이해합니다.
- `app.py`와 `pages/*.py`의 역할 차이를 이해합니다.
- `app.py`에서 `st.Page`, `st.navigation()`으로 메뉴 이름과 순서를 관리합니다.
- 왼쪽 sidebar에 로그인 UI를 두고 모든 화면에서 같은 로그인 상태를 공유합니다.
- 회원가입, 로그조회, Chat, 데이터베이스조회 화면을 각각 별도 파일로 구성합니다.
- 팀 개발에서 page 단위로 작업을 나누는 방식을 이해합니다.

## 폴더 구조

```text
06_streamlit-multipage-app
├─ README.md
├─ app.py
├─ frontend_common.py
└─ pages
   ├─ 01_signup.py
   ├─ 02_log_view.py
   ├─ 03_chat.py
   └─ 04_database_view.py
```

| 파일 | 역할 |
| --- | --- |
| `app.py` | `st.Page`, `st.navigation()`으로 왼쪽 메뉴 구성 |
| `frontend_common.py` | 로그인 상태, mock 데이터, 공통 sidebar 함수 |
| `pages/01_signup.py` | 회원가입 화면 |
| `pages/02_log_view.py` | 로그조회 화면 |
| `pages/03_chat.py` | Chat 화면 |
| `pages/04_database_view.py` | 데이터베이스조회 화면 |

## 실행 방법

```powershell
cd C:\aidev\03_supabase-ai-frontend\06_streamlit-multipage-app
C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
streamlit run .\app.py
```

실행 후 브라우저 왼쪽 사이드바에서 각 화면을 선택합니다.

이 예제는 mock 데이터만 사용하므로 아래 준비는 필요하지 않습니다.

```text
FastAPI backend 실행
.env 생성
API_BASE_URL 설정
Supabase/Gemini/Redis key 설정
```

## navigation 구조에서 화면을 개발하는 방법

Streamlit 멀티페이지 앱은 항상 `app.py`로 실행합니다.

```powershell
streamlit run .\app.py
```

그 다음 브라우저 왼쪽 메뉴에서 개발 중인 화면을 선택합니다.

예를 들어 Chat 화면을 개발한다면:

```text
수정 파일:
  C:\aidev\03_supabase-ai-frontend\06_streamlit-multipage-app\pages\03_chat.py

실행 명령:
  streamlit run .\app.py

확인 방법:
  브라우저 왼쪽 사이드바에서 03_chat 선택
```

보통 아래처럼 page 파일을 직접 실행하지 않습니다.

```powershell
streamlit run .\pages\03_chat.py
```

직접 실행하면 해당 page만 단독 앱처럼 열리기 때문에, 전체 앱의 진입점, sidebar 로그인, 다른 화면과의 이동 흐름을 함께 확인하기 어렵습니다.

## 각 화면은 무엇을 담당하나요?

| 화면 | 담당 파일 | 개발자가 구현할 내용 |
| --- | --- | --- |
| 메뉴 구성 | `app.py` | `st.Page`, `st.navigation()`으로 화면 이름과 순서 정의 |
| 회원가입 | `pages/01_signup.py` | 가입 폼, 입력값 검증, 가입 결과 표시 |
| 로그조회 | `pages/02_log_view.py` | 로그 테이블, level 필터, 차트 |
| Chat | `pages/03_chat.py` | 메시지 입력, 대화 출력, mock assistant 응답 |
| 데이터베이스조회 | `pages/04_database_view.py` | 테이블 선택, 데이터프레임 표시 |
| 공통 기능 | `frontend_common.py` | 로그인 상태, 로그아웃, sample data, 공통 sidebar |

## 팀 개발에서는 어떻게 나누나요?

실제 팀 개발에서는 화면 단위로 담당자를 나눕니다.

예:

```text
개발자 A -> 회원가입 화면
개발자 B -> 로그조회 화면
개발자 C -> Chat 화면
개발자 D -> 데이터베이스조회 화면
공통 담당자 또는 팀 리드 -> frontend_common.py, app.py
```

이렇게 나누면 각 개발자가 자기 화면 파일을 중심으로 작업할 수 있습니다.

```text
개발자 A가 주로 수정하는 파일:
  pages/01_signup.py

개발자 B가 주로 수정하는 파일:
  pages/02_log_view.py

개발자 C가 주로 수정하는 파일:
  pages/03_chat.py

개발자 D가 주로 수정하는 파일:
  pages/04_database_view.py
```

## 팀 개발에서 중요한 규칙

### 1. 공통 코드는 마음대로 바꾸지 않습니다.

`frontend_common.py`는 모든 page가 함께 쓰는 파일입니다.

여기에 들어가는 예:

```text
로그인 상태 초기화
로그인/로그아웃 함수
공통 sidebar
sample 로그 데이터
sample DB 데이터
```

공통 파일을 바꾸면 모든 화면에 영향을 줄 수 있습니다. 따라서 팀에서는 보통 아래처럼 정합니다.

```text
공통 파일 수정 전:
  팀원에게 먼저 공유
  어떤 page에 영향이 있는지 확인
  수정 후 모든 page를 한 번씩 실행 확인
```

### 2. 각 page 파일은 자기 화면만 담당합니다.

`pages/03_chat.py`에서 회원가입 UI를 고치거나, `pages/01_signup.py`에서 로그조회 로직을 고치면 구조가 흐려집니다.

좋은 기준:

```text
회원가입 관련 UI -> pages/01_signup.py
로그조회 관련 UI -> pages/02_log_view.py
Chat 관련 UI -> pages/03_chat.py
DB 조회 관련 UI -> pages/04_database_view.py
여러 화면에서 반복되는 함수 -> frontend_common.py
```

### 3. page 간 데이터 공유는 session_state로 합니다.

이 예제에서는 로그인 상태와 chat 메시지를 `st.session_state`에 저장합니다.

```text
is_logged_in
current_user
chat_messages
registered_users
```

각 page는 시작할 때 `init_state()`를 호출해 필요한 값이 없을 때 기본값을 만들어 둡니다.

```python
from frontend_common import init_state

init_state()
```

이 호출이 없으면 특정 page를 먼저 열었을 때 session_state key가 없어서 오류가 날 수 있습니다.

### 4. 작업 순서를 정하고 개발합니다.

추천 순서:

```text
1. app.py에서 전체 앱 실행 확인
2. frontend_common.py에서 로그인 sidebar 확인
3. pages/01_signup.py 회원가입 화면 개발
4. pages/02_log_view.py 로그조회 화면 개발
5. pages/03_chat.py Chat 화면 개발
6. pages/04_database_view.py DB 조회 화면 개발
7. 모든 page를 왼쪽 사이드바에서 한 번씩 열어 최종 확인
```

### 5. 충돌을 줄이는 방법

팀원이 동시에 같은 파일을 수정하면 Git 충돌이 생기기 쉽습니다.

충돌을 줄이는 방법:

```text
각자 담당 page 파일을 정합니다.
공통 파일(frontend_common.py)은 한 사람이 관리하거나, 수정 전에 팀에 알립니다.
작은 단위로 자주 commit합니다.
작업 전 최신 코드를 pull합니다.
PR 또는 코드 리뷰에서 다른 page에 영향이 있는지 확인합니다.
```

## 최종 프로젝트와의 연결

이 단원은 `99_final-frontend-project/solution_multipage`와 `04_supabase-ai-mini-project/03_project_structure/frontend_multipage`로 이어집니다.

```text
06_streamlit-multipage-app
-> backend 없는 mock 화면 흐름 연습

99_final-frontend-project/solution_multipage
-> backend_mock 또는 backend_service와 연결한 최종 멀티페이지 예제
```

즉, 06에서는 화면 분리와 팀 개발 방식을 익히고, 99에서는 실제 API 연결까지 포함한 완성 구조를 확인합니다.
