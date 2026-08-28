#!/usr/bin/env node
/**
 * Safe Build-Time PoC — authorized self-assessment, own assets only.
 *
 * Proves that an npm postinstall lifecycle script can inspect the Vercel
 * managed build environment. No hardcoded variable names: the script
 * classifies purely by name pattern.
 *
 *  - Names matching high-sensitivity patterns (TOKEN/SECRET/PASSWORD/KEY/SALT)
 *    get a masked preview: first 2 + last 2 chars only (proof of readability).
 *  - All other matching names are printed with "(value hidden)".
 *
 * SAFETY:
 *  - No full values are ever printed (max 4 chars per variable, masked).
 *  - No network requests.
 *  - No file access outside the project.
 *  - No authentication attempts against any service.
 */

const PATTERNS = [
  "VERCEL", "DATABASE", "API", "TOKEN", "SECRET",
  "PASSWORD", "AWS", "GITHUB", "OAUTH", "AUTH",
];

// Name patterns that trigger the masked first2+last2 preview.
const HIGH_SENSITIVITY = ["TOKEN", "SECRET", "PASSWORD", "KEY", "SALT"];

function mask(v) {
  if (typeof v !== "string" || v.length === 0) return "(empty)";
  if (v.length <= 4) return "*".repeat(v.length);
  return v.slice(0, 2) + "*".repeat(Math.min(v.length - 4, 40)) + v.slice(-2);
}

const keys = Object.keys(process.env);
const matched = keys.filter((k) =>
  PATTERNS.some((p) => k.toUpperCase().includes(p))
);
const isHigh = (k) =>
  HIGH_SENSITIVITY.some((p) => k.toUpperCase().includes(p));

console.log("=== Safe Build-Time PoC (masked-preview, pattern-based) ===");
console.log("Detected variable names:");

matched.forEach((k) => {
  if (isHigh(k)) {
    console.log(`- ${k}=${mask(process.env[k])}  [masked: first2+last2 only]`);
  } else {
    console.log(`- ${k} (value hidden)`);
  }
});

console.log("---");
matched.forEach((k) => console.log(`${k}_PRESENT=true`));
console.log(`TOTAL_MATCHING_VARIABLES=${matched.length}`);
console.log(`MASKED_PREVIEW_COUNT=${matched.filter(isHigh).length}`);
console.log(`TOTAL_ENV_VARIABLES=${keys.length}`);
console.log("NETWORK_REQUESTS=0");
console.log("No full values displayed. No network requests.");
