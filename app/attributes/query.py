from strawberry.fastapi import GraphQLRouter
from sqlmodel import Session, select
from typing import Any
from datetime import datetime
import httpx

from app.models.graphql_schema import *
from app.attributes.performance import fetch_metric, MetricUrl, MetricLabels, query_prometheus, PromqlFunction, get_latency_ms
from app.configuration.database import get_session
from app.models.sql_models import Stakeholder

#prometheus_url = 'http://localhost:9090/'

# Root query
@strawberry.type
class QueryMain:

    @strawberry.field
    def performance(self, stakeholder_did: str) -> Performance:
        session: Session = next(get_session())
        metrics_url = session.get(Stakeholder, stakeholder_did).metrics_url

        return Performance(
            availability=query_prometheus(metrics_url, MetricUrl.AVAILABILITY, MetricLabels.JOB_PROMETHEUS, PromqlFunction.AVG_OVER_TIME, "1h"),
            reliability=query_prometheus(metrics_url, MetricUrl.RELIABILITY, MetricLabels.IDLE_MODE, PromqlFunction.RATE, "5m"),
            energyEfficiency=query_prometheus(metrics_url, MetricUrl.ENERGY_EFFICIENCY, {}, PromqlFunction.AVG_OVER_TIME, "5m"),
            latency=get_latency_ms(metrics_url),
            throughput=query_prometheus(metrics_url, MetricUrl.THROUGHPUT, MetricLabels.JOB_WEBSERVER, PromqlFunction.RATE, "1m"),
            bandwidth=query_prometheus(metrics_url, MetricUrl.BANDWIDTH, MetricLabels.NETWORK_DEVICE_ETH, PromqlFunction.RATE, "1m"),
            jitter=query_prometheus(metrics_url, MetricUrl.JITTER, MetricLabels.PING_TARGET, PromqlFunction.AVG_OVER_TIME, "5m"),
            packetLoss=query_prometheus(metrics_url, MetricUrl.PACKET_LOSS, MetricLabels.PING_TARGET, PromqlFunction.AVG_OVER_TIME, "5m"),
            utilizationRate=1 - (query_prometheus(metrics_url, MetricUrl.UTILIZATION_RATE_AVAILABLE, MetricLabels.JOB_NODE) /
                                 query_prometheus(metrics_url, MetricUrl.UTILIZATION_RATE_TOTAL, MetricLabels.JOB_NODE)),
        )

    @strawberry.field
    def identity(self, stakeholder_did: str) -> Identity:
        # Currently not used, but will be in the future with VC
        return Identity(trust=1)

    @strawberry.field
    def reputation(self, stakeholder_did: str) -> Reputation:
        session: Session = next(get_session())
        trust = session.get(Stakeholder, stakeholder_did).reputation
        return Reputation(trust=trust)

    @strawberry.field
    def direct_trust(self, stakeholder_did: str) -> DirectTrust:
        session: Session = next(get_session())
        trust = session.get(Stakeholder, stakeholder_did).direct_trust
        return DirectTrust(trust=trust)

    @strawberry.field
    def compliance(self, stakeholder_did: str) -> Compliance:
        session: Session = next(get_session())
        trust = session.get(Stakeholder, stakeholder_did).compliance
        return Compliance(trust=trust)

    @strawberry.field
    def historical_behavior(self, stakeholder_did: str) -> HistoricalBehavior:
        session: Session = next(get_session())
        trust = session.get(Stakeholder, stakeholder_did).historical_behavior
        return HistoricalBehavior(trust=trust)

    @strawberry.field
    def location(self, stakeholder_did: str) -> Location:
        session: Session = next(get_session())
        lat = session.get(Stakeholder, stakeholder_did).location_lat
        lon = session.get(Stakeholder, stakeholder_did).location_lon
        return Location(lat=lat,
                        lon=lon)

    @strawberry.field
    def contextual_fit(self, stakeholder_did: str) -> ContextualFit:
        session: Session = next(get_session())
        trust = session.get(Stakeholder, stakeholder_did).contextual_fit
        return ContextualFit(trust=trust)

    @strawberry.field
    def third_party_validation(self, stakeholder_did: str) -> ThirdPartyValidation:
        session: Session = next(get_session())
        trust = session.get(Stakeholder, stakeholder_did).third_party_validation
        return ThirdPartyValidation(trust=trust)

schema = strawberry.Schema(query=QueryMain)
graphql_app = GraphQLRouter(schema)
