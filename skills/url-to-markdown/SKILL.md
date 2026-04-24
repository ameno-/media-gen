---
name: url-to-markdown
description: |
  Save web content into markdown before visual processing. Use when: a workflow begins from a URL,
  article page, or source webpage that needs to be turned into a local source artifact.
---

# URL to Markdown

Source ingestion should happen before illustration, cards, or publishing transforms.

## Output

- local markdown source
- optional media download

## Workflow Integration

This skill is the best first step for article-based packs.
Feed its output into `format-markdown`, then `article-illustration`, then `markdown-to-html`.
