from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from app.attributes.performance import fetch_metric, MetricUrl, MetricLabels, query_prometheus, PromqlFunction, print_all_metrics
from app.attributes.query import graphql_app
from app.configuration import database


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Creating database and tables...")
    database.create_db_and_tables()
    yield

aggregator_app = FastAPI(lifespan=lifespan)

aggregator_app.include_router(graphql_app, prefix="/graphql")

prometheus_url = 'http://localhost:9090/'
node_url = 'http://localhost:9100'


def main():

    # Calculate rate of throughput
    rate = query_prometheus(prometheus_url, MetricUrl.THROUGHPUT, MetricLabels.NETWORK_DEVICE_LO,PromqlFunction.RATE, "1m")
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
