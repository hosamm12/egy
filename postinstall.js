#!/usr/bin/env node
// TEST R2 2026-08-28 — lifecycle execution detector (authorized self-assessment, own assets only)
// .npmrc ignore-scripts=true is still present at this commit -> script must be SKIPPED if the control holds.
console.log("TEST_LIFECYCLE_EXECUTED_R2_2026-08-28=true");
process.exit(1);
