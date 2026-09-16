import os

import httpx
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


# .env 파일의 API_BASE_URL 값을 읽기 위해 환경변수를 로드합니다.
# 프론트엔드는 Supabase key를 직접 들고 있지 않고, 백엔드 API 주소만 알고 있습니다.
load_dotenv()


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


st.set_page_config(page_title="서비스 로그 대시보드")
st.title("서비스 로그 대시보드")
st.caption("백엔드가 저장한 서비스 로그를 조회하고 프론트엔드 연결 상태를 점검합니다.")


with st.sidebar:
    st.subheader("연결 설정")
    api_base_url = st.text_input("API_BASE_URL", value=API_BASE_URL)
    token = st.text_input("Access Token", value="sample-access-token", type="password")
    st.caption("실제 수업에서는 로그인 API 응답으로 받은 token을 사용합니다.")


def build_headers(access_token: str) -> dict[str, str]:
    """Authorization header를 만드는 작은 함수입니다.

    인증이 필요한 API는 보통 `Authorization: Bearer 토큰` 형식의 header를 요구합니다.
    이 함수를 따로 만들면 여러 API 호출에서 같은 코드를 반복하지 않아도 됩니다.
    """

    return {"Authorization": f"Bearer {access_token}"}


def fetch_service_logs(base_url: str, access_token: str) -> list[dict]:
    """백엔드의 서비스 로그 API를 호출합니다.

    Streamlit 화면은 로그를 직접 만들거나 Supabase에 직접 접속하지 않습니다.
    백엔드 API가 Supabase에서 로그를 조회하고, 프론트엔드는 그 결과만 받아 표시합니다.
    """

    response = httpx.get(
        f"{base_url}/api/service-logs",
        headers=build_headers(access_token),
        timeout=5.0,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("items", [])


if st.button("서비스 로그 불러오기", type="primary"):
    if not api_base_url:
        st.error("API_BASE_URL을 입력해 주세요.")
    elif not token:
        st.error("Access Token을 입력해 주세요.")
    else:
        try:
            with st.spinner("백엔드에서 서비스 로그를 불러오는 중입니다..."):
                logs = fetch_service_logs(api_base_url, token)

            st.success(f"서비스 로그 {len(logs)}건을 불러왔습니다.")

            if logs:
                df = pd.DataFrame(logs)

                ok_count = int((df["status"] == "ok").sum()) if "status" in df else 0
                warning_count = int((df["status"] == "warning").sum()) if "status" in df else 0

                col1, col2, col3 = st.columns(3)
                col1.metric("전체 로그", len(df))
                col2.metric("정상", ok_count)
                col3.metric("주의", warning_count)

                st.dataframe(df, use_container_width=True)
            else:
                st.info("표시할 서비스 로그가 없습니다.")

        except httpx.ConnectError:
            st.error("백엔드 서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인해 주세요.")
        except httpx.HTTPStatusError as error:
            st.error(f"백엔드가 오류 상태 코드를 반환했습니다: {error.response.status_code}")
            st.code(error.response.text)
        except httpx.TimeoutException:
            st.error("API 응답 시간이 초과되었습니다. 백엔드 상태를 확인해 주세요.")
        except Exception as error:
            st.error("예상하지 못한 오류가 발생했습니다.")
            st.exception(error)


st.divider()
st.subheader("학생 확인 질문")
st.markdown(
    """
- 프론트엔드가 Supabase에 직접 접속하지 않는 이유는 무엇인가요?
- 서비스 로그 저장은 어느 계층에서 담당해야 하나요?
- API 호출 실패 시 사용자에게 어떤 메시지를 보여주는 것이 좋을까요?
- 실제 배포 전에 API 주소와 token 처리는 어떻게 확인해야 할까요?
"""
)
