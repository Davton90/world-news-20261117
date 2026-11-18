# The world on 17 November 2026 — one image

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Davton90/world-news-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Davton90/world-news-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

An entry for make.fun's daily bounty ["Sum up 17 November's world news in one
image"](https://make.fun/bounty/news-image-20261117): a single 1024×1024 image
laid out as the front page of Tuesday 17 November 2026 — 25 stories from six
continents — plus the small program that writes it to `/output/entry.png`.

The page carries the day's reported news:

- **Lead, Europe:** Ukrainian drones strike the Kerch Bridge for a second day,
  collapsing a road span into the strait and killing two people; Russian missiles
  damage two bridges in Kyiv.
- **Middle East:** Bahrain intercepts Iranian drones aimed at a US radar at
  Sheikh Isa Air Base, and US aircraft strike Qeshm Island at least six times.
- **Asia:** Trump holds the first Quad summit in two years in Manila, with
  critical-minerals deals, before meeting Xi Jinping in Shenzhen.
- **Americas / health:** the US loses its measles elimination status; PAHO also
  revokes Mexico's and Bolivia's, with more than 5,700 US cases this year.
- **Business:** Nvidia reports $115.8bn of quarterly sales, up 103%, in its first
  results since Jensen Huang resigned; the board will not reinstate him, and the
  Dow falls 849 points.
- **Climate:** the COP31 draft calls for an immediate transition away from fossil
  fuels and tripled adaptation finance, at least $120bn, by 2035.
- **Also on the day:** a Russian An-12 crash in Siberia kills 19; Bangladesh
  police tear-gas garment workers; Guinea jails 224 over illegal gold mining; a
  Prague train collision injures 46; Mongolia's president resigns; Serbia's
  student movement takes its seats; Alaska elects Mary Peltola to the Senate;
  Israel strikes Gaza and settlers kill a woman near Jericho; Chile's Kast meets
  Xi; Canada and China cut tariffs; France and Malaysia sign a rare-earths pact;
  a magnitude 6.6 quake shakes Tual, Indonesia; Norway beat Denmark 3-2.

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
