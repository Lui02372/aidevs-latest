r"""Streamlit tabs frontend starter입니다.

실행:
    cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\frontend_tabs
    C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
    streamlit run .\app.py

이 파일은 탭을 만드는 역할만 합니다.
각 탭의 실제 내용은 tab_pages 폴더의 render_*_tab 함수에 작성합니다.
"""

import streamlit as st

from tab_pages.feedback_analysis_tab import render_feedback_analysis_tab
from tab_pages.log_dashboard_tab import render_log_dashboard_tab
from tab_pages.overview_tab import render_overview_tab
from tab_pages.realtime_stream_tab import render_realtime_stream_tab
from tab_pages.settings_tab import render_settings_tab


st.set_page_config(page_title="Realtime Log Dashboard", layout="wide")
st.title("AI 서비스 로그 대시보드")
st.caption("탭 기반 frontend 구조입니다.")

overview_tab, log_tab, stream_tab, feedback_tab, settings_tab = st.tabs(
    ["화면 설명", "로그 대시보드", "실시간 수신", "피드백 분석", "설정"]
)

with overview_tab:
    render_overview_tab()

with log_tab:
    render_log_dashboard_tab()

with stream_tab:
    render_realtime_stream_tab()

with feedback_tab:
    render_feedback_analysis_tab()

with settings_tab:
    render_settings_tab()
