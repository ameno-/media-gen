# Style Template

Use this template when adding a new style to the library. Copy it to `skills/media-creation/STYLES.md` and fill in the sections.

---

## [STYLE CODE]: [Style Name]

**Use when**: [One sentence describing the content types this style fits. Be specific — "Context, knowledge, memory, documentation" not "Information stuff."]

**Vibe**: [Two to three sentences describing the visual character. What does the viewer see? What's the mood? What lighting, atmosphere, scale?]

**Prompt**:
```
[YOUR FULL PROMPT HERE. Use these conventions:

- Start with the main visual element and setting
- Integrate [YOUR SUBJECT] where your specific content fits — use "[DESCRIBE HOW]" for details
- Include atmospheric details: lighting, mood, scale
- End with style descriptors: "epic fantasy", "cinematic", "hyper-detailed"
- Include color guidance: "deep teal #2a5a6a, golden amber #d4a574"
- Always include: "No text, no logos, no futuristic elements"
- Always include: mood word at the end — "mysterious, contemplative, grand" or similar

Keep the prompt under 300 words. The model truncates long prompts.
```

**Example integration**: `[How to customize the prompt for a specific post. E.g., "For a post about context engineering, replace [YOUR SUBJECT] with: constellation diagrams and glowing index markings visible on illuminated manuscripts"]`

**Service**: [Any tool — all tools work for all styles. If one tool produces notably better results for this style, note it here. Otherwise: Any tool]

**Aspect ratio**: 16:9 (2560x1440 output) unless your style needs a different ratio

**Example output**: `examples/[style-code]-[example-name]_001.jpg`

---

## Style Naming Conventions

- **Code**: Two characters + number (e.g., B1, PS, TB)
- **Name**: Short, evocative (e.g., "The Gilded Mechanism", "The Deep Current")
- **File prefix**: `examples/[code]-[name]_001.jpg`

## Quality Checklist

Before committing a new style:

- [ ] Prompt produces epic-scale, atmospheric results
- [ ] Color palette uses ACIDBATH tokens (deep teal, dusk plum, golden amber, warm cream) or explicitly defined custom colors
- [ ] Prompt includes "No text, no logos, no futuristic elements"
- [ ] At least one example image in `examples/`
- [ ] README.md gallery is updated with the new style
- [ ] README.md quick selector is updated
- [ ] STYLE-TEMPLATE.md section above is removed after use

## Example: Adding B7

```
## B7: The Iron Garden

**Use when**: Maintenance, iteration, refinement, technical debt, ongoing work.

**Vibe**: An overgrown mechanical garden. Brass mechanisms wrapped in vines, moss-covered gears, flowers growing through broken clockwork. Peaceful decay. Ancient machinery reclaimed by nature.

**Prompt**:
```

An overgrown mechanical garden at dawn. Brass clockwork gears and copper pipes are intertwined with flowering vines and moss. [YOUR SUBJECT] — [DESCRIBE HOW] — sits at the center, half-buried in soil and flowers. A small figure tends the garden with a watering can. Warm golden light, morning mist, dew on leaves. Epic fantasy, hyper-detailed. Deep teal, golden amber, moss green. Peaceful, contemplative. No text, no logos, no futuristic elements.

```

**Example integration**: "For a post about AI maintenance, [YOUR SUBJECT] is: a small brass AI chip wrapped in flowering vines, glowing faintly"

**Service**: Any tool
```
