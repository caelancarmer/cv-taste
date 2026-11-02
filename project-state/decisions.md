# Decisions — cv-taste

## D-001 — per-repo crash-safe handoff v2
- recorded-on: 2026-11-02
- source: owner direction to adopt adaptive V2 in every caelancarmer repository
- decision: checkpoint/recovery/session records belong locally to this repository; no global shared state replaces original Git/PR/CI truth.
- implementation: review branch only, bootstrap status BASELINE-ONLY; no automatic merge or runtime integration inferred.

## D-002 — domain-specific safety
- observed-source: repository root/README and metadata, 2026-11-02
- invariant: Renderer and PDF layout proof; never substitute fictional candidate data for real applicant facts; protect job-application privacy; inspect SKILL.md.
