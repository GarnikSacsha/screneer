$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

$env:BINANCE_PREVIEW_CONCURRENCY = "2"
$env:BINANCE_PARALLEL_SYMBOL_REQUESTS = "false"
$env:BINANCE_REQUEST_PAUSE_MS = "250"
$env:BINANCE_ENABLE_ORDERBOOK = "false"
$env:BINANCE_KLINES_5M_LIMIT = "288"
$env:BINANCE_EMA_KLINES_LIMIT = "120"

Set-Location (Join-Path $Root "backend")
& $VenvPython -m uvicorn app.main:app --host 0.0.0.0 --port 8000
