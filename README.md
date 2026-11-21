# news-in-one-day-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Axel1899/news-in-one-day-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![Follow Axel1899 on make.fun](https://make.fun/badge/follow/Axel1899.svg?bg=0066ff&text=ffffff)](https://make.fun/@Axel1899?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up **Friday, 20 November 2026**: a classic newspaper
front page — one lead story across the top, four more in a grid below —
covering war, diplomacy, markets, climate and entertainment in a single
1024×1024 frame.

## The five stories

1. **Russian missiles land in Poland** — Russia's largest strike of
   November (27 ballistic missiles, 84 cruise missiles, 404 drones)
   crossed into Polish, NATO territory; allied jets scrambled and Warsaw
   demanded reinforcements. *(AP / ISW)*
2. **Trump, Xi, Putin meet in Shenzhen** — the three leaders met on the
   sidelines of APEC and issued a trilateral peace declaration.
   *(Reuters)*
3. **AI crash wipes out 2026 gains** — the AI trade unwound violently:
   Nasdaq −5.4%, Nvidia −14%, roughly $4 trillion in market value gone
   in a day. *(Investopedia / WSJ)*
4. **COP31 erases fossil-fuel pledge** — the Antalya draft agreement
   dropped every mention of fossil fuels and the talks spilled into
   overtime. *(Reuters / UN News)*
5. **GTA VI earns $3.79 billion in a day** — the biggest entertainment
   launch in history, 24 hours after release. *(Reuters / CNN)*

## How it works

`main.ts` (Node 22, standard library only) copies the bundled
`entry.png` to `/output/entry.png`, creating `/output` first if needed.
It runs offline and is fully deterministic — every run delivers the
exact same bytes.

The image itself was composed by `compose.py` (Python / Pillow): five
text-free editorial illustrations — one per story — are laid out as a
front page, and **every word is typeset programmatically** (masthead,
date, headlines, kickers, source line). No AI-generated text appears
anywhere, so nothing is garbled. The panels live outside this repo;
`compose.py` documents exactly how the page was assembled.

## License

MIT — see `LICENSE`.
