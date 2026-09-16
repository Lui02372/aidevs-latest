# Streamlit 사용 가이드

이 문서는 `03_supabase-ai-frontend` 과정에서 Streamlit을 사용할 때 반복해서 참고하는 기본 사용법을 정리한 문서입니다.
공식 문서의 전체 내용을 그대로 옮긴 것이 아니라, 수업에서 필요한 흐름만 초보자 기준으로 다시 정리했습니다.

## 먼저 참고하면 좋은 공식 사이트

Streamlit은 기능 변화가 빠른 편이므로, 실제 사용 중 막히면 아래 공식 문서를 먼저 확인합니다.

| 주제 | 공식 문서 |
| --- | --- |
| Streamlit 전체 문서 | [Streamlit documentation](https://docs.streamlit.io/) |
| 설치와 첫 실행 | [Install Streamlit using command line](https://docs.streamlit.io/get-started/installation/command-line) |
| 기본 개념 | [Basic concepts of Streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts) |
| 앱 실행 방식 | [Run your Streamlit app](https://docs.streamlit.io/develop/concepts/architecture/run-your-app) |
| API Reference | [Streamlit API reference](https://docs.streamlit.io/develop/api-reference) |
| Session State | [st.session_state](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state) |
| Caching | [Caching overview](https://docs.streamlit.io/develop/concepts/architecture/caching) |
| Forms | [Using forms](https://docs.streamlit.io/develop/concepts/architecture/forms) |
| Layout | [Layouts and containers](https://docs.streamlit.io/develop/api-reference/layout) |
| Secrets | [Secrets management](https://docs.streamlit.io/develop/concepts/connections/secrets-management) |
| Multipage apps | [Multipage apps](https://docs.streamlit.io/develop/concepts/multipage-apps) |
| Chat UI | [st.chat_input](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input) |

## Streamlit은 무엇인가요?

Streamlit은 Python 코드만으로 웹 화면을 빠르게 만들 수 있는 프레임워크입니다.
HTML, CSS, JavaScript를 직접 많이 작성하지 않아도 텍스트, 입력창, 버튼, 표, 차트, 파일 업로드, 챗봇 UI를 만들 수 있습니다.

이 과정에서 Streamlit은 아래 역할을 합니다.

```text
사용자 화면
-> 입력값 받기
-> FastAPI 백엔드 호출
-> 응답 결과 표시
-> 로그인 token과 대화 상태 관리
```

중요한 기준은 이것입니다.

```text
Streamlit = 화면과 사용자 상호작용 담당
FastAPI = Supabase, Auth, Gemini, Redis 호출 담당
```

프론트엔드 Streamlit 앱에는 `SUPABASE_SERVICE_ROLE_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `UPSTASH_REDIS_REST_TOKEN` 같은 민감한 값을 넣지 않습니다.

## 설치와 실행

이 과정에서는 `03_supabase-ai-frontend` 폴더의 공통 가상환경을 사용합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit --version
```

Streamlit 앱은 일반 Python 실행 명령이 아니라 `streamlit run`으로 실행합니다.

```powershell
streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

정상 실행되면 브라우저에서 보통 아래 주소가 열립니다.

```text
http://localhost:8501
```

공식 문서에서는 `python -m streamlit run your_script.py`도 같은 방식으로 사용할 수 있다고 설명합니다.
터미널에서 `streamlit` 명령이 잘 잡히지 않을 때는 아래처럼 실행할 수 있습니다.

```powershell
python -m streamlit run .\01_streamlit-basic\01_streamlit-project-setup\01_hello-streamlit.py
```

## Streamlit 코드의 기본 구조

Streamlit 앱은 위에서 아래로 실행되는 Python 스크립트입니다.
사용자가 버튼을 누르거나 입력값을 바꾸면 스크립트가 다시 실행됩니다.

```python
import streamlit as st

st.title("AI 서비스 화면")
st.write("Streamlit으로 화면을 만듭니다.")

name = st.text_input("이름")

if st.button("인사하기"):
    st.success(f"{name}님, 안녕하세요!")
```

초보자가 꼭 기억할 점은 다음과 같습니다.

```text
1. Streamlit 파일은 위에서 아래로 다시 실행됩니다.
2. 버튼, 입력창, 선택창 같은 widget은 사용자 상호작용을 만듭니다.
3. 다시 실행되어도 유지해야 하는 값은 st.session_state에 저장합니다.
```

## 화면 출력

가장 자주 쓰는 출력 함수는 아래와 같습니다.

| 기능 | 예시 |
| --- | --- |
| 제목 | `st.title("제목")` |
| 큰 제목 | `st.header("섹션")` |
| 작은 제목 | `st.subheader("소제목")` |
| 일반 출력 | `st.write(data)` |
| Markdown | `st.markdown("**굵게**")` |
| 코드 표시 | `st.code(code, language="python")` |
| 성공 메시지 | `st.success("성공")` |
| 경고 메시지 | `st.warning("확인 필요")` |
| 오류 메시지 | `st.error("오류")` |

`st.write()`는 문자열, 숫자, 리스트, 딕셔너리, DataFrame 등 여러 값을 빠르게 확인할 때 편합니다.
수업 초반에는 `st.write()`로 값을 먼저 확인하고, 이후 표나 차트로 다듬는 흐름이 좋습니다.

## 입력 Widget

사용자 입력을 받는 대표 widget은 아래와 같습니다.

| 기능 | 예시 |
| --- | --- |
| 한 줄 텍스트 | `st.text_input("질문")` |
| 여러 줄 텍스트 | `st.text_area("내용")` |
| 숫자 입력 | `st.number_input("나이")` |
| 선택 박스 | `st.selectbox("모델", options)` |
| 다중 선택 | `st.multiselect("태그", options)` |
| 체크박스 | `st.checkbox("동의")` |
| 버튼 | `st.button("실행")` |
| 파일 업로드 | `st.file_uploader("파일 선택")` |

예시:

```python
import streamlit as st

question = st.text_area("AI에게 물어볼 질문")
model = st.selectbox("모델 선택", ["mock", "gemini"])

if st.button("질문 보내기"):
    if not question.strip():
        st.warning("질문을 입력하세요.")
    else:
        st.write({"model": model, "question": question})
```

## Button과 rerun 이해

Streamlit은 사용자가 widget을 조작할 때 스크립트를 다시 실행합니다.
`st.button()`은 클릭된 순간에만 `True`가 됩니다.
따라서 버튼 클릭 후에도 값을 유지해야 하면 `st.session_state`를 함께 사용합니다.

```python
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("증가"):
    st.session_state.count += 1

st.write("현재 값:", st.session_state.count)
```

수업에서 자주 생기는 문제는 “버튼을 누르면 화면 값이 초기화된다”는 것입니다.
이때는 유지해야 하는 값을 일반 변수에만 두지 말고 `st.session_state`에 넣습니다.

## Session State

`st.session_state`는 한 사용자의 브라우저 세션 동안 값을 저장하는 공간입니다.
공식 문서에서는 session state를 script rerun 사이에서 변수를 공유하는 방식으로 설명합니다.

03 과정에서는 주로 아래 값을 저장합니다.

```text
access_token
로그인한 사용자 email
대화 메시지 목록
현재 선택된 메뉴
API 호출 결과
```

예시:

```python
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
```

주의할 점:

```text
Session State는 브라우저 탭 또는 세션 기준입니다.
새로고침이나 새 접속 상황에서는 초기화될 수 있습니다.
영구 저장이 필요한 데이터는 백엔드 API를 통해 DB에 저장합니다.
```

## Forms

입력창이 여러 개 있을 때, 값이 바뀔 때마다 앱이 다시 실행되면 불편할 수 있습니다.
이때 `st.form()`을 사용하면 여러 입력을 모아 제출 버튼을 눌렀을 때 한 번에 처리할 수 있습니다.

```python
import streamlit as st

with st.form("profile_form"):
    name = st.text_input("이름")
    email = st.text_input("이메일")
    submitted = st.form_submit_button("저장")

if submitted:
    st.success(f"{name} / {email} 저장 요청")
```

로그인, 회원가입, 설정 저장처럼 여러 값을 한 번에 보내는 화면은 `form`으로 만드는 것이 좋습니다.

## Layout

Streamlit은 화면 배치를 위해 sidebar, columns, tabs, expander, container 같은 기능을 제공합니다.

| 기능 | 사용 상황 |
| --- | --- |
| `st.sidebar` | 메뉴, 로그인 상태, 설정값 |
| `st.columns()` | 좌우로 나누어 입력과 결과 표시 |
| `st.tabs()` | 관련 화면을 탭으로 구분 |
| `st.expander()` | 상세 정보나 로그를 접었다 펼치기 |
| `st.container()` | 여러 요소를 하나의 영역으로 묶기 |

예시:

```python
import streamlit as st

with st.sidebar:
    st.header("설정")
    api_mode = st.selectbox("API 모드", ["mock", "service"])

left, right = st.columns([1, 2])

with left:
    st.text_area("질문")

with right:
    st.subheader("AI 응답")
    st.info("아직 응답이 없습니다.")
```

03 과정에서는 너무 복잡한 디자인보다, 입력 영역과 결과 영역을 명확히 나누는 것을 우선합니다.

## 표와 차트

데이터를 화면에 보여 줄 때는 아래 기능을 자주 사용합니다.

| 기능 | 예시 |
| --- | --- |
| 표 | `st.dataframe(df)` |
| 정적 표 | `st.table(df)` |
| 라인 차트 | `st.line_chart(df)` |
| 바 차트 | `st.bar_chart(df)` |
| Altair 차트 | `st.altair_chart(chart, use_container_width=True)` |

운영 로그나 대화 이력은 처음에는 `st.dataframe()`으로 보여 주고, 필요할 때 차트로 확장합니다.

## Chat UI

Streamlit은 챗봇 UI를 만들기 위한 `st.chat_input()`과 `st.chat_message()`를 제공합니다.

```python
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": "mock 응답입니다."})
    st.rerun()
```

챗봇 화면에서 중요한 기준은 다음과 같습니다.

```text
사용자 메시지와 assistant 메시지를 role로 구분합니다.
화면 표시용 대화는 session_state에 저장합니다.
영구 저장용 대화는 FastAPI 백엔드에 POST 요청으로 보냅니다.
```

## API 호출

03 과정에서 Streamlit은 FastAPI 백엔드를 호출합니다.
프론트엔드는 `API_BASE_URL`만 알고, 실제 Supabase/Gemini 처리는 백엔드가 담당합니다.

```python
import os
import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

if st.button("서버 상태 확인"):
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=5)
        response.raise_for_status()
        st.success(response.json())
    except httpx.HTTPError as error:
        st.error(f"백엔드 연결 실패: {error}")
```

로그인 후 보호된 API를 호출할 때는 Authorization header를 사용합니다.

```python
headers = {
    "Authorization": f"Bearer {st.session_state.access_token}",
}

response = httpx.get(f"{API_BASE_URL}/me", headers=headers, timeout=5)
```

## 로딩과 오류 처리

API 호출은 실패할 수 있습니다.
백엔드가 꺼져 있거나, 주소가 틀렸거나, token이 없거나, 네트워크가 느릴 수 있습니다.

Streamlit 화면에서는 아래처럼 사용자에게 현재 상태를 보여 줍니다.

```python
import httpx
import streamlit as st

with st.spinner("AI 응답을 기다리는 중입니다..."):
    try:
        response = httpx.post("http://127.0.0.1:8000/ai/chat", json={"message": "안녕"}, timeout=10)
        response.raise_for_status()
        st.success("응답을 받았습니다.")
        st.write(response.json())
    except httpx.ConnectError:
        st.error("백엔드 서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인하세요.")
    except httpx.HTTPStatusError as error:
        st.error(f"API 오류: {error.response.status_code}")
    except httpx.TimeoutException:
        st.error("요청 시간이 초과되었습니다.")
```

초보자 실습에서는 오류를 숨기지 말고, 화면에 무엇을 확인해야 하는지 보여 주는 것이 좋습니다.

## Caching

Streamlit은 script rerun이 자주 일어나기 때문에, 오래 걸리는 계산이나 반복 조회를 줄이기 위해 cache를 사용할 수 있습니다.

공식 문서 기준으로 크게 두 가지를 구분합니다.

| 기능 | 사용 상황 |
| --- | --- |
| `st.cache_data` | API 조회 결과, DataFrame, JSON처럼 복사 가능한 데이터 |
| `st.cache_resource` | DB 연결, 모델 객체처럼 여러 번 만들기 부담되는 리소스 |

예시:

```python
import httpx
import streamlit as st

@st.cache_data(ttl=30)
def fetch_logs(api_base_url: str) -> list[dict]:
    response = httpx.get(f"{api_base_url}/service-logs", timeout=5)
    response.raise_for_status()
    return response.json()
```

주의:

```text
사용자별 token이 필요한 API 응답을 무심코 cache하면 보안 문제가 생길 수 있습니다.
개인별 데이터는 cache key에 사용자 구분값이 들어가는지 확인하거나, 처음에는 cache 없이 구현합니다.
```

## Secrets와 환경변수

Streamlit 공식 문서는 민감 정보를 Git 저장소에 올리지 말고, repository 밖의 파일이나 환경변수로 관리하라고 안내합니다.
Streamlit에는 `st.secrets`와 `.streamlit/secrets.toml` 방식도 있습니다.

하지만 이 과정의 기본 실습에서는 프론트엔드가 민감 key를 직접 가지지 않습니다.

```text
03 과정 기본:
API_BASE_URL만 프론트엔드 .env에 둡니다.

백엔드 .env:
SUPABASE_SERVICE_ROLE_KEY
GEMINI_API_KEY
OPENAI_API_KEY
UPSTASH_REDIS_REST_TOKEN
```

Streamlit Community Cloud에 배포할 때는 앱 설정의 Secrets에 필요한 환경값을 넣을 수 있습니다.
다만 이 과정에서는 프론트엔드에 `API_BASE_URL` 정도만 두고, 실제 key는 백엔드 배포 환경에 둡니다.

## Multipage app

Streamlit은 여러 페이지 앱을 만들 수 있습니다.
공식 문서에서는 `st.Page`와 `st.navigation`을 선호 방식으로 설명하며, 간단한 경우 `pages/` 디렉토리 방식도 사용할 수 있습니다.

03 과정 초보자 실습에서는 처음부터 multipage 구조를 강제하지 않습니다.
대신 최종 프로젝트에서 화면이 커질 때 아래처럼 나누는 것을 고려합니다.

```text
app.py
pages/
  01_Login.py
  02_Chat.py
  03_History.py
  04_Service_Logs.py
```

처음에는 한 파일에서 완성하고, 코드가 길어질 때 페이지 분리를 선택 확장으로 진행합니다.

## 03 과정에서의 권장 개발 순서

Streamlit 화면은 아래 순서로 만드는 것이 가장 덜 막힙니다.

```text
1. st.title, st.write로 화면이 뜨는지 확인합니다.
2. text_input, button으로 입력과 클릭 흐름을 만듭니다.
3. mock 데이터로 결과 표시 화면을 완성합니다.
4. API_BASE_URL을 읽어 백엔드 /health를 호출합니다.
5. 실제 API 요청을 연결합니다.
6. 로딩, 오류, 빈 결과 메시지를 추가합니다.
7. session_state로 token과 대화 상태를 유지합니다.
8. 필요하면 form, tabs, sidebar로 화면을 정리합니다.
```

## 자주 막히는 지점

| 증상 | 확인할 것 |
| --- | --- |
| `streamlit` 명령을 찾을 수 없음 | `.venv` 활성화, `pip install -r requirements.txt` |
| 브라우저가 열리지 않음 | 터미널에 표시된 Local URL 직접 열기 |
| 수정했는데 화면이 이상함 | Streamlit rerun 또는 브라우저 새로고침 |
| 버튼 클릭 후 값이 사라짐 | `st.session_state` 사용 여부 |
| 백엔드 연결 실패 | FastAPI 서버 실행 여부, `API_BASE_URL`, 포트 번호 |
| 401 또는 403 오류 | 로그인 token, Authorization header |
| 비밀 key 노출 위험 | 프론트엔드 `.env`에 service role/API key가 없는지 확인 |
| 배포 후 환경값 없음 | Streamlit Cloud Secrets 또는 배포 환경 변수 확인 |

## 수업 기준 요약

```text
Streamlit 실행:
streamlit run 파일명.py

상태 유지:
st.session_state

여러 입력 한 번에 제출:
st.form + st.form_submit_button

화면 배치:
sidebar, columns, tabs, expander

백엔드 호출:
httpx + API_BASE_URL

민감정보:
프론트엔드가 아니라 백엔드 환경변수에 저장
```
