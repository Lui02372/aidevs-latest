r"""배포 전 점검 화면입니다."""

import streamlit as st

from frontend_common import init_state, render_sidebar


init_state()

st.title("4. 배포 전 점검")
st.caption("Streamlit frontend를 배포하기 전에 확인해야 할 항목입니다.")

with st.sidebar:
    render_sidebar()

st.checkbox("로컬 프론트 개발은 backend_mock으로 먼저 확인했다.")
st.checkbox("실제 배포는 backend_service를 Render에 배포해 연결한다.")
st.checkbox("Render start command는 uvicorn app.main:app --host 0.0.0.0 --port $PORT로 설정한다.")
st.checkbox("Upstash Redis는 선택 확장이며 token은 backend_service 환경변수에만 둔다.")
st.checkbox("Streamlit Community Cloud secrets에 API_BASE_URL을 등록한다.")
st.checkbox("프론트엔드에 service role key, LLM API key, Redis token을 두지 않았다.")

st.divider()
st.markdown(
    """
    배포 흐름:

    ```text
    FastAPI backend -> Render
    Redis -> Upstash
    Streamlit frontend -> Streamlit Community Cloud
    ```

    Streamlit에는 `API_BASE_URL`만 넣습니다.
    Supabase service role key, Gemini/OpenAI API key, Redis token은 frontend에 넣지 않습니다.
    """
)
