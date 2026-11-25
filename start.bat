@echo off
title PharmaIntelligence AI - Launcher
color 0B

echo ===============================================================================
echo                PHARMAINTELLIGENCE AI - ENTERPRISE HEALTH DSS
echo        Explainable AI Decision-Support Platform for Pharmaceutical Logistics
echo ===============================================================================
echo.

set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

echo [*] Checking Python Virtual Environment...
if not exist "%ROOT_DIR%.venv\Scripts\python.exe" (
    color 0C
    echo [ERROR] Virtual environment not found at .venv\Scripts\python.exe
    echo Please run: python -m venv .venv ^&^& .venv\Scripts\pip install -r backend\requirements.txt
    pause
    exit /b 1
)

echo [*] Checking Database Initialization...
if not exist "%ROOT_DIR%pharmaintelligence_dev.db" (
    echo [*] Initializing SQLite database schemas...
    "%ROOT_DIR%.venv\Scripts\python.exe" -c "import sys; sys.path.insert(0, 'backend'); from app.database.connection import engine; from app.database.base import Base; import app.models; Base.metadata.create_all(bind=engine); print('Database initialized successfully.')"
)

echo [*] Launching FastAPI Backend on http://localhost:8000 ...
start "PharmaIntelligence AI - Backend API (:8000)" cmd /k "color 0A && cd /d %ROOT_DIR% && .venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --port 8000"

echo [*] Launching Next.js Frontend on http://localhost:3000 ...
start "PharmaIntelligence AI - Next.js Frontend (:3000)" cmd /k "color 09 && cd /d %ROOT_DIR%frontend && pnpm dev"

echo.
echo ===============================================================================
echo  PharmaIntelligence AI services are starting up!
echo.
echo  - Frontend Dashboard:       http://localhost:3000
echo  - Backend API Docs:         http://localhost:8000/docs
echo  - Default Login:            admin@pharmaintelligence.et / Admin123!Secure
echo ===============================================================================
echo.
echo Both services are running in separate terminal windows.
echo You can minimize this window or close it.
pause
