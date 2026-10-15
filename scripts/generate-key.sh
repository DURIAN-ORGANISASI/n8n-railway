#!/usr/bin/env sh
set -eu
if ! command -v openssl >/dev/null 2>&1; then
  echo "OpenSSL is required. Install it or use scripts/generate-key.ps1 on Windows." >&2
  exit 1
fi
openssl rand -hex 32
