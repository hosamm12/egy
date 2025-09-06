#!/usr/bin/env bash
set -euo pipefail
echo "🔍 Local Deep Scan - $(date)"

# Install deps (Ubuntu/Codespaces)
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y jq
fi

# Gitleaks via docker (portable)
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found; skipping docker-based gitleaks."
else
  docker run --rm -v "$PWD":/repo zricethezav/gitleaks:latest \
    detect --source=/repo --no-git --report-format json --report-path /repo/gitleaks.local.json --exit-code 1 \
    || echo "[!] Gitleaks found secrets (exit non-zero)"
fi

# Node deps scan (if package.json)
if [ -f package.json ]; then
  if ! command -v npm >/dev/null 2>&1; then
    echo "npm not found; skip npm audit"
  else
    npm audit --audit-level=high || true
  fi
fi

# Repo fingerprint
find . -type f -not -path "./.git/*" -print0 | sort -z | xargs -0 shasum -a 256 | shasum -a 256 | awk '{print $1}' > repo.local.hash
echo "Repo hash: $(cat repo.local.hash)"

echo "✅ Local scan done."
