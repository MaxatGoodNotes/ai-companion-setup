# Project Bootstrap — Reference

## Cursor paths (macOS)

| Item | Path |
|------|------|
| User global rules | `~/.cursor/rules/*.mdc` |
| User skills | `~/.cursor/skills/<name>/SKILL.md` |
| Project rules | `<repo>/.cursor/rules/*.mdc` |
| Project skills | `<repo>/.cursor/skills/<name>/SKILL.md` |

Do not write into `~/.cursor/skills-cursor/` (reserved for Cursor).

---

## claude-skills — selective domain mapping

Source: [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (MIT). Counts and names may change; verify on the repo.

Use this table to **pick domains**, not to install everything.

| User intent | Start with these upstream folders |
|-------------|-----------------------------------|
| Backend / APIs / Lambdas | `engineering/`, `engineering-team/` |
| Frontend / fullstack | `engineering-team/` (frontend, a11y) |
| DevOps / CI / K8s | `engineering/` (ci-cd, helm, terraform) |
| Product / PM / discovery | `product-team/` |
| Marketing / content | `marketing-skill/` |
| Compliance / quality (medical, ISO) | `ra-qm-team/` |
| Exec / strategy decks | `c-level-advisor/` |
| Finance / SaaS metrics | `finance/` |

**Cursor install** (from upstream docs): clone repo, then:

```bash
./scripts/convert.sh --tool cursor
./scripts/install.sh --tool cursor --target /path/to/your/project
```

Use `--force` only if you understand it will overwrite. Prefer **pinning** a git SHA in your notes when reproducibility matters.

---

## Security audit — practical commands

**Repo content (quick):**

```bash
git grep -nEi 'api_key|apikey|secret|password|token|ghp_|gho_|xox[baprs]-|sk-[a-zA-Z0-9]{10,}|BEGIN (RSA |OPENSSH )?PRIVATE'
```

**Python skill scripts** (if present under project):

```bash
# Review for subprocess/shell/eval/urllib without pinning
grep -R -nE 'eval\(|exec\(|subprocess|os\.system|urllib\.request|socket\.connect' --include='*.py' .
```

Upstream publishes a **skill-security-auditor** in that ecosystem; if you clone claude-skills, you can run their script against a skill folder before merging into your project. See upstream `engineering/skill-security-auditor/` and [SECURITY.md](https://github.com/alirezarezvani/claude-skills/blob/main/SECURITY.md) in the repo.

---

## Professional vs personal (quick)

| Topic | Personal | Professional |
|-------|----------|--------------|
| Default GitHub visibility | User choice; private common | Private + org policy |
| PII in examples | Avoid real data | Forbidden (candidates, customers) |
| License | User choice | Legal / OSS office approval |
| AI rules in repo | Optional | Often required for team alignment |

---

## gh CLI reminders

```bash
gh auth status
gh repo create --help
gh repo view --web
```

Use HTTPS or SSH remotes per user preference; do not commit deploy keys.
