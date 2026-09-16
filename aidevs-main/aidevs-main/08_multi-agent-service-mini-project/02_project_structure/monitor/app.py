"""Auto Healing 운영 모니터 화면입니다.

실행 방법:
    cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
    streamlit run monitor/app.py --server.port 8802
"""

import os

import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Auto Healing Monitor", layout="wide")
st.title("Auto Healing Monitor")

if st.button("Check backend health"):
    response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    st.json(response.json())

st.caption("프로젝트가 확장되면 이 화면에 복구 이력, 파이프라인 상태, CloudWatch 로그 요약을 표시합니다.")
