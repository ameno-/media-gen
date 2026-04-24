---
name: diagram-creation
description: |
  Create professional diagrams for architecture, flow, timeline, state, and concept explanation.
  Use when: a pack or article needs a diagram artifact, or when a video storyboard needs a
  diagram-first scene design.
---

# Diagram Creation

Use this skill for static explanatory diagrams rendered from editable source files.

## Toolchain

- **Graphviz** (`dot`) — primary render engine, produces SVG and PNG
- Source format: `.dot` (DOT language)
- Install: `brew install graphviz` (or `brew bundle` from the repo root)

## Output

- `diagrams/diagram.dot` — editable DOT source
- `outputs/diagram.svg` — primary render (vector, embeddable)
- `outputs/diagram.png` — raster export

## Diagram Types

| Type | Graphviz layout | When to use |
|---|---|---|
| Architecture | `rankdir=LR`, `dot` engine | component relationships, system overviews |
| Concept flow | `rankdir=TD`, `dot` engine | teaching progressions, idea chains |
| State machine | `rankdir=LR`, `dot` engine | finite state diagrams |
| Timeline | `rankdir=LR`, `neato` engine | chronological sequences |
| Dependency graph | `neato` or `fdp` engine | dependency maps, org charts |

## Design Rules

- Dark background: `#0f172a`
- Semantic color roles from the visual system:
  - cyan `#22d3ee` — primary/input nodes
  - amber `#fbbf24` — core/emphasis nodes
  - emerald `#34d399` — output/result nodes
  - slate `#94a3b8` — edge labels, connectors
- Monospace labels: `fontname="Menlo"`
- `style="filled,rounded"` for all nodes
- `splines=ortho` for clean right-angle edges

## Workflow

### Pack-generated starter

When a pack is built, `diagrams/diagram.dot` is written automatically with a context-appropriate
template. Edit it to match the actual architecture before rendering:

```bash
# Inspect the starter
cat generated/my-pack/diagrams/diagram.dot

# Edit to match your content
$EDITOR generated/my-pack/diagrams/diagram.dot

# Render via the pack command
python3 scripts/run_pack.py --pack-dir generated/my-pack --only diagram
```

### Direct generation (full regenerate + render)

```bash
python3 scripts/generate_diagram.py --pack-dir generated/my-pack
```

### Render-only (after manual edits)

```bash
python3 scripts/generate_diagram.py --pack-dir generated/my-pack --render-only
```

### Manual dot invocation

```bash
dot -Tsvg diagrams/diagram.dot -o outputs/diagram.svg
dot -Tpng diagrams/diagram.dot -o outputs/diagram.png
```

## Workflow Integration

Packs emit `modules/diagram-brief.md` with content context.
Use it to understand what the diagram should show before editing `diagrams/diagram.dot`.
The SVG output can be embedded directly in articles and used as a reference image in Manim scenes.
