# Setup Guide

## Backends

- `mmx image` for stills
- `mmx music` for soundtrack
- `mmx speech` for narration
- Graphviz (`dot`) for architecture and concept diagrams
- Manim for video render
- ffmpeg for stitch and mux
- LaTeX for `MathTex` and equation-heavy Manim scenes

## Step 0: Install System Dependencies

```bash
bash scripts/setup_system_deps.sh
```

This installs the packages declared in `Brewfile`:

- `cairo`
- `pango`
- `pkgconf`
- `ffmpeg`
- `mactex-no-gui`

Notes:

- The TeX cask install may require macOS admin privileges because it runs the system installer.
- `mactex-no-gui` is the full, least-surprising option for `MathTex`, but it needs significant free disk space.
- If disk is tight, `basictex` is the smaller fallback, but you may need extra TeX Live packages later for complex scenes.

## Step 1: Configure Keys

```bash
cp config.example.sh config.sh
source config.sh
```

## Step 2: Verify MiniMax

```bash
mmx auth status
mmx image --help
mmx music generate --help
mmx speech synthesize --help
```

## Step 3: Set Up Manim

Create a local virtualenv for video work:

```bash
bash scripts/setup_manim_env.sh
```

This creates `.venv-manim/` and installs `manim` there.

If you only need the OpenRouter adapter, install its Python dependency with:

```bash
python3 -m pip install -r requirements.txt --break-system-packages
```

## Step 4: Verify Dependencies

Required for full video flow:

- `ffmpeg`
- `dot` (Graphviz, from `brew bundle` or `brew install graphviz`)
- `.venv-manim/bin/python -m manim`
- `latex`
- `pdflatex`

Optional but recommended for math-heavy scenes:

- LaTeX (`latex` / `pdflatex`) for `MathTex`

The generated starter Manim scenes in this repo do not require LaTeX. Advanced equation animations do.

## Step 6: Validate Setup

```bash
python3 scripts/check_setup.py
```

## Step 5: Test the Pack Workflow

```bash
python3 scripts/smoke_test.py
```

If `.venv-manim` exists, you can also render a generated pack:

```bash
python3 scripts/build_media_pack.py \
  --pack lesson \
  --title "Context Routing" \
  --brief "Teach the core mechanism of context routing." \
  --subject "knowledge flowing through a routing graph"

python3 scripts/run_pack.py \
  --pack-dir generated/context-routing-lesson \
  --only cover-image soundtrack narration manim-render video-mux
```
