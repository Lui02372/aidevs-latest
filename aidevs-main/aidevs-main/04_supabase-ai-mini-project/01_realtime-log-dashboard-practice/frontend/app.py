r"""04 미니 프로젝트 실시간 로그 대시보드 frontend 실행 파일입니다.

실행:
    cd C:\aidev\04_supabase-ai-mini-project\01_realtime-log-dashboard-practice\frontend
    C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
    streamlit run .\app.py

이 파일은 왼쪽 메뉴 이름을 명확하게 지정합니다.
각 화면의 실제 내용은 pages 폴더의 Python 파일에 나누어 둡니다.
"""

import streamlit as st


st.set_page_config(page_title="Realtime Log Dashboard", layout="wide")

pages = [
    st.Page("pages/00_overview.py", title="화면설명"),
    st.Page("pages/01_log_input_and_query.py", title="1. 로그입력.조회"),
    st.Page("pages/02_sse_timed_receive.py", title="2. SSE 시간 설정 수신"),
    st.Page("pages/03_sse_continuous_receive.py", title="3. SSE 3분 자동 수신"),
]

navigation = st.navigation(pages)
navigation.run()
