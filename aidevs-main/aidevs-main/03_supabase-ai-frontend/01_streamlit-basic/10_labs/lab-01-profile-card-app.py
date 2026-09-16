r"""Lab 01: 프로필 카드 앱 실습입니다.

이 파일은 Streamlit의 가장 기본적인 입력과 출력 흐름을 연습하기 위한 실습입니다.
사용자가 이름, 관심 역할, 자기소개 문장을 입력하면 화면 아래에 간단한 프로필 카드처럼 보여 줍니다.

이 실습에서 확인할 내용:
    1. st.text_input으로 한 줄 텍스트를 입력받는 방법
    2. st.selectbox로 정해진 목록 중 하나를 선택하는 방법
    3. st.text_area로 여러 줄 문장을 입력받는 방법
    4. if 조건문으로 입력값이 있을 때와 없을 때 화면을 다르게 보여 주는 방법

실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\01_streamlit-basic\10_labs\lab-01-profile-card-app.py
"""

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("프로필 카드 앱")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

name = st.text_input("이름")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
role = st.selectbox("관심 역할", ["AI 개발자", "백엔드 개발자", "프론트엔드 개발자", "데이터 분석가"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
message = st.text_area("나를 소개하는 한 문장")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

st.divider()  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.

if name and message:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.header(name)  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    st.write(f"관심 역할: {role}")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    st.info(message)  # 다음 행동을 안내하는 정보 메시지를 표시합니다.
else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
    st.warning("이름과 소개 문장을 입력하면 프로필 카드가 완성됩니다.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.

