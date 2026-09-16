"""장애 이벤트 API 라우터입니다.

라우터는 URL별 API 함수를 모아 두는 공간입니다.
main.py가 너무 커지지 않도록 incidents 관련 API를 이 파일로 분리합니다.
"""

from uuid import uuid4

from fastapi import APIRouter, HTTPException

from ..agents.workflow import run_auto_healing_workflow
from ..schemas.incident import IncidentRequest, RecoveryResult


router = APIRouter(tags=["incidents"])

RECOVERY_STORE: dict[str, RecoveryResult] = {}


@router.post("/incidents", response_model=RecoveryResult)
def create_incident(request: IncidentRequest) -> RecoveryResult:
    """장애 이벤트를 접수하고 Auto Healing 흐름을 실행합니다."""

    incident_id = f"inc-{uuid4().hex[:8]}"
    result = run_auto_healing_workflow(incident_id, request)
    RECOVERY_STORE[incident_id] = result
    return result


@router.get("/recoveries/{incident_id}", response_model=RecoveryResult)
def get_recovery_result(incident_id: str) -> RecoveryResult:
    """장애 이벤트 ID로 복구 결과를 조회합니다."""

    result = RECOVERY_STORE.get(incident_id)
    if result is None:
        raise HTTPException(status_code=404, detail="복구 결과를 찾을 수 없습니다.")
    return result
