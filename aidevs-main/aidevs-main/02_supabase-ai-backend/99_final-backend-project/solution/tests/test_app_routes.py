r"""99_final-backend-project solution API 흐름 테스트입니다.

실행 방법:
    cd C:\aidev\02_supabase-ai-backend\99_final-backend-project\solution
    python -m pytest tests

이 테스트는 최종 백엔드 프로젝트 solution의 기본 흐름을 확인합니다.
Supabase 환경변수를 비워 두면 앱은 메모리 저장소 모드로 동작합니다.
그래서 실제 Supabase 프로젝트가 없어도 상품 등록, AI 설명 생성, 서비스 로그 조회 흐름을 빠르게 검증할 수 있습니다.
초보자는 이 파일을 통해 "외부 서비스가 없어도 mock/memory 모드로 핵심 API 흐름을 테스트할 수 있다"는 점을 이해하면 됩니다.
"""

import os

from fastapi.testclient import TestClient

from app.main import app


def test_product_ai_description_flow() -> None:
    """상품 등록부터 AI 설명 생성, 서비스 로그 조회까지의 기본 흐름을 확인합니다."""

    # Supabase 연결 값을 비워 두면 테스트는 실제 DB가 아니라 메모리 저장소를 사용합니다.
    # 이 방식은 수강생 PC마다 Supabase 설정이 달라도 같은 테스트를 실행할 수 있게 해 줍니다.
    os.environ["SUPABASE_URL"] = ""
    os.environ["SUPABASE_SERVICE_ROLE_KEY"] = ""

    # TestClient는 uvicorn 서버를 켜지 않고도 FastAPI 앱에 요청을 보낼 수 있는 테스트 도구입니다.
    client = TestClient(app)

    # /health는 앱이 실행 가능한 상태인지 확인하는 가장 기본적인 API입니다.
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["storage"] == "memory"

    # 상품을 하나 등록합니다. 이후 AI 설명 생성 API에서 이 상품 정보를 사용합니다.
    product = client.post(
        "/products",
        json={
            "name": "AI 노트",
            "description": "학습 내용을 정리하는 노트",
            "target_audience": "입문자",
        },
    )
    assert product.status_code == 200

    # 등록된 상품 ID로 AI 설명 생성을 요청합니다.
    # 테스트 환경에서는 실제 LLM API를 호출하지 않고 mock 응답을 사용합니다.
    product_id = product.json()["id"]
    ai_response = client.post(f"/products/{product_id}/ai-description")
    assert ai_response.status_code == 200
    assert ai_response.json()["actual_api_called"] is False

    # 상품 등록과 AI 설명 생성 과정에서 서비스 로그가 남았는지 확인합니다.
    logs = client.get("/service-logs")
    assert logs.status_code == 200
    assert len(logs.json()) >= 2
