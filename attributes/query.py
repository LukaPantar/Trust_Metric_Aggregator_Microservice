from strawberry.fastapi import GraphQLRouter

from models.graphql_schema import *
from attributes.performance import fetch_metric, MetricUrl, MetricLabels, query_prometheus, PromqlFunction

prometheus_url = 'http://localhost:9090/'
node_url = 'http://localhost:9100'

# Root query
@strawberry.type
class QueryMain:

    @strawberry.field
    def performance_metrics(self, stakeholder_id: str) -> PerformanceMetrics:
        return PerformanceMetrics(
            availability=int(stakeholder_id),
            reliability=1,
            energyEfficiency=1,
            latency=1,
            throughput=query_prometheus(prometheus_url, PromqlFunction.RATE, MetricUrl.THROUGHPUT, MetricLabels.NETWORK_DEVICE, 1),
            bandwidth=fetch_metric(node_url, MetricUrl.BANDWIDTH, MetricLabels.NETWORK_DEVICE),
            jitter=1,
            packetLoss=1,
            utilizationRate=1,
        )

    @strawberry.field
    def identity(self, stakeholder_id: str) -> Identity:
        return Identity(trust=1)

    @strawberry.field
    def reputation(self, stakeholder_id: str) -> Reputation:
        return Reputation(trust=1)

    @strawberry.field
    def direct_trust(self, stakeholder_id: str) -> DirectTrust:
        return DirectTrust(trust=0.8)

    @strawberry.field
    def compliance(self, stakeholder_id: str) -> Compliance:
        return Compliance(trust=1)

    @strawberry.field
    def historical_behavior(self, stakeholder_id: str) -> HistoricalBehavior:
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
