#!/usr/bin/env python3
"""Publish the finished news sheet into the grader's output directory.

All of the drawing happened while the entry was being built. This program has
one job: place the committed bitmap where the harness looks for it, using only
the standard library and writing exactly the same bytes on every invocation.
"""

import os
from shutil import copyfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ART = os.path.join(HERE, "entry.png")

if not os.path.isfile(ART):
    raise RuntimeError("the news sheet bitmap is missing from the snapshot")

os.makedirs(OUT, exist_ok=True)
copyfile(ART, os.path.join(OUT, "entry.png"))
print("published the news sheet to", OUT)
