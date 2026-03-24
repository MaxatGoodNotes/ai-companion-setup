---
name: ai-companion-live2d-custom
description: >-
  Syncs customizations from ai-companion-setup into Open-LLM-VTuber: witchZ3 model
  files, expression_commands.py, toggle-inject.js, model_dict.json, prompts, and
  frontend index.html. Use when editing Live2D expressions, chat commands, emotion
  maps, or browser-injected toggles for the witchZ3 VTuber.
---

# AI Companion — Live2D & frontend customizations

Maps **this repo’s** `customizations/` tree onto a local **Open-LLM-VTuber** checkout. Follow [customizations/INSTALL.md](../../customizations/INSTALL.md) for the full mapping.

## Source → destination (Open-LLM-VTuber root)

| Source (here) | Destination |
|---------------|-------------|
| `customizations/model_dict.json` | `model_dict.json` |
| `customizations/expression_commands.py` | `src/open_llm_vtuber/expression_commands.py` |
| `customizations/toggle-inject.js` | `frontend/toggle-inject.js` |
| `customizations/index.html` | `frontend/index.html` |
| `customizations/live2d_expression_prompt.txt` | `prompts/utils/live2d_expression_prompt.txt` |
| `customizations/witchZ3/*.exp3.json`, `witchZ3.model3.json` | `live2d-models/witchZ3/witchZ3/` |

## WitchZ3 expression index (reference)

Face **F1–F11** and poses **N1–N10** occupy low indices; **tongue** and toggles **E/Q/R/T/ET/W/Y** are listed in `witchZ3.model3.json`. **emotionMap** in `model_dict.json` must match indices after any reorder.

## Frontend quirks

- **Expression commands** send a **silent WAV** so the bundled player applies expressions.
- **toggle-inject.js** uses a **WebSocket Proxy** and a **requestAnimationFrame** loop; writes both live and saved parameter buffers. Bump **`?v=`** on the script tag in `index.html` after edits to **avoid stale cache**.
- **Server** should send **`Cache-Control: no-cache`** for `.json` / `.exp3.json` (see INSTALL patches).

## Security

- Do not log **candidate PII** or user voice content in code paths you add.
- **Third-party** minified `main-*.js` patches — keep surgical; document the exact line changed for upgrades.

## When to use another skill

- **Repo bootstrap / new GitHub project** → **project-bootstrap**.
- **Upstream Python architecture** inside `open-llm-vtuber` → that repo’s `.cursor/rules/olv-core-rules.mdc`.
