r"""화면 설명 페이지입니다.

실행:
    streamlit run .\app.py
    왼쪽 메뉴에서 "화면설명"을 선택합니다.
"""

import streamlit as st

from frontend_common import api_base_url, render_backend_status


st.title("AI 서비스 실시간 로그 대시보드")
st.caption("Supabase DB 저장, Upstash Redis 이벤트 전달, FastAPI SSE, Streamlit 표시 흐름을 확인합니다.")

st.info(
    "이 실습은 REST API로 로그를 저장/조회하는 화면과, "
    "SSE로 새 로그 이벤트를 실시간 수신하는 화면을 분리해서 확인합니다."
)

st.markdown(
    """
    | 화면 | 핵심 역할 | 저장 또는 전달 방식 |
    | --- | --- | --- |
    | `1. 로그입력.조회` | 로그를 생성하고 저장된 로그를 다시 조회합니다. | Supabase DB에 저장합니다. 실패하면 수업용 memory fallback에 임시 저장합니다. |
    | `2. SSE 시간 설정 수신` | 정해진 시간 동안 새 로그 이벤트를 받습니다. | 저장하지 않고 Redis pub/sub 또는 memory queue로 전달된 이벤트를 표시합니다. |
    | `3. SSE 3분 자동 수신` | 화면이 열리면 바로 실시간 이벤트 수신을 시작하고 약 3분 동안 표시합니다. | 저장하지 않고 Redis pub/sub 또는 memory queue로 전달된 이벤트를 자동으로 표시합니다. |
    """
)

st.subheader("저장과 실시간 수신의 차이")
st.markdown(
    """
    ```text
    로그입력.조회 화면
    -> POST /logs로 로그 생성
    -> Supabase DB 또는 memory fallback에 저장
    -> GET /logs로 이미 저장된 로그 목록을 다시 조회

    SSE 수신 화면
    -> GET /stream/logs로 SSE 연결 열기
    -> 연결 이후 새로 생기는 로그 이벤트를 실시간으로 수신
    -> 별도로 저장하지 않고 전달된 이벤트만 화면에 표시
    ```
    """
)

with st.expander("fallback은 언제 사용하나요?"):
    st.markdown(
        """
        이 예제에는 두 종류의 fallback이 있습니다.

        ## 1. 저장소 fallback

        `1. 로그입력.조회` 화면은 먼저 실제 DB인 **Supabase DB**에 로그 저장을 시도합니다.

        ```text
        POST /logs 요청
        -> Supabase DB 저장 시도
        -> 성공하면 Supabase DB에 저장
        -> 실패하면 memory fallback에 임시 저장
        ```

        **Supabase DB**는 실제 데이터베이스이므로 서버를 껐다 켜도 데이터가 남습니다.

        **memory fallback**은 FastAPI 서버가 실행되는 동안만 유지되는 임시 저장소입니다.
        서버를 끄면 memory fallback에 저장된 로그는 사라집니다.

        ## 2. 실시간 전달 fallback

        SSE 화면은 먼저 **Upstash Redis pub/sub**으로 새 로그 이벤트를 전달하려고 시도합니다.

        ```text
        GET /stream/logs 요청
        -> Upstash Redis pub/sub 구독 시도
        -> 성공하면 Redis를 통해 새 로그 이벤트 수신
        -> 실패하면 memory queue로 같은 서버 안에서만 임시 전달
        ```

        **Redis pub/sub**은 실제 실시간 이벤트 전달 채널입니다.

        **memory queue fallback**은 FastAPI 서버 한 대 안에서만 동작하는 임시 전달 방식입니다.
        여러 서버로 배포한 환경에서는 신뢰하기 어렵습니다.

        둘 다 운영용 대체 구조가 아니라, Supabase 또는 Redis 설정이 아직 안 되어도
        수업 중 화면 흐름을 먼저 확인하기 위한 교육용 안전장치입니다.
        """
    )

with st.sidebar:
    st.subheader("연결")
    st.code(f"API_BASE_URL={api_base_url()}")
    render_backend_status()
