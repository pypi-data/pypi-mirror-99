# Drafting

Headless utilities for graphics programming in Python, meant for use in graphics programming environments like Coldtype, DrawBot, Blender, or hardware drawing machines like AxiDraw.

## Features

- Geometric primitives (`drafting/geometry`) for slicing & dicing rectangles (CGGeometry-inspired)
- Color primitives for easy color manipulation (`drafting/color`)
- Fluent-programming `RecordingPen` subclass (`drafting/pens`) with common pen operations & a DrawBot variant (`drafting/pens/drawbotpen`)
- Line-oriented text-setting primitives, based on HarfBuzz-via-FontGoggles (`drafting/text/reader`)
- DrawBot-specific integration shortcuts (`drafting/drawbot`)
- Symbolic shorthand language for vector-drawing-from-code (APL-inspired) (`drafting/sh`)

All-in-all, a mess of bizarre features inspired by a mess of bizarre influences, but features that I use regularly via [Coldtype](https://coldtype.goodhertz.com), which is currently being refactored to use this library as a directy dependency.

An example? Sure here's an example:

```python
import drafting.drawbot as dr
from drafting.text.richtext import RichText

f1 = dr.Font.Cacheable("~/Type/fonts/fonts/ObviouslyVariable.ttf")
r = dr.page_rect()

rt = (RichText(r,
        "DRAF[high]/TING", {
        "default": dr.Style(f1, 200,
            wght=0.25,
            wdth=0.15,
            slnt=1,
            fill=dr.bw(0.2)),
        "high": dr.Style(f1, 250,
            ro=1,
            wdth=0.25,
            wght=1,
            tu=-50, # tracking-in-units
            fill=dr.hsl(0.9, 0.9, 0.8),
            stroke=dr.hsl(0.55, 0.9, 0.4),
            strokeWidth=5)},
        invisible_boundaries="/")
    .xa() # center each line
    .align(r)
    .chain(dr.dbdraw))
```


## Why?

All formerly part of [Coldtype](https://coldtype.goodhertz.com), but broken out into an independent library for easier integration in programs like DrawBot and (in the future) Blender.

## Acknowledgments

* ``drafting.fontgoggles`` contains parts of the `FontGoggles <https://github.com/justvanrossum/fontgoggles>`_ codebase, written by Just van Rossum, Copyright (c) 2019 Google, LLC. Just is also responsible for DrawBot which the main inspiration behind this project.

* ``drafting.text`` relies heavily (via FontGoggles) on the incredible `HarfBuzz <https://github.com/harfbuzz/harfbuzz>`_ text shaping library.

* ``drafting.pens.outlinepen`` contains code written by Frederik Berlaen, Copyright (c) 2016

* ``drafting.pens.translationpen`` contains code written by Loïc Sander, Copyright (c) 2014
