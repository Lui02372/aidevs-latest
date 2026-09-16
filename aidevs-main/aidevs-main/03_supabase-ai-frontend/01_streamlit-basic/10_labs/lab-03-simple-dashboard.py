r"""Lab 03: 간단 대시보드 실습입니다.

이 파일은 Streamlit의 sidebar, columns, metric을 사용해서
학습 시간과 실습 상태를 한눈에 보는 작은 대시보드 화면을 만드는 실습입니다.

이 실습에서 확인할 내용:
    1. st.set_page_config로 페이지 제목과 레이아웃을 설정하는 방법
    2. st.sidebar로 입력 영역을 왼쪽 사이드바에 배치하는 방법
    3. st.columns로 메인 화면을 여러 열로 나누는 방법
    4. st.metric으로 숫자나 상태값을 대시보드처럼 보여 주는 방법

실행:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\01_streamlit-basic\10_labs\lab-03-simple-dashboard.py
"""

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.set_page_config(page_title="간단 대시보드", layout="wide")  # Streamlit 페이지의 브라우저 제목과 레이아웃 같은 기본 설정을 지정합니다.
st.title("간단 대시보드 실습")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

with st.sidebar:  # 화면 왼쪽 사이드바 영역에 입력 컴포넌트를 배치합니다.
    user = st.text_input("사용자")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    study_time = st.number_input("오늘 학습 시간", min_value=0.0, max_value=12.0, value=2.0, step=0.5)  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    completed = st.checkbox("오늘 예제를 모두 실행했습니다")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

col_time, col_status = st.columns(2)  # 메인 화면을 여러 열로 나누어 대시보드 요소를 배치합니다.

with col_time:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.metric("학습 시간", f"{study_time}시간")  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

with col_status:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    status_text = "완료" if completed else "진행 중"  # 조건 결과를 사람이 읽기 쉬운 상태 문구로 변환해 저장합니다.
    st.metric("실습 상태", status_text)  # 핵심 숫자나 상태값을 대시보드 지표 형태로 표시합니다.

if user:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    st.write(f"{user}님의 오늘 학습 기록입니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
    st.info("사이드바에서 사용자 이름을 입력하세요.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.

