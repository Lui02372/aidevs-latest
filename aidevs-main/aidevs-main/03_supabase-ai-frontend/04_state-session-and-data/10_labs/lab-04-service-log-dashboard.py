import os

import httpx
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


load_dotenv()


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


st.title("Lab 04. 서비스 로그 조회")
st.caption("백엔드 서비스 로그 API를 호출하고 표로 표시하는 실습입니다.")


api_base_url = st.text_input("API_BASE_URL", value=API_BASE_URL)
token = st.text_input("Access Token", value="sample-access-token", type="password")


if st.button("로그 조회"):
    try:
        response = httpx.get(
            f"{api_base_url}/api/service-logs",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
        response.raise_for_status()

        logs = response.json().get("items", [])
        st.success(f"{len(logs)}건의 로그를 조회했습니다.")

        if logs:
            st.dataframe(pd.DataFrame(logs), use_container_width=True)
        else:
            st.info("표시할 로그가 없습니다.")

    except httpx.ConnectError:
        st.error("백엔드 서버가 실행 중인지 확인해 주세요.")
    except httpx.HTTPStatusError as error:
        st.error(f"API 오류가 발생했습니다: {error.response.status_code}")
        st.code(error.response.text)
    except Exception as error:
        st.error("예상하지 못한 오류가 발생했습니다.")
        st.exception(error)
