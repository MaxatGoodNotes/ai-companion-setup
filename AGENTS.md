# AGENTS.md — AI Companion (ai-companion-setup)

## What this repository is

- **Setup guide + config + customization files** for a **local** AI VTuber stack (Ollama + Kokoro + [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber)).
- **Not** the full application source: the Python server and `live2d-models/` assets live in a separate local clone (commonly `~/Documents/open-llm-vtuber`).

## Cursor skills (this repo)

| Skill | Path |
|-------|------|
| Stack & ports | `/.cursor/skills/ai-companion-stack/SKILL.md` |
| Live2D / frontend sync | `/.cursor/skills/ai-companion-live2d-custom/SKILL.md` |

## Cursor rules — Engineering core (third-party)

| Source | Path |
|--------|------|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) `engineering-team/` → Cursor `.mdc` | `.cursor/rules/*.mdc` |

See [`.cursor/rules/README.md`](.cursor/rules/README.md) for commit pin, license, and how to refresh. Rules are **not** always-on (`alwaysApply: false`); enable or @-reference as needed.

## Global meta-skills (user machine)

- **project-bootstrap** — [cursor-master-rules](https://github.com/MaxatGoodNotes/cursor-master-rules) `skills-cursor/project-bootstrap/`

## Third-party skill packs

See [docs/claude-skills-recommendations.md](docs/claude-skills-recommendations.md) for curated picks from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills). Do not bulk-install; audit before trust.

## Secrets

- **Never** commit API keys, tokens, or chat logs. `conf.yaml` uses placeholders for optional cloud keys.

## Install customizations

Follow [customizations/INSTALL.md](customizations/INSTALL.md).
