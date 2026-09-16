"""05 과정에서 사용하는 Handoff 계약과 책임 상태입니다."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator


HandoffStatus = Literal[
    "proposed", "validated", "accepted", "rejected",
    "transferred", "completed", "failed",
]


class HandoffEnvelope(BaseModel):
    handoff_id: str = Field(min_length=5)
    task_id: str
    trace_id: str
    from_agent: str
    to_agent: str
    responsibility: str = Field(min_length=5, max_length=300)
    context: dict[str, object]
    context_version: int = Field(default=1, ge=1)
    user_id: str
    hop_count: int = Field(default=1, ge=1, le=3)
    status: HandoffStatus = "proposed"

    @model_validator(mode="after")
    def agents_must_be_different(self) -> "HandoffEnvelope":
        if self.from_agent == self.to_agent:
            raise ValueError("자기 자신에게 Handoff할 수 없습니다.")
        return self


class HandoffState(BaseModel):
    task_id: str
    owner_agent: str
    status: Literal["running", "completed", "failed"] = "running"
    processed_handoff_ids: set[str] = Field(default_factory=set)
    events: list[dict[str, object]] = Field(default_factory=list)


class WeatherHandoffDecision(BaseModel):
    agent_id: Literal["weather_agent"] = "weather_agent"
    handoff_required: bool
    target_agent: Literal["itinerary_agent"] | None = None
    reason: str
    responsibility: str | None = None
    handoff_context: dict[str, object] = Field(default_factory=dict)

    @model_validator(mode="after")
    def fields_must_match_decision(self) -> "WeatherHandoffDecision":
        if self.handoff_required and (self.target_agent is None or not self.responsibility):
            raise ValueError("Handoff에는 대상과 책임이 필요합니다.")
        if not self.handoff_required and (self.target_agent or self.handoff_context):
            raise ValueError("Handoff가 없으면 대상과 Context가 비어 있어야 합니다.")
        return self
