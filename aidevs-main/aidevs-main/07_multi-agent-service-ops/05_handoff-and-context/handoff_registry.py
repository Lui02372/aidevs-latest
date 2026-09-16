"""YAML 경로 선언을 읽고 Python Guard로 Handoff를 검증합니다."""

from pathlib import Path

import yaml

from handoff_models import HandoffEnvelope


POLICY_FILE = Path(__file__).resolve().parent / "handoff_policies.yaml"
FORBIDDEN_CONTEXT_KEYS = {
    "api_key", "password", "secret", "raw_messages",
    "payment_token", "internal_prompt",
}


def load_routes() -> dict[str, dict]:
    document = yaml.safe_load(POLICY_FILE.read_text(encoding="utf-8"))
    return document["handoff_routes"]


def find_route(handoff: HandoffEnvelope) -> dict:
    for route in load_routes().values():
        if route["from_agent"] == handoff.from_agent and route["to_agent"] == handoff.to_agent:
            return route
    raise PermissionError("허용되지 않은 Handoff 경로입니다.")


def validate_handoff(handoff: HandoffEnvelope, expected_user_id: str) -> HandoffEnvelope:
    if handoff.user_id != expected_user_id:
        raise PermissionError("다른 사용자의 Handoff는 처리할 수 없습니다.")
    route = find_route(handoff)
    if handoff.hop_count > route["max_hops"]:
        raise PermissionError("경로별 최대 Handoff 횟수를 초과했습니다.")

    allowed = set(route["required_context"] + route["optional_context"])
    exposed = set(handoff.context) & FORBIDDEN_CONTEXT_KEYS
    unknown = set(handoff.context) - allowed
    missing = set(route["required_context"]) - set(handoff.context)
    if exposed:
        raise ValueError(f"민감 Context가 포함됐습니다: {sorted(exposed)}")
    if unknown:
        raise ValueError(f"허용되지 않은 Context입니다: {sorted(unknown)}")
    if missing:
        raise ValueError(f"필수 Context가 없습니다: {sorted(missing)}")
    return handoff.model_copy(update={"status": "validated"})


def select_context(route: dict, full_state: dict[str, object]) -> dict[str, object]:
    allowed = route["required_context"] + route["optional_context"]
    return {key: full_state[key] for key in allowed if key in full_state}
