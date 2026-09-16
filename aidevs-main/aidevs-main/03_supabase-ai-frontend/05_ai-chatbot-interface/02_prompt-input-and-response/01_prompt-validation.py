import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

st.title("프롬프트 입력 검증")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

prompt = st.text_area("질문", placeholder="질문을 입력하세요")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

if st.button("응답 생성"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    if not prompt.strip():  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        st.warning("질문을 입력하세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.
    elif len(prompt) < 5:  # 앞 조건이 False일 때 추가 조건을 검사합니다.
        st.warning("질문을 조금 더 구체적으로 작성하세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.success("질문이 정상적으로 입력되었습니다.")  # 작업이 성공했음을 초록색 성공 메시지로 표시합니다.
        st.write(prompt)  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.


