# RealBio — Dataset datasheet

Documentation for the RealBio benchmark dataset (following the *Datasheets for Datasets* spirit). RealBio asks whether an AI agent can **choreograph the front-end of a bioinformatics pipeline** — route the request to the right analysis, then configure it correctly — not just describe the biology. The full preprint ships with this repo: [`paper/RealBio_benchmark.pdf`](paper/RealBio_benchmark.pdf).

> **Scope.** RealBio is the **non-clinical, objectively-scorable orchestration** benchmark (routing + parameter pre-fill). The clinical-pharmacology tasks that previously appeared here — drug-exposure/PBPK, Phase-I dose-finding/BOIN — and QC gating have moved to the companion **DrugDev-Bench**.

## Motivation

Most agentic-bio benchmarks are scored by each system's own judge on its own private task set — non-comparable across systems and open to (often unintentional) self-grading. RealBio was built to be **objectively scored, cross-system, and anti-self-grading by construction**: fixed public items, published ground truth, one shared deterministic scorer (`src/score.py`), and no LLM judge for the objective tasks.

## Composition

**370 items across 2 core tasks**, each with a machine-checkable answer and (where relevant) an `acceptable_alts` set. No item is drawn from any system's training corpus; each is **generated or adapted from a documented public source with a stated rationale**. RealBio is a **growing** benchmark — further non-clinical agentic tasks are re-added as every system is measured on the same items with the same metric.

| Task | n | How items were created (source + rationale) | Difficulty strata |
|---|---:|---|---|
| `cross_domain_routing` | 200 | **Adapted from the nf-core catalog documentation** — each query written from a real pipeline's documented use case (item `notes` cite the source page); `disqualified` lists near-miss distractors. Rationale: public, catalog-neutral routing targets. | direct 125 · indirect 36 · adversarial 39 |
| `param_prefill` | 170 | **Constructed by inference category** (genome_inference, …); each pairs a request with parameters that are *clearly stated* and those that must **not** be filled. Rationale: test inference + over-fill avoidance. | easy 61 · medium 72 · hard 37 |

**Moved to DrugDev-Bench.** The clinical-pharmacology tasks (`pbpk_benchmark`, `boin_benchmark`) and QC gating (`protocol_thresholds`) that earlier shipped here have moved to the companion **DrugDev-Bench** release, which owns the drug-development evaluation.

**Withheld internal tasks.** Internal tasks (`license_gating`, `memory_benchmark`) are excluded from this public release — their ground truth scores one system's product-specific behaviour, not a neutral cross-system task.

## Collection & labeling

Items were authored by the BioMate team from the public sources above. Ground truth is a public catalog name (routing — with `acceptable_alts` crediting valid near-equivalents) or an expected key–value parameter set plus a `must_not_fill` list (parameter pre-fill), derived from the nf-core catalog and its documented parameter schemas.

## Scoring

One committed scorer, `src/score.py` — exact/threshold match against published ground truth, **no LLM judge**. Every leaderboard cell re-scores from committed `results/<system>/*.jsonl`. Non-answers count as failures (they are never silently dropped). Each score reports its n and a 95% Wilson interval.

## Known limitations

- **Catalog-derived routing labels.** Routing ground truth is defined against the nf-core catalog; `acceptable_alts` credit valid near-equivalents, but a system targeting an out-of-catalog tool with an equivalent capability is scored as a miss. This is a deliberate, documented convention, not a silent one.
- **Parameter F1 convention.** An incorrect value on an expected key is counted as a false negative (not additionally a false positive); `must_not_fill` violations are reported separately rather than folded into F1. Read F1 alongside the violation count.
- **Contamination risk.** Items are authored from public sources; public items may later enter training data. Original authorship reduces but does not eliminate this risk.

## Uses & distribution

Intended for **cross-system evaluation of bioinformatics AI agents**. Released **CC-BY-4.0**. Run your system on the fixed items, score with `src/score.py`, and your result is directly comparable to the leaderboard.
