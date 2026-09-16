"""Chat 탭입니다."""
import httpx
import streamlit as st

API_BASE_URL = "https://zero2-mini-project-2.onrender.com"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

def product_create() -> None:
    """로그인 후 mock 대화를 입력하고 누적 표시합니다."""

    st.subheader("Product")
    st.caption("로그인 후 mock 대화를 입력하고 누적 표시합니다.")

    with st.form("product_form", clear_on_submit=True):
        product_id = st.number_input("ID")
        product_name = st.text_input("NAME", placeholder="품명 입력")
        product_price = st.number_input("PRICE")

        submitted = st.form_submit_button("전송")

    if submitted:

        if not product_id or not product_name or not product_price:
            st.warning("모두 입력 하세요")
        else:
            product_name = product_name.strip()
            payload = {"id": product_id, "name": product_name, "price":product_price}  # 백엔드 Pydantic 모델이 기대하는 JSON 구조로 데이터를 만듭니다.
            with st.spinner("전송후 기다립니다."):
                response = httpx.post(f"{API_BASE_URL}/product/create", json=payload, timeout=15.0)  # 메시지 API에 POST 요청을 보냅니다.
            if response.status_code == 200:
                result = response.json()
                st.info("입력 완료")
                st.info(f"{result["id"]} {result["name"]} {result["price"]}")
            else:
                st.warning("오류")
      