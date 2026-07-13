$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$port = 8502
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$healthUrl = "http://localhost:$port/_stcore/health"
$appUrl = "http://localhost:$port"

if (-not (Test-Path $python)) {
    Write-Error "No se encontro el interprete del entorno virtual en $python"
}

try {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    $processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($processId in $processIds) {
        if ($processId) {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Warning "No se pudo liberar el puerto $port automaticamente: $($_.Exception.Message)"
}

Start-Job -Name 'streamlit-browser-launcher' -ScriptBlock {
    param($healthUrlParam, $appUrlParam)

    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        try {
            $response = Invoke-WebRequest -UseBasicParsing $healthUrlParam -TimeoutSec 2
            if ($response.Content -match 'ok') {
                Start-Process $appUrlParam
                return
            }
        } catch {
        }
        Start-Sleep -Milliseconds 500
    }
} -ArgumentList $healthUrl, $appUrl | Out-Null

Write-Host "Esperando que Streamlit quede disponible en $appUrl"
& $python -m streamlit run Scoutingapp.py --server.headless true --server.address localhost --server.port $port --browser.serverAddress localhost --browser.serverPort $port
