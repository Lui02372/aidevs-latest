r"""Lab 04. UI 리뷰와 리팩토링이 필요한 Streamlit 예제입니다.

실행 명령:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-04_ui-review-and-refactor\messy_dashboard.py

이 파일은 큰 오류 없이 실행되지만, 화면 구조와 코드 구조가 정리되어 있지 않습니다.
수강생은 Codex에게 "바로 고쳐줘"라고 하기 전에 먼저 리뷰를 요청합니다.

프롬프트 예시:
    이 Streamlit 코드를 UI/상태관리/보안/리팩토링 관점에서 리뷰해주세요.
    아직 코드는 수정하지 말고, 우선순위가 높은 문제 5개와 수정 방향을 알려주세요.
"""

import streamlit as st


st.title("서비스 로그 대시보드")
st.write("로그인한 사용자의 서비스 로그를 확인합니다.")

# 의도적인 문제:
# 상태 초기화가 화면 코드 사이에 흩어져 있고, token 값을 화면에 그대로 보여 줍니다.
if "token" not in st.session_state:
    st.session_state.token = "sample-access-token"

st.write("현재 token:", st.session_state.token)

logs = [
    {"event": "login_success", "status": "ok", "message": "student 로그인 성공"},
    {"event": "chat_request", "status": "ok", "message": "질문 응답 생성"},
    {"event": "api_timeout", "status": "warning", "message": "외부 API 응답 지연"},
]

st.write("전체 로그 개수:", len(logs))

filter_text = st.text_input("상태 필터", value="")

filtered = []
for item in logs:
    if filter_text == "":
        filtered.append(item)
    else:
        if filter_text in item["status"]:
            filtered.append(item)

st.write(filtered)

if st.button("로그 새로고침"):
    st.write("새로고침했습니다.")

if st.button("로그아웃"):
    st.session_state.token = None
    st.write("로그아웃했습니다.")

st.write("개선 힌트")
st.write("- token은 화면에 직접 보여 주지 않는 편이 좋습니다.")
st.write("- 상태 초기화, 필터링, 화면 출력은 함수로 나눌 수 있습니다.")
st.write("- 빈 결과일 때 안내 메시지를 보여 주면 좋습니다.")
