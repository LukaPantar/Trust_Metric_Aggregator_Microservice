from strawberry.fastapi import GraphQLRouter

from models.graphql_schema import *
from attributes.performance import fetch_metric, MetricUrl, MetricLabels, query_prometheus, PromqlFunction

prometheus_url = 'http://localhost:9090/'
node_url = 'http://localhost:9100'

# Root query
@strawberry.type
class QueryMain:

    @strawberry.field
    def performance_metrics(self) -> PerformanceMetrics:
        return PerformanceMetrics(
            availability=1,
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
    def identity(self) -> Identity:
        return Identity(trust=1)

    @strawberry.field
    def reputation(self) -> Reputation:
        return Reputation(trust=1)

    @strawberry.field
    def direct_trust(self) -> DirectTrust:
        return DirectTrust(trust=0.8)

    @strawberry.field
    def compliance(self) -> Compliance:
        return Compliance(trust=1)

    @strawberry.field
    def historical_behavior(self) -> HistoricalBehavior:
        return HistoricalBehavior(trust=0.8)

    @strawberry.field
    def location(self) -> Location:
        return Location(lat=46.05,
                        lon=14.47)

    @strawberry.field
    def contextual_fit(self) -> ContextualFit:
        return ContextualFit(trust=0.7)

    @strawberry.field
    def third_party_validation(self) -> ThirdPartyValidation:
        return ThirdPartyValidation(trust=0.6)

schema = strawberry.Schema(query=QueryMain)
graphql_app = GraphQLRouter(schema)
