# Project-state v2 recovery policy — cv-taste

1. **Preflight** read instructions/state/recovery/evidence; inspect real branch, PRs and exact CI. Main README or an old chat is never live source truth.
2. **Before work** record a bounded attempt with `node scripts/project-state.mjs begin <session-id> <task-id> <expected-head-sha>` when locally available. Without local runtime, agent must explicitly checkpoint through reviewable file updates, not claim CLI ran.
3. **After material work** use `close` with evidence ref and a reported result, refresh current-state, open-tasks, handoff together and push to reviewed branch. Agent reports are NOT independent proof.
4. **After a crashed/no-load chat** read `recover` read-only. If the active execution is non-null, a checkpoint is torn, checkout is stale or side effects are unknown, STOP and inspect Git/PR/CI/device/outbox; never auto retry an ambiguous action.
5. **Concurrency**: local writer lock only; Git remote coordination via non-forced fast-forward push. If rejected or divergent, reconcile rather than force push. Repo JSON is not a distributed transaction ledger.
6. **Evidence/privacy**: link exact source refs and sanitized receipts; do not copy secrets, private source bodies, documents, screenshots or full chat history.
7. **Domain**: Renderer and PDF layout proof; never substitute fictional candidate data for real applicant facts; protect job-application privacy; inspect SKILL.md. No merge, deployment, charged executor, wallet/phone/browser mutation or external publication without explicit scoped approval.
