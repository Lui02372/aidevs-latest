"""Lab 04-06: 실제 Support Agent가 최소 Context와 업무 책임을 Refund Agent에 넘깁니다.

시나리오:
    배송 지연 문의를 처리하던 Gemini Support Agent가 환불 조건 확인이 필요하다고
    판단합니다. Handoff 계약과 Python Guard를 통과한 경우에만 Gemma Refund Agent가
    현재 업무의 책임을 인수합니다.

학습 질문:
    결과를 요청하고 돌려받는 함수 호출과 현재 업무 책임을 넘기는 Handoff는 무엇이
    다를까요?

확인할 내용:
    누가 누구에게 어떤 책임과 Context를 넘겼는지 기록하고 사용자, 허용 경로, 민감정보,
    최대 Hop을 검사합니다. 정상 흐름에서는 실제 LLM을 최대 2회 호출합니다.
"""

import json
from typing import Literal

from pydantic import BaseModel, Field

from shared.travel_contracts import HandoffDecision
from shared.travel_llm import provider_for_agent, run_learning_agent, run_with_metadata


class SupportHandoff(BaseModel):
    task_id: str
    trace_id: str
    from_agent: Literal["support_agent"] = "support_agent"
    to_agent: Literal["refund_agent"] = "refund_agent"
    responsibility: str = Field(min_length=5, max_length=300)
    context: dict[str, object]
    user_id: str
    hop_count: int = Field(default=1, ge=1, le=3)


def handoff_guard_agent(handoff: SupportHandoff, expected_user_id: str) -> None:
    if handoff.user_id != expected_user_id:
        raise PermissionError("다른 사용자의 Handoff는 받을 수 없습니다.")
    forbidden = {"api_key", "password", "secret", "raw_messages", "payment_token"}
    exposed = forbidden.intersection(handoff.context)
    if exposed:
        raise ValueError(f"전달하면 안 되는 Context가 있습니다: {sorted(exposed)}")


def support_agent(message: str) -> dict:
    prompt = f"""당신은 support_agent입니다.
배송 지연 문의에서 환불 조건 확인이 필요하면 refund_agent로 Handoff하세요.
handoff_context에는 order_id와 issue만 넣고 비밀번호·Token·전체 대화는 넣지 마세요.
요청: {message}
HandoffDecision 계약으로 반환하세요."""
    return run_with_metadata(provider_for_agent("support_agent"), prompt, HandoffDecision)


def refund_agent(message: str, handoff: SupportHandoff) -> dict:
    return run_learning_agent("refund_agent", handoff.responsibility, message, handoff.model_dump())


if __name__ == "__main__":
    request = "ORDER-102 배송이 일주일 늦었습니다. 환불 조건을 확인해 주세요."
    decision = support_agent(request)
    print("=== Support Agent 결정 ===")
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    if decision["result"] is None:
        print("Support Agent 오류로 Handoff를 실행하지 않습니다.")
    elif not decision["result"]["handoff_required"]:
        print("Support Agent가 계속 책임을 담당합니다.")
    else:
        if decision["result"]["target_agent"] != "refund_agent":
            raise ValueError("Support Agent가 허용되지 않은 Handoff 대상을 선택했습니다.")
        allowed_context_keys = {"order_id", "issue"}
        proposed_context = decision["result"]["handoff_context"]
        safe_context = {key: value for key, value in proposed_context.items() if key in allowed_context_keys}
        safe_context.setdefault("order_id", "ORDER-102")
        safe_context.setdefault("issue", "배송이 일주일 지연됨")
        handoff = SupportHandoff(
            task_id="support-001",
            trace_id="trace-001",
            responsibility="배송 지연 주문의 환불 가능 조건과 필요한 정보를 안내한다.",
            context=safe_context,
            user_id="user-101",
        )
        handoff_guard_agent(handoff, expected_user_id="user-101")
        print("\n=== 검증된 Handoff ===")
        print(handoff.model_dump_json(indent=2))
        accepted = refund_agent(request, handoff)
        print("\n=== 책임을 인수한 Refund Agent ===")
        print(json.dumps(accepted, ensure_ascii=False, indent=2))
