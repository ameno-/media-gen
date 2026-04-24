# media-gen

Integrated media pack generation for AI agents. Use `mmx` for image, music, and TTS. Use Manim for video. Use ffmpeg to assemble the final cut.

## What It Does

- **Organized by deliverable.** Build `promo-pack` and `lesson-pack` outputs, not one-off assets.
- **Shared media backend.** `mmx image`, `mmx music`, and `mmx speech` cover stills, soundtrack, and narration.
- **Programmatic video.** Manim owns the video lane for explainers, architecture builds, and technical motion.
- **Integrated output.** Packs generate prompts, narration, a Manim project, design-module briefs, commands, and final assembly steps together.

## Pack Model

The repo has two layers:

- **Capabilities**: `media-creation`, `music-creation`, `manim-video`, `motion-edit`
- **Packs**: `promo-pack`, `lesson-pack`

Typical flow:

```text
brief
  -> still prompts
  -> cover / diagram / cards / article-illustration briefs
  -> soundtrack prompt
  -> narration script
  -> manim plan/script/concat
  -> render scenes
  -> stitch + mux
  -> final asset pack
```

## The Aesthetic

Epic fantasy meets technical content. Massive scale, atmospheric depth, warm amber light against dark teal shadows. Grand scale with intimate human presence.

```text
Deep teal:      #2a5a6a   (sky, water, shadows)
Dusk plum:      #8a5a6a   (accent, depth)
Golden amber:   #d4a574   (light, warmth)
Warm cream:     #e8dcc4   (stone, parchment)
Dark indigo:    #1a1a2a   (deep background)
```

## Quick Start

```bash
git clone https://github.com/ameno-/media-gen.git
cd media-gen
bash scripts/setup_system_deps.sh
bash scripts/setup_manim_env.sh
cp config.example.sh config.sh
source config.sh
```

`setup_system_deps.sh` uses Homebrew and may prompt for admin access when installing the TeX distribution.

Direct generation:

```bash
mmx image generate --prompt "Epic technical banner" --aspect-ratio 16:9
mmx music generate --prompt "Cinematic technical soundtrack" --instrumental --out soundtrack.mp3
mmx speech synthesize --text "Welcome to the lesson." --out narration.mp3
```

Build a full pack:

```bash
python3 scripts/build_media_pack.py \
  --pack lesson \
  --title "Context Routing" \
  --brief "Teach the core mechanism of context routing." \
  --subject "knowledge flowing through a routing graph"

python3 scripts/run_pack.py --pack-dir generated/context-routing-lesson --dry-run
```

## Skills

### Capabilities

- [`skills/media-creation/`](skills/media-creation/) - static image styles and still generation
- [`skills/music-creation/`](skills/music-creation/) - soundtrack generation via `mmx music`
- [`skills/manim-video/`](skills/manim-video/) - Manim-based video production
- [`skills/motion-edit/`](skills/motion-edit/) - stitch and mux lane after render
- [`skills/cover-image/`](skills/cover-image/) - stronger hero and header still direction
- [`skills/diagram-creation/`](skills/diagram-creation/) - architecture and concept diagrams
- [`skills/image-cards/`](skills/image-cards/) - card/carousel sequences
- [`skills/article-illustration/`](skills/article-illustration/) - section-aware article visuals
- [`skills/format-markdown/`](skills/format-markdown/) - markdown cleanup before visual/publish steps
- [`skills/url-to-markdown/`](skills/url-to-markdown/) - source ingestion from URLs
- [`skills/markdown-to-html/`](skills/markdown-to-html/) - publishing transform
- [`skills/compress-image/`](skills/compress-image/) - final still optimization
- [`skills/imagine-backend/`](skills/imagine-backend/) - optional multi-provider still backend

### Packs

- [`skills/promo-pack/`](skills/promo-pack/) - launches, announcements, hero assets, short promos
- [`skills/lesson-pack/`](skills/lesson-pack/) - explainers, tutorials, educational visuals

See [`docs/PACKS.md`](docs/PACKS.md) for the integrated builder and runner flow.
See [`docs/VISUAL-SYSTEM.md`](docs/VISUAL-SYSTEM.md) for the shared design language.

## Dependency Manifests

- [Brewfile](/Users/ameno/dev/media-gen/Brewfile) for macOS system deps
- [requirements.txt](/Users/ameno/dev/media-gen/requirements.txt) for the OpenRouter adapter
- [requirements-manim.txt](/Users/ameno/dev/media-gen/requirements-manim.txt) for the Manim render env

## AI Agent Integration

### Letta Code

```bash
cp -r skills/media-creation ~/.letta/skills/
cp -r skills/music-creation ~/.letta/skills/
cp -r skills/manim-video ~/.letta/skills/
cp -r skills/promo-pack ~/.letta/skills/
cp -r skills/lesson-pack ~/.letta/skills/
```

### Claude Code

```bash
cp -r skills/media-creation ~/.claude/skills/
cp -r skills/music-creation ~/.claude/skills/
cp -r skills/manim-video ~/.claude/skills/
cp -r skills/promo-pack ~/.claude/skills/
cp -r skills/lesson-pack ~/.claude/skills/
```

Say "build a promo pack" or "build a lesson pack" and the agent can route stills to `mmx`, video to Manim, and assembly to ffmpeg.

## File Structure

```text
media-gen/
├── README.md
├── config.example.sh
├── scripts/
│   ├── build_media_pack.py
│   ├── render_manim_pack.py
│   ├── run_pack.py
│   ├── setup_manim_env.sh
│   └── smoke_test.py
├── skills/
│   ├── media-creation/
│   ├── music-creation/
│   ├── manim-video/
│   ├── motion-edit/
│   ├── cover-image/
│   ├── diagram-creation/
│   ├── image-cards/
│   ├── article-illustration/
│   ├── format-markdown/
│   ├── url-to-markdown/
│   ├── markdown-to-html/
│   ├── compress-image/
│   ├── imagine-backend/
│   ├── promo-pack/
│   └── lesson-pack/
├── adapters/
│   └── openrouter_image.py
├── docs/
│   ├── SETUP.md
│   ├── CLI-INTEGRATION.md
│   ├── PACKS.md
│   ├── VISUAL-SYSTEM.md
│   └── STYLE-TEMPLATE.md
└── examples/
```

## Security

No API keys in this repo. All keys are environment variables.

```bash
OPENROUTER_API_KEY   # OpenRouter image generation
OPENAI_API_KEY       # Codex/OpenAI image usage
MINIMAX_API_KEY      # mmx image / music / speech
```

Copy `config.example.sh` to `config.sh`, fill in keys, never commit it.

Check the local setup and key presence:

```bash
python3 scripts/check_setup.py
```
