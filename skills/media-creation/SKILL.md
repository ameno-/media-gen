---
name: media-creation
description: |
  Unified image generation skill. Routes to the right backend (OpenRouter/Nano Banana,
  Codex CLI, MiniMax CLI, ChatGPT/DALL-E) based on style. Whimsical aesthetic is the
  default. Loads STYLES.md for prompt templates and SERVICES.md for invocation details.
  Use when: generating any image, banner, illustration, or creative asset.
---

# Media Creation

Abstracted image generation — one skill, multiple backends, whimsical default.

## The One Rule

**Whimsical is the default aesthetic.** If you say "generate X" without specifying a style, go whimsical first. Ask one clarifying question only if the content genuinely needs a different treatment.

## The Security Model

**No API keys are ever in this repo.** All keys live in environment variables:
- `OPENROUTER_API_KEY` — OpenRouter image generation
- `OPENAI_API_KEY` — Codex CLI batch mode / DALL-E API
- `MINIMAX_API_KEY` — MiniMax CLI (if using mmx with auth)

See `config.example.sh` for the full variable list.

## Decision Tree

```
1. What is this for?
   └── Blog banner        → Technical Blog style (OpenRouter)
   └── Standalone creative → Whimsical (default) → Codex CLI
   └── Editorial asset     → See STYLES.md asset type guide
   └── Not sure            → Whimsical, ask which variant

2. What style?
   └── No preference       → Whimsical (DEFAULT)
   └── "something like X"  → Match to closest Whimsical variant
   └── "technical"         → Technical Blog
   └── "medieval/old map"  → Navigator's Chart
   └── "Victorian/steampunk" → Clockwork Mechanism
   └── "illuminated"       → Guild Ledger
   └── "celestial/star map" → Constellation Map
   └── "folk art/loom"     → Enchanted Loom
   └── "surreal/painterly" → Painterly / Surrealist
   └── "scholarly/ancient" → Historical Mysticism

3. Which service?
   └── See SERVICES.md — service is determined by style, not manually chosen
```

## Style Families (Quick Reference)

| Style | Character | Service |
|---|---|---|
| Whimsical (DEFAULT) | Historical fantasy, warm, literary | Codex CLI |
| Guild Ledger | Medieval illuminated manuscript | Codex CLI |
| Clockwork Mechanism | Victorian steampunk | Codex CLI |
| Constellation Map | Celestial cartography | Codex CLI |
| Enchanted Loom | Folk-art magical | Codex CLI |
| Navigator's Chart | Age of exploration | Codex CLI |
| Historical Mysticism | Ancient observatories, scholars | OpenRouter |
| Painterly / Surrealist | Bierstadt meets Beksiński | ChatGPT + reference |
| Technical Blog | Clean, brand-consistent | OpenRouter |

Full prompts → `STYLES.md` | Service details → `SERVICES.md`

## How to Ask Questions

When clarification is needed, ask **one question with clear choices**.

**Good**: "Whimsical — which variant: illuminated manuscript, steampunk clockwork, celestial map, or age-of-exploration nautical chart?"

**When not to ask**: If the content is obviously whimsical in nature ("an illustration of a curious explorer"), use Whimsical and pick the closest variant.

## Service Invocation

See `SERVICES.md` for detailed invocation. Adapters are in `adapters/`:

| Backend | Adapter | Invocation |
|---|---|---|
| OpenRouter | `adapters/openrouter_image.py` | `python adapters/openrouter_image.py "[prompt]" -o out.png` |
| Codex CLI | Native | `codex exec "$imagegen generate..."` |
| MiniMax CLI | Native | `mmx image generate --prompt "..."` |
| ChatGPT | Web UI | chat.openai.com |

## What This Skill Does

- Composes prompts using the style templates in `STYLES.md`
- Selects the appropriate service based on style → service mapping
- Executes generation via the appropriate backend
- Reports result path back

## What This Skill Does NOT Do

- Manage file storage, naming, or versioning (not a file manager)
- Hardcode any API keys or secrets (environment variables only)
- Generate text, video, or audio
