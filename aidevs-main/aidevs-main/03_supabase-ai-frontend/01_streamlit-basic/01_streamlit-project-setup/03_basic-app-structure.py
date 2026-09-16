import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


def render_header():  # 화면 맨 위에 표시할 제목 영역을 함수로 분리합니다.
    st.title("기본 앱 구조")  # Streamlit 화면의 가장 큰 제목을 표시합니다.
    st.write("함수를 사용해 화면 영역을 나누는 간단한 예제입니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.


def render_content():  # 앱의 중심 내용이 들어갈 본문 영역을 함수로 분리합니다.
    st.header("본문 영역")  # 본문 영역이 시작된다는 것을 사용자가 알 수 있게 섹션 제목을 표시합니다.
    st.write("실제 앱에서는 이 영역에 입력, 결과, 표, 차트 등을 배치합니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.


def render_footer():  # 화면 아래쪽의 보조 설명 영역을 함수로 분리합니다.
    st.divider()  # 본문과 하단 설명을 시각적으로 나누는 구분선을 표시합니다.
    st.caption("01_streamlit-basic / 01_streamlit-project-setup")  # 보조 설명이나 현재 위치를 작은 글씨로 표시합니다.


render_header()  # 제목 영역을 화면에 그립니다.
render_content()  # 본문 영역을 화면에 그립니다.
render_footer()  # 하단 보조 설명 영역을 화면에 그립니다.
