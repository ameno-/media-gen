---
name: manim-video
description: |
  Production pipeline for mathematical and technical animations using Manim Community Edition.
  Use when: explainer videos, architecture animations, algorithm walkthroughs, data stories,
  educational motion, or any pack that needs programmatic video instead of generative video.
---

# Manim Video

Video is a production pipeline, not a single prompt.

## Stack

- Manim Community Edition for scene rendering
- ffmpeg for stitch and audio mux
- `mmx speech` for narration
- `mmx music` for soundtrack
- `mmx image` for stills and promotional key art

## Pipeline

`PLAN -> CODE -> RENDER -> STITCH -> AUDIO -> REVIEW`

1. Plan the narrative arc in `plan.md`
2. Write one Manim script with one scene class per section
3. Render scenes at `-ql` first, then `-qh` for production
4. Stitch scene clips with `ffmpeg`
5. Add narration and music after the visual cut is stable

## Local Commands

```bash
python3 scripts/render_manim_pack.py --pack-dir generated/example-lesson
python3 scripts/render_manim_pack.py --pack-dir generated/example-lesson --mux-only
```

## Creative Direction

Follow the Hermes model:

- geometry before algebra
- opacity layering for focus
- breathing room after key reveals
- consistent palette, typography, and motion timing
