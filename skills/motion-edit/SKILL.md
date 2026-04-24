---
name: motion-edit
description: |
  Post-production lane for media packs. Use when stitching Manim scenes, muxing narration
  and music, trimming outputs, or preparing final delivery variants after render.
---

# Motion Edit

This skill is the finishing lane, not the video generator.

## Responsibilities

- stitch Manim scene renders
- mux narration and soundtrack
- create final delivery variants
- verify runtime, legibility, and clean end frames

## Default Tooling

- `ffmpeg` for stitch and mux
- `python3 scripts/render_manim_pack.py --mux-only` for pack-aware assembly
