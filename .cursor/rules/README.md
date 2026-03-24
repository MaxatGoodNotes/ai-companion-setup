# Engineering core — Cursor rules (third-party)

These `.mdc` files are the **`engineering-team/`** bundle from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), converted with `./scripts/convert.sh --tool cursor`.

| Field | Value |
|-------|--------|
| **Upstream commit** | `17228eff68e215404c25de5ca671f50aa5d46170` |
| **License** | MIT (see upstream [LICENSE](https://github.com/alirezarezvani/claude-skills/blob/main/LICENSE)) |
| **Count** | 26 rules (full `engineering-team` set) |

**Scripts:** Many skills reference `scripts/` under the upstream repo path `engineering-team/<skill-name>/`. Run those from a cloned [claude-skills](https://github.com/alirezarezvani/claude-skills) checkout if you need the Python helpers; they are **not** vendored here.

**Update:** Re-clone upstream, run `convert.sh --tool cursor`, then copy only `integrations/cursor/rules/<name>.mdc` for the skills you want.
