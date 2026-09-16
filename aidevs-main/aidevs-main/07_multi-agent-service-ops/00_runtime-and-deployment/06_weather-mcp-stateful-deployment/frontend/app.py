"""
시나리오
수강생이 도시·날짜·Cloud LLM을 선택해 Weather Agent를 실행합니다. 화면은 최종 답변뿐
아니라 실제 호출한 MCP Tool 이름과 Open-Meteo 결과를 함께 보여 주어 근거를 확인합니다.
"""

import os
import time
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Weather MCP Agent", page_icon="🌦️", layout="wide")
st.sidebar.title("학습 메뉴")
page = st.sidebar.radio("이동", ["Weather Agent", "실행 이력", "구조 이해", "Health Check"])
st.title("Stateful Weather MCP aws Deployment")

if page == "Weather Agent":
    city = st.text_input("도시", "서울")
    day_label = st.radio("날짜", ["내일", "오늘"], horizontal=True)
    provider = st.selectbox("Cloud LLM", ["openai", "gemini"])
    if st.button("실제 날씨 조회", type="primary", use_container_width=True):
        try:
            response = requests.post(f"{BACKEND_URL}/api/weather", json={"city": city, "day": "tomorrow" if day_label == "내일" else "today", "provider": provider}, timeout=90)
            response.raise_for_status()
            started = response.json()
            run_id = started["run_id"]
            progress_box = st.empty()
            for _ in range(90):
                progress_response = requests.get(f"{BACKEND_URL}/api/runs/{run_id}/progress", timeout=5)
                progress_response.raise_for_status()
                progress = progress_response.json()
                progress_box.progress(progress["progress"], text=progress["message"])
                if progress["stage"] in {"completed", "failed"}:
                    break
                time.sleep(1)
            if progress["stage"] == "failed":
                raise RuntimeError(progress["message"])
            if progress["stage"] != "completed":
                raise RuntimeError("90초 안에 실행이 완료되지 않았습니다.")
            result = {"run_id": run_id, **progress["result"]}
            st.success(result["answer"])
            cache_text = "Redis Cache 사용" if result["cache_hit"] else "Weather MCP 실제 호출"
            st.caption(f"Run ID: {result['run_id']} · {result['provider']} · {result['model']} · {cache_text}")
            with st.expander("실제 Open-Meteo Tool Result", expanded=True):
                st.json(result["tool_result"])
        except (requests.RequestException, RuntimeError) as error:
            response = getattr(error, "response", None)
            detail = response.text if response is not None else str(error)
            st.error(f"Backend 요청 실패: {detail}")
elif page == "실행 이력":
    try:
        response = requests.get(f"{BACKEND_URL}/api/runs", timeout=10)
        response.raise_for_status()
        runs = response.json()["runs"]
        st.caption("PostgreSQL에 영구 저장된 최근 실행입니다.")
        if not runs:
            st.info("아직 저장된 실행이 없습니다.")
        for item in runs:
            with st.expander(f"{item['city']} · {item['requested_day']} · {item['provider']} · {item['created_at']}"):
                st.write(item["answer"])
                st.json(item["tool_result"])
    except requests.RequestException as error:
        st.error(f"이력 조회 실패: {error}")
elif page == "구조 이해":
    st.code("Browser → Frontend → Backend Agent → Weather MCP → Open-Meteo\n                         ├→ Redis 진행 상태·날씨 Cache\n                         ├→ PostgreSQL 영구 실행 이력\n                         └→ OpenAI 또는 Gemini")
    st.info("인프라는 계속 유지하고 Application 세 Container만 CI/CD로 다시 배포합니다.")
else:
    try:
        response = requests.get(f"{BACKEND_URL}/health/ready", timeout=5)
        response.raise_for_status()
        st.success("Backend와 Weather MCP가 준비되었습니다.")
        st.json(response.json())
    except requests.RequestException as error:
        st.error(f"Readiness 실패: {error}")
