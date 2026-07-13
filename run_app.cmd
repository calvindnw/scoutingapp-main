@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo No se encontro el interprete del entorno virtual en .venv\Scripts\python.exe
  exit /b 1
)

.venv\Scripts\python.exe -m streamlit run Scoutingapp.py --server.headless true --server.address localhost --server.port 8502 --browser.serverAddress localhost --browser.serverPort 8502