import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


def create_learning_reply(topic, question):  # 요청 본문으로 받은 데이터를 새 항목으로 저장합니다.
    return f"[{topic}] 주제에 대한 질문입니다. 핵심 질문: {question}"  # 함수 실행 결과를 호출한 위치로 돌려줍니다.


st.title("응답 템플릿 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

topic = st.selectbox("주제", ["Streamlit", "FastAPI", "Supabase", "API 연동"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
question = st.text_input("질문")  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.

if st.button("템플릿 응답 보기"):  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
    if question:  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        st.write(create_learning_reply(topic, question))  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.
    else:  # 위 조건들이 모두 False일 때 실행할 대체 흐름입니다.
        st.warning("질문을 입력하세요.")  # 주의가 필요한 상황을 경고 메시지로 표시합니다.


