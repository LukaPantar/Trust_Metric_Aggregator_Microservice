from fastapi import FastAPI
from typing import List, Optional
import strawberry

# Response
@strawberry.type
class PerformanceMetrics:
    availability: Optional[float] = None
    reliability: Optional[float] = None
    energyEfficiency: Optional[float] = None
    latency: Optional[float] = None
    throughput: Optional[float] = None
    bandwidth: Optional[float] = None
    jitter: Optional[float] = None
    packetLoss: Optional[float] = None
    utilizationRate: Optional[float] = None

@strawberry.type
class Identity:
    trust: float

@strawberry.type
class Reputation:
    trust: float

@strawberry.type
class DirectTrust:
    trust: float

@strawberry.type
class Compliance:
    trust: float

@strawberry.type
class HistoricalBehavior:
    trust: float

@strawberry.type
class Location:
    lat: float
    lon: float

@strawberry.type
class ContextualFit:
    trust: float

@strawberry.type
class ThirdPartyValidation:
    trust: float

'''@strawberry.type
class Attributes:
    performance: PerformanceMetrics
    identity: Identity
    reputation: Reputation
    direct_trust: DirectTrust
    compliance: Compliance
    historical_behavior: HistoricalBehavior
    location: Location
    contextual_fit: ContextualFit
    third_party_validation: ThirdPartyValidation'''


