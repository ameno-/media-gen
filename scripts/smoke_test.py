#!/usr/bin/env python3
"""Local smoke tests for media-gen."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def run(command: list[str], *, allow_failure: bool = False) -> tuple[int, str, str]:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 and not allow_failure:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.returncode, result.stdout, result.stderr


def main() -> int:
    summary: dict[str, object] = {
        "python": sys.version.split()[0],
        "mmx_path": shutil.which("mmx"),
        "dot_path": shutil.which("dot"),
        "ffmpeg_path": shutil.which("ffmpeg"),
        "latex_path": shutil.which("latex"),
        "pdflatex_path": shutil.which("pdflatex"),
        "manim_path": shutil.which("manim"),
        "venv_manim_python": str((REPO_ROOT / ".venv-manim/bin/python")) if (REPO_ROOT / ".venv-manim/bin/python").exists() else "",
        "env_keys_present": {
            "MINIMAX_API_KEY": bool(__import__("os").getenv("MINIMAX_API_KEY")),
            "OPENROUTER_API_KEY": bool(__import__("os").getenv("OPENROUTER_API_KEY")),
            "OPENAI_API_KEY": bool(__import__("os").getenv("OPENAI_API_KEY")),
        },
    }

    for command in (
        ["mmx", "--help"],
        ["mmx", "image", "--help"],
        ["mmx", "music", "generate", "--help"],
        ["mmx", "speech", "synthesize", "--help"],
    ):
        run(command)

    auth_status = run(
        ["mmx", "auth", "status", "--output", "json", "--quiet"],
        allow_failure=True,
    )
    summary["mmx_auth_status_code"] = auth_status[0]

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        promo_dir = run(
            [
                "python3",
                "scripts/build_media_pack.py",
                "--pack",
                "promo",
                "--title",
                "Launch Forge",
                "--brief",
                "Promote a new agent workflow release with cinematic launch assets.",
                "--subject",
                "an orchestration engine",
                "--cta",
                "Try the release",
                "--out-dir",
                str(tmp_path),
            ]
        )[1].strip()
        lesson_dir = run(
            [
                "python3",
                "scripts/build_media_pack.py",
                "--pack",
                "lesson",
                "--title",
                "How Context Routing Works",
                "--brief",
                "Teach the core mechanism of context routing to engineers.",
                "--subject",
                "knowledge flowing through a routing graph",
                "--out-dir",
                str(tmp_path),
            ]
        )[1].strip()

        run(["python3", "scripts/run_pack.py", "--pack-dir", promo_dir, "--dry-run"])
        run(["python3", "scripts/run_pack.py", "--pack-dir", lesson_dir, "--dry-run"])

        summary["promo_pack_dir"] = promo_dir
        summary["lesson_pack_dir"] = lesson_dir
        summary["promo_commands"] = len(
            json.loads((Path(promo_dir) / "commands.json").read_text(encoding="utf-8"))
        )
        summary["lesson_commands"] = len(
            json.loads((Path(lesson_dir) / "commands.json").read_text(encoding="utf-8"))
        )
        summary["lesson_manim_script"] = str(Path(lesson_dir) / "manim" / "script.py")
        summary["promo_module_briefs"] = len(list((Path(promo_dir) / "modules").glob("*.md")))

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
