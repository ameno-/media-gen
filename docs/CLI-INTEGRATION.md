# CLI Integration Guide

## Letta Code

### Installation

```bash
cp -r skills/media-creation ~/.letta/skills/
```

### Loading the Skill

When you start a Letta session and want to generate images:

```
Load the media-creation skill.
```

Or if your Letta supports skill invocation by name:

```
/media-creation
```

The skill file `SKILL.md` is read by Letta and its routing logic becomes available.

### How It Works in Letta

1. Letta loads `SKILL.md` from `~/.letta/skills/media-creation/`
2. SKILL.md references `STYLES.md` and `SERVICES.md` (same directory)
3. You describe what you want to generate
4. The skill routes to the appropriate backend based on style
5. The skill executes via the adapter or native CLI

### Letting Letta Handle the Aesthetic

The whole point: you say "generate a banner" and Letta knows:
- Whimsical = default
- Whimsical → Codex CLI
- Codex handles the generation

No re-explaining the aesthetic every session.

---

## Claude Code

### Installation

```bash
cp -r skills/media-creation ~/.claude/skills/
```

### Usage

Claude Code will discover the skill and you can invoke it as:

```
/media-creation
```

Or load it in context and use it generically.

---

## Direct CLI Usage (No Agent)

### OpenRouter

```bash
python adapters/openrouter_image.py "A curious alchemist" -o output.png

# With options
python adapters/openrouter_image.py "A curious alchemist" \
  -o output.png \
  -m google/gemini-2.5-flash-image-preview \
  -a 16:9
```

### MiniMax CLI

```bash
mmx image generate --prompt "A curious alchemist" --aspect-ratio 16:9

# Save to specific location
mmx image generate \
  --prompt "A curious alchemist" \
  --out-dir ./banners \
  --out-prefix alchemist \
  --aspect-ratio 16:9
```

### Codex CLI

```bash
# Interactive
codex "$imagegen generate a curious alchemist banner"

# Non-interactive
codex exec "$imagegen generate a curious alchemist banner"
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | For OpenRouter | Get from openrouter.ai/keys |
| `OPENAI_API_KEY` | For Codex batch / DALL-E | Get from platform.openai.com/api-keys |
| `MINIMAX_API_KEY` | For mmx auth | Get from minimaxi.com/developer |

All are optional — you only need the key for the backend you're using.
