r"""Lab 02: 학습 점검 앱 실습입니다.

이 파일은 사용자가 오늘 학습한 주제, 자신감 점수, 학습 요약을 입력하면
조건에 따라 다른 피드백 메시지를 보여 주는 Streamlit 실습입니다.

이 실습에서 확인할 내용:
    1. st.selectbox로 학습 주제를 선택하는 방법
    2. st.slider로 숫자 범위 값을 입력받는 방법
    3. st.button을 눌렀을 때만 결과 영역을 표시하는 방법
    4. if/elif/else 조건문으로 success, info, warning 메시지를 구분하는 방법

실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\01_streamlit-basic\10_labs\lab-02-learning-check-app.py
"""

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("학습 점검 앱")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

topic = st.selectbox("오늘 학습한 주제", ["Streamlit 실행", "텍스트 출력", "입력 위젯", "레이아웃"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
confidence = st.slider("자신감", min_value=1, max_value=5, value=3)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
summary = st.text_area("오늘 배운 내용을 한 문장으로 정리하세요")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

if st.button("점검하기"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.subheader("점검 결과")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    st.write(f"학습 주제: {topic}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    st.write(f"자신감: {confidence}점")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    if confidence >= 4 and summary:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        st.success("다음 단계로 넘어갈 준비가 좋습니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
    elif summary:  # 앞 조건이 False일 때 추가 조건을 검사합니다.
        st.info("예제를 한 번 더 수정하면서 익숙해져 보세요.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.warning("배운 내용을 한 문장으로 정리해 보세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.

