---
name: music-creation
description: |
  Music and soundtrack generation for media packs using MiniMax CLI (mmx).
  Use when: soundtrack, background music, theme stings, launch music, lesson beds,
  or instrumental cues are needed.
---

# Music Creation

Treat music as part of the deliverable.

## Default Lane

Use `mmx music generate` for most work.

```bash
mmx music generate \
  --prompt "Cinematic launch soundtrack with warm brass and restrained percussion" \
  --instrumental \
  --out outputs/soundtrack.mp3 \
  --non-interactive \
  --quiet
```

## Decision Rules

1. `promo-pack` -> uplifting, memorable, clean ending for CTA.
2. `lesson-pack` -> focused, restrained, non-distracting, supports narration.
3. Instrumental by default. Only use lyrics when the user explicitly asks for a song.
4. Keep music beneath narration in the final mix.

## Prompt Formula

`purpose + mood + instrumentation + tempo + structure + avoidance`
