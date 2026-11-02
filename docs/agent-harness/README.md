# ChatGPT-first execution harness

Purpose: make the owner's short instruction `Kerjakan task2 selanjutnya itu dengan loop penuh. Kerjakan 5 tugas secara loop itu agar efisien` usable as an intent to run a bounded five-task cycle on this project.

## Triggering
In ordinary ChatGPT Chat, a connected host must resolve active project context and explicitly fetch root AGENTS.md and `.agents/skills/execute-next-batch/SKILL.md` before calling tools. Repo files alone do not automatically run or schedule anything. Codex is optional. No new paid services, daemon, CI workflow or API key is installed.

## Cycle
RESOLVE → INSPECT REAL HEAD/PR/ISSUES/CI → RECONCILE STATE → SELECT ≤5 ELIGIBLE TASKS → EXECUTE + TEST → CHECKPOINT → REPORT. Repeating the exact phrase should move to new tasks based on fresh verified state; never replay unconfirmed side effects.

## State and handoff
Prefer existing project-specific `project-state/` or a canonical ledger on the active branch; docs/agent-harness/state.md is only a bootstrap fallback. After each meaningful task record ID, status (PASS/FAIL/BLOCKED/NOT_RUN), exact SHA, evidence, ownership, blockers and next actions in a reviewable change. If not written, report NOT_SAVED. Avoid duplicate truth ledgers.

## Safety
No implicit merge, deployment, publication, access expansion, credential disclosure or spending. Preserve existing instructions and project conventions. Use plain text fenced trees for hierarchy and reports. A file's existence is not verification of execution or automatic activation.
