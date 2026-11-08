# PharmaIntelligence AI - Deployment and Infrastructure

This directory contains containerization profiles, reverse proxy definitions, target environment declarations, and monitoring setups.

## Contents

- **`docker/`**: Production multi-stage Dockerfiles for Backend API, Next.js Frontend, and ML Worker.
- **`nginx/`**: Reverse proxy configs, SSL termination, and rate-limiting directives.
- **`environments/`**: Environment variable configurations and k8s / docker-compose manifests for `development`, `staging`, and `production`.
- **`monitoring/`**: Prometheus metrics scraping configs, Grafana dashboard definitions, and alerting rules for service health and model inference drift.

## Quickstart with Docker Compose

```bash
# Build and start all services in detached mode
docker compose up -d --build

# View container logs
docker compose logs -f
```
