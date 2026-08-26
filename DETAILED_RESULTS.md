# Per-sample results — every system, every item

`results_detailed.csv` (and `.jsonl`) is the complete per-sample record: **one row per (system, task, item)**, regenerable with `python3 src/build_detailed.py`.

## Fields

| Column | Meaning |
|---|---|
| `system` | model / system name (as on the leaderboard) |
| `task` | one of the 5 tasks |
| `id` | item id (matches `<task>/data.jsonl`) |
| `difficulty` | the item's difficulty stratum |
| `prediction` | the system's raw prediction |
| `ground_truth` | the published correct answer |
| `correct` | per-item correctness, recomputed with the same logic as `src/score.py` (for `param_prefill`, a per-item F1 with any `must_not_fill` violations noted) |
| `latency_ms` | wall-clock latency for that item, where the run logged it |
| `prompt_tokens`, `completion_tokens` | per-item tokens — **only `boin_benchmark` and `pbpk_benchmark` logged these**; blank elsewhere |
| `cost_usd` | per-item cost = (prompt×price_in + completion×price_out)/10⁶ × 1.05 (OpenRouter fee); only where per-item tokens exist |
| `cost_note` | how cost was derived, or why it's blank |

## Coverage (what per-sample data actually exists)

| System | routing | param | protocol | boin | pbpk |
|---|---:|---:|---:|---:|---:|
| **BioMate** (product) | 200 | — | — | — | — |
| Claude Opus 5 | 200 | 170 | 100 | 20 | 15 |
| Gemini 3.1 Pro | 200 | 170 | 100 | 20 | 15 |
| GPT-5.6 | 200 | 170 | 100 | 20 | 15 |
| GPT-5.6-luna | 200 | 170 | 100 | 20 | 15 |
| Kimi K3 | 200 | 170 | 100 | 20 | 15 |
| DeepSeek V4 | 200 | 170 | 100 | 20 | 15 |
| GLM-5.2 | 200 | 170 | 100 | 20 | 15 |
| Qwen3.8-Max | 200 | 170 | 100 | 20 | 15 |
| Biomni (A1) | 40 | 40 | 40 | 20 | 15 |

## Important caveats (read before comparing rows)

1. **BioMate has same-item per-sample data for `routing` only.** Its `param_prefill` / `protocol` / `pbpk` / `boin` leaderboard cells come from **BioMate's own separate benchmark harness on *different items***, not the RealBio items — so there are **no same-item per-sample predictions** for those tasks, and BioMate is absent from them here. Treat BioMate's non-routing leaderboard numbers as **cross-harness, same-metric, different-item** figures, not same-item head-to-heads.
2. **Biomni** routing used **catalog mode** (the candidate workflow list was provided in-context), while the 8 LLMs' routing used **bare mode** (no list) — so Biomni's routing is not a like-for-like input to the LLMs'. Biomni also ran **n=40 pilot subsets** on routing/param/protocol.
3. **Per-item cost exists only for `boin` and `pbpk`** (the only tasks that logged per-item tokens). `routing` / `param` / `protocol` have per-item latency but not per-item tokens.
4. **Token counts across models reflect different tokenizers** (see the tokenizer table in `README.md`); costs are still correct (each model bills its own tokens × its own price).
