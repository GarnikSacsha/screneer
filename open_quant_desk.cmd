@echo off
set "PAGE=%~dp0index.html"
set "CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe"
set "EDGE=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

if exist "%CHROME%" (
  start "" "%CHROME%" "%PAGE%"
  exit /b
)

if exist "%EDGE%" (
  start "" "%EDGE%" "%PAGE%"
  exit /b
)

start "" "%PAGE%"
