<#
.SYNOPSIS
    PharmaIntelligence AI - One-Click Development Environment Launcher
.DESCRIPTION
    Launches FastAPI Backend (port 8000) and Next.js Frontend (port 3000)
    in dedicated interactive terminal processes.
#>

param (
    [switch]$OpenBrowser,
    [switch]$SeedData
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "                PHARMAINTELLIGENCE AI - ENTERPRISE HEALTH DSS                  " -ForegroundColor Cyan
Write-Host "       Explainable AI Decision-Support Platform for Pharmaceutical Logistics   " -ForegroundColor DarkCyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verify Virtual Environment
$PythonExe = Join-Path $ScriptDir ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "[ERROR] Python virtual environment not found at .venv\Scripts\python.exe" -ForegroundColor Red
    Write-Host "Run: python -m venv .venv; .venv\Scripts\pip install -r backend\requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host "[✓] Python Virtual Environment detected." -ForegroundColor Green

# 2. Verify Database
$DbPath = Join-Path $ScriptDir "pharmaintelligence_dev.db"
if (-not (Test-Path $DbPath)) {
    Write-Host "[*] Initializing SQLite database schema..." -ForegroundColor Yellow
    & $PythonExe -c "import sys; sys.path.insert(0, 'backend'); from app.database.connection import engine; from app.database.base import Base; import app.models; Base.metadata.create_all(bind=engine); print('Database initialized.')"
}
Write-Host "[✓] SQLite database verified: $DbPath" -ForegroundColor Green

# Optional: Seed Synthetic Clinical Data
if ($SeedData) {
    Write-Host "[*] Seeding realistic Ethiopian healthcare datasets..." -ForegroundColor Yellow
    & $PythonExe -m app.management.generate_synthetic --facilities 8 --months 24 --seed-db
    Write-Host "[✓] Database seeded successfully." -ForegroundColor Green
}

# 3. Launch Backend in new window
Write-Host "[*] Starting FastAPI Backend on http://localhost:8000 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { `$Host.UI.RawUI.WindowTitle = 'PharmaIntelligence Backend (:8000)'; cd '$ScriptDir'; .\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --port 8000 }"

# 4. Launch Frontend in new window
Write-Host "[*] Starting Next.js Frontend on http://localhost:3000 ..." -ForegroundColor Cyan
$FrontendDir = Join-Path $ScriptDir "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { `$Host.UI.RawUI.WindowTitle = 'PharmaIntelligence Frontend (:3000)'; cd '$FrontendDir'; pnpm dev }"

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Green
Write-Host " Services Successfully Dispatched:" -ForegroundColor Green
Write-Host "   • Web Dashboard:    http://localhost:3000" -ForegroundColor White
Write-Host "   • Interactive Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "   • Default Login:    admin@pharmaintelligence.et / Admin123!Secure" -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Green
Write-Host ""

if ($OpenBrowser) {
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:3000"
}
