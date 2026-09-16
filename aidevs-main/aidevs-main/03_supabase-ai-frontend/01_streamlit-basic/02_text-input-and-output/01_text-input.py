import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("텍스트 입력 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

name = st.text_input("이름을 입력하세요")  # 사용자가 입력한 이름 문자열을 name 변수에 저장합니다.

if name:  # name에 빈 문자열이 아닌 값이 들어 있으면 인사말을 표시합니다.
    st.write(f"안녕하세요, {name}님!")  # 입력받은 이름을 포함해 인사말을 화면에 출력합니다.
else:  # 아직 이름을 입력하지 않은 상태라면 안내 메시지를 표시합니다.
    st.warning("이름을 입력하면 인사말이 표시됩니다.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.
