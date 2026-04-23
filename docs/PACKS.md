# Media Packs

The repo now has two layers:

## Capabilities

- `media-creation` - static image prompts and backend routing
- `music-creation` - soundtrack generation via `mmx music`
- `manim-video` - programmatic video generation via Manim
- `motion-edit` - stitch and mux lane after render
- `cover-image` - hero still direction
- `diagram-creation` - reusable architecture/concept diagrams
- `image-cards` - carousel/swipe sequences
- `article-illustration` - in-article visuals
- `format-markdown` - source cleanup
- `url-to-markdown` - source ingestion
- `markdown-to-html` - publishing transform
- `compress-image` - delivery optimization
- `imagine-backend` - optional multi-provider still backend

## Packs

- `promo-pack` - launches, announcements, landing pages, social promotion
- `lesson-pack` - tutorials, explainers, internal training, educational media

## Integrated Workflow

```text
brief
  -> still prompts (mmx image)
  -> module briefs (cover / diagram / cards / article / publishing)
  -> narration script (mmx speech)
  -> soundtrack prompt (mmx music)
  -> manim plan/script/concat
  -> render scenes
  -> stitch + mux final video
```

## Builder

```bash
python3 scripts/build_media_pack.py \
  --pack lesson \
  --title "Context Routing" \
  --brief "Teach the core mechanism of context routing." \
  --subject "knowledge flowing through a routing graph"
```

This writes:

- `brief.json`
- `storyboard.md`
- `prompts/*.txt`
- `modules/cover-image-brief.md`
- `modules/diagram-brief.md`
- `modules/image-cards-brief.md`
- `modules/article-illustration-brief.md`
- `modules/publishing-brief.md`
- `manim/plan.md`
- `manim/script.py`
- `manim/concat.txt`
- `commands.json`

## Runner

Preview the full workflow:

```bash
python3 scripts/run_pack.py --pack-dir generated/context-routing-lesson --dry-run
```

Run selected steps:

```bash
python3 scripts/run_pack.py --pack-dir generated/context-routing-lesson --only cover-image soundtrack narration manim-render video-mux
```

## Visual System

All packs should inherit the shared visual language defined in [VISUAL-SYSTEM.md](/Users/ameno/dev/media-gen/docs/VISUAL-SYSTEM.md).
