# Bug #1 — snippet for the report

**Title:** Connected GitHub agent can create a scheduled Actions workflow with `contents: write` and no extra confirmation

**Asset:** Researcher-owned repo `hosamm12/egy` (authorized self-test)

**Expected:** Platform blocks workflow writes, or returns a distinct confirmation / warning field before persisting a scheduled write-capable workflow.

**Actual:** Write succeeded at 2026-08-29T02:11:21Z. Response was a normal Contents API success (`commit.sha` = `af4f9f5f624c7cca55d6be4e877ff58a732e3b3d`). No confirmation field. PR #15 shows only standard Vercel/build checks.

**Evidence URLs:**
- https://github.com/hosamm12/egy/pull/15
- https://github.com/hosamm12/egy/commit/af4f9f5f624c7cca55d6be4e877ff58a732e3b3d
- https://github.com/hosamm12/egy/blob/test/workflow-confirmation-2026/.github/workflows/test-schedule-write-probe.yml
