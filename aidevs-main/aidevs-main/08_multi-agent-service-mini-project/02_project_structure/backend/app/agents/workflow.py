"""간단한 멀티 에이전트 협업 흐름입니다.

실제 LangGraph나 복잡한 Agent 프레임워크를 바로 쓰기 전에,
각 Agent가 어떤 입력을 받고 어떤 결과를 넘기는지 함수 단위로 먼저 이해합니다.
"""

from ..recovery.strategies import choose_recovery_strategy
from ..schemas.incident import IncidentRequest, RecoveryResult


def diagnose_failure(message: str) -> str:
    """장애 메시지를 보고 장애 유형을 단순 분류합니다."""

    lowered = message.lower()
    if "timeout" in lowered:
        return "network_timeout"
    if "500" in lowered or "5xx" in lowered:
        return "api_5xx"
    if "injection" in lowered or "ignore previous" in lowered:
        return "prompt_injection"
    return "unknown_failure"


def run_auto_healing_workflow(incident_id: str, request: IncidentRequest) -> RecoveryResult:
    """Supervisor -> Diagnosis -> Recovery -> Validation 흐름을 단순 실행합니다."""

    failure_type = diagnose_failure(request.message)
    strategy = choose_recovery_strategy(failure_type)

    if strategy == "block_request":
        final_status = "blocked"
        summary = "Guardrail Agent가 위험한 요청으로 판단해 복구 실행을 차단했습니다."
    elif strategy == "manual_review":
        final_status = "needs_review"
        summary = "장애 유형을 확정하지 못해 수동 검토가 필요합니다."
    else:
        final_status = "success"
        summary = f"{strategy} 전략을 선택하고 Health Check를 통과한 것으로 기록했습니다."

    return RecoveryResult(
        incident_id=incident_id,
        service_name=request.service_name,
        failure_type=failure_type,
        selected_strategy=strategy,
        final_status=final_status,
        summary=summary,
    )
