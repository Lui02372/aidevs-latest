"""
[화면 시나리오]
학습자는 왼쪽 메뉴에서 Health, 현재 Redis Task, PostgreSQL 실행 이력과 운영 요약을
각각 확인합니다. 새 Multi-Agent Task를 접수하면 화면이 Redis 상태를 1초마다 폴링해
Progress와 현재 Agent를 갱신합니다. 승인 대기 상태에서는 사용자 결정 후 최종 결과와
PostgreSQL Trace를 확인합니다.
"""

import os
import time
from uuid import uuid4

import httpx
import streamlit as st


API_URL = os.getenv("MULTI_AGENT_API_URL", "http://127.0.0.1:8000").rstrip("/")
USER_ID = "demo-user"


def api(method: str, path: str, **kwargs):
    response = httpx.request(method, f"{API_URL}{path}", timeout=20, **kwargs)
    response.raise_for_status()
    return response.json()


def poll_task(task_id: str) -> dict[str, object]:
    progress_area = st.progress(0)
    state_area = st.empty()
    trace_area = st.empty()
    latest: dict[str, object] = {}

    for _ in range(300):
        latest = api("GET", f"/api/tasks/{task_id}", params={"user_id": USER_ID})
        progress_area.progress(int(latest["progress"]))
        state_area.info(
            f"상태: {latest['status']} · 현재 Agent: {latest.get('current_agent') or '-'}"
        )
        trace_area.dataframe(latest.get("trace", []), use_container_width=True, hide_index=True)
        if latest["status"] in {"waiting_approval", "completed", "rejected", "failed"}:
            return latest
        time.sleep(1)
    raise TimeoutError("5분 안에 Task 상태가 종료 지점에 도달하지 않았습니다.")


st.set_page_config(page_title="08 Observable Multi-Agent Service", page_icon="📈", layout="wide")
st.sidebar.title("📈 Observable Service")
menu = st.sidebar.radio(
    "학습 메뉴",
    ["과정 안내", "Task 실행", "Live Executions", "Execution History", "Operations Dashboard", "Health Check"],
)
st.sidebar.caption(f"사용자: {USER_ID}")
st.sidebar.caption(f"API: {API_URL}")

if "task_id" not in st.session_state:
    st.session_state.task_id = ""

if menu == "과정 안내":
    st.title("08 Observable Multi-Agent Service")
    st.code("Log → Trace → Health → Redis Live State → PostgreSQL History → Dashboard")
    st.write("현재 상태는 Redis, 완료 후 영구 이력은 PostgreSQL에서 확인합니다.")
elif menu == "Task 실행":
    st.title("실제 Multi-Agent Task 실행")
    request = st.text_area(
        "여행 요청",
        "부산으로 2박 3일 여행을 가려고 해. 예산은 60만원이고 해산물 알레르기가 있어. 대중교통을 이용할 거야.",
    )
    if st.button("Queue에 Task 접수", type="primary", use_container_width=True):
        try:
            task = api(
                "POST",
                "/api/tasks",
                json={"user_id": USER_ID, "request": request, "idempotency_key": f"ui-{uuid4().hex}"},
            )
            st.session_state.task_id = task["task_id"]
            st.session_state.last_task = poll_task(task["task_id"])
        except Exception as error:
            st.error(f"요청 또는 폴링 실패: {error}")

    task = st.session_state.get("last_task")
    if task:
        st.subheader(f"현재 상태: {task['status']}")
        if task.get("error"):
            st.error(task["error"])
        if task.get("result"):
            st.json(task["result"])
        if task["status"] == "waiting_approval":
            approve_column, reject_column = st.columns(2)
            if approve_column.button("승인", use_container_width=True):
                st.session_state.last_task = api("POST", f"/api/tasks/{task['task_id']}/decision", json={"user_id": USER_ID, "decision": "approve"})
                st.rerun()
            if reject_column.button("거절", use_container_width=True):
                st.session_state.last_task = api("POST", f"/api/tasks/{task['task_id']}/decision", json={"user_id": USER_ID, "decision": "reject"})
                st.rerun()
elif menu == "Live Executions":
    st.title("Redis Live Executions")
    try:
        st.dataframe(api("GET", "/api/operations/live"), use_container_width=True, hide_index=True)
    except Exception as error:
        st.error(str(error))
elif menu == "Execution History":
    st.title("PostgreSQL Execution History")
    try:
        history = api("GET", "/api/operations/history")
        st.dataframe(history, use_container_width=True, hide_index=True)
        task_id = st.text_input("상세 Trace를 조회할 Task ID", st.session_state.task_id)
        if st.button("영구 Trace 조회", disabled=not task_id):
            st.json(api("GET", f"/api/tasks/{task_id}/history", params={"user_id": USER_ID}))
    except Exception as error:
        st.error(str(error))
elif menu == "Operations Dashboard":
    st.title("Operations Dashboard")
    try:
        summary = api("GET", "/api/operations/summary")
        st.metric("현재 Redis Task", summary.get("live_task_count", 0))
        st.subheader("상태별 Task")
        st.json(summary.get("tasks_by_status", {}))
        st.subheader("Agent별 Event와 실패")
        st.dataframe(summary.get("agents", []), use_container_width=True, hide_index=True)
    except Exception as error:
        st.error(str(error))
else:
    st.title("Liveness와 Readiness")
    for name, path in [("전체 Health", "/health"), ("Liveness", "/health/live"), ("Readiness", "/health/ready")]:
        try:
            st.write(name)
            st.json(api("GET", path))
        except Exception as error:
            st.error(f"{name}: {error}")
