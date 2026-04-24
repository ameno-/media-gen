# CLAUDE.md

Thin repo guide for AI coding agents.

## What This Repo Is

Integrated media-pack workflow:

- `mmx image` for stills
- `mmx music` for soundtrack
- `mmx speech` for narration
- Manim for video
- ffmpeg for stitch/mux

Do not route video generation through `mmx video` in this repo.

## First Steps

If local setup is unknown:

```bash
python3 scripts/check_setup.py
```

If system deps are missing:

```bash
bash scripts/setup_system_deps.sh
bash scripts/setup_manim_env.sh
```

If keys are not configured:

```bash
cp config.example.sh config.sh
source config.sh
```

## Primary Scripts

- `python3 scripts/build_media_pack.py ...` -> create pack directory, prompts, Manim project, commands
- `python3 scripts/run_pack.py --pack-dir ... --dry-run` -> inspect full workflow
- `python3 scripts/run_pack.py --pack-dir ... --only ...` -> run selected steps
- `python3 scripts/generate_diagram.py --pack-dir ...` -> render diagram from DOT source
- `python3 scripts/render_manim_pack.py --pack-dir ...` -> render/mux Manim lane directly
- `python3 scripts/smoke_test.py` -> repo smoke test
- `python3 scripts/check_setup.py` -> dependency/key check

## Agent Routing

Use these skills:

- `skills/promo-pack/` for launches and promo work
- `skills/lesson-pack/` for explainers and educational work
- `skills/manim-video/` for video
- `skills/music-creation/` for soundtrack
- `skills/media-creation/` for stills
- `skills/cover-image/` for hero stills
- `skills/diagram-creation/` for architecture and concept diagrams
- `skills/image-cards/` for visual card sequences
- `skills/article-illustration/` for article visuals
- `skills/url-to-markdown/` + `skills/format-markdown/` + `skills/markdown-to-html/` for article source and publish flow
- `skills/compress-image/` for final optimization
- `skills/imagine-backend/` as optional non-mmx still backend
- `skills/motion-edit/` for stitch/mux/post

## Required Keys

- `MINIMAX_API_KEY` for the default workflow

Optional:

- `OPENROUTER_API_KEY`
- `OPENAI_API_KEY`

## Constraints

- Never commit `config.sh` or secrets
- Prefer the repo scripts over ad hoc commands
- For equation-heavy Manim scenes, verify `latex`/`pdflatex` first
