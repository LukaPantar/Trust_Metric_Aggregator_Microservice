import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Stakeholder(SQLModel, table=True):
    did: str = Field(
        primary_key=True, index=True
    )

    type: int
    name: str

    identity: str = Field()

    provider: Optional[str] = None

    reputation: Optional[float] = None
    direct_trust: Optional[float] = None
    compliance: Optional[float] = None
    historical_behavior: Optional[float] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    contextual_fit: Optional[float] = None
    third_party_validation: Optional[float] = None

    created_at: datetime

    metrics_url: str