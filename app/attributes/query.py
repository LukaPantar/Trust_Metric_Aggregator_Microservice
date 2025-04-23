from strawberry.fastapi import GraphQLRouter

from app.models.graphql_schema import *
from app.attributes.performance import fetch_metric, MetricUrl, MetricLabels, query_prometheus, PromqlFunction

prometheus_url = 'http://localhost:9090/'
node_url = 'http://localhost:9100'

# Root query
@strawberry.type
class QueryMain:

    @strawberry.field
    def performance(self, stakeholder_did: str) -> Performance:
        return Performance(
            availability=query_prometheus(prometheus_url, PromqlFunction.AVG_OVER_TIME, MetricUrl.AVAILABILITY, MetricLabels.JOB_PROMETHEUS, "1h"),
            reliability=query_prometheus(prometheus_url, PromqlFunction.RATE, MetricUrl.RELIABILITY, MetricLabels.IDLE_MODE, "5m"),
            energyEfficiency=query_prometheus(prometheus_url, PromqlFunction.AVG_OVER_TIME, MetricUrl.ENERGY_EFFICIENCY, {}, "5m"),
            latency=1,  # TODO using Blackbox exporter
            throughput=1,  # TODO setup http server
            bandwidth=query_prometheus(prometheus_url, PromqlFunction.RATE, MetricUrl.BANDWIDTH, MetricLabels.NETWORK_DEVICE_LO, "1m"),
            jitter=1,  # TODO using Blackbox exporter
            packetLoss=1,  # TODO using Blackbox exporter
            utilizationRate=(1 - (fetch_metric(node_url, MetricUrl.UTILIZATION_RATE_AVAILABLE) / fetch_metric(node_url, MetricUrl.UTILIZATION_RATE_TOTAL))),
        )

    @strawberry.field
    def identity(self, stakeholder_did: str) -> Identity:
        return Identity(trust=1)

    @strawberry.field
    def reputation(self, stakeholder_did: str) -> Reputation:
        return Reputation(trust=1)

    @strawberry.field
    def direct_trust(self, stakeholder_did: str) -> DirectTrust:
        return DirectTrust(trust=0.8)

    @strawberry.field
    def compliance(self, stakeholder_did: str) -> Compliance:
        return Compliance(trust=1)

    @strawberry.field
    def historical_behavior(self, stakeholder_did: str) -> HistoricalBehavior:
        return HistoricalBehavior(trust=0.8)

    @strawberry.field
    def location(self, stakeholder_id: str) -> Location:
        return Location(lat=46.05,
                        lon=14.47)

    @strawberry.field
    def contextual_fit(self, stakeholder_id: str) -> ContextualFit:
        return ContextualFit(trust=0.7)

    @strawberry.field
    def third_party_validation(self, stakeholder_id: str) -> ThirdPartyValidation:
        return ThirdPartyValidation(trust=0.6)

schema = strawberry.Schema(query=QueryMain)
graphql_app = GraphQLRouter(schema)
