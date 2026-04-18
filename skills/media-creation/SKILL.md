---
name: media-creation
description: |
  Epic fantasy banner generation for AI agents. Loads STYLES.md for prompt templates,
  picks the best available tool from SERVICES.md. No aesthetic re-explaining.
  Use when: generating any image, banner, illustration, or creative asset.
---

# Media Creation

Epic fantasy banner generation — prompts live here, not in your head.

## The Core Idea

Load this skill → agent knows the aesthetic. You say "generate a banner" → agent picks the right style prompt and generates with whatever tool is available.

## Security Model

**No API keys in this repo.** All keys are environment variables:
- `OPENROUTER_API_KEY` — OpenRouter (Nano Banana, Flux, GPT5 Image)
- `OPENAI_API_KEY` — Codex CLI batch mode / DALL-E
- `MINIMAX_API_KEY` — MiniMax CLI

See `config.example.sh` for the full variable list.

## Decision Tree

```
1. What is this for?
   └── Banner / header image  → Pick from STYLES.md
   └── Editorial illustration → Pick from STYLES.md
   └── Avatar / icon          → Custom prompt, 1:1 aspect ratio
   └── Not sure               → B1 Gilded Mechanism (code/engineering) or B2 Flooded Archive (knowledge/docs)

2. What style fits the content?
   └── Code, engineering, systems → B1 Gilded Mechanism
   └── Context, knowledge, docs  → B2 Flooded Archive
   └── Agents, strategy, planning → B3 Observatory Throne
   └── Predictions, vision       → B4 Star Map
   └── Building, construction     → B5 Forge Below
   └── Data, flow, streams      → B6 Deep Current
   └── Surreal, narrative        → PS Painterly
   └── Clean, editorial          → TB Technical Clean

3. Which tool to use?
   └── Pick whichever is available and has quota:
       - MiniMax CLI: mmx image generate --prompt "..." --aspect-ratio 16:9
       - OpenRouter:  python adapters/openrouter_image.py "..." -o out.png -a 16:9
       - Codex CLI:   codex exec "$imagegen generate ..."
       - ChatGPT:    chat.openai.com (web UI, for reference images)
```

## Style Quick Reference

| Style | Use for |
|---|---|
| B1 Gilded Mechanism | Code, engineering, agents, tools |
| B2 Flooded Archive | Context, knowledge, memory, docs |
| B3 Observatory Throne | Agents, strategy, planning |
| B4 Star Map | Predictions, vision, overview |
| B5 Forge Below | Building, construction, crafts |
| B6 Deep Current | Data, flow, streams, pipelines |
| PS Painterly | Surreal, narrative, layered |
| TB Technical Clean | Clean editorial, diagrams |

Full prompts → `STYLES.md` | Tool invocation → `SERVICES.md`

## How to Ask Questions

Ask one clarifying question with clear choices when the content could fit multiple styles.

**Good**: "Context engineering post — B2 Flooded Archive (library/water) or B1 Gilded Mechanism (gears/systems)?"

**When not to ask**: If the content topic clearly maps to one style, just use it.

## Adding New Styles

See `docs/STYLE-TEMPLATE.md` for the template. Every style needs:
1. Name, use case, vibe description
2. Prompt template with `[YOUR SUBJECT]` placeholders
3. Service notes if relevant
4. Example output in `examples/`

## What This Skill Does

- Loads style prompts from `STYLES.md`
- Picks the best available tool from `SERVICES.md`
- Composes the full prompt with user's subject matter
- Executes generation and reports the result path

## What This Skill Does NOT Do

- Route styles to specific models — image gen is generic
- Manage file storage or versioning
- Hardcode API keys or secrets
- Generate text, video, or audio
