from pathlib import Path  # 파일과 폴더 경로를 안전하게 다루기 위해 pathlib의 Path를 가져옵니다.

import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


# 실행:
#   cd C:\aidev\03_supabase-ai-frontend
#   .\.venv\Scripts\Activate.ps1
#   streamlit run .\01_streamlit-basic\02_text-input-and-output\05_image-output.py

st.title("이미지 출력 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

# 현재 파일(05_image-output.py)이 들어 있는 폴더를 기준으로 이미지 폴더 위치를 계산합니다.
# 이 파일은 01_streamlit-basic/02_text-input-and-output 폴더 안에 있고,
# 이미지는 01_streamlit-basic/imgs 폴더 안에 있으므로 parent.parent를 사용합니다.
current_file = Path(__file__).resolve()
image_dir = current_file.parent.parent / "imgs"

# imgs 폴더 안에서 화면에 표시할 수 있는 이미지 파일만 찾습니다.
# glob("*.png")는 png 파일을 찾고, glob("*.jpg")는 jpg 파일을 찾습니다.
image_files = sorted(
    list(image_dir.glob("*.png"))
    + list(image_dir.glob("*.jpg"))
    + list(image_dir.glob("*.jpeg"))
)

if not image_files:  # 이미지 파일이 하나도 없으면, 화면에 오류 대신 안내 메시지를 보여 줍니다.
    st.warning(f"이미지 파일을 찾을 수 없습니다: {image_dir}")
    st.write("imgs 폴더에 png, jpg, jpeg 파일을 넣은 뒤 다시 실행해 보세요.")
else:
    # 이미지가 여러 개 있을 수도 있으므로 selectbox로 어떤 이미지를 보여 줄지 선택하게 합니다.
    selected_name = st.selectbox(
        "화면에 출력할 이미지를 선택하세요",
        [image_file.name for image_file in image_files],
    )

    # 사용자가 선택한 파일 이름과 일치하는 실제 이미지 경로를 찾습니다.
    selected_image = image_dir / selected_name

    st.caption(f"이미지 경로: {selected_image}")  # 현재 어떤 파일을 출력하는지 작은 설명으로 보여 줍니다.

    # st.image는 이미지 파일 경로, URL, 이미지 객체 등을 화면에 출력할 수 있습니다.
    # use_container_width=True를 사용하면 이미지가 화면 너비에 맞게 자연스럽게 조절됩니다.
    st.image(
        selected_image,
        caption=f"{selected_name} 파일을 Streamlit 화면에 출력했습니다.",
        use_container_width=True,
    )
