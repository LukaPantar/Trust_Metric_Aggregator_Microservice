from strawberry.fastapi import GraphQLRouter
from sqlmodel import Session, select
from typing import Any
from datetime import datetime

from app.models.graphql_schema import *
from app.attributes.performance import fetch_metric, MetricUrl, MetricLabels, query_prometheus, PromqlFunction
from app.configuration.database import get_session
from app.models.sql_models import Stakeholder

#prometheus_url = 'http://localhost:9090/'
node_url = 'http://localhost:9100'


# Root query
@strawberry.type
class QueryMain:

    @strawberry.field
    def performance(self, stakeholder_did: str) -> Performance:
        session: Session = next(get_session())
        metrics_url = session.get(Stakeholder, stakeholder_did).metrics_url

        return Performance(
            availability=query_prometheus(metrics_url, PromqlFunction.AVG_OVER_TIME, MetricUrl.AVAILABILITY, MetricLabels.JOB_PROMETHEUS, "1h"),
            reliability=query_prometheus(metrics_url, PromqlFunction.RATE, MetricUrl.RELIABILITY, MetricLabels.IDLE_MODE, "5m"),
            energyEfficiency=query_prometheus(metrics_url, PromqlFunction.AVG_OVER_TIME, MetricUrl.ENERGY_EFFICIENCY, {}, "5m"),
            latency=1,  # TODO using Blackbox exporter
            throughput=1,  # TODO setup http server
            bandwidth=query_prometheus(metrics_url, PromqlFunction.RATE, MetricUrl.BANDWIDTH, MetricLabels.NETWORK_DEVICE_LO, "1m"),
            jitter=1,  # TODO using Blackbox exporter
            packetLoss=1,  # TODO using Blackbox exporter
            utilizationRate=(1 - (fetch_metric(node_url, MetricUrl.UTILIZATION_RATE_AVAILABLE) / fetch_metric(node_url, MetricUrl.UTILIZATION_RATE_TOTAL))),
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
