"""상품과 서비스 로그 저장을 담당하는 서비스 파일입니다.

이 파일은 수업용으로 중요한 구조를 보여 줍니다.

1. Supabase 설정이 있으면 실제 Supabase 테이블에 저장합니다.
2. Supabase 설정이 없으면 Python 리스트에 임시 저장합니다.

이런 방식을 사용하는 이유:
    초보자는 처음부터 DB 연결에서 막힐 수 있습니다.
    그래서 먼저 memory 모드로 API 흐름을 이해하고,
    이후 `.env`와 schema.sql을 설정해 Supabase 모드로 확장할 수 있게 합니다.

주의:
    memory 모드는 서버를 재시작하면 데이터가 사라집니다.
    실제 프로젝트나 제출 결과에서는 Supabase 같은 영구 저장소를 사용하는 것이 좋습니다.
"""

import os
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.core import config  # noqa: F401  # .env 로드를 보장합니다.
from app.schemas.product_schema import ProductCreate

try:
    from supabase import create_client
except ImportError:
    # supabase 패키지가 설치되어 있지 않아도 앱 자체는 memory 모드로 실행되게 합니다.
    # 최종 프로젝트에서 Supabase를 실제로 쓰려면 requirements.txt 설치가 필요합니다.
    create_client = None


# Supabase를 사용하지 않을 때 임시로 데이터를 저장하는 리스트입니다.
# 서버가 실행 중인 동안만 유지되고, 서버를 끄면 사라집니다.
memory_products: list[dict] = []
memory_logs: list[dict] = []


def now_text() -> str:
    """현재 UTC 시간을 문자열로 반환합니다.

    API 응답과 로그에 created_at 값을 넣기 위해 사용합니다.
    """

    return datetime.now(timezone.utc).isoformat()


def is_real_value(value: str | None) -> bool:
    """환경변수가 비어 있지 않고 `.env.example`의 예시 값도 아닌지 확인합니다."""

    cleaned = (value or "").strip()
    return bool(cleaned) and not cleaned.startswith(("your-", "https://your-"))


def get_supabase_client() -> Any | None:
    """Supabase 클라이언트를 만들 수 있으면 반환하고, 아니면 None을 반환합니다.

    필요한 환경변수:
        SUPABASE_URL
        SUPABASE_SERVICE_ROLE_KEY

    None을 반환하는 경우:
        1. `.env` 값이 비어 있음
        2. `.env.example`에 있는 예시 값 그대로임
        3. supabase 패키지가 설치되어 있지 않음
    """

    url = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    if not is_real_value(url) or not is_real_value(key) or create_client is None:
        return None

    return create_client(url, key)


def get_storage_mode() -> str:
    """현재 저장소 모드를 문자열로 알려 줍니다.

    `/health` API에서 이 값을 보여 주면 지금 DB 연결 상태를 쉽게 확인할 수 있습니다.
    """

    return "supabase" if get_supabase_client() else "memory"


def save_log(action: str, status: str, detail: str | None = None) -> None:
    """서비스에서 발생한 작업 로그를 저장합니다.

    예:
        상품 등록 성공
        AI 설명 생성 성공
        없는 상품 ID로 AI 설명 생성 실패
    """

    log = {
        "id": str(uuid4()),
        "action": action,
        "status": status,
        "detail": detail,
        "created_at": now_text(),
    }

    supabase = get_supabase_client()
    if supabase:
        # Supabase 모드에서는 final_service_logs 테이블에 저장합니다.
        # id와 created_at은 schema.sql의 기본값이 자동으로 채웁니다.
        supabase.table("final_service_logs").insert(
            {
                "action": action,
                "status": status,
                "detail": detail,
            }
        ).execute()
        return

    # memory 모드에서는 Python 리스트에 저장합니다.
    memory_logs.append(log)


def create_product(payload: ProductCreate) -> dict:
    """상품을 새로 등록합니다.

    payload는 Pydantic 모델이므로 이미 기본적인 값 검증이 끝난 상태입니다.
    Supabase 모드에서는 DB insert 결과를 반환하고,
    memory 모드에서는 직접 만든 dict를 리스트에 넣고 반환합니다.
    """

    product = {
        "id": str(uuid4()),
        "name": payload.name,
        "description": payload.description,
        "target_audience": payload.target_audience,
        "ai_description": None,
        "created_at": now_text(),
    }

    supabase = get_supabase_client()
    if supabase:
        # Supabase Python SDK의 기본 흐름:
        # table("테이블명").insert({...}).execute()
        result = supabase.table("final_products").insert(
            {
                "name": payload.name,
                "description": payload.description,
                "target_audience": payload.target_audience,
            }
        ).execute()
        product = result.data[0]
    else:
        memory_products.append(product)

    save_log("create_product", "success", f"상품 등록: {payload.name}")
    return product


def list_products() -> list[dict]:
    """상품 목록을 최신순으로 조회합니다."""

    supabase = get_supabase_client()
    if supabase:
        # Supabase에서는 created_at 기준 내림차순으로 조회합니다.
        result = (
            supabase.table("final_products")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return result.data

    # memory 모드에서도 최신 등록 상품이 먼저 보이도록 뒤집어서 반환합니다.
    return list(reversed(memory_products))


def find_product(product_id: str) -> dict | None:
    """상품 ID로 상품 하나를 찾습니다.

    찾으면 dict를 반환하고, 없으면 None을 반환합니다.
    """

    supabase = get_supabase_client()
    if supabase:
        # eq("id", product_id)는 SQL의 WHERE id = product_id 조건과 비슷합니다.
        result = (
            supabase.table("final_products")
            .select("*")
            .eq("id", product_id)
            .execute()
        )
        if not result.data:
            return None
        return result.data[0]

    # memory 모드에서는 리스트를 순회하면서 id가 같은 상품을 찾습니다.
    return next((item for item in memory_products if item["id"] == product_id), None)


def update_ai_description(product_id: str, ai_description: str) -> None:
    """상품의 AI 설명 필드를 수정합니다."""

    supabase = get_supabase_client()
    if supabase:
        # Supabase update도 table().update().eq().execute() 순서로 많이 사용합니다.
        (
            supabase.table("final_products")
            .update({"ai_description": ai_description})
            .eq("id", product_id)
            .execute()
        )
        return

    # memory 모드에서는 찾은 dict를 직접 수정합니다.
    product = find_product(product_id)
    if product is not None:
        product["ai_description"] = ai_description


def list_service_logs() -> list[dict]:
    """서비스 로그 목록을 최신순으로 조회합니다."""

    supabase = get_supabase_client()
    if supabase:
        result = (
            supabase.table("final_service_logs")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return result.data

    return list(reversed(memory_logs))
