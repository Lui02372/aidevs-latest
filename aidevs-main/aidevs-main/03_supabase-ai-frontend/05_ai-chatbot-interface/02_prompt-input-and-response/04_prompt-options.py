import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.


def create_reply(prompt, tone):  # 요청 본문으로 받은 데이터를 새 항목으로 저장합니다.
    if tone == "짧게":  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        return f"요약 답변: {prompt}"  # 함수 실행 결과를 호출한 위치로 돌려줍니다.
    if tone == "자세히":  # 조건식이 True일 때만 아래 들여쓰기 블록을 실행합니다.
        return f"자세한 답변: 질문의 배경을 확인하고 단계별로 설명하겠습니다. 질문: {prompt}"  # 함수 실행 결과를 호출한 위치로 돌려줍니다.
    return f"실습 중심 답변: 먼저 직접 실행해 보고 결과를 확인하세요. 질문: {prompt}"  # 함수 실행 결과를 호출한 위치로 돌려줍니다.


st.title("프롬프트 옵션 예제")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

tone = st.radio("응답 방식", ["짧게", "자세히", "실습 중심"])  # 계산 결과나 입력값을 이후 코드에서 다시 쓰기 위해 변수에 저장합니다.
prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.

if prompt:  # 사용자가 채팅 입력창에 질문을 입력했을 때만 메시지 처리 로직을 실행합니다.
    st.chat_message("user").write(prompt)  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.
    st.chat_message("assistant").write(create_reply(prompt, tone))  # role 값에 맞는 채팅 말풍선 영역에 메시지를 출력합니다.


