---
name: lesson-pack
description: |
  Build teaching and educational media packs for explainers, tutorials, and workshops.
  Use when: lesson launch, concept explainer, tutorial visuals, internal training, course media.
---

# Lesson Pack

Teaching work needs a structured output set.

## Deliverables

- cover image
- lesson diagram
- concept card
- narration
- soundtrack
- storyboard
- manim plan/script

## Workflow

1. Define the concept, audience, and learning outcome.
2. Build the pack skeleton:

```bash
python3 scripts/build_media_pack.py \
  --pack lesson \
  --title "Lesson title" \
  --brief "What the learner should understand by the end." \
  --subject "main concept visualized"
```

3. Review `storyboard.md` and prompt files.
4. Use `run_pack.py` to dry-run or execute the integrated workflow.

## Routing

- stills -> `mmx image`
- narration -> `mmx speech`
- soundtrack -> `mmx music`
- video -> `manim-video`
- final assembly -> `motion-edit`
