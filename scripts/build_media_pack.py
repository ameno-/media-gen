#!/usr/bin/env python3
"""Build a repeatable media pack from a short brief."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path


SLUG_RE = re.compile(r"[^a-z0-9]+")
MONO_FONT = "Menlo"
VISUAL_SYSTEM_REF = "docs/VISUAL-SYSTEM.md"

DIAGRAM_PALETTE = {
    "bg": "#0f172a",
    "panel": "#12141A",
    "primary": "#22d3ee",
    "secondary": "#34d399",
    "accent": "#fbbf24",
    "muted": "#94a3b8",
    "ink": "#EAEAEA",
}


STYLE_LIBRARY = {
    "B1": {
        "name": "The Gilded Mechanism",
        "frame": (
            "A single massive brass gear, thirty meters wide, suspended above dark teal water "
            "at twilight. {subject} integrated subtly into the gear's surface — {detail}. "
            "A tiny hooded figure stands on the gear's edge. Golden amber light catches the "
            "gear's teeth. Deep teal water reflects the light. Cinematic, epic fantasy, "
            "hyper-detailed. No text, no logos."
        ),
    },
    "B2": {
        "name": "The Flooded Archive",
        "frame": (
            "A vast underground stone archive, its floor submerged in dark water reflecting "
            "floating lanterns. {subject} — {detail} — visible on ancient scrolls and "
            "illuminated manuscripts. A single scholar rows a small boat through the waterway. "
            "Epic fantasy, atmospheric, hyper-detailed. No text, no logos."
        ),
    },
    "B3": {
        "name": "The Observatory Throne",
        "frame": (
            "Three monumental stone figures seated on a narrow mountain peak above an endless "
            "sea of mist. {subject} — {detail} — glows faintly in their hands. Golden dawn "
            "light breaks over distant mountains. Monumental, contemplative, epic fantasy. "
            "No text, no logos."
        ),
    },
    "B4": {
        "name": "The Star Map",
        "frame": (
            "A deep indigo night sky filled with hundreds of stars and five major constellation "
            "arcs. {subject} shaped by the constellation paths — {detail}. A robed figure with "
            "an astrolabe looks upward. Hyper-detailed astronomy chart meets epic fantasy. "
            "No text, no logos."
        ),
    },
    "B5": {
        "name": "The Forge Below",
        "frame": (
            "A vast underground forge carved into dark stone, lit by a crack in the ceiling. "
            "{subject} — {detail} — rests on the central anvil. A figure works at a side forge "
            "while sparks rise into darkness. Warm amber light, dramatic, hyper-detailed. "
            "No text, no logos."
        ),
    },
    "B6": {
        "name": "The Deep Current",
        "frame": (
            "A vast underground cavern with a wide river carrying hundreds of glowing lights. "
            "{subject} drifting like luminescent river creatures — {detail}. Ancient stone "
            "arches span the water. A robed figure watches from the near bank. Epic fantasy, "
            "surreal, atmospheric. No text, no logos."
        ),
    },
}


PACK_SPECS = {
    "promo": {
        "default_style": "B1",
        "goal": "promotional launch pack",
        "image_assets": [
            ("hero-image", "16:9"),
            ("social-square", "1:1"),
            ("vertical-poster", "9:16"),
        ],
        "video_mode": "architecture-diagram",
        "scene_titles": ["The Promise", "The Mechanism", "The Call To Action"],
    },
    "lesson": {
        "default_style": "B2",
        "goal": "teaching and educational media pack",
        "image_assets": [
            ("cover-image", "16:9"),
            ("lesson-diagram", "4:3"),
            ("concept-card", "1:1"),
        ],
        "video_mode": "concept-explainer",
        "scene_titles": ["The Question", "The Mechanism", "The Recap"],
    },
}


@dataclass
class CommandRecord:
    name: str
    kind: str
    prompt_path: str
    output_path: str
    command: list[str]


def slugify(value: str) -> str:
    slug = SLUG_RE.sub("-", value.lower()).strip("-")
    return slug or "media-pack"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a media pack from a short brief.")
    parser.add_argument("--pack", choices=sorted(PACK_SPECS), required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--brief", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--audience", default="general technical audience")
    parser.add_argument("--tone", default="cinematic, clear, ambitious")
    parser.add_argument("--cta", default="")
    parser.add_argument("--detail", default="rendered as a mythic technical motif")
    parser.add_argument("--style", choices=sorted(STYLE_LIBRARY))
    parser.add_argument("--voice", default=os.getenv("MEDIA_GEN_MINIMAX_VOICE", "English_expressive_narrator"))
    parser.add_argument("--out-dir", default=os.getenv("MEDIA_GEN_OUTPUT_DIR", "generated"))
    return parser.parse_args()


def render_image_prompt(
    style_code: str,
    title: str,
    brief: str,
    subject: str,
    detail: str,
    audience: str,
    tone: str,
) -> str:
    style = STYLE_LIBRARY[style_code]
    core = style["frame"].format(subject=subject, detail=detail)
    return (
        f"{core}\n\n"
        f"Project: {title}.\n"
        f"Brief: {brief}.\n"
        f"Audience: {audience}.\n"
        f"Tone: {tone}.\n"
        "Preserve the house palette: deep teal, dusk plum, golden amber, warm cream. "
        "Make the composition legible at thumbnail size."
    )


def render_music_prompt(pack: str, title: str, brief: str, tone: str) -> str:
    mood = "uplifting and resolute" if pack == "promo" else "focused and illuminating"
    return (
        f"Instrumental soundtrack for '{title}'. Brief: {brief}. Tone: {tone}. "
        f"Mood: {mood}. Build for a 20-30 second technical cinematic piece with a clean "
        "opening, one lift, and a restrained finish. Avoid vocals."
    )


def render_narration(pack: str, title: str, brief: str, subject: str, cta: str) -> str:
    if pack == "promo":
        lines = [
            f"{title}.",
            f"{brief}",
            f"At the center is {subject}.",
            "This system turns complexity into momentum.",
        ]
        if cta:
            lines.append(cta)
        return " ".join(lines)
    return " ".join(
        [
            f"{title}.",
            f"{brief}",
            f"We will use {subject} as the anchor visual.",
            "First, orient the learner. Then reveal the mechanism. Finally, summarize the key takeaway.",
        ]
    )


def render_storyboard(
    title: str,
    brief: str,
    subject: str,
    audience: str,
    cta: str,
) -> str:
    lines = [
        f"# Storyboard: {title}",
        "",
        f"Brief: {brief}",
        f"Audience: {audience}",
        f"Subject: {subject}",
    ]
    if cta:
        lines.append(f"CTA: {cta}")
    lines.extend(
        [
            "",
            "## Beats",
            "1. Orient the viewer with the core problem or promise.",
            "2. Reveal the mechanism, idea, or outcome in one memorable visual move.",
            "3. Land on a clear end state that can be turned into a CTA frame or recap still.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_visual_system_snapshot(pack: str, title: str, subject: str, tone: str) -> str:
    return (
        f"# Visual System Snapshot: {title}\n\n"
        f"Pack: {pack}\n"
        f"Subject: {subject}\n"
        f"Tone: {tone}\n\n"
        f"Shared reference: `{VISUAL_SYSTEM_REF}`\n\n"
        "Use dark backgrounds, semantic accent colors, monospace labels for explanatory graphics, "
        "and layered opacity for focus. Every still, diagram, card, and Manim scene should inherit "
        "the same hierarchy model.\n"
    )


def render_cover_brief(pack: str, title: str, brief: str, subject: str, style_name: str, cta: str) -> str:
    cta_line = f"CTA support: {cta}\n" if cta else ""
    return (
        f"# Cover Image Brief\n\n"
        f"Project: {title}\n"
        f"Pack: {pack}\n"
        f"House style: {style_name}\n"
        f"Subject: {subject}\n"
        f"Brief: {brief}\n"
        f"{cta_line}"
        "Goal: one strong anchor image with clear negative space, a dominant metaphor, and "
        "enough graphic simplicity to work in video payoff scenes, article headers, and social crops.\n"
    )


def render_diagram_brief(pack: str, title: str, brief: str, subject: str) -> str:
    diagram_type = "architecture" if pack == "promo" else "concept flow"
    return (
        f"# Diagram Brief\n\n"
        f"Project: {title}\n"
        f"Suggested type: {diagram_type}\n"
        f"Brief: {brief}\n"
        f"Subject: {subject}\n\n"
        "Use semantic color roles, dark background, monospace labels, and editable source output "
        "before raster export. This diagram should be reusable inside Manim blocking and article embeds.\n"
    )


def render_image_cards_brief(pack: str, title: str, brief: str, subject: str, cta: str) -> str:
    recommended_sequence = "cover + 2 concept cards + CTA" if pack == "promo" else "cover + 3 teaching cards + recap"
    cta_line = f"End card CTA: {cta}\n" if cta else ""
    return (
        f"# Image Cards Brief\n\n"
        f"Project: {title}\n"
        f"Brief: {brief}\n"
        f"Subject: {subject}\n"
        f"{cta_line}"
        f"Recommended sequence: {recommended_sequence}\n\n"
        "Each card should have one informational purpose, with card 1 establishing the visual anchor. "
        "Maintain motif and palette consistency across the full sequence.\n"
    )


def render_article_illustration_brief(pack: str, title: str, brief: str, subject: str) -> str:
    emphasis = "section-level support visuals for the article or post body"
    return (
        f"# Article Illustration Brief\n\n"
        f"Project: {title}\n"
        f"Brief: {brief}\n"
        f"Subject: {subject}\n"
        f"Goal: {emphasis}\n\n"
        "Map visuals to article structure. Use illustrations where comprehension improves, not where "
        "the content merely mentions a noun. Prefer article-specific metrics, terms, and metaphors.\n"
    )


def render_publishing_brief(pack: str, title: str, brief: str) -> str:
    return (
        f"# Publishing Brief\n\n"
        f"Project: {title}\n"
        f"Brief: {brief}\n\n"
        "Publishing flow: source markdown -> format markdown -> insert illustrations -> convert to HTML "
        "if needed -> compress export images for delivery.\n"
    )


def render_manim_plan(
    pack: str,
    title: str,
    brief: str,
    subject: str,
    audience: str,
    tone: str,
    cta: str,
) -> str:
    scene_titles = PACK_SPECS[pack]["scene_titles"]
    voiceover = render_narration(pack, title, brief, subject, cta)
    lines = [
        f"# {title} - Manim Plan",
        "",
        f"Mode: {PACK_SPECS[pack]['video_mode']}",
        f"Audience: {audience}",
        f"Tone: {tone}",
        "",
        "## Narrative Arc",
        f"Problem/Promise: {brief}",
        f"Aha Moment: {subject} becomes visually legible through staged reveals.",
        "",
        "## Scenes",
    ]
    for index, scene_title in enumerate(scene_titles, start=1):
        lines.extend(
            [
                f"### Scene {index}: {scene_title}",
                f"- Focus: {subject}",
                "- Visual weight: primary element at full opacity, support elements dimmed.",
                "- Exit: clean fade to prepare for the next scene.",
                "",
            ]
        )
    lines.extend(
        [
            "## Voiceover",
            voiceover,
            "",
            "## Rendering",
            "- Draft: use `-ql` for fast iteration",
            "- Production: use `-qh` after review",
        ]
    )
    return "\n".join(lines) + "\n"


def scene_class_names(pack: str) -> list[str]:
    if pack == "promo":
        return ["Scene1Promise", "Scene2Mechanism", "Scene3CallToAction"]
    return ["Scene1Question", "Scene2Mechanism", "Scene3Recap"]


def render_manim_script(pack: str, title: str, brief: str, subject: str, cta: str) -> str:
    scene_names = scene_class_names(pack)
    final_line = cta or "Key takeaway"
    return f"""from manim import *

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
MUTED = "#666666"
MONO = "{MONO_FONT}"


def build_header(text: str, color: str) -> Text:
    return Text(text, font=MONO, font_size=36, color=color, weight=BOLD)


def build_body(text: str) -> Text:
    return Text(text, font=MONO, font_size=24, color=WHITE, line_spacing=0.8)


class {scene_names[0]}(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = build_header({title!r}, PRIMARY).to_edge(UP, buff=0.7)
        brief = build_body({brief!r}).next_to(title, DOWN, buff=0.6)
        frame = RoundedRectangle(width=11, height=3.2, corner_radius=0.2, color=PRIMARY, stroke_width=3)
        frame.set_fill(PRIMARY, opacity=0.08)
        frame.next_to(brief, DOWN, buff=0.7)
        label = build_body({subject!r}).move_to(frame.get_center())
        self.play(Write(title), run_time=1.5)
        self.wait(0.8)
        self.play(FadeIn(brief, shift=UP * 0.2), run_time=1.0)
        self.wait(0.8)
        self.play(Create(frame), FadeIn(label), run_time=1.4)
        self.wait(1.4)
        self.play(FadeOut(VGroup(title, brief, frame, label)), run_time=0.6)


class {scene_names[1]}(Scene):
    def construct(self):
        self.camera.background_color = BG
        left = RoundedRectangle(width=3.0, height=1.6, corner_radius=0.18, color=PRIMARY, stroke_width=3)
        left.set_fill(PRIMARY, opacity=0.12)
        left.shift(LEFT * 3.2)
        middle = RoundedRectangle(width=3.0, height=1.6, corner_radius=0.18, color=SECONDARY, stroke_width=3)
        middle.set_fill(SECONDARY, opacity=0.12)
        right = RoundedRectangle(width=3.0, height=1.6, corner_radius=0.18, color=ACCENT, stroke_width=3)
        right.set_fill(ACCENT, opacity=0.12)
        right.shift(RIGHT * 3.2)
        arrow_one = Arrow(left.get_right(), middle.get_left(), buff=0.25, color=WHITE)
        arrow_two = Arrow(middle.get_right(), right.get_left(), buff=0.25, color=WHITE)
        left_text = build_body("Context").move_to(left.get_center())
        mid_text = build_body("Mechanism").move_to(middle.get_center())
        right_text = build_body("Outcome").move_to(right.get_center())
        note = build_header("Structure in motion", ACCENT).to_edge(UP, buff=0.7)
        self.play(Write(note), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(left), FadeIn(left_text), run_time=0.8)
        self.wait(0.5)
        self.play(GrowArrow(arrow_one), FadeIn(middle), FadeIn(mid_text), run_time=1.0)
        self.wait(0.5)
        self.play(GrowArrow(arrow_two), FadeIn(right), FadeIn(right_text), run_time=1.0)
        self.wait(1.6)
        self.play(FadeOut(VGroup(note, left, middle, right, left_text, mid_text, right_text, arrow_one, arrow_two)), run_time=0.6)


class {scene_names[2]}(Scene):
    def construct(self):
        self.camera.background_color = BG
        ring = Circle(radius=1.6, color=ACCENT, stroke_width=5)
        ring.set_fill(ACCENT, opacity=0.08)
        pulse = Circle(radius=2.1, color=PRIMARY, stroke_width=2)
        pulse.set_stroke(opacity=0.4)
        final_text = build_header({final_line!r}, ACCENT)
        final_text.next_to(ring, DOWN, buff=0.8)
        self.play(Create(ring), run_time=1.0)
        self.play(Create(pulse), run_time=0.8)
        self.wait(0.6)
        self.play(Write(final_text), run_time=1.0)
        self.wait(2.0)
"""


def _dot_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _dot_node(color: str, penwidth: float = 1.5, fontsize: int = 12) -> str:
    p = DIAGRAM_PALETTE
    return (
        f'color="{color}", fillcolor="{p["panel"]}", penwidth={penwidth}, '
        f'fontsize={fontsize}, fontcolor="{p["ink"]}"'
    )


def render_diagram_dot(pack: str, title: str, subject: str) -> str:
    p = DIAGRAM_PALETTE
    t = _dot_escape(title)
    s = _dot_escape(subject)
    shared_graph = (
        f'    graph [\n'
        f'        bgcolor="{p["bg"]}", fontname="Menlo", fontsize=13,\n'
        f'        fontcolor="{p["ink"]}", pad=0.6, splines=ortho,\n'
        f'        label="{t}", labelloc=t,\n'
        f'    ]\n'
        f'    node [\n'
        f'        shape=box, style="filled,rounded",\n'
        f'        fillcolor="{p["panel"]}", fontname="Menlo", fontsize=12,\n'
        f'        fontcolor="{p["ink"]}", color="{p["primary"]}",\n'
        f'        penwidth=1.5, margin="0.25,0.15",\n'
        f'    ]\n'
        f'    edge [\n'
        f'        color="{p["muted"]}", fontname="Menlo", fontsize=10,\n'
        f'        fontcolor="{p["muted"]}", arrowsize=0.85,\n'
        f'    ]\n'
    )
    if pack == "promo":
        body = (
            f'\n'
            f'    INPUT [{_dot_node(p["primary"], 2.0)}  label="Input"]\n'
            f'    CORE  [{_dot_node(p["accent"],  2.5, 13)} label="{s}"]\n'
            f'    OUT_A [{_dot_node(p["secondary"], 2.0)} label="Outcome A"]\n'
            f'    OUT_B [{_dot_node(p["secondary"], 2.0)} label="Outcome B"]\n'
            f'\n'
            f'    INPUT -> CORE\n'
            f'    CORE  -> OUT_A\n'
            f'    CORE  -> OUT_B\n'
        )
        return f'digraph architecture {{\n{shared_graph}    rankdir=LR,\n{body}}}\n'
    body = (
        f'\n'
        f'    Q [{_dot_node(p["primary"], 2.0)}  label="The Question"]\n'
        f'    M [{_dot_node(p["accent"],  2.5, 13)} label="{s}"]\n'
        f'    R [{_dot_node(p["secondary"], 2.0)} label="The Takeaway"]\n'
        f'\n'
        f'    Q -> M [label="leads to"]\n'
        f'    M -> R [label="reveals"]\n'
    )
    return f'digraph concept_flow {{\n{shared_graph}    rankdir=TD,\n{body}}}\n'


def write_diagram_project(pack_dir: Path, pack: str, title: str, subject: str) -> Path:
    diagrams_dir = pack_dir / "diagrams"
    diagrams_dir.mkdir(parents=True, exist_ok=True)
    dot_path = diagrams_dir / "diagram.dot"
    dot_path.write_text(render_diagram_dot(pack, title, subject), encoding="utf-8")
    return dot_path


def write_manim_project(pack_dir: Path, pack: str, title: str, brief: str, subject: str, audience: str, tone: str, cta: str) -> tuple[Path, Path, Path]:
    manim_dir = pack_dir / "manim"
    renders_dir = manim_dir / "renders"
    manim_dir.mkdir(parents=True, exist_ok=True)
    renders_dir.mkdir(parents=True, exist_ok=True)
    plan_path = manim_dir / "plan.md"
    script_path = manim_dir / "script.py"
    concat_path = manim_dir / "concat.txt"
    plan_path.write_text(
        render_manim_plan(pack, title, brief, subject, audience, tone, cta),
        encoding="utf-8",
    )
    script_path.write_text(
        render_manim_script(pack, title, brief, subject, cta),
        encoding="utf-8",
    )
    concat_lines = [f"file 'renders/{scene}.mp4'" for scene in scene_class_names(pack)]
    concat_path.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    return plan_path, script_path, concat_path


def write_module_briefs(pack_dir: Path, pack: str, title: str, brief: str, subject: str, tone: str, style_code: str, cta: str) -> dict[str, str]:
    modules_dir = pack_dir / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "visual_system": modules_dir / "visual-system.md",
        "cover_image": modules_dir / "cover-image-brief.md",
        "diagram": modules_dir / "diagram-brief.md",
        "image_cards": modules_dir / "image-cards-brief.md",
        "article_illustration": modules_dir / "article-illustration-brief.md",
        "publishing": modules_dir / "publishing-brief.md",
    }
    files["visual_system"].write_text(render_visual_system_snapshot(pack, title, subject, tone), encoding="utf-8")
    files["cover_image"].write_text(
        render_cover_brief(pack, title, brief, subject, STYLE_LIBRARY[style_code]["name"], cta),
        encoding="utf-8",
    )
    files["diagram"].write_text(render_diagram_brief(pack, title, brief, subject), encoding="utf-8")
    files["image_cards"].write_text(render_image_cards_brief(pack, title, brief, subject, cta), encoding="utf-8")
    files["article_illustration"].write_text(
        render_article_illustration_brief(pack, title, brief, subject),
        encoding="utf-8",
    )
    files["publishing"].write_text(render_publishing_brief(pack, title, brief), encoding="utf-8")
    return {key: str(path) for key, path in files.items()}


def build_commands(pack: str, pack_dir: Path, voice: str) -> list[CommandRecord]:
    commands: list[CommandRecord] = []
    prompts_dir = pack_dir / "prompts"
    outputs_dir = pack_dir / "outputs"
    manim_dir = pack_dir / "manim"

    for asset_name, aspect in PACK_SPECS[pack]["image_assets"]:
        prompt_path = prompts_dir / f"{asset_name}.txt"
        commands.append(
            CommandRecord(
                name=asset_name,
                kind="image",
                prompt_path=str(prompt_path),
                output_path=str(outputs_dir / asset_name),
                command=[
                    "mmx",
                    "image",
                    "generate",
                    "--prompt",
                    prompt_path.read_text(encoding="utf-8"),
                    "--aspect-ratio",
                    aspect,
                    "--out-dir",
                    str(outputs_dir),
                    "--out-prefix",
                    asset_name,
                    "--non-interactive",
                    "--quiet",
                ],
            )
        )

    soundtrack_prompt = prompts_dir / "soundtrack.txt"
    commands.append(
        CommandRecord(
            name="soundtrack",
            kind="music",
            prompt_path=str(soundtrack_prompt),
            output_path=str(outputs_dir / "soundtrack.mp3"),
            command=[
                "mmx",
                "music",
                "generate",
                "--prompt",
                soundtrack_prompt.read_text(encoding="utf-8"),
                "--instrumental",
                "--out",
                str(outputs_dir / "soundtrack.mp3"),
                "--non-interactive",
                "--quiet",
            ],
        )
    )

    narration_prompt = prompts_dir / "narration.txt"
    commands.append(
        CommandRecord(
            name="narration",
            kind="tts",
            prompt_path=str(narration_prompt),
            output_path=str(outputs_dir / "narration.mp3"),
            command=[
                "mmx",
                "speech",
                "synthesize",
                "--text-file",
                str(narration_prompt),
                "--voice",
                voice,
                "--out",
                str(outputs_dir / "narration.mp3"),
                "--non-interactive",
                "--quiet",
            ],
        )
    )

    commands.append(
        CommandRecord(
            name="diagram",
            kind="diagram",
            prompt_path=str(pack_dir / "diagrams" / "diagram.dot"),
            output_path=str(outputs_dir / "diagram.svg"),
            command=[
                "python3",
                "scripts/generate_diagram.py",
                "--pack-dir",
                str(pack_dir),
                "--render-only",
            ],
        )
    )

    commands.extend(
        [
            CommandRecord(
                name="manim-render",
                kind="video",
                prompt_path=str(manim_dir / "plan.md"),
                output_path=str(outputs_dir / "video.mp4"),
            command=[
                "python3",
                "scripts/render_manim_pack.py",
                "--pack-dir",
                str(pack_dir),
                "--quality",
                "low",
                "--render-only",
            ],
        ),
            CommandRecord(
                name="video-mux",
                kind="post",
                prompt_path=str(manim_dir / "concat.txt"),
                output_path=str(outputs_dir / "video-with-audio.mp4"),
                command=[
                    "python3",
                    "scripts/render_manim_pack.py",
                    "--pack-dir",
                    str(pack_dir),
                    "--mux-only",
                ],
            ),
        ]
    )
    return commands


def write_manifest(
    pack: str,
    title: str,
    style_code: str,
    audience: str,
    tone: str,
    pack_dir: Path,
    commands: list[CommandRecord],
) -> None:
    lines = [
        f"# {title}",
        "",
        f"Pack type: `{pack}`",
        f"Style: `{style_code}` - {STYLE_LIBRARY[style_code]['name']}",
        f"Audience: {audience}",
        f"Tone: {tone}",
        "",
        "## Deliverables",
    ]
    for command in commands:
        lines.append(f"- `{command.name}` ({command.kind}) -> `{Path(command.output_path).name}`")
    lines.extend(
        [
            "",
            "## Module Briefs",
            "- `modules/cover-image-brief.md`",
            "- `modules/diagram-brief.md`",
            "- `modules/image-cards-brief.md`",
            "- `modules/article-illustration-brief.md`",
            "- `modules/publishing-brief.md`",
            "",
            "## Diagram Source",
            "- `diagrams/diagram.dot` (edit before running the diagram step)",
        ]
    )
    lines.extend(
        [
            "",
            "## Run",
            "```bash",
            f"python3 scripts/run_pack.py --pack-dir {pack_dir}",
            "```",
            "",
            "Use `--dry-run` on `run_pack.py` to inspect the full integrated workflow.",
        ]
    )
    (pack_dir / "asset-plan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    pack = args.pack
    style_code = args.style or PACK_SPECS[pack]["default_style"]
    pack_dir = Path(args.out_dir) / f"{slugify(args.title)}-{pack}"
    prompts_dir = pack_dir / "prompts"
    outputs_dir = pack_dir / "outputs"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    image_prompt = render_image_prompt(
        style_code,
        args.title,
        args.brief,
        args.subject,
        args.detail,
        args.audience,
        args.tone,
    )
    music_prompt = render_music_prompt(pack, args.title, args.brief, args.tone)
    narration = render_narration(pack, args.title, args.brief, args.subject, args.cta)
    storyboard = render_storyboard(
        args.title,
        args.brief,
        args.subject,
        args.audience,
        args.cta,
    )

    for asset_name, _ in PACK_SPECS[pack]["image_assets"]:
        (prompts_dir / f"{asset_name}.txt").write_text(image_prompt, encoding="utf-8")
    (prompts_dir / "soundtrack.txt").write_text(music_prompt, encoding="utf-8")
    (prompts_dir / "narration.txt").write_text(narration, encoding="utf-8")
    (prompts_dir / "storyboard.txt").write_text(storyboard, encoding="utf-8")

    plan_path, script_path, concat_path = write_manim_project(
        pack_dir,
        pack,
        args.title,
        args.brief,
        args.subject,
        args.audience,
        args.tone,
        args.cta,
    )
    module_paths = write_module_briefs(
        pack_dir,
        pack,
        args.title,
        args.brief,
        args.subject,
        args.tone,
        style_code,
        args.cta,
    )
    dot_path = write_diagram_project(pack_dir, pack, args.title, args.subject)

    brief = {
        "pack": pack,
        "title": args.title,
        "brief": args.brief,
        "subject": args.subject,
        "audience": args.audience,
        "tone": args.tone,
        "cta": args.cta,
        "detail": args.detail,
        "style": style_code,
        "style_name": STYLE_LIBRARY[style_code]["name"],
        "voice": args.voice,
        "video_backend": "manim",
    }
    (pack_dir / "brief.json").write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
    (pack_dir / "storyboard.md").write_text(storyboard, encoding="utf-8")

    commands = build_commands(pack, pack_dir, args.voice)
    (pack_dir / "commands.json").write_text(
        json.dumps([command.__dict__ for command in commands], indent=2) + "\n",
        encoding="utf-8",
    )
    write_manifest(pack, args.title, style_code, args.audience, args.tone, pack_dir, commands)

    metadata = {
        "pack_dir": str(pack_dir),
        "plan_path": str(plan_path),
        "script_path": str(script_path),
        "concat_path": str(concat_path),
        "dot_path": str(dot_path),
        "module_paths": module_paths,
    }
    (pack_dir / "pack-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(pack_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
