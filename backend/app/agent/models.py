from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

RiskHorizon = Literal["intraday", "intrawick"]
RiskLevel = Literal["low", "moderate", "high", "extreme", "unknown"]
RiskRegime = Literal[
    "base_building",
    "trend_expansion",
    "flow_divergence",
    "exhaustion_risk",
    "unclear",
    "needs_context",
]
RiskStance = Literal["monitor", "avoid", "needs_context"]


class RiskBriefRequest(BaseModel):
    symbol: str = Field(min_length=2, max_length=24, pattern=r"^[A-Za-z0-9]+$")
    horizon: RiskHorizon = "intrawick"

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.strip().upper()


class RiskEvidence(BaseModel):
    id: str
    category: Literal["snapshot", "sector", "event", "policy", "quality"]
    label: str
    value: str
    source: str


class RiskBriefDraft(BaseModel):
    summary: str = Field(min_length=12, max_length=500)
    regime: RiskRegime
    stance: RiskStance
    risk_level: RiskLevel
    confidence: float = Field(ge=0, le=1)
    strengths: list[str] = Field(max_length=5)
    risks: list[str] = Field(max_length=5)
    invalidations: list[str] = Field(max_length=4)
    watch_conditions: list[str] = Field(max_length=4)
    evidence_ids: list[str] = Field(min_length=1, max_length=12)


class AgentToolTrace(BaseModel):
    name: str
    status: Literal["completed", "rejected", "failed"]
    duration_ms: int = Field(ge=0)
    result_count: int = Field(ge=0)


class AgentRunTrace(BaseModel):
    run_id: str
    status: Literal["completed", "fallback", "failed"]
    provider: Literal["openai", "deterministic"]
    model: str | None = None
    response_id: str | None = None
    duration_ms: int = Field(ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    tool_calls: list[AgentToolTrace]
    safety_flags: list[str]
    fallback_reason: str | None = None


class RiskBriefResponse(RiskBriefDraft):
    symbol: str
    horizon: RiskHorizon
    sector: str | None
    snapshot_ts: datetime
    snapshot_age_minutes: float = Field(ge=0)
    data_quality: str
    evidence: list[RiskEvidence]
    requires_human_review: Literal[True] = True
    execution_allowed: Literal[False] = False
    disclaimer: str
    trace: AgentRunTrace


class RiskAgentConfigResponse(BaseModel):
    enabled: bool
    configured: bool
    model: str
    fallback_available: bool = True
    execution_allowed: Literal[False] = False
    tools: list[str]
