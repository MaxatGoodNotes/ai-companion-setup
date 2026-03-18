#!/bin/bash
# Quick-start script for macOS (Apple Silicon)
# Usage: chmod +x start.sh && ./start.sh

set -e

KOKORO_DIR="${KOKORO_DIR:-$HOME/Documents/kokoro-tts}"
VTUBER_DIR="${VTUBER_DIR:-$HOME/Documents/open-llm-vtuber}"

cleanup() {
    echo "\nStopping all services..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# Ensure Ollama is running
if ! pgrep -x ollama > /dev/null; then
    echo "Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Start Kokoro TTS
echo "Starting Kokoro TTS on :8880..."
cd "$KOKORO_DIR"
source .venv/bin/activate
export USE_GPU=true USE_ONNX=false DEVICE_TYPE=mps PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTHONPATH=$(pwd):$(pwd)/api
export MODEL_DIR=src/models VOICES_DIR=src/voices/v1_0 WEB_PLAYER_PATH=$(pwd)/web
uvicorn api.src.main:app --host 0.0.0.0 --port 8880 &
sleep 10

# Start VTuber
echo "Starting Open-LLM-VTuber on :12393..."
cd "$VTUBER_DIR"
uv run run_server.py &
sleep 10

# Open browser
open http://localhost:12393

echo "\n=== AI Companion is running ==="
echo "VTuber UI:    http://localhost:12393"
echo "Kokoro TTS:   http://localhost:8880/web/"
echo "Press Ctrl+C to stop all services."
wait
