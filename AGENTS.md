# CV work

For CV or resume creation and tailoring in this repository, read `SKILL.md`.
Use the supporting files under `assets/` and the renderer under `scripts/`.

Preserve the Latin Modern Roman typography and layout unless the current request
selects another style. Tailor content to the current role and supplied facts.
The reference candidate, organizations, and achievements are fictional examples.
Never use them as facts about a real applicant.

Follow the candidate-data rule in `SKILL.md` and publication guidance in `docs/publication.md`.

Respect current instructions and established authorization. Discuss a draft in
chat when requested. Use the requested delivery channel; Notion delivery is
optional and requires an authorized destination. Do not submit applications or
contact recruiters without explicit instruction.

Keep changes small and readable. Reuse `assets/style.tex` instead of duplicating
layout settings. Use Python's standard library where adequate; add a dependency
only for a demonstrated need. Run the renderer tests after renderer changes and
inspect the rendered reference after layout changes. Tests should exercise actual
failure cases rather than repeat implementation details. Never claim a check was
performed unless its result was inspected.

Do not write scores or self-assessments; use inspected tool output as evidence.
Every field in a generated report must be computed from the artifact.
Error messages must include the underlying cause.
State each rule or value once and reference it elsewhere.
Tests that need an external tool must skip with a clear reason when it is absent.

## Project-state v2 preflight (mandatory)
At every agent session, batch, handoff, or chat-load failure read `project-state/README.md`, `current-state.md`, `decisions.md`, `open-tasks.md`, `handoff.md`, recovery policy + JSON and evidence index; inspect live Git, current PR/CI and source evidence. Node 20+ local checkouts: `node scripts/project-state.mjs verify` then `recover`; `begin` before material execution and `close` after a bounded task. Status `reported-pass` is not independent verification. If active execution or a torn checkpoint is discovered: STOP, reconcile real side effects, never auto-replay. Update all three state markdown files together and push only to review branches; no forced push, auto merge, deploy, cost or secrets. Existing more-specific instructions still apply. Focus: Renderer and PDF layout proof; never substitute fictional candidate data for real applicant facts; protect job-application privacy; inspect SKILL.md. This file alone cannot force external hosts to comply.
