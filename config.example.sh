# media-gen configuration
# Copy this file to config.sh and fill in your keys.
# config.sh is in .gitignore — never commit it.

# Required for the default repo workflow:
# MiniMax CLI (mmx) powers stills, soundtrack, and TTS.
# Get key: https://www.minimaxi.com/developer
export MINIMAX_API_KEY="..."

# Optional: OpenRouter still generation via Nano Banana / Gemini 2.5 Flash Image
# Get key: https://openrouter.ai/keys
export OPENROUTER_API_KEY="sk-or-v1-..."

# Optional: OpenAI-backed image workflows / Codex batch mode
# Get key: https://platform.openai.com/api-keys
export OPENAI_API_KEY="sk-..."

# Optional: HTTP referer for OpenRouter (helps with rate limits)
export OPENROUTER_REFERER="https://github.com/your-username/media-gen"

# Optional defaults for this repo
export MEDIA_GEN_OUTPUT_DIR="./generated"
export MEDIA_GEN_MINIMAX_VOICE="English_expressive_narrator"

# Optional: point the render helper at a specific Manim interpreter
# export MANIM_PYTHON_BIN="$PWD/.venv-manim/bin/python"
