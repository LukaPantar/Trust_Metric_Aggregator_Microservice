# Trust_Metric_Aggregator_Microservice

This repository contains microservice for aggregating and sending any required data for trust calculation.

## Architecture and used technology

Microservice is written in [Python](https://www.python.org/) 3.13+ and uses Python implementation
of [GraphQL](https://graphql.org/) query language named [Strawberry](https://strawberry.rocks/) for communication between microservices.
[Prometheus](https://prometheus.io/) (and its additional exporter [Node exporter](https://github.com/prometheus/node_exporter))
is used for collection and querying of individual performance metrics.
Python packaging and dependency management is done with [Poetry](https://python-poetry.org/).

Microservice exposes on port `8000`:
- GraphQL server for sending specific data for trust attributes. It can be accessed through `/graphql` path.

## Local testing (Linux)

 Make sure the following tools are installed:
- [Python](https://www.python.org/) 3.13+,
- [Poetry](https://python-poetry.org/),
- [Prometheus](https://prometheus.io/),
- [Node exporter](https://github.com/prometheus/node_exporter)

Currently only local machine can be used as an observed stakeholder, therefore it is necessary 
to use configuration file `performance.yml` for your local Prometheus client. 
This ensures Prometheus endpoint to run on port `9090` and Node exporter endpoint on port `9100`.
After initializing and activating Python virtual environment we install dependencies and start the application with:
```bash
$ poetry install
$ poetry run python main.py
```

Any valid GraphQL query can now be input through `/graphql` path manually or through other microservices.

## Configuration

 - `configuration/performance.yml` is used to configure local Prometheus and Node exporter and should be integrated into observed Prometheus client.