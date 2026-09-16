import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(page_title="프론트엔드 통합 점검")
st.title("프론트엔드 통합 점검")
st.caption("실제 배포 전에 Streamlit 화면이 백엔드와 연결될 준비가 되었는지 확인합니다.")


api_base_url = os.getenv("API_BASE_URL", "")


st.subheader("1. 환경변수 확인")
if api_base_url:
    st.success(f"API_BASE_URL 설정됨: {api_base_url}")
else:
    st.error("API_BASE_URL이 설정되어 있지 않습니다. .env 파일을 확인해 주세요.")


st.subheader("2. 통합 점검 체크리스트")

checks = {
    "백엔드 FastAPI 서버가 실행 중이다.": False,
    "브라우저에서 http://127.0.0.1:8000/docs 화면이 열린다.": False,
    "Streamlit 화면에서 API 호출 버튼을 눌렀을 때 응답이 표시된다.": False,
    "로그인 성공 후 token이 st.session_state에 저장된다.": False,
    "보호된 API 호출에 Authorization header가 포함된다.": False,
    "사용자별 대화 이력이 화면에 표시된다.": False,
    "서비스 로그 조회 화면이 정상적으로 열린다.": False,
    "오류 발생 시 사용자가 이해할 수 있는 안내 문구가 표시된다.": False,
}


for label in checks:
    st.checkbox(label, key=label)


st.subheader("3. 수업 범위 구분")
st.info(
    """
이 과정에서는 Streamlit 화면, API 호출, 로그인 상태, 대화 이력, 서비스 로그 조회 화면을 점검합니다.

SSE 기반 실시간 응답 스트리밍은 04_supabase-ai-mini-project에서 통합 실습으로 진행합니다.
Docker, AWS, GitHub Actions, 실제 배포와 운영 자동화는 07_multi-agent-service-ops에서 진행합니다.
"""
)


st.subheader("4. 강의 마무리 질문")
st.markdown(
    """
1. Streamlit은 어떤 역할을 하나요?
2. FastAPI 백엔드는 어떤 역할을 하나요?
3. Supabase service role key를 프론트엔드에 두면 왜 위험할까요?
4. 배포 전에 API_BASE_URL을 확인해야 하는 이유는 무엇인가요?
5. 서비스 로그 화면은 운영 관점에서 어떤 도움을 주나요?
"""
)
