r"""Lab 02. API 연결 오류가 있는 Streamlit 예제입니다.

실행 명령:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-02_api-connection-error\broken_api_client.py

먼저 아래 백엔드가 실행 중이어야 합니다.
    cd C:\aidev\03_supabase-ai-frontend\04_state-session-and-data\00_sample_backend
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

프롬프트 예시:
    이 Streamlit 파일은 백엔드 /health를 호출하려고 하지만 연결 오류가 발생합니다.
    API_BASE_URL, 포트 번호, 예외 처리 관점에서 원인을 분석해주세요.
"""

import httpx
import streamlit as st


# 의도적인 문제:
# 샘플 백엔드는 8000번 포트에서 실행되지만, 이 코드는 9999번 포트를 호출합니다.
API_BASE_URL = "http://127.0.0.1:9999"


st.title("API 연결 오류 실습")
st.caption("백엔드 /health API를 호출해 서버 상태를 확인합니다.")

if st.button("백엔드 상태 확인"):
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=3.0)
        st.write("HTTP status code:", response.status_code)
        st.json(response.json())
    except httpx.RequestError as exc:
        st.error("백엔드에 연결하지 못했습니다.")
        st.write("호출 주소:", f"{API_BASE_URL}/health")
        st.write("오류:", str(exc))
