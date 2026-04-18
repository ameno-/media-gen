# media-gen configuration
# Copy this file to config.sh and fill in your keys.
# config.sh is in .gitignore — never commit it.

# OpenRouter — image generation via Nano Banana / Gemini 2.5 Flash Image
# Get key: https://openrouter.ai/keys
export OPENROUTER_API_KEY="sk-or-v1-..."

# OpenAI — Codex CLI batch mode / DALL-E API
# Get key: https://platform.openai.com/api-keys
export OPENAI_API_KEY="sk-..."

# MiniMax — MiniMax CLI (mmx)
# Get key: https://www.minimaxi.com/developer
export MINIMAX_API_KEY="..."

# Optional: HTTP referer for OpenRouter (helps with rate limits)
export OPENROUTER_REFERER="https://github.com/your-username/media-gen"

# Optional: default output directory
# export MEDIA_GEN_OUTPUT_DIR="./generated"
