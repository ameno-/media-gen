# Style Library

All available style families and their full generation prompts. Customize the prompts — they're templates, not rules.

---

## WHIMSICAL (DEFAULT)

Warm, literary, historical fantasy. Five distinct variants — pick based on the narrative character of the content.

**Color palette (all whimsical variants)**:
```
Golden amber:   #d4a574
Sandy ochre:    #c9a86c
Deep teal:      #2a5a6a
Soft cyan:      #6a9aaa
Dusk plum:      #8a5a6a
Warm beige:      #e8dcc4
Aged parchment:  #f5f0e6
```

**Never**: neon, cyberpunk, electric blue, tech HUD, circuit boards, holograms, glitch art

---

### W1: Guild Ledger (Medieval Illuminated Manuscript)

**Use when**: Content has a sense of tradition, craft, guild organization, or scholarly record-keeping.

**Prompt**:
```
Enchanted illuminated manuscript page showing [YOUR SUBJECT]. The page has aged
parchment texture with ornate medieval borders. [DESCRIBE YOUR ELEMENTS] as
illuminated text and icons. A golden thread (NOW line) runs vertically down
the right edge like a bookmark with a glowing gem. Header: ornate calligraphic
[TITLE]. Medieval illuminated manuscript style (Très Riches Heures du Duc de Berry),
warm amber and gold on aged parchment, visible ink strokes, marginalia decorations,
wax seals with emblems, deep teal and plum accents. Scholarly magic mood.
```

**Service**: Codex CLI ($imagegen) or MiniMax CLI (mmx)
**Size**: 1536x1024 (16:9)

---

### W2: Clockwork Mechanism (Victorian Steampunk)

**Use when**: Content involves precision, timing, mechanical systems, or industrial-age aesthetics.

**Prompt**:
```
Victorian steampunk clockwork mechanism representing [YOUR SUBJECT]. Grand brass
and copper construction with visible gears, springs, and pneumatic tubes.
[DESCRIBE YOUR ELEMENTS] as mechanical tokens on brass rails. NOW line is a
silver chronometer beam. Dark workshop background with hanging oil lamps,
blueprints on walls, warm forge glow. Victorian steampunk, brass and copper
with warm amber light, rivets and gears, steam and mechanical precision.
```

**Service**: Codex CLI ($imagegen) or MiniMax CLI (mmx)
**Size**: 1536x1024 (16:9)

---

### W3: Constellation Map (Celestial Cartography)

**Use when**: Content spans time, has cosmic scope, or involves mapping unknown territory.

**Prompt**:
```
Celestial star chart on deep indigo night sky showing [YOUR SUBJECT] as
constellation paths. [DESCRIBE YOUR ELEMENTS] as connected star formations.
NOW line: celestial equator - glowing band dividing 'what was' from 'what
will be'. Deep space with nebulae, cosmic dust. Astronomy chart meets
fantasy constellation art. Rich indigo, gold, amber, teal. Cosmic wonder mood.
```

**Service**: Codex CLI ($imagegen) or MiniMax CLI (mmx)
**Size**: 1536x1024 (16:9)

---

### W4: Enchanted Loom (Folk-Art Magical)

**Use when**: Content involves weaving together threads, craftsmanship, or textile metaphors.

**Prompt**:
```
Grand magical medieval loom where [YOUR SUBJECT] is being woven into tapestry.
Dark wood frame with carved runes. [DESCRIBE YOUR ELEMENTS] as horizontal
threads with different colors and states. NOW line: gleaming silver shuttle
actively weaving. Completed tapestry sections glow; unfinished portion is
shadowy/hazy. Cozy workshop background with candles, starlit window, magical
particles floating. Folk-art magical realism, warm candlelight, rich fabrics.
Craftsman warmth mood.
```

**Service**: Codex CLI ($imagegen) or MiniMax CLI (mmx)
**Size**: 1536x1024 (16:9)

---

### W5: Navigator's Chart (Age of Exploration)

**Use when**: Content involves journey, discovery, venturing into unknown waters, or maritime metaphors.

**Prompt**:
```
Weathered nautical sea chart (age of exploration style) showing [YOUR SUBJECT]
as sea voyage. Parchment texture, compass roses, sea monsters in margins.
[DESCRIBE YOUR ELEMENTS] as shipping lanes with vessels in different states
(sails, anchored, etc.). NOW line is prime meridian - golden line dividing
known waters from uncharted. Completed milestones as islands with flags.
Age of exploration cartography with magical sea charts, sepia and aged parchment,
hand-drawn ink illustrations, decorative compass roses. Adventure mood.
```

**Service**: Codex CLI ($imagegen) or MiniMax CLI (mmx)
**Size**: 1536x1024 (16:9)

---

## HM: Historical Mysticism

**Use when**: Scholarly, ancient knowledge, observatory, library themes.

**Aesthetic**: Ancient observatories, scholars, scrolls, stone architecture. Golden hour, candlelight, atmospheric haze.

**Prompt framework**:
```
[YOUR SUBJECT] in the style of historical mysticism: ancient observatory interiors
or stone library chambers, scholars in robes working by candlelight, astronomical
instruments, aged scrolls and manuscripts, grand archways revealing candlelit
chambers, golden hour light streaming through stone windows. Warm amber lantern
glow, dusty golden beams, atmospheric haze. Deep teal and dusk plum shadows.
Scholarly, contemplative, discovery mood. Medieval/Renaissance scholarly aesthetic.
Rich warm tones, soft atmospheric lighting, deep shadows. NO cyberpunk, NO neon,
NO tech HUD, NO futuristic elements.
```

**Reference colors**:
- Golden amber: #d4a574
- Sandy ochre: #c9a86c
- Deep teal: #2a5a6a
- Dusk plum: #8a5a6a
- Aged parchment: #f5f0e6

**Service**: OpenRouter (Nano Banana) via `adapters/openrouter_image.py`
**Size**: 2560x1440 (banner) or 1536x864 (16:9)

---

## PS: Painterly / Surrealist

**Use when**: Cinematic narrative, deep concept pieces, surreal over-under compositions.

**Aesthetic**: Albert Bierstadt landscapes + Zdzisław Beksiński surrealism + Hayao Miyazaki intricacy. Split-level over-under composition. Stippled texture, visible oil paint brushwork. Maximalist Victorian/steampunk architecture. Chiaroscuro lighting — golden internal glow vs dark water.

**Prompt framework**:
```
Top-down cross-sectional over-under view of [YOUR SCENE].

**Surface Level (upper 2/3):**
[Describe the surface world — river, boats, sky, light]

**Below the Surface (bottom 1/3, visible through translucent water):**
[Describe the hidden world beneath — architecture, activity, glow]

**Distant focal point:**
[Describe the distant landmark]

**Style Reference:**
- Maximalist Victorian/steampunk architecture
- Stippled texture with floating embers/dust motes
- Chiaroscuro lighting — golden internal glow vs dark water
- Atmospheric perspective — hazy distant mountains
- Painterly oil paint aesthetic with visible brushwork
- Burnt orange #d4a574, amber #c9a86c, deep indigo #2a5a6a, dusk plum #8a5a6a

**Constraints:**
- NO cyberpunk, NO neon, NO futuristic tech
- NO circuit boards, NO holograms, NO HUD elements
- YES to steampunk, Victorian, mythic, surrealist
- YES to painterly textures, stippling, visible brushwork
```

**Reference image required**: Upload a reference image that matches the aesthetic you want as a style guide. (The style reference above describes the ideal look.)

**Service**: ChatGPT + reference image upload (web UI)
**Size**: 1536x864 (16:9) or 2560x1440 (banner)

---

## TB: Technical Blog

**Use when**: Clean banners, technical diagrams, data cards, editorial illustrations.

**Prompt framework**:
```
[YOUR SUBJECT] in a clean technical blog style: clear composition, legible at
small sizes, brand-consistent colors. [DESCRIBE THE CONTENT]. Professional,
modern, minimal decorative elements. [YOUR BRAND COLORS if applicable]. No
background clutter, suitable for blog header use.
```

**Design tokens example** (adapt to your brand):
- Accent: #8a5a6a (dusk plum)
- Foreground: #2a2a28 (near-black)
- Background: warm cream or transparent

**Service**: OpenRouter (Nano Banana) via `adapters/openrouter_image.py`
**Size**: 2560x1440 (banner) or 1536x864 (16:9)

---

## Quick Style Selector

| Content character | Style |
|---|---|
| Traditional, craft, guild | W1 Guild Ledger |
| Precision, timing, machinery | W2 Clockwork Mechanism |
| Cosmic scope, mapping unknown | W3 Constellation Map |
| Weaving, textile, craft | W4 Enchanted Loom |
| Journey, voyage, discovery | W5 Navigator's Chart |
| Ancient knowledge, scholars | HM Historical Mysticism |
| Cinematic, surreal, painterly | PS Painterly / Surrealist |
| Technical blog, diagrams | TB Technical Blog |
| Not specified, no strong aesthetic signal | Whimsical → ask which variant |
