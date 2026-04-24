# Visual System

Shared design system for stills, diagrams, cards, article illustration, and Manim scenes.

## Principles

- Clarity before ornament
- Dark backgrounds with controlled color accents
- Layered opacity for focus
- Prompt-file-first reproducibility
- Consistent typography across still and motion assets

## Core Palette

| Token | Hex | Use |
|---|---|---|
| `bg.deep` | `#0f172a` | global background |
| `bg.panel` | `#12141A` | cards, video backdrops |
| `primary.cyan` | `#22d3ee` | user-facing, highlight, active |
| `secondary.emerald` | `#34d399` | processing, system health |
| `accent.amber` | `#fbbf24` | emphasis, callouts, CTA |
| `alert.rose` | `#fb7185` | risk, warning, contrast |
| `muted.slate` | `#94a3b8` | support copy, connectors |
| `ink.white` | `#EAEAEA` | main text |

## Typography

- Monospace for diagrams and Manim labels: `Menlo`, `JetBrains Mono`, `SF Mono`
- Editorial sans for image prompts when text is implied but not rendered
- Minimum on-canvas readable label size: `18px`

## Composition Rules

- One visual thesis per frame
- Primary object at 1.0 emphasis
- Supporting objects at 0.35-0.6 emphasis
- Structural lines/grids at 0.12-0.2 emphasis
- Leave 20-30 percent negative space for overlays or motion

## Capability Mapping

| Capability | Primary Use | Shared System Requirement |
|---|---|---|
| Cover image | hero stills, article headers | title hierarchy, anchor object, negative space |
| Diagram | architecture, flow, concept maps | grid, semantic color roles, legible connectors |
| Image cards | social sequences, swipe decks | sequence consistency, prompt-file chain |
| Article illustration | in-article visuals | position-aware purpose, article-specific labels |
| Markdown to HTML | publishing output | preserve visual hierarchy from source markdown |
| Compress image | delivery optimization | final export only |
| URL to markdown | source ingestion | save source before visual generation |

## Pack Usage

Every pack should emit:

- a cover-image brief
- a diagram brief
- an image-card brief
- an article-illustration brief
- a publishing brief

These briefs should inherit the same palette, typography, and emphasis model.
