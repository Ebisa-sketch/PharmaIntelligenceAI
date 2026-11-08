# Deployment Guide

## PharmaIntelligence AI — Production Deployment

> **Document status:** Draft  
> **Last updated:** 2026-11-05

---

## 1. Deployment Overview

This guide covers the steps required to deploy PharmaIntelligence AI to a production or staging environment. The system consists of three primary services:

| Service | Technology | Default Port |
|---------|-----------|-------------|
| Frontend | Next.js (Node.js) | 3000 |
| Backend API | FastAPI (Python/Uvicorn) | 8000 |
| Database | PostgreSQL 15 | 5432 |

---

## 2. Prerequisites

- Docker Engine 24+ and Docker Compose v2
- A Linux server (Ubuntu 22.04 LTS recommended) or cloud VM
- Domain name with DNS configured (for HTTPS)
- SSL/TLS certificate (Let's Encrypt recommended)
- At least 4 GB RAM and 2 vCPUs for a minimal deployment

---

## 3. Docker Compose Production Deployment

### 3.1 Prepare environment

```bash
cp .env.example .env
# Edit .env with production values:
#   - Set a strong SECRET_KEY
#   - Set POSTGRES_PASSWORD to a secure value
#   - Set ENVIRONMENT=production
#   - Set DEBUG=False
#   - Configure NEXT_PUBLIC_API_URL to the production API domain
```

### 3.2 Build and start services

```bash
docker-compose -f docker-compose.yml up -d --build
```

### 3.3 Run database migrations

```bash
docker-compose exec backend alembic upgrade head
```

### 3.4 Seed initial data (optional)

```bash
docker-compose exec backend python scripts/database/seed_database.py
```

---

## 4. Reverse Proxy (Nginx)

Place the Nginx configuration in `deployment/nginx/` to:

- Terminate TLS at the proxy
- Route `/api` to the backend service on port 8000
- Route all other requests to the frontend on port 3000
- Set security headers (HSTS, X-Content-Type-Options, X-Frame-Options)

---

## 5. Database Backup Strategy

- Schedule daily `pg_dump` backups via cron
- Store backups in encrypted off-site storage
- Test restore procedures monthly
- Retain at least 30 days of daily backups

---

## 6. Monitoring and Health Checks

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Backend liveness check |
| `GET /api/v1/health` | API readiness check |
| Frontend `/` | Frontend availability |

Configure uptime monitoring (e.g., UptimeRobot, Prometheus + Grafana) to alert on downtime.

---

## 7. Security Checklist

- [ ] All secrets stored in environment variables, not in code
- [ ] Database not exposed to public network
- [ ] HTTPS enforced on all endpoints
- [ ] CORS restricted to production frontend domain
- [ ] Rate limiting enabled on authentication endpoints
- [ ] Audit logging enabled
- [ ] File upload size limits configured
- [ ] Error messages do not leak internal details

---

## 8. Scaling Considerations

- **Horizontal scaling:** Run multiple backend replicas behind a load balancer
- **Database:** Consider connection pooling (PgBouncer) for high concurrency
- **Background jobs:** Add Celery workers and Redis when long-running ML tasks are needed
- **CDN:** Place the frontend behind a CDN for static asset delivery

---

## 9. Rollback Procedure

1. Tag every release in Git before deploying
2. Keep the previous Docker image available
3. To rollback: `docker-compose down && docker-compose up -d` with the previous image tag
4. Rollback database migrations: `alembic downgrade -1`

---

## 10. Limitations

- This guide covers a single-server Docker Compose deployment
- Kubernetes, cloud-managed services, and CI/CD pipeline integration are future extensions
- Real facility data must not be deployed without proper authorization and security controls

