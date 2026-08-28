#!/usr/bin/env node
// Test 5 marker: proves lifecycle execution by failing install intentionally.
// Harmless: no env access, no network, no fs.
console.log("TEST_LIFECYCLE_EXECUTED=true");
process.exit(1);
