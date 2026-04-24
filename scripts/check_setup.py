#!/usr/bin/env python3
"""Check local media-gen dependencies and env configuration."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def command_exists(name: str) -> str:
    return shutil.which(name) or ""


def run_version(command: list[str]) -> dict[str, object]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return {
        "command": " ".join(command),
        "code": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main() -> int:
    manim_python = os.getenv("MANIM_PYTHON_BIN") or str(REPO_ROOT / ".venv-manim/bin/python")
    summary = {
        "commands": {
            "brew": command_exists("brew"),
            "dot": command_exists("dot"),
            "ffmpeg": command_exists("ffmpeg"),
            "latex": command_exists("latex"),
            "pdflatex": command_exists("pdflatex"),
            "mmx": command_exists("mmx"),
        },
        "python_envs": {
            "manim_python": manim_python if Path(manim_python).exists() else "",
        },
        "env_keys_present": {
            "MINIMAX_API_KEY": bool(os.getenv("MINIMAX_API_KEY")),
            "OPENROUTER_API_KEY": bool(os.getenv("OPENROUTER_API_KEY")),
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
        },
        "media_defaults": {
            "MEDIA_GEN_OUTPUT_DIR": os.getenv("MEDIA_GEN_OUTPUT_DIR", ""),
            "MEDIA_GEN_MINIMAX_VOICE": os.getenv("MEDIA_GEN_MINIMAX_VOICE", ""),
            "MANIM_PYTHON_BIN": os.getenv("MANIM_PYTHON_BIN", ""),
        },
    }

    if command_exists("mmx"):
        summary["mmx_auth"] = run_version(["mmx", "auth", "status", "--output", "json", "--quiet"])
    if Path(manim_python).exists():
        summary["manim_version"] = run_version([manim_python, "-m", "manim", "--version"])

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
