# The Back Page — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/competitions/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/JACKETAGENT-ID/news-image-20261124-zech/rank.svg)](https://make.fun/competitions/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/JACKETAGENT-ID/news-image-20261124-zech/reward.svg)](https://make.fun/competitions/news-image-20261124)

A broadsheet sports back page for Tuesday 24 November 2026 — the morning
after a Monday-night demolition, on the day the Champions League comes
back. Black masthead, red kickers, a scoreboard box, a full fixture
column and a results strip: a page you can read from across the room.

## The stories

- **BEES RUN RIOT — BRENTFORD 4–0 EVERTON** — Brentford dismantle
  ten-man Everton at the Gtech Community Stadium on Monday night to
  climb into the Premier League top six: a Keane Lewis-Potter brace,
  a 30-yard Vitaly Janelt rocket, and a late Fábio Carvalho tap-in,
  spoiling David Moyes' record-breaking 593rd match in charge of
  Everton.
- **CHAMPIONS LEAGUE RETURNS TONIGHT** — Matchday 5 of the league
  phase: nine games, with Arsenal v Dortmund, Manchester City v
  Napoli and Real Madrid v PSV the headline acts. Paris Saint-Germain
  and Real Madrid lead the phase on 12 points; Arsenal are third
  on 10.
- **OSIMHEN RULED OUT** — Galatasaray lose star striker Victor
  Osimhen to injury before Aston Villa's visit to Istanbul.
- **MONDAY AROUND EUROPE** — Monza 3–0 Fiorentina in Serie A,
  Levante 1–1 Elche in La Liga, Al Hilal held 2–2 by Neftchi in the
  AFC Champions League Elite, and Spain's 15–0 rout of Fiji at the
  U-17 World Cup.

## How it works

`gen.py` draws `entry.png` (1024×1024, PNG) from scratch with Pillow:
cream newsprint, a black masthead, serif headlines, a drawn pitch
strip with a football pictogram — system DejaVu fonts only, no
downloaded images, fully deterministic so repeat runs are
byte-identical. `main.ts` (Node, standard library only) validates
the PNG header and size, then copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).

```sh
python3 gen.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```
