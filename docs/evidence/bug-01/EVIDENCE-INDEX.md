# Evidence pack — authorized workflow write probe

**Repo:** https://github.com/hosamm12/egy  
**Researcher / owner:** hosamm12  
**Date (UTC):** 2026-08-29  
**Authorization:** Owner-authorized test on own repository. No merge to `main`.  
**Scope:** GitHub Actions workflow file creation via connected agent/GitHub Contents API.

Do **not** merge this branch into `main`. A scheduled workflow with `contents: write` only becomes dangerous on the default branch.

---

## Finding (one sentence)

A connected GitHub session authenticated as the repo owner created `.github/workflows/*.yml` containing `on.schedule` plus `permissions: contents: write` and `pull-requests: write`. The Contents API returned a normal success payload with **no extra confirmation, warning, or distinct status field**.

---

## Primary artifacts (Bug #1 confirmation)

| ID | Artifact | Value |
|---|---|---|
| E1 | Evidence branch | `test/workflow-confirmation-2026` |
| E2 | Closed PR (not merged) | https://github.com/hosamm12/egy/pull/15 |
| E3 | Probe write commit | `af4f9f5f624c7cca55d6be4e877ff58a732e3b3d` @ 2026-08-29T02:11:21Z |
| E4 | File blob SHA | `8a3cf33a0e7a81796198283783348643fd7a2145` |
| E5 | Live file on evidence branch | https://github.com/hosamm12/egy/blob/test/workflow-confirmation-2026/.github/workflows/test-schedule-write-probe.yml |
| E6 | Commit URL | https://github.com/hosamm12/egy/commit/af4f9f5f624c7cca55d6be4e877ff58a732e3b3d |
| E7 | Cleanup delete commit | `3e1fbac76161e1656fec7db360a75d508df80f03` @ 2026-08-29T02:11:56Z |
| E8 | Restore-for-evidence commit | `0fafd8cc352e2f75002cbc804c9e487a0244e4e3` @ 2026-08-29T02:12:40Z |
| E9 | `main` SHA (unchanged) | `aac6844c25b5f05a80f7de008b8a965d07970435` |
| E10 | Authenticated actor | `hosamm12` (uid 213127102), repo `admin` / `push` true |

---

## Step results

### Step 3 — API confirmation signal?

**No.** Distinct confirmation / warning field: **NO**

See `api-response-step3.json`.

### Step 4 — PR permission-aware signal?

**No.** Distinct schedule+write permission flag on the PR object: **NO**

`mergeable_state: blocked` is protected `main` + failed `Vercel – egy` status, not a workflow-permissions warning.

### Step 5 — cleanup vs evidence

PR #15 closed without merge. Probe file restored on this branch only. `main` untouched. Branch kept as evidence.
