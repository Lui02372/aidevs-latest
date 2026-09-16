"""Lab 01-11: Handoff로 실행 책임을 다른 Agent에게 넘깁니다.

시나리오:
    Support Agent가 배송 지연 상담을 처리하다가 승인된 환불이 필요하다고 판단합니다.
    Support Agent는 환불을 직접 실행하지 않고 Refund Agent에게 책임과 최소 Context를
    전달합니다. Refund Agent가 Handoff를 수락한 뒤 책임 주체가 바뀝니다.

학습 질문:
    함수 호출 결과를 받는 것과 현재 업무 책임을 다른 Agent에게 넘기는 것은 무엇이
    다를까요?

범위:
    최소 필드만 사용합니다. 사용자·Task·민감정보·hop count Guard는 05에서 다룹니다.
"""

from dataclasses import dataclass

from shared.travel_contracts import HandoffDecision
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


@dataclass(frozen=True)
class Handoff:
    from_agent: str
    to_agent: str
    responsibility: str
    context: dict[str, object]


def support_agent(request: str) -> dict:
    prompt = f"""당신은 support_agent입니다.
배송 상태를 안내할 수 있지만 환불 실행은 refund_agent에게 넘겨야 합니다.
승인 ID가 있는 환불 요청만 handoff_required=true로 판단하세요.
요청: {request}
HandoffDecision 계약으로 반환하세요."""
    return run_with_metadata(provider_for_agent("support_agent"), prompt, HandoffDecision)


def create_handoff(decision: dict) -> Handoff | None:
    if not decision["handoff_required"]:
        return None
    if decision["target_agent"] != "refund_agent":
        raise ValueError("허용되지 않은 Handoff 대상입니다.")
    required_keys = {"order_id", "amount", "approval_id"}
    missing_keys = required_keys - set(decision["handoff_context"])
    if missing_keys:
        raise ValueError(f"Handoff Context 필수 항목 누락: {sorted(missing_keys)}")
    return Handoff(
        from_agent="support_agent",
        to_agent="refund_agent",
        responsibility=decision["reason"],
        context=decision["handoff_context"],
    )


def refund_agent(handoff: Handoff, current_agent: str) -> dict[str, object]:
    if handoff.to_agent != current_agent:
        raise PermissionError("Handoff 대상 Agent만 책임을 인수할 수 있습니다.")
    result = run_learning_agent("refund_agent", "승인된 환불 요청을 검토하고 처리 안내를 작성한다.", handoff.responsibility, handoff.context)
    return {
        "owner": current_agent,
        "responsibility": handoff.responsibility,
        "accepted": result["error"] is None,
        "agent_result": result,
    }


if __name__ == "__main__":
    request = "order-301 배송 지연으로 35,000원 환불이 승인되었습니다. 승인 ID는 approval-901입니다."
    support_result = support_agent(request)
    print("Support Agent 결과:", support_result)
    if support_result["error"]:
        print("Handoff 중단: Support Agent가 실패했습니다.")
    else:
        try:
            handoff = create_handoff(support_result["result"])
        except ValueError as error:
            handoff = None
            print("Handoff 계약 오류:", error)
        if handoff is None:
            print("Handoff 없음: Support Agent가 계속 책임집니다.")
        else:
            accepted = refund_agent(handoff, "refund_agent")
            print("Handoff:", handoff)
            print("인수 결과:", accepted)
            print("책임 주체 변경:", accepted["owner"] == "refund_agent" and accepted["accepted"])

            try:
                refund_agent(handoff, "support_agent")
            except PermissionError as error:
                print("잘못된 인수 차단:", error)
