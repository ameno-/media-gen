---
name: markdown-to-html
description: |
  Convert markdown into styled HTML for publishing and review. Use when: article or pack outputs
  need HTML delivery, email-ready formatting, or previewable long-form layouts.
---

# Markdown to HTML

This is the publishing transform, not the content authoring step.

## Output

- styled HTML from markdown
- optional theme selection
- preview or publish-ready artifact

## Workflow Integration

Use after `format-markdown` and `article-illustration`.
Packs should emit `modules/publishing-brief.md` when the final deliverable includes article pages or embed-ready HTML.
