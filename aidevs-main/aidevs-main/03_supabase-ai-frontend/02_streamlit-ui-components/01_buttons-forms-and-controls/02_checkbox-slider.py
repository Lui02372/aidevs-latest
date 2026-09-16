import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("체크박스와 슬라이더 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

show_detail = st.checkbox("상세 설명 보기")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
score = st.slider("이해도 점수", min_value=0, max_value=100, value=70)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.write(f"현재 점수: {score}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if show_detail:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.write("체크박스는 선택 여부를 True 또는 False 값으로 반환합니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    st.write("슬라이더는 지정한 범위 안의 숫자 값을 반환합니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

if score >= 80:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.success("다음 단계로 넘어가도 좋습니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
elif score >= 50:  # 앞 조건이 False일 때 추가 조건을 검사합니다.
    st.info("예제를 한 번 더 바꿔 보세요.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.
else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
    st.warning("기본 예제를 다시 실행해 보세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.

