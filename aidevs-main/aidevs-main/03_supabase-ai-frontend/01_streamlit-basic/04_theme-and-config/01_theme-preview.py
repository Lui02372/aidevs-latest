r"""Streamlit 테마 설정 확인 예제입니다.

이 예제는 같은 폴더 안의 `.streamlit/config.toml` 파일을 읽어 화면 테마를 적용합니다.

실행 위치가 중요합니다.
반드시 `04_theme-and-config` 폴더로 이동한 뒤 실행합니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend\01_streamlit-basic\04_theme-and-config
    ..\..\.venv\Scripts\Activate.ps1
    streamlit run .\01_theme-preview.py

확인:
    - 전체 배경이 흰색인지 확인합니다.
    - 기본 글자가 검정색인지 확인합니다.
    - 버튼과 선택 강조 색상이 config.toml의 primaryColor를 따르는지 확인합니다.
"""

import streamlit as st


st.set_page_config(
    page_title="Streamlit Theme Preview",
    page_icon="🎨",
    layout="centered",
)

st.title("Streamlit 테마 설정 확인")

st.write(
    "이 화면은 `04_theme-and-config/.streamlit/config.toml` 파일의 테마 설정을 기준으로 표시됩니다."
)

st.info(
    "테마는 Python 코드가 아니라 `.streamlit/config.toml` 파일에서 설정합니다. "
    "테마를 수정한 뒤에는 Streamlit 앱을 종료하고 다시 실행하는 것이 가장 확실합니다."
)

st.subheader("입력 위젯 색상 확인")

topic = st.selectbox(
    "확인할 항목을 선택하세요",
    ["배경색", "글자색", "강조색", "입력 영역"],
)

mode = st.radio(
    "화면 모드",
    ["기본", "연습", "프로젝트"],
    horizontal=True,
)

memo = st.text_area(
    "테마 확인 메모",
    placeholder="예: 배경은 흰색이고 글자는 검정색으로 보입니다.",
)

if st.button("선택 내용 확인"):
    st.success(f"선택 항목: {topic} / 화면 모드: {mode}")
    if memo.strip():
        st.write("메모:", memo)
    else:
        st.warning("메모를 입력하지 않았습니다.")

st.subheader("테마 설정 파일 예시")

st.code(
    """
[theme]
base = "light"
primaryColor = "#2563eb"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#000000"
font = "sans serif"
""".strip(),
    language="toml",
)

st.caption(
    "이 예제의 테마는 이 폴더 안의 `.streamlit/config.toml`에만 들어 있습니다. "
    "다른 예제 전체에 자동 적용하지 않기 위해 과정 최상위가 아니라 실습 폴더 안에 둡니다."
)
