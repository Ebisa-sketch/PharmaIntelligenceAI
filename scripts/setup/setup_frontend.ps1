<#
.SYNOPSIS
    Sets up Node.js dependencies and environment for PharmaIntelligence AI frontend.
.DESCRIPTION
    Checks Node.js/npm/pnpm availability, installs frontend packages, and configures environment variables.
#>

[CmdletBinding()]
param(
    [string]$FrontendDir = "frontend",
    [switch]$CleanInstall
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " PharmaIntelligence AI - Frontend Setup   " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verify Node and Package Manager
try {
    $nodeVersion = & node -v 2>&1
    Write-Host "[✓] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Error "Node.js is not found on PATH. Please install Node.js 18+."
}

if (-not (Test-Path -Path $FrontendDir)) {
    Write-Error "Frontend directory '$FrontendDir' does not exist."
}

Push-Location $FrontendDir

try {
    # Check for package manager preference (pnpm -> npm)
    $pkgManager = "npm"
    if (Get-Command "pnpm" -ErrorAction SilentlyContinue) {
        $pkgManager = "pnpm"
    }

    Write-Host "[*] Using package manager: $pkgManager" -ForegroundColor Yellow

    if ($CleanInstall) {
        Write-Host "[*] Cleaning node_modules..." -ForegroundColor Yellow
        if (Test-Path "node_modules") { Remove-Item -Recurse -Force "node_modules" }
        if (Test-Path "package-lock.json") { Remove-Item -Force "package-lock.json" }
        if (Test-Path "pnpm-lock.yaml") { Remove-Item -Force "pnpm-lock.yaml" }
    }

    Write-Host "[*] Installing frontend dependencies..." -ForegroundColor Yellow
    if ($pkgManager -eq "pnpm") {
        & pnpm install
    } else {
        & npm install
    }
    Write-Host "[✓] Frontend dependencies installed successfully." -ForegroundColor Green

    # Setup environment
    if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
        Write-Host "[*] Creating frontend .env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "[✓] Frontend .env created." -ForegroundColor Green
    }
} finally {
    Pop-Location
}

Write-Host "`nFrontend setup completed successfully!" -ForegroundColor Green
Write-Host "To start development server: cd $FrontendDir; npm run dev" -ForegroundColor Cyan
