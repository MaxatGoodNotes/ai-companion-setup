---
name: project-bootstrap
description: >-
  Bootstraps new personal or professional software projects end-to-end: intake,
  repo creation, Cursor rules, optional skill packs from alirezarezvani/claude-skills,
  and a security gate before first push. Use when the user says new project,
  bootstrap, scaffold repo, greenfield, or wants to create a project from scratch.
---

# Project Bootstrap (Meta Skill)

Orchestrates **project creation for any stack**, distinguishing **personal** vs **professional** guardrails. The agent follows this playbook; the human approves irreversible steps (GitHub visibility, org policy).

## Principles

1. **Default secure**: private repo unless the user explicitly wants public; no secrets in git; `.gitignore` before first commit.
2. **Minimum viable structure**: README, license choice, `.gitignore`, optional `AGENTS.md` / `CONTRIBUTING.md` when the project will have collaborators.
3. **Rules are layered**: user global rules → project rules → optional third-party skill packs (audited).
4. **Professional projects**: stricter secrets, no candidate/customer PII in examples, align with employer policies; **personal**: still no secrets in repo, but fewer compliance artifacts unless the user wants them.

---

## Phase 0 — Classify and intake

Ask the user (or infer from context) and record in a short **Project Brief** (paste into README or `docs/PROJECT_BRIEF.md`):

| Question | Why |
|----------|-----|
| **Personal or professional?** | Drives compliance, naming, visibility defaults. |
| **One-line purpose** | Aligns folder name and README title. |
| **Primary language / runtime** | Drives `.gitignore`, CI template, linter choice. |
| **License** | MIT default for personal OSS; employer may require proprietary / internal-only. |
| **GitHub: org or user, public/private?** | `gh repo create` flags. |
| **Will this handle sensitive data?** | If yes: add security checklist, encryption, secrets manager story — do not store real secrets in repo. |
| **Cursor: copy global rules into project?** | See Phase 4. |

If **professional** and the repo is employer-related: remind the user of **internal policies** (allowed licenses, required security review, data classification). Do not assume public GitHub is allowed.

---

## Phase 1 — Filesystem scaffold

1. Choose a **folder name** (lowercase, hyphens, e.g. `my-service`).
2. Create the directory (or workspace root if already open).
3. Add **minimum files**:
   - `README.md` — title, purpose, setup stub, link to Project Brief if used.
   - `.gitignore` — language-appropriate (Node, Python, Go, etc.); always include `.env`, `.env.*`, `*.pem`, OS junk (`.DS_Store`).
   - `LICENSE` — only if open-source intent confirmed; else omit or use org template.
4. Optional but recommended:
   - `AGENTS.md` — how AI assistants should work in this repo (stack, test command, deploy).
   - `.editorconfig` — if multi-editor team.

Do **not** commit secrets or real API keys. Use `.env.example` with placeholder values only.

---

## Phase 2 — Git initialization

```bash
cd /path/to/project
git init
git add .
git status   # verify no secrets / no giant artifacts
git commit -m "chore: initial project scaffold"
```

If the user already has commits, skip `git init` and work from current history.

---

## Phase 3 — GitHub repository

Use **`gh` CLI** (authenticated). Never embed tokens in commands.

```bash
# Default: private, user account (adjust --org if needed)
gh repo create <repo-name> --private --source=. --remote=origin --push
```

If the user wants **public**:

```bash
gh repo create <repo-name> --public --source=. --remote=origin --push
```

If `origin` exists, use `git remote -v` and `git push -u origin main` (or `master` — detect default branch).

**Professional**: prefer **private** repos under org; confirm with user before `--public`.

---

## Phase 4 — Cursor rules (global + project)

### 4a User global rules (reference)

Typical location on macOS: `~/.cursor/rules/*.mdc`. These apply across workspaces when `alwaysApply: true` or when globs match.

**Do not blindly duplicate** every global rule into the repo (duplication drifts). Options:

- **Link in AGENTS.md**: “Global rules live in `~/.cursor/rules/`; clone this machine’s setup for new devs.”
- **Copy selectively**: copy only rules that must travel with the repo (e.g. team conventions). Rename to `.cursor/rules/*.mdc` in the project.

### 4b Project rules

Create `.cursor/rules/` when team-shared conventions are needed:

```text
.cursor/rules/
  project-conventions.mdc   # globs or alwaysApply as appropriate
```

See [reference.md](reference.md) for suggested globs.

---

## Phase 5 — Optional: skill packs from `claude-skills`

Upstream catalog: **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** — large MIT-licensed library of skills with multi-tool conversion (including Cursor as `.mdc` rules).

### 5a Do not bulk-install everything

Installing **all** converted rules creates noise, token bloat, and conflicting instructions. Instead:

1. Read the user’s **Project Brief** and map **domains** → **folders** in that repo (engineering, product-team, marketing-skill, etc.).
2. Prefer **official install path** from upstream: clone repo, run `./scripts/convert.sh --tool cursor`, then `./scripts/install.sh --tool cursor --target /path/to/project` **only after** the user confirms scope (or cherry-pick specific skill folders into `.cursor/rules/` manually).
3. Document what was installed in `README.md` under “AI / Cursor conventions”.

### 5b Security before trusting upstream skills

Treat third-party skill content like **untrusted code**:

- Prefer installing from a **pinned commit** or release tag.
- Run a **security pass** (Phase 6) on any downloaded `scripts/` under the project.
- Optionally use upstream’s **skill-security-auditor** concept: static scan for injection / exfiltration patterns (see [reference.md](reference.md)).

---

## Phase 6 — Security audit (gate before “done”)

Complete before declaring bootstrap finished:

1. **Secrets scan**: `git grep -iE 'api_key|secret|password|BEGIN PRIVATE|ghp_|sk-'` (and fix or remove hits).
2. **Files**: no `.env` committed; `.env.example` only with placeholders.
3. **Dependencies**: if `package.json` / `requirements.txt` / `go.mod` exists — plan for `npm audit` / `pip audit` / govulncheck in CI later.
4. **Third-party skills/scripts**: if copied from claude-skills or elsewhere, read `scripts/*.py` for network calls, `eval`, `exec`, shelling out with user input.
5. **Professional / PII**: no customer or candidate data in fixtures, screenshots, or logs in repo.

Record a short **Security checklist** section in README or `docs/SECURITY.md` for professional projects.

---

## Phase 7 — Handoff

Deliver to the user:

- Repo URL (`gh repo view --web` or printed HTTPS URL).
- What was created (files, rules, skill packs).
- Next steps: install deps, CI template, branch protection (org), Dependabot.

---

## When to stop and ask the human

- Creating a repo under an **employer org** without confirmation.
- **Public** repo with license or IP concerns.
- Running **unreviewed** install scripts from the internet with elevated permissions.
- Any request that would **paste secrets** into the repo or chat.

---

## Related files

- [reference.md](reference.md) — domain → claude-skills mapping, audit commands, Cursor paths.
- [README.md](README.md) — human-facing summary in the companion-setup repo.
