# Setup Guide

## Prerequisites

At least one of:
- **OpenRouter API key** — https://openrouter.ai/keys (for Nano Banana / Gemini 2.5 Flash Image)
- **OpenAI API key** — https://platform.openai.com/api-keys (for Codex CLI or DALL-E)
- **MiniMax CLI** — `npm install -g mmx` (https://www.minimaxi.com/developer)

You don't need all three. Start with one.

---

## Step 1: Clone and Configure

```bash
git clone https://github.com/ameno-/media-gen.git
cd media-gen
cp config.example.sh config.sh
```

Edit `config.sh` and add your API key(s). Do not commit `config.sh`.

```bash
# In config.sh
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

---

## Step 2: Source Your Config

```bash
source config.sh
# Or add to your .bashrc / .zshrc:
echo 'source /path/to/media-gen/config.sh' >> ~/.zshrc
```

---

## Step 3: Test the Adapter

```bash
# Test OpenRouter
python adapters/openrouter_image.py "A small glowing flask" -o test.png

# Test MiniMax (if installed)
mmx image generate --prompt "A small glowing flask" --aspect-ratio 1:1

# Test Codex (if installed)
codex exec "$imagegen generate a small glowing flask"
```

---

## Step 4: Install in Your AI Agent

### Letta Code

```bash
cp -r skills/media-creation ~/.letta/skills/
```

Restart your Letta session or trigger a recompile. The skill loads automatically when invoked.

### Claude Code

```bash
cp -r skills/media-creation ~/.claude/skills/
```

Use `/media-creation` or it loads as a general skill.

---

## Dependencies

The OpenRouter adapter requires only `httpx`:

```bash
pip install httpx
# or
uv pip install httpx
```

No other dependencies.

---

## Troubleshooting

### "OPENROUTER_API_KEY not set"

You forgot to source your config:
```bash
source config.sh
```

### "Rate limit exceeded"

You've hit OpenRouter's rate limit. Wait a moment, or use Codex CLI or MiniMax CLI as a fallback.

### Codex CLI not generating images

Make sure you're in a Codex session with image generation enabled. Use `codex --help` to verify installation.
