# RealBio — 60–90s launch video

**Format:** short vertical (9:16), fast cuts, screen-recording + motion-text. Target ~80s.
**Voiceover tone:** crisp, confident, a little provocative. **On-screen text** mirrors the VO
key phrases. **No posted claim beyond the repo numbers.**

---

## Script + shot list

| # | Time | Voiceover | On-screen / shot |
|---|------|-----------|------------------|
| 1 | 0:00–0:07 | "An AI can write a flawless paragraph about pharmacokinetics… and still pick the wrong dose." | Cold open: a slick LLM chat answer scrolling — then a red ✗ stamps over it. |
| 2 | 0:07–0:15 | "Because real biology isn't an essay. It's a pipeline you have to choreograph." | Five connected nodes animate left-to-right: **Route → Configure → QC → Model → Dose**. |
| 3 | 0:15–0:24 | "So we built RealBio — an open benchmark for whether an AI agent can actually run it, end to end." | RealBio wordmark drops in. Subtitle: "505 fixed public items · 5 real tasks." |
| 4 | 0:24–0:36 | "No AI judge. No private test set. Fixed public items, published ground truth, one open deterministic scorer. You can't self-grade your way up it." | Split screen: left "other benchmarks → AI judges itself 🔁"; right "RealBio → one open scorer ✅". Terminal shows `python3 src/score.py …`. |
| 5 | 0:36–0:50 | "The finding? Frontier models are brilliant at biology knowledge — and weak at execution. Weakest exactly where it costs the most." | Bar chart builds: knowledge bars tall, execution bars short. Highlight the execution gap in red. |
| 6 | 0:50–1:02 | "Predicting drug exposure: the frontier-LLM average is eight percent. Nobody we tested beats twenty. Dose-finding: a mean of twenty-four percent — some models never return a usable answer." | Big numbers punch in: **0.08**, then **≤0.20**, then **0.24**. Small caption: "PBPK · BOIN." |
| 7 | 1:02–1:12 | "BioMate leads the orchestration and QC tasks — routing ninety-seven, QC ninety-three — and ties for the best score on the one task nobody's solved yet." | Leaderboard row highlights: BioMate 0.965 / 0.925 glow; PBPK column shows a flat "tied, hard" tag. |
| 8 | 1:12–1:20 | "It's open. It's auditable. Run your own agent — and land a directly comparable number." | Repo URL fills screen: **github.com/bioMate-AI/realbio-benchmark**. CC-BY-4.0 badge. |
| 9 | 1:20–1:24 | "Can your agent choreograph the pipeline?" | Tagline card, RealBio + BioMate logos, CTA: "Clone it. Score it." |

---

## Storyboard notes

- **Visual motif:** the 5-node relay (Route → Configure → QC → Model → Dose) is the spine of the
  whole video — reuse it in shots 2, 5, and 9 so the "choreography" idea lands.
- **Honesty beat (shot 6–7):** keep the PBPK framing as "hard for everyone / tied for best," not
  "BioMate wins." The number is 0.200 and no system exceeds it — that candor is a selling point.
- **Color:** calm teal/slate base; a single red accent reserved for the execution-gap/✗ moments.
- **Numbers on screen must match the repo:** PBPK frontier-LLM mean 0.08, board max 0.200; BOIN
  LLM mean 0.24; BioMate routing 0.965, QC 0.925, param-F1 0.848, BOIN 0.80.
- **Captions on throughout** (sound-off autoplay). End card holds the URL for ≥3s.
- **Music:** building synth, hard stop on the final tagline.
