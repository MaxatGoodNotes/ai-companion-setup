# Skills audit — AI Companion (March 2026)

## Scope

- **Setup & docs repo:** [ai-companion-setup](https://github.com/MaxatGoodNotes/ai-companion-setup) (this repo) — config, `customizations/`, scripts, `PLAN.md`.
- **Runtime codebase:** [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) (local clone) — Python server, `frontend/`, `live2d-models/`.

## What existed before this change

| Location | Contents |
|----------|----------|
| **User global** `~/.cursor/rules/` | Personal rules (web search, security, git workflow, etc.) |
| **User global** `~/.cursor/skills-cursor/` | Meta skills from [cursor-master-rules](https://github.com/MaxatGoodNotes/cursor-master-rules), including **project-bootstrap** |
| **User** `~/.cursor/skills/google-calendar/` | Calendar skill (unrelated to VTuber) |
| **Open-LLM-VTuber** `.cursor/rules/olv-core-rules.mdc` | Upstream coding guidelines for the Python app |
| **ai-companion-setup** | **No** `.cursor/skills/` — setup was documented only in `README`, `INSTALL.md`, `PLAN.md` |

## Gap

The companion stack is **two places** (setup repo + upstream fork). Agents had no **project-scoped skill** describing ports, sync paths, Live2D safety, or optional third-party skill packs.

## What we added (this repo)

| Skill | Purpose |
|-------|---------|
| [ai-companion-stack](../.cursor/skills/ai-companion-stack/SKILL.md) | Ollama + Kokoro + Open-LLM-VTuber + ports; editing `conf.yaml`, `start.sh` |
| [ai-companion-live2d-custom](../.cursor/skills/ai-companion-live2d-custom/SKILL.md) | Syncing `customizations/` into Open-LLM-VTuber, witchZ3, toggle-inject, expression commands |

### Engineering core (third-party rules)

| Source | Location |
|--------|----------|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) `engineering-team/` (converted to Cursor) | [`.cursor/rules/*.mdc`](../.cursor/rules/) — see [README](../.cursor/rules/README.md) |

Plus [claude-skills recommendations](claude-skills-recommendations.md) and **AGENTS.md** at repo root.

## Security note

Never commit API keys, Kokoro tokens, or chat logs. `conf.yaml` in this repo should stay placeholder-only for any cloud keys.
