"""장애 이벤트와 복구 결과 데이터 구조를 정의합니다.

Pydantic 모델을 사용하면 API 요청/응답의 필수 필드와 타입을 명확히 할 수 있습니다.
"""

from pydantic import BaseModel, Field


class IncidentRequest(BaseModel):
    """사용자가 backend로 보내는 장애 이벤트 요청입니다."""

    service_name: str = Field(..., examples=["backend"])
    message: str = Field(..., examples=["backend timeout occurred"])
    severity: str = Field(default="medium", examples=["low", "medium", "high"])


class RecoveryResult(BaseModel):
    """Auto Healing 흐름이 처리한 결과입니다."""

    incident_id: str
    service_name: str
    failure_type: str
    selected_strategy: str
    final_status: str
    summary: str
