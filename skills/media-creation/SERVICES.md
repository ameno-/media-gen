# Available Tools

Image generation is generic — the style prompt is what matters, not the tool. Pick whichever is available and has quota.

All configuration via environment variables — no keys in this repo.

## Security Model

- **Never commit API keys** — use environment variables only
- **Use `.gitignore`** — keep `config.sh` and `*.png` outputs out of version control
- **Adapter scripts are read-only** — they call APIs, they don't store secrets

---

## T1: MiniMax CLI (mmx)

**Recommended default.** Fast, simple, no batch overhead.

```bash
mmx image generate --prompt "your prompt" --aspect-ratio 16:9

# Multiple variants
mmx image generate --prompt "..." --n 4 --out-dir ./output/ --out-prefix banner

# Non-interactive (for scripts)
mmx image generate --prompt "..." --quiet --output json
```

**Options**:
- `--prompt <text>` — Image description (required)
- `--aspect-ratio <ratio>` — `16:9`, `1:1`, `9:16`, etc.
- `--n <count>` — Number of images (default: 1)
- `--out-dir <dir>` — Download directory
- `--out-prefix <prefix>` — Filename prefix
- `--quiet` — Suppress non-essential output
- `--output json` — JSON output (for scripting)
- `--subject-ref` — Subject reference for character consistency

**Install**: `npm install -g mmx` (https://www.minimaxi.com/developer)
**Model**: `image-01`
**Auth**: `mmx auth login` or set `MINIMAX_API_KEY`

---

## T2: OpenRouter

**Best for precise prompts and larger output sizes.**

```bash
OPENROUTER_API_KEY="sk-..." python adapters/openrouter_image.py \
  "your prompt" -o output.png -a 16:9 -s 2K
```

**Options**:
- `--model` — `google/gemini-2.5-flash-image-preview` (default), `google/gemini-2.0-flash-image-generation`, `black-forest-labs/flux-2-max`, `openai/gpt-5-image`
- `--aspect-ratio` — `1:1`, `16:9` (default), `9:16`, `21:9`, `4:3`, `3:4`
- `--size` — `1K` (~1024px), `2K` (~2048px, default), `4K` (~4096px)

**Get key**: https://openrouter.ai/keys

**Python API**:
```python
import sys
sys.path.insert(0, "adapters")
from openrouter_image import generate_image, ImageConfig, ImageModel, AspectRatio

config = ImageConfig(
    model=ImageModel.NANO_BANANA,
    aspect_ratio=AspectRatio.LANDSCAPE
)
result = generate_image("your prompt", "output.png", config)
```

---

## T3: Codex CLI

**Good for quick iterations in a Codex session.**

```bash
# Interactive
codex "$imagegen generate your prompt"

# Non-interactive
codex exec "$imagegen generate your prompt"

# With reference image
codex -i /path/to/reference.png "Use this as style reference: your description"
```

**Install**: https://codex.ai
**Auth**: Codex subscription, or set `OPENAI_API_KEY` for API pricing
**Batch mode**: Set `OPENAI_API_KEY`, then ask Codex to use API for batch generation

---

## T4: ChatGPT / DALL-E 3

**Use when you need reference image upload (Painterly style).**

Web UI: https://chat.openai.com

1. Attach a reference image
2. Paste prompt
3. Download result

**Python API**:
```python
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="Your prompt",
    size="1792x1024",
    quality="standard",
    n=1
)
```

**Auth**: `OPENAI_API_KEY`

---

## When to Use What

| Situation | Tool |
|---|---|
| Quick banner, batch generation | MiniMax CLI (mmx) |
| Larger output (4K), precise control | OpenRouter |
| Iterating in a Codex session | Codex CLI |
| Reference image upload needed | ChatGPT web UI |

**Fallback chain**: MiniMax → OpenRouter → Codex → ChatGPT

If one tool is down or quota-exhausted, move to the next in the list. The style prompt does the work — the tool is interchangeable.
