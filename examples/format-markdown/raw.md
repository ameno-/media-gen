# ai agents and media generation

so basically what happens is you give the agent a brief. it reads it. then it decides what tools to use. like maybe it needs an image or a video or some music. the agent picks the right skill and runs it.

## the tools

theres a bunch of tools:
- image generation (mmx image)
- music (mmx music)
- narration with tts (mmx speech)
- diagrams with graphviz
- video with manim
- stitching with ffmpeg

## how it works

the agent gets a brief like "make a lesson about context routing". it figures out the style (flooded archive maybe). it writes prompts. it runs commands. it assembles the outputs.

its actually pretty simple once you see the pattern. brief goes in, pack comes out.

## things to know

- dont use mmx video in this repo
- always dry run first
- check your keys before starting
- LaTeX needs to be installed for math scenes
