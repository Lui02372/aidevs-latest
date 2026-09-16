r"""Streamlit multipage 구조를 익히기 위한 진입 파일입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend\06_streamlit-multipage-app
    C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
    streamlit run .\app.py

이 예제는 backend 없이 화면 흐름만 익히는 mock 앱입니다.
app.py에서는 st.Page와 st.navigation으로 왼쪽 메뉴 이름과 순서를 정합니다.
각 화면의 실제 구현은 pages 폴더 아래 Python 파일에 작성합니다.
"""

import streamlit as st


st.set_page_config(page_title="Streamlit Multipage App", layout="wide")

pages = [
    st.Page("pages/01_signup.py", title="회원가입"),
    st.Page("pages/02_log_view.py", title="로그조회"),
    st.Page("pages/03_chat.py", title="Chat"),
    st.Page("pages/04_database_view.py", title="데이터베이스조회"),
]

navigation = st.navigation(pages)
navigation.run()
