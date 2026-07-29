@echo off
setlocal
set "ROOT=%~dp0"
set "PYTHON=%ROOT%.venv\Scripts\python.exe"
set "URL=http://127.0.0.1:8000"

if not exist "%PYTHON%" (
  echo Quant Desk environment is missing.
  echo Run: python -m venv .venv
  echo Then: .venv\Scripts\python -m pip install -e ".\backend[dev]"
  pause
  exit /b 1
)

start "Quant Desk API" powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%start_quant_desk_server.ps1"

powershell.exe -NoProfile -Command ^
  "$deadline=(Get-Date).AddSeconds(20); while((Get-Date)-lt $deadline){try{Invoke-WebRequest '%URL%/api/health' -UseBasicParsing | Out-Null; exit 0}catch{Start-Sleep -Milliseconds 400}}; exit 1"

if errorlevel 1 (
  echo Quant Desk API did not become ready within 20 seconds.
  pause
  exit /b 1
)

start "" "%URL%"
