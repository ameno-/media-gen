# AGENTS.md

Repo-local instructions for coding agents.

## Purpose

This repo builds integrated media packs.

Backend split:

- stills -> `mmx image`
- soundtrack -> `mmx music`
- narration -> `mmx speech`
- video -> Manim
- assembly -> ffmpeg

Do not use `mmx video` as the primary video path here.

## Standard Workflow

1. Check environment:

```bash
python3 scripts/check_setup.py
```

2. If needed, install deps:

```bash
bash scripts/setup_system_deps.sh
bash scripts/setup_manim_env.sh
```

3. If keys are missing:

```bash
cp config.example.sh config.sh
source config.sh
```

4. Build a pack:

```bash
python3 scripts/build_media_pack.py \
  --pack lesson \
  --title "Example" \
  --brief "Teach the mechanism clearly." \
  --subject "knowledge flowing through a routing graph"
```

5. Inspect commands before spending quota:

```bash
python3 scripts/run_pack.py --pack-dir generated/example-lesson --dry-run
```

6. Run selected steps:

```bash
python3 scripts/run_pack.py \
  --pack-dir generated/example-lesson \
  --only cover-image soundtrack narration manim-render video-mux
```

## Scripts Agents Should Prefer

- `scripts/check_setup.py`
- `scripts/setup_system_deps.sh`
- `scripts/setup_manim_env.sh`
- `scripts/build_media_pack.py`
- `scripts/run_pack.py`
- `scripts/generate_diagram.py`
- `scripts/render_manim_pack.py`
- `scripts/smoke_test.py`

## Skill Routing

- promo work -> `skills/promo-pack/`
- educational work -> `skills/lesson-pack/`
- video generation -> `skills/manim-video/`
- soundtrack -> `skills/music-creation/`
- stills -> `skills/media-creation/`
- hero still direction -> `skills/cover-image/`
- diagrams -> `skills/diagram-creation/`
- card/carousel sequences -> `skills/image-cards/`
- section-aware article visuals -> `skills/article-illustration/`
- URL ingestion -> `skills/url-to-markdown/`
- markdown cleanup -> `skills/format-markdown/`
- HTML publishing -> `skills/markdown-to-html/`
- delivery optimization -> `skills/compress-image/`
- optional multi-provider still backend -> `skills/imagine-backend/`
- stitch/mux -> `skills/motion-edit/`

## Key Env Vars

Required:

- `MINIMAX_API_KEY`

Optional:

- `OPENROUTER_API_KEY`
- `OPENAI_API_KEY`
- `MEDIA_GEN_OUTPUT_DIR`
- `MEDIA_GEN_MINIMAX_VOICE`
- `MANIM_PYTHON_BIN`

## Safety

- Never commit secrets
- Never assume TeX exists; check for `latex` / `pdflatex`
- Use repo scripts instead of re-deriving workflow logic
