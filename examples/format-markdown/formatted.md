# Ai agents and media generation

So basically what happens is you give the agent a brief. It reads it. Then it decides what tools to use. Like maybe it needs an image or a video or some music. The agent picks the right skill and runs it.

## The tools

Theres a bunch of tools:
- image generation (mmx image)
- music (mmx music)
- narration with tts (mmx speech)
- diagrams with graphviz
- video with manim
- stitching with ffmpeg

## How it works

The agent gets a brief like "make a lesson about context routing". It figures out the style (flooded archive maybe). It writes prompts. It runs commands. It assembles the outputs.

Its actually pretty simple once you see the pattern. Brief goes in, pack comes out.

## Things to know

- dont use mmx video in this repo
- always dry run first
- check your keys before starting
- LaTeX needs to be installed for math scenes