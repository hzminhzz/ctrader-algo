from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, ClassVar, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

Timeframe = Literal["M1", "M5", "M15", "M30", "H1", "H4", "D1"]
SpreadMode = Literal["fixed", "market"]
CommissionMode = Literal["per_lot", "per_million", "none"]
UtcTimestamp = Annotated[datetime, Field()]
NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class BacktestManifest(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    strategy_id: NonEmptyStr
    symbol: NonEmptyStr
    timeframe: Timeframe
    start: UtcTimestamp
    end: UtcTimestamp
    starting_balance: Annotated[float, Field(gt=0)]
    spread_mode: SpreadMode
    commission_mode: CommissionMode
    parameter_set_path: NonEmptyStr
    output_path: NonEmptyStr
    run_id: NonEmptyStr

    @field_validator("start", "end")
    @classmethod
    def validate_utc_timestamp(cls, value: datetime) -> datetime:
        if value.utcoffset() != timezone.utc.utcoffset(value):
            msg = "timestamp must be UTC"
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def validate_date_order(self) -> "BacktestManifest":
        if self.end <= self.start:
            msg = "end must be after start"
            raise ValueError(msg)
        return self
