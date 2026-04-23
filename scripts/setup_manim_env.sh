#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv-manim
.venv-manim/bin/python -m pip install --upgrade pip
.venv-manim/bin/python -m pip install -r requirements-manim.txt

echo "Manim environment ready: $ROOT_DIR/.venv-manim"
