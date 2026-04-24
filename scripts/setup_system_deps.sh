#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required for system dependency setup."
  exit 1
fi

brew bundle --file Brewfile

echo "System dependencies ready."
