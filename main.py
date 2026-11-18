"""make.fun entry — "Sum up 17 November's world news in one image".

The image is entry.png beside this file: a hand-set front page of the day's
news (Kerch Bridge strike, Iran's strike on a US radar in Bahrain, Trump's
Asia trip, the US losing measles-free status, Nvidia's board refusing its
ex-CEO), drawn by tools/render_entry.py and committed as the bytes to submit.

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
