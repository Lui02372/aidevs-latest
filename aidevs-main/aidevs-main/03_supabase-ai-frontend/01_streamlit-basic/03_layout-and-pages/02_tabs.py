from pathlib import Path  # 이미지 파일 위치를 안전하게 찾기 위해 Path를 가져옵니다.

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("Tabs 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

# 현재 파일은 01_streamlit-basic/03_layout-and-pages 폴더 안에 있습니다.
# 이미지는 01_streamlit-basic/imgs 폴더 안에 있으므로 parent.parent를 사용해 상위 폴더로 이동합니다.
image_path = Path(__file__).resolve().parent.parent / "imgs" / "springai.png"

tab_summary, tab_detail, tab_memo, tab_image = st.tabs(["요약", "상세", "메모", "이미지"])  # 탭 이름을 순서대로 지정합니다.

with tab_summary:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.header("요약")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    st.write("핵심 내용을 짧게 보여주는 영역입니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

with tab_detail:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.header("상세")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    st.write("표, 차트, 긴 설명 같은 상세 정보를 배치할 수 있습니다.")  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

with tab_memo:  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
    st.header("메모")  # 이 줄은 예제의 핵심 동작을 단계별로 보여주기 위한 코드입니다.
    memo = st.text_area("메모를 입력하세요")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
    st.write("입력한 메모:", memo)  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

with tab_image:  # 이미지 탭을 선택했을 때만 이 영역의 내용이 화면에 보입니다.
    st.header("이미지")  # 이미지 탭의 제목을 표시합니다.

    if image_path.exists():  # 이미지 파일이 실제로 있을 때만 st.image로 출력합니다.
        st.image(
            image_path,
            caption="imgs 폴더의 springai.png 이미지입니다.",
            use_container_width=True,
        )
    else:  # 이미지 파일이 없으면 오류 대신 확인할 경로를 안내합니다.
        st.warning(f"이미지를 찾을 수 없습니다: {image_path}")

