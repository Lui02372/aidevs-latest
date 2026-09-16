r"""Streamlit tabs 구조를 익히기 위한 진입 파일입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend\07_streamlit-tabs-app
    C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
    streamlit run .\app.py

이 예제는 backend 없이 화면 흐름만 익히는 mock 앱입니다.
app.py에서는 st.tabs()로 탭을 만들고, 실제 화면은 tab_pages 폴더의 함수로 분리합니다.
"""

import streamlit as st

from frontend_common import init_state
from tab_pages.chat_tab import render_chat_tab
from tab_pages.product_create import product_create
from tab_pages.product_select import product_select

init_state()

st.set_page_config(page_title="Streamlit Tabs App", layout="wide")
st.title("Streamlit 탭 기반 화면 구성")
st.caption("최종 프로젝트 전에 st.tabs 구조와 탭별 파일 분리 방식을 연습합니다.")

# with st.sidebar:
#     # render_login_sidebar()
#     st.text("Tab")

# product_create_tab,overview_tab, signup_tab, log_tab, chat_tab, database_tab = st.tabs(
#     ["Product Create","화면설명", "회원가입", "로그조회", "Chat", "데이터베이스조회"]
# )
product_create_tab, product_select_tab, chat_tab = st.tabs(
    ["Product Create","Product Select", "Chat"]
)
with product_create_tab:
    product_create()
with product_select_tab:
    product_select()
with chat_tab:
    render_chat_tab()

