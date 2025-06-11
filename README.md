# Trust_Metric_Aggregator_Microservice

This repository contains the microservice for aggregating and sending any required data for trust calculation in a distributed trust management system.

## Architecture and Used Technology

- **Language:** [Python](https://www.python.org/) 3.13+
- **API:** [Strawberry GraphQL](https://strawberry.rocks/) for inter-microservice communication
- **Metrics:** [Prometheus](https://prometheus.io/) and [Node Exporter](https://github.com/prometheus/node_exporter) for performance metric collection
- **Dependency Management:** [Poetry](https://python-poetry.org/)
- **Containerization:** [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

The microservice exposes a GraphQL server on port `8000` at the `/graphql` path for trust attribute data queries.

## Setup Instructions

### 1. **Clone the repository and enter the folder:**
   ```powershell
   git clone https://github.com/LukaPantar/Trust_Metric_Aggregator_Microservice
   cd TrustMetricAggregatorMicroservice
   ```

### 2. **Create the `.env` file:**
   - Copy the contents of `.env.TEMPLATE` to a new file named `.env` in the same directory.

### 3. **(Optional, if running with other microservices)**
   - Ensure a Docker network exists for inter-service communication:
     ```powershell
     docker network create trust-network
     ```

### 4. **Start the microservice with Docker Compose:**
   ```powershell
   docker compose up --build
   ```
   - The service will be available at `http://localhost:8000/graphql`.

### 5. **(Optional) Testing with Prometheus**
   - A test Prometheus service is provided in `test_service/`. You can use its `docker-compose.yml` to spin up a test Prometheus and Node Exporter environment for local metric collection.

## Notes
- For full system operation, ensure all microservices are running and connected to the same Docker network.
- Only the `.env.TEMPLATE` is committed; you must create your own `.env` file before starting the service.
- For Prometheus metric testing, see the `test_service/` directory for example configurations.