
import requests
from typing import Optional
from prometheus_client.parser import text_string_to_metric_families
import time
from enum import StrEnum

class MetricUrl(StrEnum):
    AVAILABILITY = ""
    RELIABILITY = ""
    ENERGY_EFFICIENCY = ""
    LATENCY = ""
    THROUGHPUT = "node_network_receive_bytes_total"
    BANDWIDTH = "node_network_mtu_bytes"
    JITTER = ""
    PACKET_LOSS = ""
    UTILIZATION_RATE = ""

class PromqlFunction(StrEnum):
    RATE = "rate"

class MetricLabels:
    #NETWORK_DEVICE = {"device": "enp59s0u1u4"}
    NETWORK_DEVICE = {"device": "lo"}


PERFORMANCE_METRICS = [
    MetricUrl.AVAILABILITY,
    MetricUrl.RELIABILITY,
    MetricUrl.ENERGY_EFFICIENCY,
    MetricUrl.LATENCY,
    MetricUrl.THROUGHPUT,
    MetricUrl.BANDWIDTH,
    MetricUrl.JITTER,
    MetricUrl.PACKET_LOSS,
    MetricUrl.UTILIZATION_RATE,
]


def fetch_metric(metrics_url, metric_name, label_filter) -> Optional[float]:
    response = requests.get(f"{metrics_url}/metrics")
    response.raise_for_status()
    metrics_data = response.text

    for family in text_string_to_metric_families(metrics_data):
        for sample in family.samples:
            if sample.name == metric_name:
                if all(sample.labels.get(k) == v for k, v in label_filter.items()):
                    return sample.value
    return None

def query_prometheus(metrics_url, promql_function, metric_name, label_filter, duration_min) -> Optional[float]:

    promql_query = f"{promql_function}({metric_name}[{duration_min}m])"

    response = requests.get(
        f"{metrics_url}/api/v1/query",
        params={'query': promql_query}
    )
    response.raise_for_status()

    result_json = response.json()['data']['result']
    for sample in result_json:

        if all(sample["metric"].get(k) == v for k, v in label_filter.items()):
            # First value is timestamp second is the value of metric as a string
            result_value = float(sample["value"][1])
            return result_value

    return None

def measure_rate_of_metric(metrics_url, metric_name, label_filter, delay_s):

    value1 = fetch_metric(metrics_url, metric_name, label_filter)
    time1 = time.time()

    time.sleep(delay_s)

    value2 = fetch_metric(metrics_url, metric_name, label_filter)
    time2 = time.time()

    if value1 is not None and value2 is not None:
        rate = (value2 - value1) / (time2 - time1)
        return rate

    return None

def print_all_metrics(metrics_url):
    response = requests.get(metrics_url)
    response.raise_for_status()
    metrics_data = response.text
    for family in text_string_to_metric_families(metrics_data):
        for sample in family.samples:
            name, labels, value = sample.name, sample.labels, sample.value
            print(f"Metric: {name}, Labels: {labels}, Value: {value}")
