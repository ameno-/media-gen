#!/usr/bin/env python3
"""Run or dry-run a generated media pack."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandRecord:
    name: str
    kind: str
    prompt_path: str
    output_path: str
    command: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run or dry-run generated media pack commands.")
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", nargs="*", default=[])
    return parser.parse_args()


def load_commands(pack_dir: Path) -> list[CommandRecord]:
    data = json.loads((pack_dir / "commands.json").read_text(encoding="utf-8"))
    return [CommandRecord(**item) for item in data]


def main() -> int:
    args = parse_args()
    commands = load_commands(Path(args.pack_dir))
    if args.only:
        allowed = set(args.only)
        commands = [command for command in commands if command.name in allowed]
    if not commands:
        raise SystemExit("No commands selected.")

    failures = 0
    for command in commands:
        rendered = " ".join(shlex.quote(part) for part in command.command)
        print(f"[{command.kind}] {command.name}")
        print(rendered)
        if args.dry_run:
            continue
        result = subprocess.run(command.command, check=False)
        if result.returncode != 0:
            failures += 1
            print(f"FAILED: {command.name} ({result.returncode})")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
