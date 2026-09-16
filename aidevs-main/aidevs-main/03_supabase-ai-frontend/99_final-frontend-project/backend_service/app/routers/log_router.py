from fastapi import APIRouter, Depends

from app.core.security import get_bearer_token
from app.schemas.log_schema import ServiceLogResponse
from app.services.auth_service import get_user_by_token
from app.services.log_service import list_service_logs


router = APIRouter(tags=["logs"])


@router.get("/service-logs", response_model=list[ServiceLogResponse])
def service_logs_api(token: str = Depends(get_bearer_token)) -> list[dict]:
    """로그인한 사용자의 서비스 로그를 Supabase에서 조회합니다."""

    user = get_user_by_token(token)
    return list_service_logs(user)
