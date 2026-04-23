---
name: imagine-backend
description: |
  Optional multi-provider image generation backend with prompt-file-first and batch support.
  Use when: a workflow needs more than the default mmx still lane, especially for reference-image
  support, provider switching, or stable batch throughput.
---

# Imagine Backend

This is an optional still-image backend layer.

## Why It Exists

- prompt-file-first generation
- batch execution from saved prompts
- multiple providers and model routing
- reference-image capable still workflows

## Default Position

Keep `mmx` as the simplest default still backend for this repo.
Use this skill when the workflow needs:

- reference-image editing
- non-MiniMax providers
- batch still generation from multiple prompt files
- provider-specific image models

## Workflow Integration

Pairs well with:

- `cover-image`
- `image-cards`
- `article-illustration`

Recommendation: integrate as an optional backend, not as the only image path.
