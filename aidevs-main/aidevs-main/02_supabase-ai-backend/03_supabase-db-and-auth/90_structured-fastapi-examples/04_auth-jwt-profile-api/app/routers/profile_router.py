"""Profile 관련 API 경로입니다."""

from fastapi import APIRouter

from app.schemas.profile_schema import ProfilePublic, ProfileUpdate
from app.services import auth_service, profile_service


# prefix="/profile"을 사용하면 아래 endpoint들이 /profile 경로 아래에 묶입니다.
router = APIRouter(prefix="/profile")


@router.get("", response_model=ProfilePublic)
def get_profile(user: auth_service.CurrentUser) -> ProfilePublic:
    """현재 로그인한 사용자의 프로필을 조회합니다."""

    # user는 auth_service.get_current_user가 Bearer token을 검증한 결과입니다.
    # user.access_token을 Supabase REST API에 전달하면 RLS가 auth.uid()를 판단할 수 있습니다.
    return profile_service.get_profile(user.access_token)


@router.put("", response_model=ProfilePublic)
def upsert_profile(
    request: ProfileUpdate,
    user: auth_service.CurrentUser,
) -> ProfilePublic:
    """현재 로그인한 사용자의 프로필을 생성하거나 수정합니다."""

    return profile_service.upsert_profile(user.id, user.access_token, request)
