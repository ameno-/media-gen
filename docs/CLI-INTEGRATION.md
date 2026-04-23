# CLI Integration Guide

## Letta Code

### Installation

```bash
cp -r skills/media-creation ~/.letta/skills/
cp -r skills/music-creation ~/.letta/skills/
cp -r skills/manim-video ~/.letta/skills/
cp -r skills/promo-pack ~/.letta/skills/
cp -r skills/lesson-pack ~/.letta/skills/
```

### Invocation

```text
/media-creation
/music-creation
/manim-video
/promo-pack
/lesson-pack
```

## Claude Code

### Installation

```bash
cp -r skills/media-creation ~/.claude/skills/
cp -r skills/music-creation ~/.claude/skills/
cp -r skills/manim-video ~/.claude/skills/
cp -r skills/promo-pack ~/.claude/skills/
cp -r skills/lesson-pack ~/.claude/skills/
```

### Invocation

```text
/media-creation
/music-creation
/manim-video
/promo-pack
/lesson-pack
```

## Direct CLI Usage

### MiniMax

```bash
mmx image generate --prompt "Epic technical banner" --aspect-ratio 16:9
mmx music generate --prompt "Technical cinematic bed" --instrumental --out soundtrack.mp3
mmx speech synthesize --text "Welcome to the lesson." --out narration.mp3
```

### Manim

```bash
bash scripts/setup_manim_env.sh
.venv-manim/bin/python -m manim -ql path/to/script.py Scene1Question
```

### Pack Builder

```bash
python3 scripts/build_media_pack.py \
  --pack lesson \
  --title "Context Routing" \
  --brief "Teach the core mechanism of context routing." \
  --subject "knowledge flowing through a routing graph"

python3 scripts/run_pack.py --pack-dir generated/context-routing-lesson --dry-run
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | Optional | OpenRouter still generation |
| `OPENAI_API_KEY` | Optional | OpenAI image usage |
| `MINIMAX_API_KEY` | For `mmx` | Image, music, and speech |
| `MEDIA_GEN_MINIMAX_VOICE` | Optional | Default TTS voice for pack builds |
| `MEDIA_GEN_OUTPUT_DIR` | Optional | Default pack output directory |
| `MANIM_PYTHON_BIN` | Optional | Override Manim interpreter path |
