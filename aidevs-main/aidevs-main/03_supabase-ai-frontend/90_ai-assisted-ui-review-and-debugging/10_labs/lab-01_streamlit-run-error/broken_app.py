r"""Lab 01. Streamlit 실행 오류가 있는 예제입니다.

실행 명령:
    cd C:\aidev\03_supabase-ai-frontend
    .\.venv\Scripts\Activate.ps1
    streamlit run .\90_ai-assisted-ui-review-and-debugging\10_labs\lab-01_streamlit-run-error\broken_app.py

이 파일은 일부러 문제가 들어 있는 코드입니다.
수강생은 오류 메시지를 보고 바로 고치기보다, 먼저 Codex에게 원인 분석을 요청합니다.

프롬프트 예시:
    이 Streamlit 파일을 실행하면 NameError가 발생합니다.
    import 순서와 st 객체 사용 위치를 중심으로 원인을 설명해주세요.
    아직 코드는 수정하지 말고 확인 순서만 알려주세요.
"""

# 의도적인 문제:
# st는 streamlit 모듈을 import한 뒤에 사용할 수 있습니다.
# 하지만 아래 줄은 import보다 먼저 st를 사용하므로 실행 시 NameError가 발생합니다.
st.title("Streamlit 실행 오류 실습")

import streamlit as st


st.write("이 문장은 import 순서를 고친 뒤에 화면에 표시됩니다.")

if st.button("확인"):
    st.success("버튼 클릭이 정상적으로 처리되었습니다.")
