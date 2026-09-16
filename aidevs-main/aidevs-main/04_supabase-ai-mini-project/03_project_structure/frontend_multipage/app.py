r"""Streamlit multipage frontend starter입니다.

실행:
    cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_multipage
    C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
    streamlit run .\app.py

이 파일은 왼쪽 메뉴에 표시할 화면 목록만 정의합니다.
각 화면의 실제 구현은 pages 폴더 아래 Python 파일에 작성합니다.
"""

import streamlit as st


st.set_page_config(page_title="Realtime Log Dashboard", layout="wide")

pages = [
    st.Page("pages/00_overview.py", title="화면 설명"),
    st.Page("pages/01_log_dashboard.py", title="로그 대시보드"),
    st.Page("pages/02_realtime_stream.py", title="실시간 수신"),
    st.Page("pages/03_feedback_analysis.py", title="피드백 분석"),
    st.Page("pages/04_settings.py", title="설정"),
]

navigation = st.navigation(pages)
navigation.run()
