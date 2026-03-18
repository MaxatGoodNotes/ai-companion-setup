# Quick-start script for Windows
# Usage: powershell -ExecutionPolicy Bypass -File start.ps1

$KokoroDir = if ($env:KOKORO_DIR) { $env:KOKORO_DIR } else { "$HOME\Documents\Kokoro-FastAPI" }
$VTuberDir = if ($env:VTUBER_DIR) { $env:VTUBER_DIR } else { "$HOME\Documents\Open-LLM-VTuber" }

# Check if Ollama is running
$ollamaRunning = Get-Process -Name ollama -ErrorAction SilentlyContinue
if (-not $ollamaRunning) {
    Write-Host "Ollama should be running as a Windows service."
    Write-Host "If not, run: ollama serve"
}

# Start Kokoro TTS
Write-Host "Starting Kokoro TTS on :8880..."
$kokoro = Start-Process powershell -ArgumentList @("-NoExit", "-Command", @"
    cd '$KokoroDir'
    .venv\Scripts\activate
    `$env:USE_GPU='true'
    `$env:USE_ONNX='false'
    `$env:DEVICE_TYPE='cuda'
    `$env:PYTHONPATH="`$PWD;`$PWD\api"
    `$env:MODEL_DIR='src/models'
    `$env:VOICES_DIR='src/voices/v1_0'
    `$env:WEB_PLAYER_PATH="`$PWD\web"
    uvicorn api.src.main:app --host 0.0.0.0 --port 8880
"@) -PassThru

Start-Sleep 15

# Start VTuber
Write-Host "Starting Open-LLM-VTuber on :12393..."
$vtuber = Start-Process powershell -ArgumentList @("-NoExit", "-Command", @"
    cd '$VTuberDir'
    uv run run_server.py
"@) -PassThru

Start-Sleep 15

# Open browser
Start-Process "http://localhost:12393"

Write-Host ""
Write-Host "=== AI Companion is running ==="
Write-Host "VTuber UI:    http://localhost:12393"
Write-Host "Kokoro TTS:   http://localhost:8880/web/"
Write-Host "Close the spawned terminal windows to stop services."
Read-Host "Press Enter to exit this launcher"
