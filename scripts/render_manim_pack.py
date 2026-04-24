#!/usr/bin/env python3
"""Render or mux the Manim portion of a generated media pack."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


QUALITY_FLAGS = {
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Manim pack and optionally mux audio.")
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument("--quality", choices=sorted(QUALITY_FLAGS), default="low")
    parser.add_argument("--manim-python", default="")
    parser.add_argument("--mux-only", action="store_true")
    parser.add_argument("--render-only", action="store_true")
    return parser.parse_args()


def detect_python(explicit: str) -> str:
    if explicit:
        return explicit
    env_python = os.getenv("MANIM_PYTHON_BIN", "")
    if env_python and Path(env_python).exists():
        return env_python
    candidate = REPO_ROOT / ".venv-manim/bin/python"
    if candidate.exists():
        return str(candidate)
    return "python3"


def load_brief(pack_dir: Path) -> dict[str, object]:
    return json.loads((pack_dir / "brief.json").read_text(encoding="utf-8"))


def scene_names(pack_type: str, pack_dir: Path | None = None) -> list[str]:
    if pack_dir is not None:
        json_path = pack_dir / "manim" / "scenes.json"
        txt_path = pack_dir / "manim" / "scenes.txt"
        if json_path.exists():
            data = json.loads(json_path.read_text(encoding="utf-8"))
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return data
        if txt_path.exists():
            names = [line.strip() for line in txt_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if names:
                return names
    if pack_type == "promo":
        return ["Scene1Promise", "Scene2Mechanism", "Scene3CallToAction"]
    return ["Scene1Question", "Scene2Mechanism", "Scene3Recap"]


def ensure_command(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Missing required command: {name}")


def run(command: list[str], cwd: Path) -> None:
    print(" ".join(command))
    result = subprocess.run(command, cwd=cwd, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def render(pack_dir: Path, python_bin: str, quality: str) -> Path:
    brief = load_brief(pack_dir)
    pack_type = str(brief["pack"])
    manim_dir = pack_dir / "manim"
    renders_dir = manim_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    script_path = manim_dir / "script.py"
    for scene in scene_names(pack_type, pack_dir):
        run(
            [
                python_bin,
                "-m",
                "manim",
                QUALITY_FLAGS[quality],
                "--media_dir",
                str(manim_dir / "media"),
                "--output_file",
                scene,
                str(script_path),
                scene,
            ],
            cwd=manim_dir,
        )
        source = next((manim_dir / "media").rglob(f"{scene}.mp4"), None)
        if source is None:
            raise SystemExit(f"Rendered file for {scene} not found.")
        target = renders_dir / f"{scene}.mp4"
        target.write_bytes(source.read_bytes())
    return renders_dir


def mux(pack_dir: Path) -> Path:
    ensure_command("ffmpeg")
    manim_dir = pack_dir / "manim"
    concat_path = manim_dir / "concat.txt"
    final_video = pack_dir / "outputs" / "video.mp4"
    with_audio = pack_dir / "outputs" / "video-with-audio.mp4"
    soundtrack = pack_dir / "outputs" / "soundtrack.mp3"
    narration = pack_dir / "outputs" / "narration.mp3"

    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-c",
            "copy",
            str(final_video),
        ],
        cwd=manim_dir,
    )

    audio_inputs: list[str] = []
    filter_complex = ""
    if narration.exists() and soundtrack.exists():
        audio_inputs = ["-i", str(narration), "-i", str(soundtrack)]
        filter_complex = "[2:a]volume=0.25[music];[1:a][music]amix=inputs=2:duration=longest[aout]"
    elif narration.exists():
        audio_inputs = ["-i", str(narration)]
    elif soundtrack.exists():
        audio_inputs = ["-i", str(soundtrack)]

    if not audio_inputs:
        return final_video

    command = ["ffmpeg", "-y", "-i", str(final_video), *audio_inputs]
    if filter_complex:
        command.extend(["-filter_complex", filter_complex, "-map", "0:v:0", "-map", "[aout]"])
    else:
        command.extend(["-map", "0:v:0", "-map", "1:a:0"])
    command.extend(["-shortest", "-c:v", "copy", str(with_audio)])
    run(command, cwd=pack_dir)
    return with_audio


def main() -> int:
    args = parse_args()
    pack_dir = Path(args.pack_dir).resolve()
    python_bin = detect_python(args.manim_python)
    if not args.mux_only:
        render(pack_dir, python_bin, args.quality)
    if not args.render_only:
        mux(pack_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
