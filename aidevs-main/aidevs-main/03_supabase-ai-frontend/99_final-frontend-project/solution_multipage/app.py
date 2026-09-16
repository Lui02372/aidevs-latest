r"""개인화 AI 챗봇 서비스 멀티페이지 solution의 진입 파일입니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend\99_final-frontend-project\solution_multipage
    C:\aidev\03_supabase-ai-frontend\.venv\Scripts\Activate.ps1
    streamlit run .\app.py

이 파일은 왼쪽 메뉴에 표시할 화면 목록과 이름을 정의합니다.
각 화면의 실제 구현은 pages 폴더 아래 Python 파일에 작성합니다.
"""

import streamlit as st


st.set_page_config(page_title="Personal AI Chatbot", page_icon="AI", layout="wide")

pages = [
    st.Page("pages/01_chatbot.py", title="1. 챗봇"),
    st.Page("pages/02_conversation_history.py", title="2. 대화 기록"),
    st.Page("pages/03_service_logs.py", title="3. 서비스 로그"),
    st.Page("pages/04_deployment_checklist.py", title="4. 배포 전 점검"),
]

navigation = st.navigation(pages)
navigation.run()
