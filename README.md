# AI Companion Setup

A local, fully offline AI VTuber companion with voice interaction and a Live2D animated avatar. Think Grok's companion mode, but running entirely on your machine with no cloud dependency.

## What This Is

| Component | What | Why |
|-----------|------|-----|
| **LLM** | [Dolphin Llama 3](https://ollama.com/library/dolphin-llama3) via Ollama | Uncensored, playful, conversational — no alignment filters |
| **TTS** | [Kokoro](https://github.com/remsky/Kokoro-FastAPI) (82M params) | Human-sounding local voice synthesis, 67 voice options |
| **ASR** | Sherpa-ONNX SenseVoice | Local speech-to-text, multilingual |
| **Frontend** | [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) v1.2.1 | Live2D avatar, browser-based UI, WebSocket architecture |

Everything runs locally. No API keys. No cloud. No data leaves your machine.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  Browser (localhost:12393)                   │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ Live2D Mao  │  │ Voice input/output   │  │
│  └─────────────┘  └──────────────────────┘  │
└──────────────────────┬──────────────────────┘
                       │ WebSocket
┌──────────────────────▼──────────────────────┐
│  Open-LLM-VTuber Server (:12393)            │
│  Orchestrates ASR → LLM → TTS pipeline      │
└───┬──────────────┬──────────────┬───────────┘
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌──────────┐  ┌────────────┐
│ Ollama │  │ Kokoro   │  │ SenseVoice │
│ :11434 │  │ TTS      │  │ (built-in) │
│        │  │ :8880    │  │            │
│ dolphin│  │ af_sky+  │  │ sherpa-onnx│
│ -llama3│  │ af_bella │  │            │
└────────┘  └──────────┘  └────────────┘
```

---

## Cursor & AI assistants

Project-scoped skills live in [`.cursor/skills/`](.cursor/skills/). See [AGENTS.md](AGENTS.md) for agent context, [docs/SKILLS_AUDIT.md](docs/SKILLS_AUDIT.md) for what was added and why, and [docs/claude-skills-recommendations.md](docs/claude-skills-recommendations.md) for optional third-party skill packs ([alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)).

---

## Prerequisites

| Tool | macOS | Windows |
|------|-------|---------|
| **Git** | Pre-installed | [git-scm.com](https://git-scm.com/download/win) |
| **Ollama** | `brew install ollama` | [ollama.com/download](https://ollama.com/download/windows) |
| **ffmpeg** | `brew install ffmpeg` | `winget install ffmpeg` or [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) |
| **uv** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **espeak-ng** | `brew install espeak` | [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases) (add to PATH) |
| **Python** | Managed by uv | Managed by uv |

---

## Setup (Step by Step)

### 1. Pull the LLM model

```bash
# Start Ollama (if not already running)
ollama serve

# In another terminal — pull the model (~4.7 GB download)
ollama pull dolphin-llama3
```

Dolphin Llama 3 is an 8B parameter model fine-tuned by Eric Hartford with alignment/moralizing responses removed. It needs ~6 GB RAM.

### 2. Clone and install Open-LLM-VTuber

```bash
git clone https://github.com/Open-LLM-VTuber/Open-LLM-VTuber.git
cd Open-LLM-VTuber

# Init the frontend submodule
git submodule update --init --recursive

# Install Python dependencies
uv sync
```

### 3. Copy the config

Copy the `conf.yaml` from this repo into the `Open-LLM-VTuber` directory:

```bash
cp /path/to/ai-companion-setup/conf.yaml ./conf.yaml
```

Or start from the default and make the key changes:

```bash
cp config_templates/conf.default.yaml conf.yaml
```

Then edit `conf.yaml` with these changes:

| Setting | Path in YAML | Value |
|---------|-------------|-------|
| LLM provider | `agent_settings.basic_memory_agent.llm_provider` | `ollama_llm` |
| Model | `llm_configs.ollama_llm.model` | `dolphin-llama3:latest` |
| Temperature | `llm_configs.ollama_llm.temperature` | `1.2` |
| MCP tools | `agent_settings.basic_memory_agent.use_mcpp` | `False` |
| TTS engine | `tts_config.tts_model` | `openai_tts` |
| Kokoro voice | `tts_config.openai_tts.voice` | `af_sky+af_bella` |

### 4. Set up Kokoro TTS

#### macOS (Apple Silicon — uses Metal/MPS)

```bash
git clone https://github.com/remsky/Kokoro-FastAPI.git
cd Kokoro-FastAPI

# Create venv and install
uv venv && source .venv/bin/activate
uv pip install -e .

# Download the model (~315 MB)
python docker/scripts/download_model.py --output api/src/models/v1_0

# Start with MPS acceleration
export USE_GPU=true USE_ONNX=false DEVICE_TYPE=mps PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTHONPATH=$(pwd):$(pwd)/api
export MODEL_DIR=src/models VOICES_DIR=src/voices/v1_0 WEB_PLAYER_PATH=$(pwd)/web
uvicorn api.src.main:app --host 0.0.0.0 --port 8880
```

#### Windows (NVIDIA GPU — uses CUDA)

```powershell
git clone https://github.com/remsky/Kokoro-FastAPI.git
cd Kokoro-FastAPI

# Create venv and install (with GPU support)
uv venv
.venv\Scripts\activate
uv pip install -e ".[gpu]"

# Download model
python docker\scripts\download_model.py --output api\src\models\v1_0

# Start with CUDA
$env:USE_GPU="true"; $env:USE_ONNX="false"; $env:DEVICE_TYPE="cuda"
$env:PYTHONPATH="$PWD;$PWD\api"
$env:MODEL_DIR="src/models"; $env:VOICES_DIR="src/voices/v1_0"
$env:WEB_PLAYER_PATH="$PWD\web"
uvicorn api.src.main:app --host 0.0.0.0 --port 8880
```

#### Windows (CPU only — no NVIDIA GPU)

```powershell
# Same as above but replace the install line:
uv pip install -e ".[cpu]"

# And start without GPU flags:
$env:USE_GPU="false"; $env:USE_ONNX="true"
```

#### Fallback: Edge TTS (no setup needed)

If you don't want to run Kokoro, change `tts_model` in `conf.yaml` to `edge_tts`. It uses Microsoft's cloud TTS and requires internet but zero setup. Sound quality is decent but more robotic.

### 5. Launch

You need **three terminals** running simultaneously:

**Terminal 1 — Ollama**
```bash
ollama serve
```

**Terminal 2 — Kokoro TTS**
```bash
cd Kokoro-FastAPI
# (activate venv and set env vars as above)
uvicorn api.src.main:app --host 0.0.0.0 --port 8880
```

**Terminal 3 — VTuber Server**
```bash
cd Open-LLM-VTuber
uv run run_server.py
```

Open `http://localhost:12393` in your browser.

Or use the quick-start scripts included in this repo:
- **macOS:** `chmod +x start.sh && ./start.sh`
- **Windows:** `powershell -ExecutionPolicy Bypass -File start.ps1`

---

## Windows-Specific Notes

### Ollama on Windows
- Download the Windows installer from [ollama.com](https://ollama.com/download/windows)
- Ollama runs as a system service automatically after install
- Models are stored in `%USERPROFILE%\.ollama\models`
- If you have an NVIDIA GPU, Ollama will use CUDA automatically

### espeak-ng on Windows
- Download the `.msi` installer from [GitHub releases](https://github.com/espeak-ng/espeak-ng/releases)
- After install, add `C:\Program Files\eSpeak NG` to your system PATH
- Verify: `espeak-ng --version`

### GPU Acceleration

| Component | macOS (Apple Silicon) | Windows (NVIDIA) | Windows (CPU) |
|-----------|----------------------|-------------------|---------------|
| Ollama | Metal (automatic) | CUDA (automatic) | CPU fallback |
| Kokoro TTS | MPS | CUDA | ONNX CPU |
| ASR | CPU | CPU (or CUDA) | CPU |

### Path Differences
- macOS: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`
- macOS env: `export VAR=value`
- Windows PowerShell: `$env:VAR="value"`

---

## Customization

### Change the personality

Edit `persona_prompt` in `conf.yaml`:

```yaml
persona_prompt: |
  You are an irreverent, witty, and playful AI companion...
```

The current prompt creates a Grok-like personality — sarcastic, opinionated, warm.

### Change the voice

Edit `tts_config.openai_tts.voice` in `conf.yaml`. Available voices:

| Voice | Style |
|-------|-------|
| `af_sky+af_bella` | Bright, expressive American female (default) |
| `af_heart` | Warm, friendly female |
| `af_nova` | Energetic female |
| `am_puck` | Playful male |
| `am_adam` | Calm male |
| `bf_emma` | British female |
| `bm_george` | British male |

You can blend voices with `+`: e.g., `af_sky+af_heart`.

Browse all 67 voices at `http://localhost:8880/web/` when Kokoro is running.

### Change the LLM model

Other good options for Ollama:

| Model | Pull command | Style | Size |
|-------|-------------|-------|------|
| dolphin-llama3 | `ollama pull dolphin-llama3` | Uncensored, playful (current) | 4.7 GB |
| hermes3 | `ollama pull finalend/hermes-3-llama-3.1` | Roleplay, multi-turn | 4.7 GB |
| llama3 | `ollama pull llama3` | General purpose | 4.7 GB |
| gemma2 | `ollama pull gemma2` | Google's balanced model | 5.4 GB |
| mistral | `ollama pull mistral` | Fast, good quality | 4.1 GB |

Update `llm_configs.ollama_llm.model` in `conf.yaml` to match.

### Change the avatar

The default Live2D model is "Mao". To use a different one, add custom Live2D models to the `live2d/` folder and update `live2d_model_name` in `conf.yaml`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `__API_NOT_SUPPORT_TOOLS__` | Set `use_mcpp: False` in conf.yaml |
| TTS sounds robotic | Switch from `edge_tts` to `openai_tts` (Kokoro) |
| Kokoro not responding | Verify it's running: `curl http://localhost:8880/v1/audio/voices` |
| Ollama model not loading | Run `ollama list` to verify model is downloaded |
| "Frontend not found" | Run `git submodule update --init --recursive` |
| Slow first response | Normal — model loads into memory on first request |
| ASR model downloading on start | Normal on first launch (~999 MB SenseVoice model) |
| Windows: espeak not found | Add espeak-ng install dir to system PATH |
| Windows: CUDA not detected | Update NVIDIA drivers and verify `nvidia-smi` works |

---

## Resource Usage

| Component | RAM | Disk | GPU VRAM |
|-----------|-----|------|----------|
| Ollama (dolphin-llama3 8B) | ~6 GB | 4.7 GB | ~4 GB if GPU |
| Kokoro TTS | ~500 MB | ~400 MB | ~200 MB MPS/CUDA |
| SenseVoice ASR | ~300 MB | 1 GB | — |
| Open-LLM-VTuber server | ~200 MB | ~100 MB | — |
| **Total** | **~7 GB** | **~6.2 GB** | **~4.2 GB** |

Minimum recommended: 16 GB RAM (macOS) or 16 GB RAM + 6 GB VRAM (Windows with GPU).

---

## Upstream Projects

- [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) — the VTuber framework
- [Ollama](https://ollama.com) — local LLM runtime
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) — TTS server
- [Dolphin](https://huggingface.co/cognitivecomputations) — uncensored LLM fine-tunes by Eric Hartford
- [Sherpa-ONNX](https://github.com/k2-fsa/sherpa-onnx) — speech recognition
