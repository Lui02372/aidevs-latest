import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("Columns 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

left_col, right_col = st.columns(2)  # 메인 화면을 여러 열로 나누어 대시보드 요소를 배치합니다.

with left_col:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.header("입력 영역")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    name = st.text_input("이름")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

with right_col:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.header("결과 영역")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    if name:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        st.write(f"{name}님, 환영합니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.write("왼쪽에서 이름을 입력하세요.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

