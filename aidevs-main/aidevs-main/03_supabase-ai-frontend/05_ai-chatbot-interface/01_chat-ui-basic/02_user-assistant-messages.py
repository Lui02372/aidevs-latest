import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

def response(prompt:str):  # 사용자가 입력한 질문에 대한 답변을 생성하는 함수입니다.
    return f"{prompt} 입력한 질문에 대한 답변입니다."  # 문자열, 숫자, 객체를 반환합니다.


st.markdown(
    """
    <style>
    div[data-testid="stElementContainer"]:has(.sticky-title) {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: var(--background-color);
        padding: 1rem 0 0.5rem 0;
    }

    .sticky-title {
        margin: 0;
    }
    </style>
    <h1 class="sticky-title">역할별 메시지 출력</h1>
    """,
    unsafe_allow_html=True,
)  # 제목 영역을 화면 상단에 고정합니다.

if "messages" not in st.session_state:  # Streamlit 화면의 상태를 저장하는 session_state에 messages라는 키가 없으면 True를 반환합니다.
    st.session_state.messages = []

for message in st.session_state.messages:  # 목록이나 반복 가능한 데이터를 하나씩 꺼내 같은 작업을 반복합니다.
    with st.chat_message(message["role"]):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
        st.write(message["content"])  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})  # 사용자가 입력한 질문을 메시지 목록에 추가합니다.
    response_text = response(prompt)  # 사용자가 입력한 질문에 대한 답변을 생성합니다.
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.rerun()  # Streamlit 화면을 새로고침하여 메시지 목록을 업데이트합니다.
