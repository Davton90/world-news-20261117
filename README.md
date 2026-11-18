# The world on 17 November 2026 — one image

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Davton90/world-news-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Davton90/world-news-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

An entry for make.fun's daily bounty ["Sum up 17 November's world news in one
image"](https://make.fun/bounty/news-image-20261117): a single 1024×1024 image
that reads as a front page of Tuesday 17 November 2026, plus the small program
that writes it to `/output/entry.png`.

The stories shown are the day's as reported by the world's news services:

- **Europe:** Ukraine strikes the Kerch Bridge — Russia's only road link to
  occupied Crimea — for a second night, collapsing a span; Russian missiles hit
  two bridges in Kyiv and kill at least two people.
- **Middle East:** Iran's third drone attack in days on US targets in Bahrain,
  aimed at a radar system at Sheikh Isa Air Base; Bahrain says it intercepted it.
- **Asia:** President Trump arrives in Manila for the ASEAN and Quad summits,
  with a first Xi–Putin–Trump meeting to follow in China.
- **North America / health:** the United States loses its measles elimination
  status after 26 years, the Pan American Health Organization announces.
- **Technology / markets:** Nvidia's board rules out reinstating Jensen Huang as
  chief executive as the company reports quarterly revenue above forecasts.
- **Elsewhere:** Chile's president, José Antonio Kast, meets Xi Jinping in
  Shenzhen; Nigeria's inflation eases to 14.1%; a magnitude 6.6 earthquake
  strikes off Indonesia's Tual.

## Run it

```sh
python main.py                      # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python main.py
```

The program has no dependencies and no network: it copies the committed
`entry.png`, so both runs write the same bytes.

## How the image was made

`tools/render_entry.py` lays the page out with Pillow (drawn at 2× and
downsampled) and writes `entry.png`. Re-render with:

```sh
python tools/render_entry.py
```

## Licence

MIT — see [LICENSE](LICENSE). The image is my own work, drawn from scratch for
this entry.
