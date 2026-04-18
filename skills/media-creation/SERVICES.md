# Service Abstraction Layer

Four image generation backends. Style determines which one to use. All configuration via environment variables — no keys in this repo.

## Security Model

- **Never commit API keys** — use environment variables only
- **Use `.gitignore`** — keep `config.sh` and `*.png` outputs out of version control
- **Adapter scripts are read-only** — they call APIs, they don't store secrets

---

## Service → Style Routing Table

| Style Family | Primary Service | Fallback |
|---|---|---|
| Whimsical (all 5 variants) | Codex CLI | MiniMax CLI (mmx) |
| Historical Mysticism | OpenRouter (Nano Banana) | MiniMax CLI (mmx) |
| Painterly / Surrealist | ChatGPT + reference | MiniMax CLI (mmx) |
| Technical Blog | OpenRouter (Nano Banana) | MiniMax CLI (mmx) |
| Any (when primary unavailable) | MiniMax CLI (mmx) | Codex CLI |

---

## S1: OpenRouter (Nano Banana / Gemini 2.5 Flash Image)

**Adapter**: `adapters/openrouter_image.py`
**Env var**: `OPENROUTER_API_KEY`

### Quick invoke

```bash
OPENROUTER_API_KEY="sk-..." python adapters/openrouter_image.py \
  "Your prompt here" -o output.png -a "16:9"
```

### Programmatic (Python)

```python
import sys
sys.path.insert(0, "adapters")
from openrouter_image import generate_image, ImageConfig, ImageModel, AspectRatio

config = ImageConfig(
    model=ImageModel.NANO_BANANA,
    aspect_ratio=AspectRatio.LANDSCAPE
)
result = generate_image("Your prompt", "output.png", config)
print(result.file_path)
```

### Options

**Models**:
- `NANO_BANANA` = `google/gemini-2.5-flash-image-preview` (default)
- `NANO_BANANA_PRO` = `google/gemini-2.0-flash-image-generation`
- `FLUX_MAX` = `black-forest-labs/flux-2-max`
- `GPT5_IMAGE` = `openai/gpt-5-image`

**Aspect ratios**: `1:1`, `16:9` (default), `9:16`, `21:9`, `9:21`, `4:3`, `3:4`

**Sizes**: `1K` (~1024px), `2K` (~2048px), `4K` (~4096px)

**Get an API key**: https://openrouter.ai/keys

**Known limitations**: Text/spelling errors, complex layouts can break.

---

## S2: Codex CLI (gpt-image-1.5)

**CLI**: `codex` (OpenAI Codex CLI — https://codex.ai)
**Env var**: `OPENAI_API_KEY` (for batch/API mode)

### Interactive (recommended)

```bash
codex "$imagegen generate a whimsical guild ledger banner..."
```

### Non-interactive exec

```bash
codex exec "$imagegen generate your prompt here"
```

### In a specific directory

```bash
codex --cd ./my-project "$imagegen generate a banner for..."
```

### With reference image

```bash
codex -i /path/to/reference.png "Use this as style reference: your description"
```

### Batch mode (API pricing applies)

Set `OPENAI_API_KEY` in your environment, then ask Codex to use the API:
```
"Generate 4 whimsical banner variants via the API using this prompt..."
```

**Costs**:
- Included in Codex subscription: counts 3-5x faster against usage limits
- With `OPENAI_API_KEY`: API pricing applies instead — use for batch generation

---

## S3: MiniMax CLI (mmx)

**CLI**: `mmx` (MiniMax CLI — https://www.minimaxi.com/developer)
**Env var**: `MINIMAX_API_KEY` (or `mmx auth login`)

### Installation

```bash
npm install -g mmx
# or: curl -fsSL https://... | sh
```

### Image generation

```bash
# Basic
mmx image generate --prompt "your prompt" --aspect-ratio 16:9

# Multiple variants
mmx image generate --prompt "..." --n 4 --out-dir ./output/ --out-prefix my-banner

# Non-interactive (for scripts)
mmx image generate --prompt "..." --quiet --output json
```

### Options

- `--prompt <text>` — Image description (required)
- `--aspect-ratio <ratio>` — `16:9`, `1:1`, `9:16`, etc.
- `--n <count>` — Number of images (default: 1)
- `--out-dir <dir>` — Download directory
- `--out-prefix <prefix>` — Filename prefix
- `--quiet` — Suppress non-essential output
- `--output json` — JSON output (for scripting)
- `--subject-ref` — Subject reference for character consistency

**Model**: `image-01` (MiniMax's image generation model)

---

## S4: ChatGPT / DALL-E 3

**Web UI**: https://chat.openai.com
**API**: `OPENAI_API_KEY`

### Interactive (web UI)

1. Go to chat.openai.com
2. Attach a reference image (Painterly/Surrealist style)
3. Paste prompt
4. Download result

### With reference image

Upload your reference, then prompt: "Use this as the aesthetic style guide: [description]"

### API (Python)

```python
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="Your prompt",
    size="1792x1024",  # or "1024x1024", "1024x1792"
    quality="standard",
    n=1
)
print(response.data[0].url)
```

**Best for**: Painterly/Surrealist style (requires reference image upload — only web UI supports this well)

---

## Decision Summary

```
Is this Whimsical style?
├── Yes → Codex CLI (subscription covers it)
└── No → Is it Painterly/Surrealist?
    ├── Yes → ChatGPT + reference image upload
    └── No → Is it Technical Blog?
        ├── Yes → OpenRouter (Nano Banana)
        └── No → Is it Historical Mysticism?
            ├── Yes → OpenRouter (Nano Banana)
            └── No → Codex CLI (default)
```

**When unsure**: Default to Codex CLI. Codex handles most styles well and is covered by most subscriptions.
**When Codex/OpenRouter unavailable**: Fall back to MiniMax CLI (`mmx image generate`).
