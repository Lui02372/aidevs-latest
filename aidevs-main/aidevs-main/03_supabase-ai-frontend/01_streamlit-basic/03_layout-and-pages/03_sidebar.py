import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("Sidebar 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

with st.sidebar:  # 화면 왼쪽 사이드바 영역에 입력 컴포넌트를 배치합니다.
    st.header("설정")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    user_name = st.text_input("사용자 이름")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    theme = st.selectbox("화면 모드", ["기본", "집중", "요약"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.header("메인 화면")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
st.write(f"선택한 화면 모드: {theme}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if user_name:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.success(f"{user_name}님을 위한 화면입니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
    st.info("왼쪽 사이드바에서 사용자 이름을 입력하세요.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.

