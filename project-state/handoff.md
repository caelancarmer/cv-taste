# Handoff — cv-taste

1. Read root `AGENTS.md`, project-state README, current-state, decisions, tasks, recovery policy and JSON receipts, evidence index.
2. Run `node scripts/project-state.mjs recover` where Node 20+ local checkout exists; otherwise inspect JSON manually.
3. Verify live Git/PR/CI and source revision. Baseline `main@506e8fe3a2e19a101212cdd444053e21a8aaec8e` was only observed 2026-11-02, not an authority about active feature PRs.
4. If active execution is non-null or records disagree, reconcile the original run and remote effects first; never replay an uncertain operation.
5. Complete a bounded, authorized task and commit/push verified checkpoint on a review branch only.

Domain: Public CV/LaTeX toolkit, renderer and portable SKILL.md. Constraint: Renderer and PDF layout proof; never substitute fictional candidate data for real applicant facts; protect job-application privacy; inspect SKILL.md. No merge, deploy, release or spend without approval.
