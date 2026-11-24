# CV work

## Scope
This repository is for CV or resume creation and tailoring.
Read `SKILL.md` first, and use the supporting files under `assets/` and the renderer under `scripts/`.

## Canonical read order
1. This file (`AGENTS.md`).
2. `SKILL.md`.
3. `docs/publication.md`.
4. `assets/style.tex` and the renderer under `scripts/`.

## Inviolable rules
1. Preserve the Latin Modern Roman typography and layout unless the current request selects another style. Tailor content to the current role and supplied facts.
2. The reference candidate, organizations, and achievements are fictional examples; never use them as facts about a real applicant.
3. Follow the candidate-data rule in `SKILL.md` and publication guidance in `docs/publication.md`.
4. Respect current instructions and established authorization. Discuss a draft in chat when requested. Use the requested delivery channel; Notion delivery is optional and requires an authorized destination. Do not submit applications or contact recruiters without explicit instruction.
5. Keep changes small and readable. Reuse `assets/style.tex` instead of duplicating layout settings. Use Python's standard library where adequate; add a dependency only for a demonstrated need.
6. Run the renderer tests after renderer changes and inspect the rendered reference after layout changes. Tests should exercise actual failure cases rather than repeat implementation details. Never claim a check was performed unless its result was inspected.
7. Do not write scores or self-assessments; use inspected tool output as evidence. Every field in a generated report must be computed from the artifact.
8. Error messages must include the underlying cause.
9. State each rule or value once and reference it elsewhere.
10. Tests that need an external tool must skip with a clear reason when it is absent.

## Docs pointers
- `SKILL.md` — CV and resume creation and tailoring, including the candidate-data rule.
- `docs/publication.md` — Publication guidance.
- `assets/` — Supporting files.
- `assets/style.tex` — Layout settings to reuse.
- `scripts/` — Renderer.
