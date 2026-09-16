# 확인한 최종 소스 줄 번호로 학습 문서를 만든다. 기존 문서는 덮어쓰지 않는다.
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
TEXT = r'''# 프로젝트 코드 따라 읽기: Multi-LLM 여행 준비 앱

> 작성·검사일: 2026-09-15, 한국 시간(KST). 선택한 프로젝트 루트 안에서 확인한 소스만 해설했다. 실행 순서는 기존 [guide.md](../guide.md)를 유지한다. 이 문서의 명령은 **설명용**이며, 실제 수행한 검사는 10절에서 별도로 구분한다.

## 1. 이 프로젝트가 해결하는 문제와 대표 시나리오

여행 준비 질문을 입력하고 OpenAI·Gemini·Ollama 중 **선택한 한 공급자**의 답변을 받는 앱이다. 화면과 API를 서로 다른 컨테이너로 나누고, 최근 대화는 Redis에, 대화 기록과 여행 메모는 PostgreSQL에 저장하는 연결을 배운다. 예약·결제 기능이나 여러 에이전트의 협업, 작업 큐, MCP, 백그라운드 워커는 없다.

대표 시나리오는 다음과 같다.

1. 화면 사이드바에서 공급자를 고른다. Ollama를 선택하면 `gemma` 또는 `llama`도 고른다.
2. 채팅 입력창에 “부산 1박 2일 여행 준비물을 알려줘”를 제출한다.
3. 화면의 Python 코드가 Backend에 JSON을 보낸다. Backend는 입력을 검증하고 최근 문맥을 읽은 뒤 질문을 저장한다.
4. 선택한 모델이 답하면 답변을 영구 저장하고 Redis 문맥·통계를 갱신한다. 화면에는 답변과 공급자·모델·대체 여부가 표시된다.
5. “새 대화 시작”을 누르면 이전 Redis 문맥을 지우고 새로운 세션 ID를 사용한다. 이전 PostgreSQL 기록은 남는다.

채팅 외에 “여행 메모” 탭에서 메모 저장·조회, “서비스 상태” 탭에서 상태 조회를 할 수 있다. 화면에 있는 기능은 [[frontend/app.py|with st.sidebar:]], [[frontend/app.py|with chat_tab:]], [[frontend/app.py|with note_tab:]], [[frontend/app.py|with status_tab:]]에서 확인했다. 모델의 여행 도우미 안내문은 [[backend/services.py|def _prompt(]]에 있다.

## 2. 실제 폴더 지도와 책임

아래는 파일의 위치를 보여 주는 지도다. 호출 순서 그림은 4절에 따로 있다. 전체 인벤토리에서 외부 링크·정션은 발견하지 못했으며, `.github/workflows`, JavaScript/TypeScript, HTML 템플릿, `package.json`, 독립 JSON 앱 설정은 없다.

```text
01_simple-multi-llm-compose/
├─ frontend/                    화면 경계: Streamlit 서버
│  ├─ app.py                    위젯, 세션 ID, HTTP 요청, 결과·오류 표시
│  ├─ requirements.txt          Streamlit·httpx 의존성 범위
│  └─ Dockerfile                화면 이미지와 시작 명령
├─ backend/                     API 경계: FastAPI 서버
│  ├─ app.py                    입력 계약, 의존성 주입, 라우트와 처리 순서
│  ├─ services.py               Redis·SQL·외부 모델 통신
│  ├─ test_app.py               메모리 가짜 객체를 쓰는 계약 테스트 3개
│  ├─ requirements.txt          서버·저장소 드라이버·모델 SDK 의존성
│  └─ Dockerfile                API 이미지와 시작 명령
├─ database/
│  └─ init.sql                  스키마, 테이블 2개, 인덱스 1개 정의
├─ init_database.py             공용 DB를 준비하는 별도 관리 스크립트
├─ compose.yml                 기존 공용 서비스 + 앱 2개 빌드
├─ compose.full-stack.yml      저장소까지 생성 + 선택 Ollama
├─ compose.release.yml         준비된 앱 이미지를 받아 사용하는 설정
├─ .env.example                환경변수 예제: 변수명·용도만 해설
├─ .env                        존재만 확인, 내용 읽기·수정·복사 제외
├─ README.md                   실행 방식과 이미지 전달 교재
├─ COMPOSE_EXPLAINED.md         주소·볼륨·DB 초기화 연결 교재
├─ TROUBLESHOOTING.md           장애 실습 교재
├─ guide.md                    기존 Project Player 실행 순서, 수정하지 않음
├─ debug.log                   내용 읽기·인용·복사 제외
├─ docs/
│  └─ project-walkthrough.md    현재 통합 학습 문서
└─ .project-player/            실행기 및 이번 해설 작업의 내부 기록
   ├─ annotation-prompt.md
   ├─ setup-guide-prompt.md
   ├─ setup-guide-result.md
   ├─ setup-guide-294ce422cb344ceda8549efa9ecd53ed-result.md
   ├─ annotation-baseline/     수정 전 원본 17개와 manifest.json
   └─ annotation-tools/        주석·문서 생성 도구와 검증 JSON
```

화면은 브라우저에서 사용하는 UI지만 `frontend/app.py` 자체는 **Streamlit 서버에서 실행되는 Python**이다. `httpx` 요청도 그 프로세스가 보낸다. Backend는 세션 ID를 받아 저장소를 구분할 뿐 로그인 사용자를 확인하는 계층은 없다. 데이터 모델은 API 입력 모델과 SQL 테이블로 나뉘며 ORM은 사용하지 않는다.

## 3. 실행 환경과 설정을 구분해서 이해하기

### 런타임·패키지·가상환경

| 항목 | 실제 설정 근거 | 필요한 이유 / 이번 확인 범위 |
| --- | --- | --- |
| Python 3.12 컨테이너 | [[backend/Dockerfile|FROM python:]], [[frontend/Dockerfile|FROM python:]] | 두 앱의 실행 환경. 이미지가 실제 이 버전으로 실행 중인지는 확인하지 않았다. |
| Backend 패키지 | [[backend/requirements.txt|fastapi>=]]부터 14행 | FastAPI·Uvicorn, Redis·Psycopg, google-genai·openai, httpx. 모두 범위 명세라 정확한 설치 버전 목록은 아니다. |
| Frontend 패키지 | [[frontend/requirements.txt|streamlit>=]], [[frontend/requirements.txt|httpx>=]] | Python 화면과 API 요청에 필요하다. Node 런타임이나 npm 설치는 앱에 필요하지 않다. |
| Host venv | 루트 `.venv`·`venv` 없음 | Host에서 패키지를 격리하는 폴더다. 컨테이너로 앱을 실행할 때 Host venv가 반드시 필요한 것은 아니다. |
| 별도 초기화 도구 | [[init_database.py|import psycopg]], [[init_database.py|from dotenv import load_dotenv]] | Host에서 공용 DB를 준비할 때 사용한다. `python-dotenv`는 Backend 명세에 없고 `pytest`도 명세에 없다. |
| 이번 정적 검증용 Python | 설치된 pgAdmin 부속 Python 3.13.14 | 앱 실행 환경과 다르다. Python 3.12 문법 모드의 AST 검사에 사용했으며 패키지는 설치하지 않았다. |
| 실제 `.env` | 파일 존재만 관찰 | 입력 완료·키 유효성·실제 선택 모델은 확인하지 않았다. 기존 로그인·인증·모델 설정을 변경하지 않았다. |

Dockerfile은 `requirements.txt`를 먼저 복사·설치한 후 앱 소스를 복사한다. 명세가 그대로라면 이미지 빌드에서 패키지 계층을 재사용할 수 있다. `CMD`는 이미지 생성 때 실행하는 코드가 아니라 컨테이너 시작 때 실행할 기본 명령이다. Backend의 `app:app`은 **`app.py` 모듈 안의 `app` 객체**를 뜻한다. 근거: [[backend/Dockerfile|COPY requirements]], [[backend/Dockerfile|CMD]], [[frontend/Dockerfile|CMD]].

### 세 Compose 구성의 경계

| 구성 | 앱 공급 방식 | 저장소·모델 연결 설정 | Host에서 화면 / API | 근거 |
| --- | --- | --- | --- | --- |
| `compose.yml` | 두 앱을 로컬 소스로 빌드 | 기본값은 `host.docker.internal`의 Redis 6379·DB 5433·Ollama 11434. 환경변수로 변경 가능 | **80 → 8501** / 8000 → 8000 | [[compose.yml|build: ./backend]], [[compose.yml|REDIS_URL:]], [[compose.yml|- "80:8501"]] |
| `compose.full-stack.yml` | 두 앱 빌드 + Redis·DB + 선택 Ollama 이미지 | 네트워크 안의 `redis:6379`, `database:5432`, `ollama:11434`. 저장소 Host 포트 공개 없음 | 8501 → 8501 / 8000 → 8000 | [[compose.full-stack.yml|services:]], [[compose.full-stack.yml|REDIS_URL:]], [[compose.full-stack.yml|- "8501:8501"]] |
| `compose.release.yml` | `BACKEND_IMAGE`, `FRONTEND_IMAGE`로 기존 이미지 지정 | 기본 구성과 같이 공용 서비스로 연결 | 8501 → 8501 / 8000 → 8000 | [[compose.release.yml|image: ${BACKEND_IMAGE]], [[compose.release.yml|image: ${FRONTEND_IMAGE]], [[compose.release.yml|- "8501:8501"]] |

`80:8501`에서 왼쪽은 사용자의 PC인 Host 포트, 오른쪽은 컨테이너 내부 포트다. 컨테이너 안의 `127.0.0.1`은 그 컨테이너 자신을 가리킨다. 화면 컨테이너가 API를 찾는 주소는 세 구성 모두 `BACKEND_URL`을 통해 `backend:8000`으로 정한다. 별도의 `networks:` 선언은 없으며 Compose 기본 네트워크와 서비스 이름을 사용하도록 설정되어 있다.

Full Stack은 Redis·DB의 건강 상태를 기다린 후 Backend를 시작하고, Backend 준비 확인 성공 후 Frontend를 시작한다. 기본·release는 외부 저장소를 생성하거나 `depends_on`으로 관리하지 않고 Backend 준비 API에서 연결을 확인한다. `service_healthy`는 시작 조건이며 모델 호출 성공을 보장하지 않는다. Full Stack의 Ollama에는 healthcheck가 없고 Backend의 `depends_on`에도 없다. 근거: [[compose.full-stack.yml|depends_on:]], [[compose.full-stack.yml|profiles:]], [[compose.yml|condition: service_healthy]].

### 환경변수 이름과 용도

이 표는 `.env.example`에 있는 **키 이름**과 소스의 사용 위치를 연결한다. 예제 값·실제 자격 증명은 인용하지 않았고 환경 파일에는 주석을 넣지 않았다. `BACKEND_URL`은 예제 파일의 키 목록에는 없으며 Compose에서 Frontend에 직접 전달한다.

| 변수 이름 | 용도와 읽는 위치 | 다음 연결 |
| --- | --- | --- |
| `OPENAI_API_KEY`, `GEMINI_API_KEY` | `configured()`가 설정 존재 확인 | [[backend/services.py|def configured(]] → 선택한 SDK 분기 |
| `OPENAI_MODEL`, `GEMINI_MODEL` | 공급자 모델명 선택 | [[backend/services.py|def model(]] |
| `OLLAMA_ENABLED` | 문자열 플래그를 참/거짓으로 해석 | `configured()`; Ollama 프로필·모델 다운로드와 별개 |
| `OLLAMA_BASE_URL` | Ollama HTTP 서버 주소 | [[backend/services.py|base_url = os.getenv(]] |
| `OLLAMA_MODEL`, `GEMMA_MODEL` | `ollama_model` 선택에 따른 모델명 | `model()` → `/api/chat` 요청 본문 |
| `REDIS_URL` | Redis 접속 대상 | [[backend/services.py|self.client = redis.from_url(]] |
| `DATABASE_URL` | Backend PostgreSQL 접속 대상 | [[backend/services.py|self.url = url or os.getenv(]] |
| `HOST_DATABASE_URL` | 별도 초기화 프로그램에서 우선 사용할 접속 설정 | [[init_database.py|def host_database_url(]] |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Full Stack DB 초기 생성 및 Backend 접속 구성 | [[compose.full-stack.yml|POSTGRES_USER:]] |
| `BACKEND_IMAGE`, `FRONTEND_IMAGE` | release 이미지와 버전 선택 | `compose.release.yml`의 `image` 키 |
| `BACKEND_URL` | Streamlit에서 API 주소 구성 | [[frontend/app.py|BACKEND_URL =]] |

일반 앱 모듈은 `.env`를 직접 읽는 코드를 갖고 있지 않다. Compose가 환경변수를 컨테이너에 전달한다. `init_database.py`만 `load_dotenv`를 호출한다. 공용 DB는 이 폴더의 SQL을 자동으로 실행하지 않으며, Full Stack은 SQL을 초기화 경로에 읽기 전용으로 연결한다. **기존 볼륨에 테이블이 없다고 컨테이너 시작만으로 SQL이 재실행되는 것은 아니다.** 근거: [[init_database.py|load_dotenv(ENV_PATH)]], [[compose.full-stack.yml|- ./database/init.sql:]].

아래 명령은 파일의 의미를 읽기 위한 **설명용 예시이며 이번 작업에서 실행하지 않았다.**

```powershell
# 이미지 안에서 CMD가 의미하는 서버 시작 예시
uvicorn app:app --host 0.0.0.0 --port 8000
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
# Host의 패키지를 격리할 때 쓰는 명령의 형태
python -m venv .venv
```

현재 사용 중인 Compose 파일·이미지 태그·모델 준비 상태는 미확인이다. 8501번 응답이 있다는 사실만으로 Full Stack 또는 release 사용을 단정할 수 없다.

## 4. 전체 워크플로우: 코드에 근거한 호출 흐름

**정적 코드 흐름 그림**이다. 주요 저장·모델 호출을 실제로 재현한 실행 추적은 아니다. 저장소 주소는 3절의 선택 구성에 따라 달라지며, 모델 분기는 설정이 준비된 경우에만 진행한다.

```mermaid
flowchart TD
    B["브라우저: 여행 질문 제출"]
    F["Streamlit: 입력과 세션 ID"]
    A["api: POST /api/chat"]
    V["FastAPI: ChatRequest 검증과 Depends"]
    C["chat: 선택 공급자 설정 확인"]
    R["Redis: 최근 세션 문맥 읽기"]
    U["PostgreSQL: 사용자 메시지 저장"]
    S["MultiLLMChatService.reply: 프롬프트와 모델 선택"]
    O["조건부 OpenAI: Responses API"]
    G["조건부 Gemini: generate_content"]
    L["조건부 Ollama: POST /api/chat, stream=False"]
    P["PostgreSQL: assistant 메시지 저장"]
    W["Redis: 세션 12개 유지, TTL 갱신, 요청 통계"]
    J["JSON: answer, provider, model, request_count"]
    E["HTTP 오류: 422 또는 503"]
    D["Streamlit: 답변 또는 오류 표시"]
    B -->|"입력 이벤트"| F
    F -->|"4개 필드 JSON"| A
    A -->|"HTTP 요청"| V
    V -->|"검증 통과"| C
    V -->|"잘못된 입력"| E
    C -->|"미설정 공급자"| E
    C -->|"설정됨"| R
    R -->|"문맥 목록"| U
    U -->|"질문 저장 후 호출"| S
    S -->|"openai 선택"| O
    S -->|"gemini 선택"| G
    S -->|"ollama 선택"| L
    O -->|"LLMReply.text"| P
    G -->|"LLMReply.text"| P
    L -->|"LLMReply.text"| P
    S -->|"모델 처리 예외"| E
    P -->|"영구 저장 후"| W
    W -->|"처리 완료"| J
    J -->|"HTTP JSON 응답"| D
    E -->|"raise_for_status와 show_error"| D
    D -->|"화면 갱신"| B
```

### 노드·화살표 근거

| 노드 / 화살표 | 상대 경로·최종 줄 번호·심벌 | 무엇을 확인했는가 |
| --- | --- | --- |
| B·F·A, B→F→A | [[frontend/app.py|prompt = st.chat_input]], [[frontend/app.py|result = api("POST"]] | 입력 조건과 실제 네 필드 POST |
| A→V | [[frontend/app.py|def api(]], [[backend/app.py|@app.post("/api/chat")]] | `httpx.request`에서 FastAPI 경로로 연결 |
| V→C, V→E | [[backend/app.py|class ChatRequest]], [[backend/app.py|RedisDep =]], [[backend/app.py|def chat(]] | Pydantic 입력 검증, 의존성 생성 함수 주입 |
| C→E·R | [[backend/app.py|if not llm.configured(payload.provider)]], [[backend/app.py|recent = redis_store.load_session]] | 설정 확인 후에만 Redis 접근 |
| R·R→U | [[backend/services.py|def load_session(]], [[backend/app.py|database.add_chat_message(payload.session_id, "user"]] | Redis JSON 복원 후 사용자 기록 저장 |
| U·U→S | [[backend/services.py|def add_chat_message(]], [[backend/app.py|reply = llm.reply(]] | DB 커밋 뒤 서비스 호출 순서 |
| S | [[backend/services.py|def reply(]], [[backend/services.py|def _prompt(]], [[backend/services.py|def model(]] | 문맥 6개로 프롬프트와 모델명 구성 |
| S→O, O→P | [[backend/services.py|response = OpenAI().responses.create]], [[backend/services.py|return LLMReply(]], [[backend/app.py|database.add_chat_message(payload.session_id, "assistant"]] | OpenAI 분기 반환값으로 답변 저장 |
| S→G, G→P | [[backend/services.py|response = gemini_client.models.generate_content]], `LLMReply`, `chat`의 assistant 저장 | Gemini 분기도 같은 반환 계약 |
| S→L, L→P | [[backend/services.py|response = httpx.post(]], [[backend/services.py|text = response.json()["message"]]], `chat`의 assistant 저장 | Ollama JSON에서 내용 추출, 스트림 비활성 |
| S→E | [[backend/app.py|detail=f"Chat 처리 실패:]], [[backend/services.py|if not text:]] | 외부 호출·빈 응답 예외가 503으로 변환 |
| P·P→W | [[backend/app.py|redis_store.append_session]], [[backend/services.py|def append_session(]] | 질문·답변 영구 저장 뒤 최근 세션 갱신 |
| W→J | [[backend/app.py|request_count = redis_store.record_request(payload.message)|2]], [[backend/app.py|"answer": reply.text]], [[backend/services.py|def record_request(]] | 채팅의 통계 갱신과 최종 dict 응답. |
| J→D, E→D, D→B | [[frontend/app.py|response.raise_for_status()]], [[frontend/app.py|st.write(result["answer"])]], [[frontend/app.py|def show_error(]] | 정상 답변과 오류를 화면에 표시 |
| 실제 테이블 P·U | [[database/init.sql|CREATE TABLE IF NOT EXISTS simple_multi_llm.chat_messages]] | 저장 열은 session_id·role·content·created_at 등 |

저장소 예외도 `chat()`의 같은 `except`로 들어가 503이 된다. 그림에서는 화살표가 지나치게 겹치지 않도록 모델 예외 하나를 표시했다. **영구 기록 GET은 PostgreSQL을 읽지만, 모델 문맥은 Redis만 읽는다.** Redis가 비거나 만료됐을 때 DB 기록으로 문맥을 복원하는 코드는 없다. 메모·상태·초기화의 별도 흐름은 6절에서 다룬다.

## 5. 시간 순서: 한 번의 채팅 제출과 오류 분기

**정적 코드 순서 다이어그램**이다. `def`와 동기 HTTP/SDK 호출을 사용하며, `async`/`await`, 작업 등록 후 폴링, 토큰 스트리밍, 콜백 처리 단계는 없다. Frontend의 요청 대기 timeout은 100초, Ollama 호출은 90초로 명시되어 있다. 다른 SDK의 실제 대기 정책은 이 소스에서 직접 설정하지 않는다.

```mermaid
sequenceDiagram
    actor U as "사용자"
    participant F as "Streamlit Python"
    participant A as "FastAPI /api/chat"
    participant R as "RedisSessionStore"
    participant P as "PostgresRepository"
    participant S as "MultiLLMChatService"
    participant M as "선택한 모델 API"
    U->>F: 질문 제출과 공급자 선택
    F->>A: GET /api/chat/{session_id}
    A->>P: list_chat(session_id)
    P-->>A: 기존 기록 목록
    A-->>F: messages JSON
    F->>A: POST /api/chat, JSON 네 필드
    Note over A: ChatRequest 검증과 Depends 주입
    alt 입력 형식 위반
        A-->>F: 422 검증 오류
        F-->>U: show_error
    else 입력 유효
        A->>S: configured(provider)
        S-->>A: 환경변수 기반 참 또는 거짓
        alt 공급자 미설정
            A-->>F: 503 설정 확인 오류
            F-->>U: show_error
        else 공급자 설정됨
            A->>R: load_session(session_id)
            R-->>A: 최근 메시지 목록
            A->>P: add_chat_message(user, message)
            P-->>A: 질문 저장, 독립 트랜잭션 완료
            A->>S: reply(provider, message, recent, ollama_model)
            S->>S: _prompt와 model
            S->>M: 선택된 분기의 동기 생성 요청
            alt 모델 호출 실패
                M-->>S: 예외 또는 실패 응답
                S-->>A: 예외 전파
                A-->>F: 503 Chat 처리 실패
                F-->>U: show_error, 먼저 저장한 질문은 남음
            else 모델 텍스트 반환
                M-->>S: 생성 텍스트
                S-->>A: LLMReply
                A->>P: add_chat_message(assistant, reply.text)
                P-->>A: 답변 저장, 독립 트랜잭션 완료
                A->>R: append_session(user와 assistant)
                Note over R: RPUSH, LTRIM 마지막 12개, EXPIRE 1800초
                A->>R: record_request(message)
                R-->>A: 누적 요청 횟수
                A-->>F: answer, provider, model 등 JSON
                F-->>U: 답변과 공급자 정보 표시
            end
        end
    end
```

### 시간 순서의 근거

| 구간 | 파일·심벌·최종 줄 번호 | 주의할 점 |
| --- | --- | --- |
| POST 전에 기록 GET | [[frontend/app.py|history = api("GET"]], [[backend/app.py|def get_chat_history(]], [[backend/services.py|def list_chat(]] | 재실행 때 기존 이력을 그린 다음 제출값을 처리한다. 다이어그램은 기록 조회가 성공한 경우를 선택했다. |
| POST 검증과 객체 주입 | [[backend/app.py|class ChatRequest]], [[backend/app.py|RedisDep =]], [[backend/app.py|def chat(]] | 길이·허용 문자열·정규식 검사. 인증 단계는 없다. |
| 미설정 503 | [[backend/app.py|if not llm.configured(payload.provider)]], [[backend/services.py|def configured(]] | 저장소에 접근하기 전 반환한다. 실제 API 키 유효성 검사는 아니다. |
| 문맥 읽기·질문 저장 | [[backend/app.py|recent = redis_store.load_session]], [[backend/services.py|def add_chat_message(]] | DB 저장은 메서드마다 별도 `with` 연결이다. |
| 모델 요청·응답 | [[backend/services.py|def reply(]]부터 247행 | 분기 하나만 호출하고 `LLMReply`로 통일한다. |
| 모델 오류 전파 | [[backend/services.py|response.raise_for_status()]], [[backend/services.py|if not text:]], [[backend/app.py|detail=f"Chat 처리 실패:]] | 이미 저장한 user 행을 되돌리는 코드가 없다. |
| 답변 저장·Redis 갱신·응답 | [[backend/app.py|database.add_chat_message(payload.session_id, "assistant"]]부터 188행 | 여기서 Redis가 실패하면 두 DB 행이 남아도 전체 응답은 503이다. |
| 성공·오류 화면 | [[frontend/app.py|st.write(result["answer"])]], [[frontend/app.py|def show_error(]] | 이번에는 실제 모델 질문 제출이나 오류 유발 요청을 보내지 않았다. |

## 6. 파일별 읽기 순서와 줄별 해설

소스의 `# [학습]` 또는 SQL의 `-- [학습]` 주석을 먼저 읽고 아래 연결을 따라간다. 기존 docstring과 기존 주석은 보존했다. 범위의 숫자는 주석 삽입 후 최종 파일 기준이다.

### 6-1. 화면 → 요청 계약 → 서비스 → 테이블

| 순서 / 파일 | 최종 줄·심벌 | 쉬운 해석 | 다음 연결 |
| --- | --- | --- | --- |
| 1. `frontend/app.py` | 1–23, `BACKEND_URL`, `api` | import 역할, 환경변수 주소, 요청·오류 상태 검사·JSON 복원 | FastAPI의 실제 라우트 |
| 같은 파일 | 26–39, `show_error` | HTTP 오류는 detail, JSON이 아니면 텍스트, 연결 오류는 별도 문구 | 각 화면 블록의 except |
| 같은 파일 | 42–74 | 페이지 구성, 재실행 중 세션 ID 보존, 공급자 선택, 새 대화 처리 | DELETE 세션 API |
| 같은 파일 | 76–102 | 기존 기록 반복 렌더링 → 입력 확인 → 채팅 POST → 답변 표시 | `chat`, `get_chat_history` |
| 같은 파일 | 104–125 | 폼 제출 메모 저장·버튼 조회·상태 버튼 | `/api/notes`, `/health` |
| 2. `backend/app.py` | 1–56 | import, FastAPI 객체, 입력 BaseModel, 캐시된 생성 함수와 Annotated 별칭 | `services.py`의 객체 |
| 같은 파일 | 59–110, `live`, `health`, `ready` | 생존·저장소 상태·요청 수신 준비를 구분 | `ping`, `schema_ready`, `configured` |
| 같은 파일 | 113–147 | 메모 저장·조회와 통계. 메모 저장 후 Redis 실패는 warning | `add_note`, `list_notes`, `stats` |
| 같은 파일 | 150–188, `chat` | 설정 확인, 읽기·저장·모델 호출 순서, 예외와 응답 | 서비스의 세 클래스 |
| 같은 파일 | 191–207 | DB 이력 조회와 Redis 세션 삭제 | 전체 이력과 최근 문맥의 차이 |
| 3. `backend/services.py` | 1–24, `LLMReply` | 통신 라이브러리와 불변 반환 데이터 객체 | `reply` → `chat` |
| 같은 파일 | 27–76, `RedisSessionStore` | 접속 객체·TTL 상태·카운터·JSON 목록·세션 키 삭제 | Redis 명령 |
| 같은 파일 | 79–144, `PostgresRepository` | URL 보관, 연결 검사, 테이블 검사, SQL 매개변수, 각 호출의 연결 정리 | `database/init.sql` |
| 같은 파일 | 147–197 | 공급자 목록·환경 확인·모델 선택·최근 6개 프롬프트 | `reply` |
| 같은 파일 | 199–247, `reply` | 입력 재검사·지연 import·공급자별 호출·빈 응답 예외·공통 반환 | Backend 정상/503 응답 |
| 4. `database/init.sql` | 1–13, `notes` | 스키마와 메모 표. 자동 ID·필수 문자열·기본 시각 | `NoteRequest`, `add_note` |
| 같은 파일 | 15–29, `chat_messages`, 인덱스 | 세션별 질문·답변 표와 조회용 복합 인덱스 | `add_chat_message`, `list_chat` |
| 5. `init_database.py` | 1–31 | 기존 설명, import, 파일 기준 경로, 기본 연결 설정 | Host용 URL 선택 |
| 같은 파일 | 33–46, `host_database_url` | Host 전용 환경변수 우선, 없으면 컨테이너 주소 변환, 없으면 기본값 | `psycopg.connect` |
| 같은 파일 | 49–76, `initialize_database` | SQL 읽기·실행·테이블 조회·완료 출력. 직접 실행 가드 | DB 초기화: 이번에는 미실행 |
| 6. `backend/test_app.py` | 1–63 | 가짜 저장소·모델 클래스와 오버라이드, TestClient | 실제 네트워크 대신 메모리 객체 |
| 같은 파일 | 67–90 | 상태 계약, 채팅 성공·기록 저장, 미설정 503의 세 테스트 | 테스트의 검증 범위 읽기 |

### 6-2. 모든 API 계약

| 메서드 / 경로 | 입력 → 응답 | 호출과 오류 | 코드 근거 |
| --- | --- | --- | --- |
| GET `/health/live` | 없음 → status·service | 외부 의존성 없이 200 | [[backend/app.py|def live(]] |
| GET `/health` | 없음 → status·checks·errors | Redis PING, DB SELECT·테이블 존재, 공급자 설정. degraded여도 기본 200 | [[backend/app.py|def health(]] |
| GET `/health/ready` | 없음 → health 결과 | 저장소·스키마가 준비되지 않으면 503 | [[backend/app.py|def ready(]] |
| POST `/api/notes` | name·message → note·request_count·warning | 성공 201. DB 실패 503. DB 성공 후 Redis 실패는 201+warning | [[backend/app.py|def create_note(]] |
| GET `/api/notes` | 없음 → notes 목록 | 최신 50개 기본값. DB 실패 503 | [[backend/app.py|def get_notes(]] |
| GET `/api/stats` | 없음 → request_count·recent_request | Redis 실패 503. 현재 UI 호출 없음 | [[backend/app.py|def get_stats(]] |
| POST `/api/chat` | session_id·message·provider·ollama_model → 답변 JSON | 검증 실패 422, 미설정·처리 실패 503, 성공 200 | [[backend/app.py|def chat(]] |
| GET `/api/chat/{session_id}` | 경로 문자열 → session_id·messages | 오래된 순서 최대 100개. DB 실패 503 | [[backend/app.py|def get_chat_history(]] |
| DELETE `/api/sessions/{session_id}` | 경로 문자열 → 삭제/보존 표시 | Redis 키만 삭제. DB 이력 보존, Redis 실패 503 | [[backend/app.py|def reset_current_session(]] |

`ChatRequest`는 session_id 1–100자 및 허용 문자, message 1–2000자, provider 세 값, ollama_model 두 값을 검증한다. `NoteRequest`는 name 1–50자, message 1–500자다. 공백만 있는 문자열을 별도로 제거·거부하는 validator는 없다. GET·DELETE의 경로 session_id는 `str`만 선언되어 POST의 정규식·길이 Field 검사가 그대로 적용되는 구조는 아니다. 응답은 모두 `dict` 타입 힌트이며 별도 Pydantic 응답 모델이나 `response_model` 지정은 없다.

### 6-3. 설정·패키지·교재의 구문별 연결

JSON 문법의 파일에는 주석을 넣지 않았다. 프로젝트의 독립 앱 JSON 설정은 없으며, `CMD`의 JSON 배열은 Dockerfile 앞줄 주석으로 설명했다. `.project-player`의 JSON은 도구 증거이지 앱 설정이 아니다.

| 파일 | 줄·키 | 구문 | 쉬운 해석 | 다음 연결 |
| --- | --- | --- | --- | --- |
| `backend/Dockerfile` | 2·4·6·8·10·12 | `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD` | 기반 → 작업 폴더 → 명세 → 설치 → 모듈 → Uvicorn 시작 | `backend/app.py`의 `app` |
| `frontend/Dockerfile` | 2·4·6·8·10·12 | 같은 여섯 단계 | 다른 이미지에서 Streamlit을 시작 | `frontend/app.py` 전체 실행 |
| `backend/requirements.txt` | 2·4·6·8·10·12·14 | 이름·버전 비교·`[binary]` | 패키지별 허용 버전 범위와 선택 의존성 | import가 필요로 하는 패키지 |
| `frontend/requirements.txt` | 2·4 | `streamlit`, `httpx` | UI와 서버 간 요청 라이브러리 | 화면 위젯·`api` |
| `compose.yml` | 2–26, name·services·build·environment | 들여쓴 사전과 `${변수:-기본값}` | 앱 이름·빌드 문맥·설정 전달 | Backend 서비스 객체 |
| 같은 파일 | 27–44, ports·extra_hosts·healthcheck·restart | `8000:8000`, `CMD`, 시간값 | Host 연결과 준비 API, 간격 5초·제한 3초·10회·초기 유예 10초 | `ready()` |
| 같은 파일 | 46–60, frontend | `BACKEND_URL`, `80:8501`, `service_healthy` | 내부 API 주소와 외부 화면 주소는 다르다 | Streamlit 시작 조건 |
| `compose.release.yml` | 11·50, image | `${변수:?메시지}` | 값이 없거나 비면 오류. 로컬 소스 빌드 없음 | 게시된 이미지의 코드 |
| 같은 파일 | 12–45·51–62 | environment·ports·healthcheck·depends_on | 기본 구성과 같은 Host 저장소 연결, 화면은 8501 | API 준비 후 화면 시작 |
| `compose.full-stack.yml` | 6–21, redis | image·command·volumes·healthcheck | AOF와 `redis_data`로 기록 보존, PING 검사 | Redis 세션·통계 |
| 같은 파일 | 23–43, database | environment·volumes·`CMD-SHELL` | DB 초기 설정, 데이터 볼륨, 읽기 전용 초기화 SQL, pg_isready | `database/init.sql` |
| 같은 파일 | 45–52, ollama | profiles·image·volume | 프로필로 선택, 모델 보관 볼륨. 자동 다운로드 없음 | Backend의 Ollama 분기 |
| 같은 파일 | 54–89, backend | 내부 주소·depends_on·healthcheck | Redis·DB가 건강해진 뒤 시작, 별도 앱 준비 검사 | `ready()` |
| 같은 파일 | 91–109 | frontend·volumes | 8501 공개·Backend 대기·볼륨 이름 선언 | 화면과 데이터 수명 분리 |
| `.env.example` | 3절 표의 변수 키 | `이름=값` 형식 | 값 대신 이름과 용도만 설명. 원본 주석·복사 제외 | Compose 또는 초기화 도구 |
| `README.md` | 7–102·104–170·178–292 | 실행 방식·모델·저장소·이미지 전달 | 앱을 어떻게 준비하는지에 관한 교재 | 3절 구성 비교, 포트 차이는 10절 |
| `COMPOSE_EXPLAINED.md` | 3–47·49–90 | 주소·환경변수·초기화·볼륨 | Host 주소와 내부 서비스 이름을 구분 | 세 Compose 파일 |
| `TROUBLESHOOTING.md` | 17–111·113–130 | 서비스 장애·설정 오류·초기 SQL | 저장소별 실패가 API에 다르게 나타남 | `create_note`, `chat`, `health` |
| `guide.md` | 1–43·49–106·274–496·498–555·557–940 | Player 단계·환경·Docker·향후 CI·실습 | 기존 실행 절차를 그대로 읽는다. CI 설명은 실제 workflow가 아니다 | 소스와 이 문서의 발견 사항 |

### 6-4. 데이터가 들어 있는 모양

| 위치 | 필드 / 키 | 제약·보존 규칙 | 읽기·쓰기 근거 |
| --- | --- | --- | --- |
| PostgreSQL `simple_multi_llm.notes` | id, name, message, created_at | BIGSERIAL PK, 길이 제한, NOT NULL, DB 기본 시각 | [[database/init.sql|CREATE TABLE IF NOT EXISTS simple_multi_llm.notes]], [[backend/services.py|def add_note(]] |
| PostgreSQL `simple_multi_llm.chat_messages` | id, session_id, role, content, created_at | role은 user/assistant만. 세션·id 복합 인덱스. 이 코드의 삭제 경로 없음 | [[database/init.sql|CREATE TABLE IF NOT EXISTS simple_multi_llm.chat_messages]], [[database/init.sql|CREATE INDEX]] |
| Redis 세션 키 | `runtime_demo:session:{session_id}` | JSON 문자열 리스트, 마지막 12개, append마다 1800초 TTL 갱신 | [[backend/services.py|def append_session(]] |
| Redis 누적 요청 키 | `runtime_demo:request_count` | 메모·채팅 성공 흐름의 공용 횟수. 이 코드에서는 TTL 없음 | [[backend/services.py|def record_request(]] |
| Redis 최근 요청 키 | `runtime_demo:recent_request` | 최근 질문·메모 문자열, TTL 1800초 | 같은 `record_request` |
| Streamlit 상태 | `st.session_state.session_id` | 같은 화면 세션의 재실행 간 유지. 브라우저 재접속 때 동일 ID를 복원하는 기능 없음 | [[frontend/app.py|if "session_id" not in st.session_state:]] |

SQL은 값 자리에 `%s`를 두고 값 튜플을 별도 전달한다. `with psycopg.connect(...)`가 각 작업의 성공 시 커밋·오류 시 롤백·연결 정리를 담당한다. 대화 전체를 하나로 묶는 트랜잭션, Redis pipeline, 세션 동시 요청 잠금은 없다. DB는 공급자·모델명을 기록하지 않고 응답 JSON만 해당 정보를 담는다.

## 7. 낯선 문법을 작은 예시로 이해하기

아래 작은 예시는 **설명용**이며 프로젝트 실행 코드에 추가하지 않았다. `**kwargs`와 `async`/`await`, `yield`를 쓰는 함수는 이 프로젝트에 없다. 실제로 등장하는 `*목록`, 제너레이터 표현식, 일반 동기 함수에 집중한다.

| 이 프로젝트의 표현·위치 | 쉬운 말 | 작은 예시(설명용) | 여기서 쓰는 이유 | 흔한 실수 |
| --- | --- | --- | --- | --- |
| `from __future__ import annotations` · [[backend/services.py|from __future__]] | 타입 설명의 평가를 미룬다 | `def f(x: Later): ...` | 타입 이름을 정의 시점에 바로 계산하지 않음 | 타입 힌트가 모든 런타임 값을 자동 검사한다고 생각함 |
| `url: str \| None = None` · [[backend/services.py|def __init__(self, url: str]] | 문자열 또는 값 없음, 생략 기본값은 None | `x: int \| None = None` | 인수·환경변수·기본 주소 우선순위 | 빈 문자열과 None의 차이를 무시함 |
| `Literal[...]`, `Field(...)` · [[backend/app.py|class ChatRequest]] | 허용 선택과 길이·형식을 정한다 | `Literal["a", "b"]` | API 입력 경계를 좁힘 | 다른 GET 경로의 단순 str에도 같은 제약이 있다고 생각함 |
| `@app.post(...)` · [[backend/app.py|@app.post("/api/chat")]] | 함수에 HTTP 경로를 등록한다 | `@app.get("/hello")` | 요청을 `chat()`에 연결 | 함수 이름만 같으면 경로도 같다고 생각함 |
| `@lru_cache` · [[backend/app.py|@lru_cache]] | 동일 인수의 함수 결과를 재사용한다 | `cached_factory()` | 생성된 저장소 객체 재사용 | 모델 응답이나 세션 데이터까지 자동 캐시된다고 생각함 |
| `Annotated[..., Depends(...)]` · [[backend/app.py|RedisDep =]] | 타입과 객체 공급 규칙을 함께 적는다 | `Depends(make_store)` | FastAPI가 객체를 주입하고 테스트는 교체 가능 | `make_store()`를 미리 실행한 값과 함수 자체를 혼동함 |
| `@dataclass(frozen=True)` · [[backend/services.py|@dataclass]] | 필드를 가진 재대입 방지 객체 | `Reply(text="안녕")` | 공급자별 답변 형식을 통일 | DB에 자동 저장되는 클래스라고 생각함 |
| `@staticmethod` · [[backend/services.py|@staticmethod]] | 객체 상태 없이 쓰는 도우미 | `Formatter.join(items)` | `_prompt`는 전달받은 값만 필요 | 불필요한 self 인수를 전달함 |
| `[json.loads(item) for item in ...]` · [[backend/services.py|return [json.loads(item)]] | 목록의 각 항목을 변환한다 | `[n * 2 for n in [1, 2]]` → `[2, 4]` | Redis 문자열을 메시지 dict로 복원 | JSON 문자열과 dict를 같은 것으로 취급함 |
| `{name: ... for name in ...}` · [[backend/app.py|"providers": {name:]] | 이름별 결과 사전을 만든다 | `{x: True for x in ["a", "b"]}` | 공급자 설정 상태를 일괄 구성 | 이 계산이 실제 모델 호출이라고 생각함 |
| `*[json.dumps(...) ...]` · [[backend/services.py|self.client.rpush(]] | 목록을 여러 인수로 펼친다 | `f(*[1, 2])`는 `f(1, 2)` | RPUSH에 메시지 여러 개 전달 | `**`도 목록을 펼친다고 생각함. `**`는 매핑용이며 여기엔 없음 |
| `recent_messages[-6:]`, `join(...)` · [[backend/services.py|history =]] | 마지막 여섯 개를 줄로 이어 붙인다 | `"\n".join(str(n) for n in [1, 2])` | 프롬프트 길이를 제한 | 여섯 메시지를 여섯 대화 쌍으로 오해함 |
| `with ... as connection, ... as cursor` · [[backend/services.py|with psycopg.connect(self.url) as connection]] | 자원 사용 범위를 만들고 나갈 때 정리한다 | `with open("sample.txt") as f: ...` | DB 연결·트랜잭션·커서 수명 관리 | 서로 다른 메서드의 with까지 한 트랜잭션으로 생각함 |
| `(limit,)` · [[backend/services.py|(limit,)]] | 원소가 하나인 튜플이다 | `(3,)`은 튜플, `(3)`은 정수 | SQL 매개변수 묶음 전달 | 마지막 쉼표를 지움 |
| `raise ... from error` · [[backend/app.py|detail=f"PostgreSQL 연결 실패:]] | 새 오류와 원래 원인을 연결한다 | `raise RuntimeError("실패") from e` | API 오류로 바꾸면서 원인 연결 보존 | except가 오류를 성공으로 바꾼다고 생각함 |
| `history or '(첫 대화)'` · [[backend/services.py|f"최근 대화:]] | 문맥이 비었으면 대체 문자열 | `"" or "처음"` → `"처음"` | 첫 질문에도 안내문 구성 | `or`가 None에만 적용된다고 생각함 |
| `x if condition else y` · [[backend/services.py|if ollama_model == "gemma"]] | 조건으로 두 값 중 하나 선택 | `"낮" if hour < 18 else "밤"` | Gemma/Llama 모델명 선택 | 두 모델을 동시에 호출한다고 해석함 |
| `lambda: fake_redis` · [[backend/test_app.py|app.dependency_overrides[get_redis_store]]] | 인수 없이 객체를 돌려주는 짧은 함수 | `lambda: 3` | 테스트 의존성 교체 | 일반 앱에서도 FakeRedis가 쓰인다고 생각함 |
| `with st.sidebar`, `with st.form` · [[frontend/app.py|with st.sidebar:]], [[frontend/app.py|with st.form(]] | 화면 요소를 놓을 영역·입력 제출 묶음 | `with st.form("f"): ...` | 화면 배치와 제출 시점 관리 | 모든 with가 DB 커밋을 뜻한다고 생각함 |
| `if __name__ == "__main__"` · [[init_database.py|if __name__ ==]] | 직접 실행한 경우만 관리 함수 호출 | `python tool.py` | import만으로 DB 초기화를 실행하지 않음 | 검증하려고 초기화 스크립트를 실행함 |

Streamlit은 위젯 상호작용에 따라 스크립트를 다시 실행하며 `session_state`는 같은 세션의 재실행 사이 값을 유지한다. 폼은 여러 입력을 제출 단위로 묶는다. 이 설명은 로컬 소스를 우선으로 하고 [공식 실행 흐름 문서](https://docs.streamlit.io/develop/api-reference/execution-flow), [공식 폼 문서](https://docs.streamlit.io/develop/concepts/architecture/forms), [공식 Session State 문서](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)로 보충했다. 설치된 앱의 Streamlit 버전은 확인하지 못했다.

## 8. 대표 요청의 데이터가 변하는 과정

다음은 **비밀값 없는 설명용 가상 데이터**다. 실제 모델 응답·DB 행·사용자 로그를 가져온 것이 아니다. provider가 설정되어 있고 각 단계가 성공했다고 가정한다.

### 8-1. 요청 JSON

```json
{
  "session_id": "travel-demo-01",
  "message": "부산 1박 2일 여행 준비물을 알려줘",
  "provider": "gemini",
  "ollama_model": "gemma"
}
```

`ollama_model`은 이 예시의 Gemini 분기에서는 모델 선택에 사용되지 않지만 요청 모델에서 유효한 값인지는 검사한다. 생략하면 기본 `gemma`가 들어간다. JSON에는 SDK 인증 키를 보내지 않는다. 인증 설정은 Backend 프로세스 환경에서 사용한다.

### 8-2. 중간 데이터와 저장 순서

| 단계 | 가상 데이터 | 코드의 해석 |
| --- | --- | --- |
| 첫 세션 문맥 | `recent = []` | Redis에 키가 없으면 빈 목록. DB 이력을 읽어 채우지 않음 |
| 사용자 기록 | `{session_id: "travel-demo-01", role: "user", content: "부산 1박 2일 여행 준비물을 알려줘"}` | PostgreSQL에 먼저 한 행 저장. id와 created_at은 DB가 부여 |
| 공통 프롬프트 | 여행 준비 도우미 안내 + 최근 대화의 첫 대화 표시 + 현재 질문 | `_prompt`가 단일 문자열 생성 |
| 모델 결과 | `LLMReply(provider="gemini", model="demo-model", text="우산과 편한 신발을 챙기세요.")` | `demo-model`은 설명용 이름, 현재 설치·가용 모델을 뜻하지 않음 |
| assistant 기록 | 같은 세션의 `role: "assistant"`, `content: "우산과 편한 신발을 챙기세요."` | 사용자 행과 별도 DB 트랜잭션으로 저장 |
| Redis 목록 | user와 assistant의 `{role, content}` 두 메시지 | JSON 문자열 두 개를 RPUSH, 마지막 12개 유지, TTL 1800초 갱신 |
| 통계 | 기존 횟수 0이라는 가정이면 1 | 프로젝트 키를 공유하므로 실제 첫 질문이라도 1이라는 보장은 없음 |

### 8-3. 최종 JSON과 화면

```json
{
  "session_id": "travel-demo-01",
  "answer": "우산과 편한 신발을 챙기세요.",
  "provider": "gemini",
  "model": "demo-model",
  "request_count": 1,
  "fallback_used": false
}
```

화면은 `answer`를 말풍선에, provider·model·fallback_used를 설명 줄에 표시한다. 같은 실행에서 사용자 질문을 `st.chat_message("user")`로 추가하는 별도 구문은 없고, 다음 스크립트 실행의 기록 GET에서 저장된 질문·답변을 읽는다. 답변 POST 직후 명시적 `st.rerun()`도 없다.

### 인증·권한·상태의 범위

로그인·사용자 테이블·소유권 검사·권한별 라우트·요청 제한은 구현되어 있지 않다. 공급자 API 키는 외부 모델 인증용이며 이 앱 이용자의 로그인 토큰이 아니다. 세션 ID를 아는 호출자가 이력 GET·Redis 삭제 API에 접근하는 것을 막는 사용자 인증 코드는 없다. Redis TTL과 Streamlit 상태는 대화 편의를 위한 상태 관리다.

## 9. 파일별 coverage와 제외 목록

주석 가능한 원래 소스·설정 **13개 모두 완료**, 기존 교재 **4개 모두 읽고 연결**, 환경 예제 **1개는 키·용도 문서 해설로 대체**했다. `.env`·로그·자동 생성 기록을 완료 소스 수에 포함하지 않았다. 외부 동시 변경으로 건너뛴 파일과 인코딩 문제로 미변경한 학습 소스는 없다.

| 대상 상대 경로 | 역할 | 상태 | 설명 범위·이유 |
| --- | --- | --- | --- |
| `frontend/app.py` | Python UI | 소스 주석 완료 | 31줄 추가. import·상태·위젯·폼·요청·렌더링·오류 전체, 1–125행 |
| `backend/app.py` | Python API | 소스 주석 완료 | 41줄 추가. 입력 모델·의존성·건강 상태·메모·통계·채팅·기록·삭제 전체, 1–207행 |
| `backend/services.py` | Python 저장소·모델 서비스 | 소스 주석 완료 | 56줄 추가. 모든 클래스·메서드·SQL·세 공급자 분기, 1–247행 |
| `backend/test_app.py` | Python 계약 테스트 | 소스 주석 완료 | 21줄 추가. 세 가짜 클래스·오버라이드·세 테스트, 1–90행. 실행은 도구 부재로 미검증 |
| `init_database.py` | Python DB 관리 | 소스 주석 완료 | 16줄 추가. 기존 docstring 보존, 경로·환경 우선순위·with·조회·직접 실행 가드, 1–76행 |
| `database/init.sql` | SQL 데이터 모델 | 소스 주석 완료 | 10줄 추가. 스키마·테이블·각 열의 역할·제약·인덱스, 1–29행 |
| `backend/Dockerfile` | Backend 이미지 | 소스 주석 완료 | 명령 6개 가까이에 6줄 추가, 1–13행 |
| `frontend/Dockerfile` | Frontend 이미지 | 소스 주석 완료 | 명령 6개 가까이에 6줄 추가, 1–13행 |
| `backend/requirements.txt` | 패키지 명세 | 소스 주석 완료 | 패키지 7개별 7줄 추가, 1–14행. 버전 범위 그대로 |
| `frontend/requirements.txt` | 패키지 명세 | 소스 주석 완료 | 패키지 2개별 2줄 추가, 1–5행 |
| `compose.yml` | 공용 서비스 구성 | 소스 주석 완료 | 20줄 추가. 서비스·환경·포트·Host 연결·건강 검사·의존·재시작 정책, 1–60행 |
| `compose.release.yml` | 이미지 수신 구성 | 소스 주석 완료 | 20줄 추가. 필수 이미지 변수와 전체 연결, 1–62행 |
| `compose.full-stack.yml` | 독립 전체 구성 | 소스 주석 완료 | 34줄 추가. 모든 서비스·환경·프로필·초기화 마운트·볼륨·건강 검사, 1–109행 |
| `.env.example` | 환경 예제 | 문서 해설 대체 | 3절에서 변수 이름·용도만. 값 인용·주석 삽입·원본 복사 제외 |
| `README.md` | 실행·전달 교재 | 기존 설명 충분 | 전체 역할을 읽고 3·6·10절에 연결. 포트 불일치는 발견 사항, 파일 보존 |
| `COMPOSE_EXPLAINED.md` | 구성 교재 | 기존 설명 충분 | 전체 90행의 서비스 주소·초기화·볼륨 설명 연결, 보존 |
| `TROUBLESHOOTING.md` | 장애 교재 | 기존 설명 충분 | 전체 131행의 장애별 API 영향 연결. 오래된 health 키는 10절 기록, 보존 |
| `guide.md` | Player 실행 교재 | 기존 설명 충분 | 구조·기존 실행 순서·설정·향후 CI·실습·제한 확인. 전체 941행 바이트 보존 |
| `.env` | 실제 환경 설정 | 제외 | 존재만 확인. 내용 읽기·복사·수정·인용 없음 |
| `debug.log` | 실행 로그 | 제외 | 개인정보·비밀값 가능성이 있는 로그로 내용 접근하지 않음 |
| `.project-player/annotation-prompt.md` | 실행기 생성 자료 | 제외 | 앱 소스가 아니며 추가 지시나 실행 근거로 읽지 않음 |
| `.project-player/setup-guide-prompt.md` | 실행기 생성 자료 | 제외 | 같은 이유 |
| `.project-player/setup-guide-result.md` | 실행기 생성 자료 | 제외 | 같은 이유 |
| `.project-player/setup-guide-294ce422cb344ceda8549efa9ecd53ed-result.md` | 실행기 생성 자료 | 제외 | 같은 이유 |
| `.project-player/annotation-baseline/**` | 이번 원본 보관 | 제외 | 원본 17개 상대 경로 보존 및 해시 manifest. 앱 학습 소스로 재집계하지 않음 |
| `.project-player/annotation-tools/**` | 이번 작업 도구·검증 기록 | 제외 | JSON에 원본 코드나 자격 증명 대신 해시·판정·시간 기록. 앱 기능에 연결하지 않음 |
| `docs/project-walkthrough.md` | 통합 학습 문서 | 문서 해설 대체 | 새 문서, 요구된 10절과 두 다이어그램·근거 표 작성 |

검사에서 `.git`, 가상환경, node_modules, vendor, 빌드·배포 산출물, 캐시, 바이너리, 잠금 파일, 데이터 덤프, 인증 저장소는 학습 소스 대상으로 삼지 않았다. 루트 밖 프로젝트 소스는 해설 범위로 확장하지 않았다. JS/TS·템플릿·CI 파일은 **발견되지 않음**이며 미완료 파일이 아니다.

## 10. 검증 결과와 남은 제한

### 기준 상태와 보존

작업 경로는 요청한 `C:\수업 보관소\aidevs-latest\aidevs-main\aidevs-main\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose`와 같았다. 루트와 부모에서 적용할 `AGENTS.md` 파일은 발견하지 못했고, 사용자가 전달한 AGENTS 지침을 적용했다. `git status --short`는 Git 저장소가 아니라는 결과였다. 따라서 2026-09-15 **15:23:25 KST**에 비밀 파일·환경 예제·로그·생성 기록을 제외한 17개 파일을 [원본 폴더](../.project-player/annotation-baseline/)에 상대 경로 그대로 보관했다. [manifest.json](../.project-player/annotation-baseline/manifest.json)에 SHA-256·원본 바이트 수·인코딩·줄바꿈 수가 있다. 이 JSON은 앱 설정이 아니며 주석을 넣지 않았다.

수정 대상은 모두 UTF-8·LF였다. `guide.md`는 LF와 CRLF가 섞여 있었으나 **전체 바이트를 그대로 보존**했다. 주석 도구는 저장 전 현재 해시와 기준을 비교하고, 기준 이후 다른 변경이 있으면 그 파일을 건너뛰도록 작성했다. 실제 13개 파일에서 동시 변경은 발견하지 못했다. 기존 docstring·문자열·SQL·포트·명령·의존성 범위·라이선스·기존 주석은 보존했다.

### 실제 수행한 검사

검증 증거는 [verification-result.json](../.project-player/annotation-tools/verification-result.json), [static-validation.json](../.project-player/annotation-tools/static-validation.json), [annotation-result.json](../.project-player/annotation-tools/annotation-result.json), [http-observation.json](../.project-player/annotation-tools/http-observation.json)에 있다. 각 JSON의 `checked_at`은 검사 시각이다. 보고서 JSON 자체도 JSON 파서로 로드해 확인했다.

| 실제 명령·검사 | 검사 대상 | 결과·근거 | 한계 |
| --- | --- | --- | --- |
| `Get-Location`, 경로·링크 제외 파일 목록, `git status --short` | 루트·파일·기존 상태 | 요청 경로 일치, Git 아님. 주석 전 기준 보관 | Git 과거 변경 이력과 비교한 것은 아님 |
| 기본 `python` 호출 | Host 별칭 | 실패: WindowsApps 경로 접근 거부 | 새 Python이나 패키지를 설치하지 않음 |
| Streamlit skill `discover.py --project-dir ...` | 설치 버전별 로컬 문서 | 실패: 발견 스크립트가 선택한 Python 별칭 실행 권한 오류 | pgAdmin Python에는 Streamlit도 없음. 공식 문서로 실행 개념만 보충 |
| `python.exe -X utf8 .project-player/annotation-tools/verify.py` | 보관 원본 17개·현재 파일 | Python 3.13.14에서 실행. 13개 파일 diff는 **주석 270줄 삽입만**, 원본 줄 제거·변경 없음 | 앱 시작·패키지 import 검사 아님 |
| 같은 도구의 `ast.parse(..., feature_version=(3,12))`와 `ast.dump(..., include_attributes=False)` | Python 5개, 기준·최종 모두 | 전후 구문 검사 성공, 위치를 제외한 AST 동일 | 실제 Python 3.12 컨테이너에서 실행한 것은 아님 |
| 같은 도구의 `tokenize` 비교 | Python 5개 | 주석·비실행 줄바꿈을 제외한 토큰 동일 | 외부 서비스의 현재 동작까지 보장하지 않음 |
| 같은 도구의 SQL 토큰 비교 | `database/init.sql` | 설치된 `sqlparse`로 전후 의미 토큰 동일 | `sqlparse`는 PostgreSQL 문법 검증기 아님. SQL 실행하지 않음 |
| 같은 도구의 원문 비교 | requirements 2개, Dockerfile 2개, YAML 3개 | 새 주석을 제외한 줄·바이트 동일, UTF-8·줄바꿈 보존 | YAML·Compose·Dockerfile 전용 파서 없음. `packaging`도 없어 requirements 구문 파싱 못함 |
| `python.exe -m pytest --version` | 테스트 도구 존재 | 실패: `No module named pytest` | FastAPI·Redis·Streamlit·httpx도 이 검사 환경에 없음. 기존 테스트 3개 **미실행** |
| Node `require.resolve`와 `Get-Command` | YAML·Mermaid 검사 도구 | 로컬·전역 검색 경로에서 yaml/js-yaml/mermaid/mermaid-cli 미발견, mmdc·Docker 명령도 PATH에 없음 | 새 라이브러리 설치·npx 다운로드 없음 |
| 문서 참조·섹션·coverage 검사 | 현재 Markdown·실제 파일 | 두 다이어그램 종류, 10개 절, 파일 경로와 줄 범위, 전체 대상 파일 포함 확인 | Mermaid 실제 파싱·렌더링 **미실행**, 문법·참조 수동 검토 |
| 새 문서·추가 주석의 비밀 패턴 검사 및 수동 검토 | 신규 학습 내용만 | 토큰·개인키·자격 증명 포함 URL 인용 없음, 변수명·용도만 설명 | 비밀 파일을 열어 값 대조하지 않음. 패턴 검사는 모든 비밀을 판별하는 보증이 아님 |
| 원본 SHA-256 비교 | 기존 교재 4개, 특히 guide.md | 전부 바이트 동일 | 원래 문서의 오래된 설명은 수정하지 않음 |

최초 보조 검증 도구는 `packaging` import가 없어 중단되었다. 설치 없이 requirements의 원문 비교로 조정한 뒤 재검사했다. 한 번의 소스 출력은 콘솔 cp949가 이모지를 표현하지 못해 중단되었고, `-X utf8`로 재출력했다. 두 문제 모두 원래 앱 소스의 구문 실패가 아니다. 기준 Python 소스에는 파서 오류가 없었고 주석으로 새 구문 오류가 생기지 않았다.

### 실제 응답 관찰: 2026-09-15 15:29:56 KST에 시작한 읽기 전용 검사

Python 표준 `urllib.request`로 프록시를 사용하지 않고 각 주소에 GET, timeout 3초로 확인했다. 오류 본문·기록·환경값은 출력하거나 보관하지 않았다.

| 주소 / 검사 | 관찰 결과 | 말할 수 있는 범위 |
| --- | --- | --- |
| `http://127.0.0.1:8000/health/live` | HTTP 200, status=ok·service=backend와 일치 | 해당 시점 Backend 생존 응답 확인 |
| `http://127.0.0.1:8000/health/ready` | HTTP 200 | 해당 주소의 준비 API 성공 응답. 컨테이너/소스 버전 일치는 미확인 |
| `http://127.0.0.1:8501/_stcore/health` | HTTP 200 | 해당 포트의 상태 경로 응답. 실제 화면 렌더링·질문 제출 검증 아님 |
| `http://127.0.0.1:80/_stcore/health` | `URLError` | 그 시점 해당 주소에서 응답을 얻지 못함. 기본 Compose 파일이 잘못됐다는 판정은 아님 |

실행기의 분석 JSON은 파일·서비스 탐지 참고 자료이며 위 응답의 증거로 사용하지 않았다. 현재 응답한 서버가 어떤 Compose 파일·이미지·소스 버전으로 실행 중인지는 확정하지 않았다. 기존 서버를 중지·재시작·중복 실행하거나 자동 리로드 설정을 바꾸지 않았다. Docker up/down·빌드·볼륨 삭제·DB 초기화·migration·패키지 설치·모델 호출·GitHub push/workflow·배포도 수행하지 않았다.

### 코드에서 발견한 사항: 이번 작업에서는 수정하지 않음

| 발견 사항 | 영향과 다음에 읽을 위치 |
| --- | --- |
| README의 기본 화면 포트 설명과 실제 기본 Compose가 다름 | README는 8501을 안내하지만 `compose.yml`은 Host 80을 공개한다. [[README.md|└─ Frontend]], [[compose.yml|- "80:8501"]]. guide.md 106행에도 차이가 기록되어 있다. |
| 장애 교재의 오래된 health 키 | `TROUBLESHOOTING.md`의 `gemini_configured`와 현재 `checks.providers.gemini` 구조가 다름. [[TROUBLESHOOTING.md|- Health의]], [[backend/app.py|"providers": {name:]]. |
| 채팅은 전체 원자적 작업이 아님 | 모델 실패면 user 행이, 후반 Redis 실패면 두 DB 행이 남을 수 있다. 재시도 중복 방지 키도 없다. [[backend/app.py|def chat(]], [[backend/services.py|def add_chat_message(]]. |
| 화면 이력과 모델 문맥의 보존 범위가 다름 | PostgreSQL은 오래된 순서 최대 100개, Redis는 최근 12개, 프롬프트는 그중 마지막 6개. 긴 대화·TTL 만료 때 보이는 기록과 모델 문맥이 다를 수 있다. `list_chat`, `append_session`, `_prompt`를 함께 읽는다. |
| 상태 검사는 실제 모델 호출 성공 검사가 아님 | 키 존재나 플래그만 확인하고 ready의 성공 조건에도 공급자 준비를 요구하지 않는다. 스키마 검사는 테이블 존재만 검사. `health`, `configured`, `schema_ready`를 읽는다. |
| DB 초기화·테스트 의존성의 별도 준비 | `python-dotenv`, `pytest`가 Backend 명세에 없음. 초기화 설명은 [[guide.md|### 선택: 공용 DB 초기화에 필요한 가상환경]], 테스트 구현은 `backend/test_app.py`. 이번에는 설치하지 않음. |
| 성공 채팅 직후 사용자 말풍선 갱신 | 입력 직후에는 답변만 명시적으로 렌더링하고 다음 실행의 GET에서 기록을 다시 읽음. [[frontend/app.py|history = api("GET"]]와 [[frontend/app.py|with st.chat_message("assistant")]]를 비교한다. |
| 세션은 인증 수단이 아님 | GET·DELETE에 소유권 검사가 없고 세션별 동시 요청 직렬화도 없음. `get_chat_history`, `reset_current_session`과 `RedisSessionStore`를 읽는다. |
| 클라이언트 수명·오류 정보 처리 | Gemini 클라이언트는 지역 변수로 유지하지만 명시적 close가 없고, API 오류 detail에는 예외 문자열이 들어간다. 실제 누출을 확인한 것은 아니다. [[backend/services.py|gemini_client =]], `show_error`를 읽는다. |

### 최종 검토 판정

`impl-validator` 관점의 **작성·보존 검토는 PASS**, 검증 범위의 제한을 포함한 전체 판정은 **WARN**이다. 미완료 소스 주석은 없으나, YAML/Compose·Dockerfile 전문 파싱, PostgreSQL 문법 실행 검사, 기존 테스트 실행, Mermaid 렌더링, 실제 화면 상호작용·LLM 요청은 미검증이다. 검증 도구가 없는 항목을 통과로 집계하지 않았다.

다음 읽기 순서는 `frontend/app.py`의 POST → `backend/app.py:chat` → `backend/services.py:reply` → `add_chat_message`와 `append_session` → `database/init.sql` → 세 Compose의 연결 비교다. 실행 조작은 기존 `guide.md`의 해당 절에서 별도 작업으로 다룬다.

방법상 기존 Allkit/OtherWorlds RAG를 한 번 조회했으나 다른 프로젝트·일반 개념 자료였으므로 이 앱의 실행 근거에는 사용하지 않았다. Streamlit 공개 문서는 Context7 검색 1회·문서 조회 1회로 보충했고 비공개 소스·로그·키는 검색어에 넣지 않았다.
'''

anchors=[]
def resolve(match):
    name, needle = match.group(1).split('|',1)
    occurrence=1
    if re.search(r'\|\d+$',needle):
        needle, occurrence=needle.rsplit('|',1)
        occurrence=int(occurrence)
    assert name not in ('.env','.env.example','debug.log') and not name.startswith('.project-player/')
    rows=(ROOT/name).read_text(encoding='utf-8').splitlines()
    hits=[i for i,row in enumerate(rows,1) if needle in row and not row.lstrip().startswith(('# [학습]','-- [학습]'))]
    assert hits, f'Missing reference: {name} {needle}'
    number=hits[occurrence-1]
    anchors.append({'path':name,'needle':needle,'line':number})
    return f'[`{name}:{number}`](../{name}#L{number})'

document=re.sub(r'\[\[(.*?)\]\](?!\])',resolve,TEXT)
out=ROOT/'docs/project-walkthrough.md'
out.parent.mkdir(exist_ok=True)
with out.open('x',encoding='utf-8',newline='\n') as f:
    f.write(document)
(ROOT/'.project-player/annotation-tools/document-anchors.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'.project-player/annotation-tools/document-build.json').write_text(json.dumps({'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'references':len(anchors),'lines':len(document.splitlines())},indent=2),encoding='utf-8')
print(f'Created {out.relative_to(ROOT)}: {len(document.splitlines())} lines, {len(anchors)} source references')
