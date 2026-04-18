# media-gen

One skill, multiple image generation backends, whimsical default aesthetic.

A shared image generation system for AI coding agents. Route to the right backend (OpenRouter, Codex CLI, MiniMax CLI, ChatGPT) without re-explaining the aesthetic every session.

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/ameno-/media-gen.git
cd media-gen
cp config.example.sh config.sh
# Edit config.sh with your API keys

# 2. Source your config
source config.sh

# 3. Generate an image
# OpenRouter
python adapters/openrouter_image.py "A whimsical alchemist's workshop" -o output.png

# MiniMax
mmx image generate --prompt "A whimsical alchemist's workshop" --aspect-ratio 16:9

# Codex
codex exec "$imagegen generate a whimsical alchemist's workshop"
```

## What You Get

- **`SKILL.md`** — The skill file. Load it into any AI agent (Letta, Claude Code, etc.) and it routes generation to the right backend automatically.
- **`STYLES.md`** — 9 style families with full prompts (Whimsical default, plus Historical Mysticism, Painterly/Surrealist, Technical Blog)
- **`SERVICES.md`** — How to call each backend
- **`adapters/`** — Standalone adapter scripts (no external dependencies beyond httpx)

## The Skill System

The core idea: prompts and routing live in the skill, not in your head.

```
You: "generate a banner for my post"
Agent loads: SKILL.md
Agent checks: Whimsical = default → Codex CLI
Agent asks: "Which Whimsical variant — illuminated, steampunk, celestial, folk-art, or nautical?"
You: "illuminated"
Agent uses: Guild Ledger prompt from STYLES.md → Codex CLI
```

No re-explaining. No prompting the aesthetic from scratch every time.

## Style Families

| Style | Character | Backend |
|---|---|---|
| **Whimsical** (5 variants) | Historical fantasy, warm literary | Codex CLI |
| Historical Mysticism | Ancient observatories, scholars | OpenRouter |
| Painterly / Surrealist | Bierstadt meets Beksiński | ChatGPT + reference |
| Technical Blog | Clean, brand-consistent | OpenRouter |

See [`skills/media-creation/STYLES.md`](skills/media-creation/STYLES.md) for full prompts.

## AI Agent Integration

### Letta Code

Copy `skills/media-creation/` to your Letta skills directory:

```bash
cp -r skills/media-creation ~/.letta/skills/
```

The skill loads `STYLES.md` and `SERVICES.md` from the same directory.

### Claude Code

Copy to your Claude Code skills:

```bash
cp -r skills/media-creation ~/.claude/skills/
```

Invoke: `/media-creation` or load it as a general skill.

### Other Agents

The skill files are plain Markdown. Any agent that supports custom skills can load them. The key files:

1. **`SKILL.md`** — Entry point, routing logic, defaults
2. **`STYLES.md`** — All style prompts
3. **`SERVICES.md`** — How to call each backend

## Security

**No API keys in this repo.** All keys are environment variables.

```
OPENROUTER_API_KEY   # OpenRouter image generation
OPENAI_API_KEY       # Codex CLI batch mode / DALL-E API
MINIMAX_API_KEY      # MiniMax CLI
```

Copy `config.example.sh` → `config.sh`, fill in your keys, **never commit `config.sh`**.

See [`.gitignore`](.gitignore) for everything that stays out of version control.

## File Structure

```
media-gen/
├── README.md
├── LICENSE
├── .gitignore
├── config.example.sh      # Template — copy to config.sh, fill in keys
├── skills/
│   └── media-creation/
│       ├── SKILL.md       # Routing logic, defaults, entry point
│       ├── STYLES.md      # All 9 style families with prompts
│       └── SERVICES.md    # How to call each backend
├── adapters/
│   └── openrouter_image.py  # Standalone OpenRouter adapter
└── docs/
    ├── SETUP.md           # Detailed setup guide
    └── CLI-INTEGRATION.md # Agent-specific setup
```

## License

MIT — use it, adapt it, make it yours.
