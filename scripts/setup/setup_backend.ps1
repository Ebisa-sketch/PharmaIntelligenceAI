<#
.SYNOPSIS
    Sets up the Python virtual environment and dependencies for PharmaIntelligence AI backend.
.DESCRIPTION
    Checks Python installation, creates virtual environment (.venv), upgrades pip,
    installs requirements, and sets up local environment files.
#>

[CmdletBinding()]
param(
    [string]$VenvPath = ".venv",
    [switch]$ForceReinstall
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " PharmaIntelligence AI - Backend Setup    " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verify Python availability
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "Python is not installed or not available on PATH. Please install Python 3.10+."
}

# 2. Virtual Environment Creation
if (-not (Test-Path -Path $VenvPath) -or $ForceReinstall) {
    Write-Host "[*] Creating virtual environment at '$VenvPath'..." -ForegroundColor Yellow
    & python -m venv $VenvPath
    Write-Host "[✓] Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "[✓] Existing virtual environment found at '$VenvPath'." -ForegroundColor Green
}

$venvPython = Join-Path $VenvPath "Scripts\python.exe"
$venvPip = Join-Path $VenvPath "Scripts\pip.exe"

# 3. Upgrade pip
Write-Host "[*] Upgrading pip, setuptools, wheel..." -ForegroundColor Yellow
& $venvPython -m pip install --upgrade pip setuptools wheel --quiet

# 4. Install dependencies
$requirementsPath = "backend\requirements.txt"
if (Test-Path -Path $requirementsPath) {
    Write-Host "[*] Installing backend dependencies from $requirementsPath..." -ForegroundColor Yellow
    & $venvPip install -r $requirementsPath
    Write-Host "[✓] Dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Warning "No requirements.txt found at $requirementsPath. Please verify project structure."
}

# 5. Environment Template Check
if (-not (Test-Path -Path ".env") -and (Test-Path -Path ".env.example")) {
    Write-Host "[*] Creating initial .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[✓] .env file initialized." -ForegroundColor Green
}

Write-Host "`nBackend setup completed successfully!" -ForegroundColor Green
Write-Host "To activate virtual environment: .\$VenvPath\Scripts\Activate.ps1" -ForegroundColor Cyan
