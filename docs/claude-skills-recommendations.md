# Curated [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) picks for AI Companion

Upstream is a large MIT library (200+ skills, multi-tool conversion including Cursor). **Do not bulk-install** all converted `.mdc` rules — token noise and conflicting instructions. Use **selective** install after `git clone` + `./scripts/convert.sh --tool cursor`, or install **domain bundles** via the upstream README.

## High value for this project (personal AI + local stack)

| Domain / skill (upstream) | Why |
|---------------------------|-----|
| **engineering-team** (core) | Python/FastAPI-adjacent patterns, general engineering hygiene when patching `open-llm-vtuber` |
| **engineering** (POWERFUL) **performance-profiler** | Latency matters (voice pipeline); profiling Python/frontend when tuning |
| **engineering** **mcp-server-builder** | If you add MCP tools to the companion stack |
| **engineering** **ci-cd-pipeline-builder** | If you add CI for a fork or private mirror |
| **engineering** **skill-security-auditor** | Run on **any** third-party skill folder before merging into `.cursor/rules/` |
| **product-team** (light) | PRDs, experiment design — if you treat the companion as a product |
| **engineering-team** **playwright-pro** | Only if you automate browser tests against `localhost:12393` |

## Skip or low priority (for now)

| Domain | Why skip |
|--------|----------|
| **marketing-skill** (full) | Unless you ship a public landing page for the project |
| **ra-qm-team** | Medical/regulatory — not applicable unless you pivot use case |
| **c-level-advisor** | Unless you want exec-style memos about roadmap |

## Install pattern (safe)

1. Clone upstream at a **pinned commit** (reproducible).
2. Run `./scripts/convert.sh --tool cursor` (per [upstream README](https://github.com/alirezarezvani/claude-skills)).
3. **Cherry-pick** specific converted rules into `open-llm-vtuber/.cursor/rules/` or a **staging** folder — not 150 files at once.
4. Run upstream’s **skill-security-auditor** on any skill with `scripts/` before trusting:

   `python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/`

5. Document what you installed in the project `README` or `AGENTS.md`.

## Personas (optional)

Upstream [personas](https://github.com/alirezarezvani/claude-skills/tree/main/agents/personas) (e.g. **solo-founder**) can help multi-phase “build → ship” thinking; they are **orthogonal** to the local VTuber stack — use when you want product-style planning, not for Live2D parameter tuning.
