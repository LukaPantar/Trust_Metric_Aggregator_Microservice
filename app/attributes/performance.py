
import requests
from typing import Optional
from prometheus_client.parser import text_string_to_metric_families
import time
from enum import StrEnum
import httpx

class MetricUrl(StrEnum):
    AVAILABILITY = "up"
    RELIABILITY = "node_cpu_seconds_total"
    ENERGY_EFFICIENCY = "node_hwmon_in_volts"
    LATENCY = ""
    THROUGHPUT = "http_requests_total"
    BANDWIDTH = "node_network_receive_bytes_total"
    JITTER = "ping_rtt_std_deviation_seconds"
    PACKET_LOSS = "ping_loss_ratio"
    UTILIZATION_RATE_AVAILABLE = "node_memory_MemAvailable_bytes"
    UTILIZATION_RATE_TOTAL = "node_memory_MemTotal_bytes"


class PromqlFunction(StrEnum):
    RATE = "rate"
    AVG_OVER_TIME = "avg_over_time"


class MetricLabels:
    NETWORK_DEVICE_ETH = {"device": "eth0"}
    NETWORK_DEVICE_LO = {"device": "lo"}
    JOB_PROMETHEUS = {"job": "prometheus"}
    IDLE_MODE = {"mode": "idle"}
    JOB_NODE = {"job": "node"}
    JOB_WEBSERVER={"job": "webserver"}
    PING_TARGET={"target": "8.8.8.8"}


def fetch_metric(metrics_url: str, metric_name: str, label_filter: dict = {}) -> Optional[float]:
    response = requests.get(f"{metrics_url}/metrics")
    response.raise_for_status()
    metrics_data = response.text

    for family in text_string_to_metric_families(metrics_data):
        for sample in family.samples:
            if sample.name == metric_name:
                if all(sample.labels.get(k) == v for k, v in label_filter.items()):
                    return sample.value
    return None

def query_prometheus(metrics_url: str, metric_name: str, label_filter: dict, promql_function: str = "", duration_str: str = "") -> Optional[float]:

    if promql_function == "":
        promql_query = f"{metric_name}"
    else:
        promql_query = f"{promql_function}({metric_name}[{duration_str}])"

    response = requests.get(
        f"{metrics_url}/api/v1/query",
        params={'query': promql_query}
    )
    response.raise_for_status()

    result_json = response.json()['data']['result']
    for sample in result_json:

        if all(sample["metric"].get(k) == v for k, v in label_filter.items()):
            # First value is the timestamp, second is the value of metric as a string
            result_value = float(sample["value"][1])
            return result_value

    return None

def print_all_metrics(metrics_url):
    response = requests.get(metrics_url)
    response.raise_for_status()
    metrics_data = response.text
    for family in text_string_to_metric_families(metrics_data):
        for sample in family.samples:
            name, labels, value = sample.name, sample.labels, sample.value
            print(f"Metric: {name}, Labels: {labels}, Value: {value}")

def get_latency_ms(metrics_url: str) -> float:
    with httpx.Client() as client:
        response = client.get(metrics_url)
        return response.elapsed.total_seconds() * 1000
