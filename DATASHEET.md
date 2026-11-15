# RealBio — Dataset datasheet

Documentation for the RealBio benchmark dataset (following the *Datasheets for Datasets* spirit). RealBio asks whether an AI agent can **choreograph a bioinformatics pipeline** — route the request to the right analysis, configure it, select the right method, self-fix a failed run, and generate the workflow — not just describe the biology. The full preprint ships with this repo: [`paper/RealBio_benchmark.pdf`](paper/RealBio_benchmark.pdf).

> **Scope.** RealBio is the **non-clinical, objectively-scorable agentic-execution** benchmark (route → configure → select method → self-fix → generate workflow). The clinical-pharmacology tasks that previously appeared here — drug-exposure/PBPK, Phase-I dose-finding/BOIN — and QC gating have moved to the companion **DrugDev-Bench**.

## Motivation

Most agentic-bio benchmarks are scored by each system's own judge on its own private task set — non-comparable across systems and open to (often unintentional) self-grading. RealBio was built to be **objectively scored, cross-system, and anti-self-grading by construction**: fixed public items, published ground truth, one shared deterministic scorer (`src/score.py`), and no LLM judge for the objective tasks.

## Composition

**550 items across 5 core tasks**, each with a machine-checkable answer and (where relevant) an `acceptable_alts` set. No item is drawn from any system's training corpus; each is **generated or adapted from a documented public source with a stated rationale**. RealBio is a **growing** benchmark — further non-clinical agentic tasks are added as every system is measured on the same items with the same metric.

| Task | n | How items were created (source + rationale) | Difficulty strata |
|---|---:|---|---|
| `cross_domain_routing` | 200 | **Adapted from the nf-core catalog documentation** — each query written from a real pipeline's documented use case (item `notes` cite the source page); `disqualified` lists near-miss distractors. Rationale: public, catalog-neutral routing targets. | direct 125 · indirect 36 · adversarial 39 |
| `param_prefill` | 170 | **Constructed by inference category** (genome_inference, …); each pairs a request with parameters that are *clearly stated* and those that must **not** be filled. Rationale: test inference + over-fill avoidance. | easy 61 · medium 72 · hard 37 |
| `bioc_method_selection` | 40 | **Authored from the Bioconductor method catalog** — each item gives an analysis need, a candidate method list, the `correct_method`, valid `acceptable_alts`, and `invalid_picks` (methods that are statistically wrong for the context, e.g. ORA on a ranked statistic). Rationale: correctness-of-method, not plausibility. | by `discriminator` |
| `autofix_benchmark` | 100 | **Deliberately-broken nf-core runs** by failure category (genome_mismatch, missing_input, resource_failure, param_type_error, …); each = workflow + buggy params + a realistic error log; label = the one correct category of 10. | by `fix_difficulty` |
| `workflow_generation` | 40 | **Two partitions:** A = in-catalog (intent → analysis category, 20), B = out-of-catalog (intent → key tools, 20). Rationale: specify a pipeline, not just route to a named one. | A/B partition + difficulty |

**Moved to DrugDev-Bench.** The clinical-pharmacology tasks (`pbpk_benchmark`, `boin_benchmark`) and QC gating (`protocol_thresholds`) that earlier shipped here have moved to the companion **DrugDev-Bench** release, which owns the drug-development evaluation.

**Withheld internal tasks.** Internal tasks (`license_gating`, `memory_benchmark`) are excluded from this public release — their ground truth scores one system's product-specific behaviour, not a neutral cross-system task.

## Collection & labeling

Items were authored by the BioMate team from the public sources above. Ground truth is: a public catalog name (routing — `acceptable_alts` credit valid near-equivalents); an expected key–value parameter set plus a `must_not_fill` list (parameter pre-fill); a `correct_method` with `invalid_picks` (method selection, from the Bioconductor catalog); one of 10 objective failure categories (self-fix); or an analysis category / key-tool set (workflow generation). All are derived from public catalogs (nf-core, Bioconductor) and real error modes.

## Scoring

One committed scorer, `src/score.py` — exact/threshold match against published ground truth, **no LLM judge**. Every leaderboard cell re-scores from committed `results/<system>/*.jsonl`. Non-answers count as failures (they are never silently dropped). Each score reports its n and a 95% Wilson interval.

## Known limitations

- **Catalog-derived routing labels.** Routing ground truth is defined against the nf-core catalog; `acceptable_alts` credit valid near-equivalents, but a system targeting an out-of-catalog tool with an equivalent capability is scored as a miss. This is a deliberate, documented convention, not a silent one.
- **Parameter F1 convention.** An incorrect value on an expected key is counted as a false negative (not additionally a false positive); `must_not_fill` violations are reported separately rather than folded into F1. Read F1 alongside the violation count.
- **Contamination risk.** Items are authored from public sources; public items may later enter training data. Original authorship reduces but does not eliminate this risk.
- **Method-selection condition.** `bioc_method_selection` is reported in the **bare** condition (the item supplies the candidate list; no extra retrieval). Committed results currently cover five systems; others are `—`.
- **`workflow_generation` saturation.** The aggregate metric ties near 0.50 for most systems — it adds coverage breadth, not fine separation; read it with that caveat.
- **Coverage gaps are marked, not imputed.** A system with no committed result on a task is shown as `—`; BioMate's results on method-selection / self-fix / workflow-gen are pending and are not estimated.

## Uses & distribution

Intended for **cross-system evaluation of bioinformatics AI agents**. Released **CC-BY-4.0**. Run your system on the fixed items, score with `src/score.py`, and your result is directly comparable to the leaderboard.
