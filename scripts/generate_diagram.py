#!/usr/bin/env python3
"""Generate and render a Graphviz diagram for a media pack."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


PALETTE = {
    "bg": "#0f172a",
    "panel": "#12141A",
    "primary": "#22d3ee",
    "secondary": "#34d399",
    "accent": "#fbbf24",
    "muted": "#94a3b8",
    "ink": "#EAEAEA",
}


def dot_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _node_attrs(color: str, penwidth: float = 1.5, fontsize: int = 12) -> str:
    p = PALETTE
    return (
        f'color="{color}", fillcolor="{p["panel"]}", penwidth={penwidth}, '
        f'fontsize={fontsize}, fontcolor="{p["ink"]}"'
    )


def make_architecture_dot(title: str, subject: str) -> str:
    p = PALETTE
    t = dot_escape(title)
    s = dot_escape(subject)
    return f"""\
digraph architecture {{
    graph [
        bgcolor="{p["bg"]}",
        fontname="Menlo",
        fontsize=13,
        fontcolor="{p["ink"]}",
        pad=0.6,
        splines=ortho,
        rankdir=LR,
        label="{t}",
        labelloc=t,
    ]
    node [
        shape=box,
        style="filled,rounded",
        fillcolor="{p["panel"]}",
        fontname="Menlo",
        fontsize=12,
        fontcolor="{p["ink"]}",
        color="{p["primary"]}",
        penwidth=1.5,
        margin="0.25,0.15",
    ]
    edge [
        color="{p["muted"]}",
        fontname="Menlo",
        fontsize=10,
        fontcolor="{p["muted"]}",
        arrowsize=0.85,
    ]

    INPUT [{_node_attrs(p["primary"], 2.0)}  label="Input"]
    CORE  [{_node_attrs(p["accent"],  2.5, 13)} label="{s}"]
    OUT_A [{_node_attrs(p["secondary"], 2.0)} label="Outcome A"]
    OUT_B [{_node_attrs(p["secondary"], 2.0)} label="Outcome B"]

    INPUT -> CORE
    CORE  -> OUT_A
    CORE  -> OUT_B
}}
"""


def make_concept_flow_dot(title: str, subject: str) -> str:
    p = PALETTE
    t = dot_escape(title)
    s = dot_escape(subject)
    return f"""\
digraph concept_flow {{
    graph [
        bgcolor="{p["bg"]}",
        fontname="Menlo",
        fontsize=13,
        fontcolor="{p["ink"]}",
        pad=0.6,
        splines=ortho,
        rankdir=TD,
        label="{t}",
        labelloc=t,
    ]
    node [
        shape=box,
        style="filled,rounded",
        fillcolor="{p["panel"]}",
        fontname="Menlo",
        fontsize=12,
        fontcolor="{p["ink"]}",
        color="{p["primary"]}",
        penwidth=1.5,
        margin="0.25,0.15",
    ]
    edge [
        color="{p["muted"]}",
        fontname="Menlo",
        fontsize=10,
        fontcolor="{p["muted"]}",
        arrowsize=0.85,
    ]

    Q [{_node_attrs(p["primary"], 2.0)}  label="The Question"]
    M [{_node_attrs(p["accent"],  2.5, 13)} label="{s}"]
    R [{_node_attrs(p["secondary"], 2.0)} label="The Takeaway"]

    Q -> M [label="leads to"]
    M -> R [label="reveals"]
}}
"""


def generate_dot_source(pack_type: str, title: str, subject: str) -> str:
    if pack_type == "promo":
        return make_architecture_dot(title, subject)
    return make_concept_flow_dot(title, subject)


def render_dot(dot_path: Path, output_dir: Path) -> tuple[Path, Path]:
    dot_bin = shutil.which("dot")
    if not dot_bin:
        raise SystemExit("Graphviz 'dot' not found. Install via: brew install graphviz")
    svg_path = output_dir / "diagram.svg"
    png_path = output_dir / "diagram.png"
    for fmt, out in [("svg", svg_path), ("png", png_path)]:
        result = subprocess.run(
            [dot_bin, f"-T{fmt}", str(dot_path), "-o", str(out)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise SystemExit(f"dot render failed ({fmt}): {result.stderr.strip()}")
    return svg_path, png_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Graphviz diagram for a media pack.")
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="Skip DOT generation; render the existing diagrams/diagram.dot.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pack_dir = Path(args.pack_dir).resolve()
    brief = json.loads((pack_dir / "brief.json").read_text(encoding="utf-8"))

    diagrams_dir = pack_dir / "diagrams"
    outputs_dir = pack_dir / "outputs"
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    dot_path = diagrams_dir / "diagram.dot"

    if not args.render_only:
        dot_src = generate_dot_source(
            pack_type=str(brief["pack"]),
            title=str(brief["title"]),
            subject=str(brief["subject"]),
        )
        dot_path.write_text(dot_src, encoding="utf-8")

    if not dot_path.exists():
        raise SystemExit(f"DOT source not found: {dot_path}")

    svg_path, _ = render_dot(dot_path, outputs_dir)
    print(svg_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
