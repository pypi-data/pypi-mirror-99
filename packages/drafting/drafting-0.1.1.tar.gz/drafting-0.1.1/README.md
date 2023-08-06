# Drafting

## Features

- Geometric primitives (`drafting/geometry`)
- Color primitives for easy color manipulation (`drafting/color`)
- Fluent-programming `RecordingPen` subclass (`drafting/pens`) with common pen operations & a DrawBot variant (`drafting/pens/drawbotpen`)
- Symbolic shorthand language for vector-drawing-from-code (APL-inspired) (`drafting/sh`)


## Why?

All formerly part of [Coldtype](https://coldtype.goodhertz.com), but broken out into an independent library for easier integration in programs like DrawBot and (in the future) Blender.

## Acknowledgments

* ``drafting.fontgoggles`` contains parts of the `FontGoggles <https://github.com/justvanrossum/fontgoggles>`_ codebase, written by Just van Rossum, Copyright (c) 2019 Google, LLC. Just is also responsible for DrawBot which the main inspiration behind this project.

* ``drafting.text`` relies heavily (via FontGoggles) on the incredible `HarfBuzz <https://github.com/harfbuzz/harfbuzz>`_ text shaping library.

* ``drafting.pens.outlinepen`` contains code written by Frederik Berlaen, Copyright (c) 2016

* ``drafting.pens.translationpen`` contains code written by Loïc Sander, Copyright (c) 2014
