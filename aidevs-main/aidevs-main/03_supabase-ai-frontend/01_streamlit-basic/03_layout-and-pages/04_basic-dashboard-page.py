import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.set_page_config(page_title="기본 대시보드", layout="wide")  # 대시보드가 넓게 보이도록 페이지 레이아웃을 wide로 설정합니다.

st.title("기본 대시보드 페이지")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

with st.sidebar:  # 화면 왼쪽 사이드바 영역에 입력 컴포넌트를 배치합니다.
    st.header("필터")  # 사이드바 입력 영역의 제목을 표시합니다.
    course = st.selectbox("과정", ["Python Basic", "Streamlit Basic", "FastAPI Backend"])  # 사용자가 선택한 과정을 course 변수에 저장합니다.
    progress = st.slider("진도율", min_value=0, max_value=100, value=60)  # 슬라이더로 선택한 진도율 숫자를 progress 변수에 저장합니다.

summary_col, status_col, memo_col = st.columns(3)  # 메인 화면을 세 개의 열로 나누어 지표를 나란히 배치합니다.

with summary_col:  # 첫 번째 열에는 선택한 과정 정보를 표시합니다.
    st.metric("선택 과정", course)  # 핵심 상태값을 대시보드 지표 형태로 표시합니다.

with status_col:  # 두 번째 열에는 진도율 정보를 표시합니다.
    st.metric("진도율", f"{progress}%")  # 숫자 진도율을 대시보드 지표 형태로 표시합니다.

with memo_col:  # 세 번째 열에는 진도율에 따른 안내 메시지를 표시합니다.
    if progress >= 80:  # 진도율이 80 이상이면 마무리 단계 메시지를 표시합니다.
        st.success("마무리 점검 단계입니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
    elif progress >= 40:  # 진도율이 40 이상 80 미만이면 진행 중 메시지를 표시합니다.
        st.info("꾸준히 진행 중입니다.")  # 다음 행동을 안내하는 정보 메시지를 표시합니다.
    else:  # 진도율이 40 미만이면 기초 예제 복습을 안내합니다.
        st.warning("기초 예제부터 다시 확인하세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.

tab_overview, tab_plan = st.tabs(["개요", "학습 계획"])  # 관련 내용을 탭으로 나누어 한 화면에서 전환해 볼 수 있게 합니다.

with tab_overview:  # 첫 번째 탭에는 현재 선택 상태와 진행률을 표시합니다.
    st.write(f"현재 선택한 과정은 {course}입니다.")  # 현재 선택한 과정을 문장으로 출력합니다.
    st.progress(progress)  # 숫자 진도율을 진행 막대로 표시합니다.

with tab_plan:  # 두 번째 탭에는 학습 진행 순서를 표시합니다.
    st.write("1. 예제 실행")  # 첫 번째 학습 단계를 출력합니다.
    st.write("2. 입력값 변경")  # 두 번째 학습 단계를 출력합니다.
    st.write("3. 화면 구성 수정")  # 세 번째 학습 단계를 출력합니다.
