# project-state v2 — cv-taste

Repository-owned adaptive session and crash-recovery checkpoint (not central, not full chat replay). This repository's owner/source and domain rules always take precedence over a generic helper. Read AGENTS.md → current-state.md → decisions.md → open-tasks.md → handoff.md → recovery/recovery-policy.md → recovery JSON → sessions/session-index.json → evidence index → actual source/CI/PRs.

## Local Node 20+ commands (no network)
- `node scripts/project-state.mjs verify`: validates structural consistency, not source truth.
- `node scripts/project-state.mjs recover`: read-only advisory; never automatic replay.
- `node scripts/project-state.mjs begin <session-id> <task-id> <full-checkout-sha>`: create bounded active attempt before task.
- `node scripts/project-state.mjs close <reported-pass|failed|blocked|unknown> <evidence-ref>`: write an agent-reported checkpoint, not independently verified PASS.
- `node scripts/check-project-state.mjs`: compatibility structural entrypoint.

A crash may leave JSON partially updated, while Git checkout may be stale; on disagreement stop and reconcile. Local lock prevents simultaneous writers only within one checkout. Remote Git pushes must not overwrite newer refs and must never be forced. Update current-state, open-tasks and handoff together after each meaningful task. Archive large evidence in its original canonical location and link only sanitized immutable references here. No raw secrets, personal media, full transcripts or device data. Review PRs/CI before declaring a task complete.

## Repository adaptation
Public CV/LaTeX toolkit, renderer and portable SKILL.md.
Renderer and PDF layout proof; never substitute fictional candidate data for real applicant facts; protect job-application privacy; inspect SKILL.md.
