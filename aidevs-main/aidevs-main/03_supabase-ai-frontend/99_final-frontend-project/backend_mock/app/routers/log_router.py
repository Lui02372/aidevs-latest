from fastapi import APIRouter, Depends

from app.core.security import get_bearer_token
from app.schemas.log_schema import ServiceLogItem
from app.services.auth_service import get_user_by_token
from app.services.log_service import list_logs_for_user


router = APIRouter(tags=["logs"])


@router.get("/service-logs", response_model=list[ServiceLogItem])
def service_logs_endpoint(token: str = Depends(get_bearer_token)) -> list[dict]:
    """로그인한 사용자가 볼 수 있는 서비스 로그를 반환합니다."""

    user = get_user_by_token(token)
    return list_logs_for_user(user["email"])
