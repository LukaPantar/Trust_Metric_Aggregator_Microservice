from fastapi import FastAPI
import uvicorn

from app.attributes.performance import fetch_metric, MetricUrl, MetricLabels, query_prometheus, PromqlFunction, print_all_metrics
from app.attributes.query import graphql_app

aggregator_app = FastAPI()

aggregator_app.include_router(graphql_app, prefix="/graphql")

prometheus_url = 'http://localhost:9090/'
node_url = 'http://localhost:9100'


def main():

    # Calculate rate of throughput
    rate = query_prometheus(prometheus_url, PromqlFunction.RATE, MetricUrl.THROUGHPUT, MetricLabels.NETWORK_DEVICE_LO,"1m")
    if rate:
        print(f"Rate of throughput ({MetricUrl.THROUGHPUT}) for {MetricLabels.NETWORK_DEVICE_LO}: {rate:.2f} bytes/second")
    else:
        print("Metric not found or missing data.")

    # Calculate bandwidth
    bandwidth = fetch_metric(node_url, MetricUrl.BANDWIDTH, MetricLabels.NETWORK_DEVICE_LO)
    if bandwidth:
        print(f"Bandwidth value is {bandwidth} bytes.")
    else:
        print("Metric not found or missing data.")

    # Parse metrics using Prometheus parser
    print_all_metrics(node_url)

if __name__ == '__main__':
    uvicorn.run(aggregator_app, host="0.0.0.0", port=8000)
    #main()
