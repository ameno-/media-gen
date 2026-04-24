---
name: promo-pack
description: |
  Build promotional media packs for launches, announcements, landers, and social.
  Use when: feature launch, product announcement, campaign assets, repo banner refresh,
  release promo, teaser content.
---

# Promo Pack

Organize around the pack, not the tool.

## Deliverables

- hero image
- square social image
- vertical poster
- narration
- soundtrack
- manim video

## Workflow

1. Brief the pack in one paragraph.
2. Build the pack skeleton:

```bash
python3 scripts/build_media_pack.py \
  --pack promo \
  --title "Launch title" \
  --brief "What is being promoted and why it matters." \
  --subject "core visual subject" \
  --cta "Call to action"
```

3. Dry-run the commands:

```bash
python3 scripts/run_pack.py --pack-dir generated/launch-title-promo --dry-run
```

4. Execute selected assets when ready.

## Routing

- stills -> `mmx image`
- soundtrack -> `mmx music`
- narration -> `mmx speech`
- video -> `manim-video`
- final assembly -> `motion-edit`
