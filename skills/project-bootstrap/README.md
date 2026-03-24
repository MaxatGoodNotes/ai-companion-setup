# project-bootstrap (Cursor meta skill)

End-to-end playbook for **creating new repositories** with sensible defaults, **Cursor rules**, optional **[claude-skills](https://github.com/alirezarezvani/claude-skills)** integration, and a **security gate**.

## Install (personal)

Copy the folder to your user skills:

```bash
mkdir -p ~/.cursor/skills
cp -R skills/project-bootstrap ~/.cursor/skills/project-bootstrap
```

Or symlink:

```bash
ln -s "$(pwd)/skills/project-bootstrap" ~/.cursor/skills/project-bootstrap
```

Restart Cursor or reload skills if needed.

## Install (team / project)

Copy into a repo:

```bash
cp -R skills/project-bootstrap .cursor/skills/project-bootstrap
```

Commit `.cursor/skills/` so teammates get the same playbook.

## Trigger phrases

- “Bootstrap a new project”
- “Create a repo with Cursor rules and security check”
- “New greenfield — personal” / “professional”

## What it does not do

- Replace your employer’s security review process.
- Automatically install all third-party skills without human confirmation.
- Store secrets in the repository.

## License

Same as the parent [ai-companion-setup](https://github.com/MaxatGoodNotes/ai-companion-setup) repository.
