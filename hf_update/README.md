---
license: cc-by-4.0
pretty_name: RealBio Benchmark
task_categories:
  - other
tags:
  - bioinformatics
  - agents
  - benchmark
  - llm-evaluation
  - workflow-automation
  - drug-discovery
---

# RealBio — an open, objectively-scored benchmark for AI agents in drug development & genomics

> **Can your AI agent actually *choreograph* a multi-step pipeline — route → configure → QC → model → dose — or does it only *talk about* biology?** That is the whole question RealBio scores.

Modern drug discovery and genomics run on multi-step **computational pipelines**: pick the right analysis, configure it, quality-control the data, model the drug, and choose a safe dose. Teams increasingly want an **AI agent to drive those pipelines**. RealBio asks the blunt question: can an AI agent actually *run* one correctly end-to-end, or does it only *talk about* biology fluently?

Almost every agentic-bio benchmark is **scored by each system's own AI judge on its own private task set**, so the numbers are non-comparable and invite self-grading. RealBio fixes that: **505 fixed public items across 5 real drug-development / genomics tasks**, each with **objective, published ground truth**, graded by **one shared open deterministic scorer** (`src/score.py` — **no AI judge**). Same items, same metric, for every system — so any team can run its own agent and land a **directly comparable** number.

**Headline finding:** today's frontier LLMs are strong on biological *knowledge* but **fail at execution** — and they fail worst on the **clinical-pharmacology** tasks (predicting drug exposure, choosing a trial dose), exactly where errors matter most. A purpose-built platform (BioMate) leads the orchestration and QC tasks and ties for the top score on the hardest task, drug-exposure prediction.

## The 5 tasks (the pipeline, in order)

1. **Route** (`cross_domain_routing`, n=200) — turn a plain-English goal into the correct analysis pipeline out of a large catalog.
2. **Configure** (`param_prefill`, n=170) — fill the pipeline's parameters from what the user actually said, without inventing settings (scored by F1).
3. **QC** (`protocol_thresholds`, n=100) — decide PASS/FAIL on a real sequencing sample with the assay-specific rule (public GEO/PRIDE/EMDB accessions).
4. **Model the drug** (`pbpk_benchmark`, n=15) — predict drug exposure (Cmax/AUC/t½) within 2-fold of the published human value.
5. **Dose the trial** (`boin_benchmark`, n=20) — recommend the Phase-I MTD from emerging toxicity data using the BOIN design.

## Results (same items, same deterministic scorer, no AI judge)

| System | Routing | Param (F1) | Protocol | PBPK (2×) | BOIN |
|---|---|---|---|---|---|
| **BioMate** (product) | **0.965** | **0.848** | **0.925** | **0.200** † | **0.80** |
| Claude Opus 5 | 0.615 | 0.757 | 0.330 | 0.133 | 0.444 |
| Gemini 3.1 Pro | 0.580 | 0.693 | 0.630 | 0.000 | 0.278 |
| GPT-5.6 | 0.530 | 0.671 | 0.460 | 0.200 | 0.500 |
| Kimi K3 | 0.450 | 0.628 | 0.360 | 0.000 | 0.167 |
| DeepSeek V4 | 0.415 | 0.621 | 0.420 | 0.067 | 0.167 |
| GLM-5.2 | 0.400 | 0.641 | 0.440 | 0.000 | 0.111 |
| GPT-5.6-luna | 0.355 | 0.624 | 0.340 | 0.200 | 0.389 |
| Qwen3.8-Max | 0.345 | 0.692 | 0.460 | 0.000 | 0.111 |
| Biomni (Stanford A1) | 0.950 | 0.708 | 0.500 | 0.000 | 0.500 |

† **PBPK** is the hardest task for everyone: BioMate's **0.200 (3/15, within-2-fold)** on the same 15 PBPK items ties GPT-5.6 and GPT-5.6-luna for the best result on the board — no system exceeds 0.200. (An earlier BioMate "1.00" came from a different, non-comparable disease-state-ratio task and has been removed.)

Numbers reconcile with the preprint, *RealBio evaluates the decisions underlying bioinformatics workflow automation* (Zhang & Dike, 2026), Supplementary Table S1 (historical same-item cross-system comparison).

## Run your own system

```bash
# produce predictions.jsonl per task — {"id": ..., "prediction": <answer>} — then:
python3 src/score.py cross_domain_routing my_system/cross_domain_routing.jsonl
# → objective metric + 95% CI, no LLM judge. Directly comparable to the leaderboard.
```

## Citation

```bibtex
@misc{realbio2026,
  title  = {RealBio: evaluating the decisions underlying bioinformatics workflow automation},
  author = {Zhang, Yaoyun and Dike, Andrew},
  year   = {2026},
  note   = {BioMate AI. Preprint},
  url    = {https://github.com/bioMate-AI/realbio-benchmark}
}
```

**License:** CC-BY-4.0 — data, ground truth, scorer, and harness.
Built by [BioMate AI](https://biomate.ai) · code + leaderboard: [github.com/bioMate-AI/realbio-benchmark](https://github.com/bioMate-AI/realbio-benchmark)
