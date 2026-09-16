"""Handoff 수락과 책임 소유권 변경을 담당하는 결정적 Python 서비스입니다."""

from handoff_models import HandoffEnvelope, HandoffState
from handoff_registry import validate_handoff


def transfer_ownership_agent(
    state: HandoffState,
    handoff: HandoffEnvelope,
    target_accepted: bool,
) -> tuple[HandoffState, HandoffEnvelope]:
    if state.owner_agent != handoff.from_agent:
        raise PermissionError("현재 책임자만 Handoff를 제안할 수 있습니다.")
    if handoff.handoff_id in state.processed_handoff_ids:
        raise ValueError("이미 처리한 Handoff입니다.")

    checked = validate_handoff(handoff, expected_user_id="user-101")
    state.processed_handoff_ids.add(handoff.handoff_id)
    if not target_accepted:
        state.events.append({"event": "handoff_rejected", "owner": state.owner_agent})
        return state, checked.model_copy(update={"status": "rejected"})

    accepted = checked.model_copy(update={"status": "accepted"})
    state.owner_agent = accepted.to_agent
    state.events.extend([
        {"event": "handoff_accepted", "handoff_id": accepted.handoff_id},
        {"event": "ownership_transferred", "owner": state.owner_agent},
    ])
    return state, accepted.model_copy(update={"status": "transferred"})
