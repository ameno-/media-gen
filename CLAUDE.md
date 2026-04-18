# CLAUDE.md

This is a media generation skill library. The core skill lives in `skills/media-creation/`.

## Project Structure

- `skills/media-creation/` — The skill (SKILL.md, STYLES.md, SERVICES.md)
- `adapters/` — Standalone adapter scripts
- `docs/` — Setup and integration guides
- `config.example.sh` — API key template (copy to config.sh)

## Security

- Never commit API keys or config files
- All keys are environment variables only
- Run `source config.sh` before generating images

## Quick Commands

```bash
# Setup
cp config.example.sh config.sh
# edit config.sh with your keys
source config.sh

# Generate (OpenRouter)
python adapters/openrouter_image.py "prompt" -o output.png

# Generate (MiniMax)
mmx image generate --prompt "prompt"

# Generate (Codex)
codex exec "$imagegen generate prompt"
```

## Skill for AI Agents

When loading this project into an AI agent, point it to `skills/media-creation/SKILL.md`.
The skill handles routing to the right backend based on style — just describe what you want.
