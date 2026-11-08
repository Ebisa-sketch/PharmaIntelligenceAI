# Installation and Local Development Guide

---

## 1. System Prerequisites

Before installing PharmaIntelligence AI, ensure your host environment satisfies the following minimum prerequisites:

- **Operating System:** Windows 10/11, Ubuntu 22.04 LTS+, macOS 13+ (Ventura).
- **Python:** Version 3.11 or higher (`python --version`).
- **Node.js:** Version 20 LTS or higher (`node --version`) with `npm` or `pnpm`.
- **Database:** PostgreSQL 15 or higher (or Docker Desktop).
- **Containerization (Recommended):** Docker Engine 24+ and Docker Compose v2+.
- **Hardware Recommendations:**
  - Minimum: Dual-core CPU, 4GB RAM, 10GB free disk space.
  - Recommended for Training: Quad-core CPU, 8GB+ RAM, SSD storage.

---

## 2. Quickstart with Docker Compose (Recommended)

The fastest method to deploy a complete, isolated local environment is using Docker Compose:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/PharmaIntelligenceAI.git
cd PharmaIntelligenceAI

# 2. Prepare environment variables
cp .env.example .env

# 3. Build and launch all container services
docker compose up --build -d

# 4. Verify running services
docker compose ps
```

Once running:
- **Frontend Dashboard:** http://localhost:3000
- **FastAPI REST API Docs:** http://localhost:8000/docs
- **PostgreSQL Database:** `localhost:5432`

---

## 3. Manual Step-by-Step Local Setup

### 3.1 Backend Setup (Python FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

# Install backend dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed initial reference data (medicines, test facilities)
python -m scripts.seed_database

# Start FastAPI development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3.2 Frontend Setup (Next.js 14)

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node dependencies
npm install
# or: pnpm install

# Start Next.js local development server
npm run dev
```

---

## 4. Initial Administrative Access

Default seeded administrative credentials for local testing:
- **Email:** `admin@pharmaintel.gov.et`
- **Password:** `AdminSecure2026!`
- **Role:** `ROLE_ADMIN`

> [!WARNING]
> Always change default administrative passwords immediately upon deploying to any staging or production environment.
