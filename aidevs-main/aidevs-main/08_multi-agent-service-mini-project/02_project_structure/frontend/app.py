"""Auto Healing 사용자 화면입니다.

실행 방법:
    cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
    streamlit run frontend/app.py --server.port 8801

Docker Compose에서는 frontend 서비스가 이 파일을 실행합니다.
"""

import os

import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Auto Healing Workflow", layout="wide")
st.title("Auto Healing Workflow")

service_name = st.text_input("Service name", value="backend")
message = st.text_area("Failure message", value="backend timeout occurred")
severity = st.selectbox("Severity", ["low", "medium", "high"], index=1)

if st.button("Run Auto Healing"):
    payload = {
        "service_name": service_name,
        "message": message,
        "severity": severity,
    }
    response = requests.post(f"{BACKEND_URL}/incidents", json=payload, timeout=10)
    if response.ok:
        st.success("Auto Healing workflow completed")
        st.json(response.json())
    else:
        st.error(f"Request failed: {response.status_code}")
        st.text(response.text)
