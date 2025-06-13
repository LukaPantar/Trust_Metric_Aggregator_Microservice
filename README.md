# Trust_Metric_Aggregator_Microservice

This repository contains the microservice for aggregating and sending any required data for trust calculation in a distributed trust management system.

## Architecture and Used Technology

- **Language:** [Python](https://www.python.org/) 3.13+
- **API:** [Strawberry GraphQL](https://strawberry.rocks/) for inter-microservice communication
- **Metrics:** [Prometheus](https://prometheus.io/) with [Node Exporter](https://github.com/prometheus/node_exporter) and [Ping Exporter](https://github.com/czerwonk/ping_exporter) for performance metric collection
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
   - Copy the contents of `.env.TEMPLATE` to a new file named `.env` in the same directory and customize any settings.

### 3. Create the Docker Network (only once)
Before running any microservice, create the shared Docker network (do this only once):
```powershell
# You only need to run this ONCE for all microservices
# You can do it in any of the microservice folders
# If the network already exists, Docker will not recreate it
docker network create trust_network
```

### 4. **Start the microservice with Docker Compose:**
   ```powershell
   docker compose up --build
   ```
   - The service will be available at `http://localhost:8000/graphql`.

### 5. Environment Variables
The `.env` file is already set up for Docker-based communication. No changes are needed unless you want to customize service names or ports.

```powershell
# PostgreSQL database hostname
DATABASE_HOSTNAME=trust_aggregator_db
# PostgreSQL database port
DATABASE_PORT=5432
# PostgreSQL database username
DATABASE_USERNAME=postgres
# PostgreSQL database password
DATABASE_PASSWORD=postgres
# PostgreSQL database name
DATABASE_NAME=decentralized_kb

# PostgreSQL database name
POSTGRES_DB=decentralized_kb
# PostgreSQL database username
POSTGRES_USER=postgres
# PostgreSQL database password
POSTGRES_PASSWORD=postgres
```

### 6. **(Optional) Testing with Prometheus**
   - A test Prometheus service is provided in `test_service/`. You can use its `docker-compose.yml` to spin up a test Prometheus (with exporters) environment for local metric collection.

## Notes
- For full system operation, ensure all microservices are running and connected to the same Docker network.
- For Prometheus metric testing, see the `test_service/` directory for example configurations.
