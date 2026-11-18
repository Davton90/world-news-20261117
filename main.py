"""make.fun entry — "Sum up 17 November's world news in one image".

The image is entry.png beside this file: a front page of the day's news laid out
as a newspaper (25 stories: the Kerch Bridge strike, Iran and the US trading
blows around the Gulf, Trump's Quad summit in Manila, the US losing its
measles-free status, Nvidia's results, the COP31 draft, and briefs from six
continents), drawn by tools/render_entry.py and committed as the bytes to
submit.

The program runs twice and must write the same bytes both times, so it only
copies the committed image to /output/entry.png. Outside the grader's
container, MAKEFUN_OUTPUT_DIR stands in for /output:

    python main.py            # writes /output/entry.png
    MAKEFUN_OUTPUT_DIR=out python main.py
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")
