console.log("=== Safe Build-Time PoC ===");
// Authorized self-assessment on own assets only.
// Safety: prints variable NAMES only. No values. No network. No file access outside project.
const p = ["VERCEL", "DATABASE", "API", "TOKEN", "SECRET", "PASSWORD", "AWS", "GITHUB", "OAUTH", "AUTH"];
const f = Object.keys(process.env).filter(k => p.some(x => k.toUpperCase().includes(x)));
console.log("Detected variable names:");
f.forEach(k => console.log("- " + k + " (value hidden)"));
console.log("---");
f.forEach(k => console.log(k + "_PRESENT=true"));
console.log("TOTAL_MATCHING_VARIABLES=" + f.length);
console.log("Total:", Object.keys(process.env).length);
console.log("NETWORK_REQUESTS=0");
console.log("No values displayed. No network requests.");
