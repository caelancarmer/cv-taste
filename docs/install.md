# Install the skill

Moved verbatim from `README.md` during the README trim to 100 lines or fewer; the README now links here.

## Install the skill

Clone the repository into the skill directory used by your agent or workspace:

```bash
git clone https://github.com/caelancarmer/cv-taste.git .agents/skills/cv-taste
```

Use your fork’s URL if you maintain a separate copy. Skill discovery varies by agent; installing a directory does not automatically enable it in every session. When using this repository directly as a workspace, `AGENTS.md` points to `SKILL.md`.

If your workspace needs explicit instructions, add:

```text
For CV or resume creation and tailoring, use .agents/skills/cv-taste/SKILL.md
unless the current request selects another style.
```

If the destination already exists, inspect its contents and local changes before updating it. Do not replace unrelated files.

Example request:

> Tailor a CV for this job description using cv-taste. Use the candidate facts I provide and discuss the draft in chat first.
