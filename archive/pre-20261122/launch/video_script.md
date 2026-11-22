# RealBio — 60–90s launch video

**Format:** short vertical (9:16), fast cuts, screen-recording + motion-text. Target ~75s.
**Voiceover tone:** crisp, confident, a little provocative. **On-screen text** mirrors the VO
key phrases. **No posted claim beyond the repo numbers.**

---

## Script + shot list

| # | Time | Voiceover | On-screen / shot |
|---|------|-----------|------------------|
| 1 | 0:00–0:07 | "An AI can describe RNA-seq perfectly… and still send the job to the wrong pipeline." | Cold open: a slick LLM chat answer scrolling — then a red ✗ stamps over a mis-routed pipeline icon. |
| 2 | 0:07–0:15 | "Because real biology isn't an essay. It's a pipeline you have to choreograph: route it, configure it, pick the method, self-fix it, generate it." | Five connected nodes animate left-to-right: **Route → Configure → Select → Self-fix → Generate**. |
| 3 | 0:15–0:24 | "So we built RealBio — an open benchmark for whether an AI agent can actually get those decisions right." | RealBio wordmark drops in. Subtitle: "550 fixed public items · 5 core tasks." |
| 4 | 0:24–0:36 | "No AI judge. No private test set. Fixed public items, published ground truth, one open deterministic scorer. You can't self-grade your way up it." | Split screen: left "other benchmarks → AI judges itself 🔁"; right "RealBio → one open scorer ✅". Terminal shows `python3 src/score.py …`. |
| 5 | 0:36–0:52 | "The finding? The harder the search space, the worse they do. Classify a failure or pick from a list — they're strong. Route across hundreds of pipelines — they drop to a third-to-two-thirds." | Bar chart builds: closed-choice bars tall (0.77–1.0), open-ended routing bars short (0.35–0.62). Highlight the gap in red. |
| 6 | 0:52–1:00 | "And on configuration, they over-fill parameters they were never given — silently corrupting a run that still looks like it worked." | Animate a params form auto-filling with phantom fields; a red "INVENTED" tag flags the extras. |
| 7 | 1:00–1:10 | "BioMate leads the two open-ended tasks — routing ninety-seven, parameters eighty-five. On routing, a curated catalog beats raw model scale." | Leaderboard rows highlight: BioMate 0.965 / 0.848 glow; routing spread (0.965 vs 0.35–0.62) drawn as a wide gap. |
| 8 | 1:10–1:18 | "It's open. It's auditable. Run your own agent — and land a directly comparable number." | Repo URL fills screen: **github.com/bioMate-AI/realbio-benchmark**. CC-BY-4.0 badge. |
| 9 | 1:18–1:22 | "Can your agent choreograph the pipeline?" | Tagline card, RealBio + BioMate logos, CTA: "Clone it. Score it." |

---

## Storyboard notes

- **Visual motif:** the **Route → Configure → Select → Self-fix → Generate** chain is the spine of
  the video — reuse it in shots 2, 5–6, and 9 so the "choreography" idea lands.
- **Honesty beat (shot 5–6):** frame it as "the harder the search space, the worse they do," not
  "models are useless." Closed-choice is strong (self-fix 0.77–0.88, method-selection 0.82–1.0);
  open-ended falls off (routing 0.35–0.62, param-F1 0.62–0.76). Keep both on screen.
- **Color:** calm teal/slate base; a single red accent reserved for the execution-gap / ✗ /
  INVENTED moments.
- **Numbers on screen must match the repo:** bare-LLM routing 0.345–0.615, param-F1 0.621–0.757;
  BioMate routing 0.965, param-F1 0.848; method-selection 0.825–1.0; self-fix 0.77–0.95.
- **BioMate's method/self-fix/generate cells are `—` (pending) — do not show a number for them.**
- **Captions on throughout** (sound-off autoplay). End card holds the URL for ≥3s.
- **Music:** building synth, hard stop on the final tagline.
