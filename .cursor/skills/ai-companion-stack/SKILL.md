---
name: ai-companion-stack
description: >-
  Guides work on the local AI VTuber companion setup repo: Ollama, Kokoro TTS,
  Open-LLM-VTuber, conf.yaml, and start scripts. Use when editing ai-companion-setup,
  conf.yaml, start.sh, start.ps1, or explaining the voice/LLM pipeline without Live2D asset edits.
---

# AI Companion — Stack & setup (ai-companion-setup)

This skill applies to **[MaxatGoodNotes/ai-companion-setup](https://github.com/MaxatGoodNotes/ai-companion-setup)** — the **documentation and config** repo. The **running application** lives in a local **Open-LLM-VTuber** clone (see `README.md`).

## Architecture (mental model)

| Service | Default port | Role |
|---------|----------------|------|
| **Ollama** | `11434` | Local LLM (e.g. dolphin-llama3) |
| **Kokoro (FastAPI)** | `8880` | TTS compatible with OpenAI-style `/v1` |
| **Open-LLM-VTuber** | `12393` | FastAPI + WebSocket + static frontend |

## Files in this repo

| File | Purpose |
|------|---------|
| `conf.yaml` | `live2d_model_name`, `persona_prompt`, LLM/TTS/ASR blocks — **no real secrets** |
| `start.sh` / `start.ps1` | Launch Kokoro + VTuber (paths may differ per machine) |
| `customizations/` | Copy targets for the Open-LLM-VTuber tree (see sibling skill **ai-companion-live2d-custom**) |
| `PLAN.md` | Roadmap |

## Rules

1. **Never** commit API keys, Kokoro secrets, or user chat transcripts.
2. Prefer **local** inference; cloud keys belong in env vars, not in committed YAML.
3. **Paths** — `AGENTS.md` and `README.md` may reference `~/Documents/open-llm-vtuber`; adjust for the user’s machine.
4. After editing `conf.yaml`, user typically **restarts** the VTuber server to reload.

## When to use another skill

- Editing **Live2D expressions**, `toggle-inject.js`, or `expression_commands.py` sync paths → **ai-companion-live2d-custom**.
- **New repo from scratch** → **project-bootstrap** (cursor-master-rules).
