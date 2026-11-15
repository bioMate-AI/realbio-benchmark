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
  - genomics
---

# RealBio — an open, objectively-scored benchmark for agentic bioinformatics & genomics execution

> **Can your AI agent actually *choreograph* a bioinformatics pipeline — route the request to the right analysis, then configure it correctly — or does it only *talk about* biology?** That is the question RealBio scores.

Genomics and bioinformatics run on multi-step **computational pipelines**, and the first two moves decide whether the whole run is even valid: **pick the right analysis**, then **configure it** from what the user actually said. RealBio asks the blunt question: can an AI agent get those execution decisions right, or does it only sound knowledgeable?

Almost every agentic-bio benchmark is **scored by each system's own AI judge on its own private task set**, so the numbers are non-comparable and invite self-grading. RealBio fixes that: **370 fixed public items across 2 core agentic-execution tasks**, each with **objective, published ground truth**, graded by **one shared open deterministic scorer** (`src/score.py` — **no AI judge**). Same items, same metric, for every system — so any team can run its own agent and land a **directly comparable** number.

**Headline finding:** today's frontier LLMs are strong on biological *knowledge* but **weak at execution** — used directly they **misroute requests** (0.35–0.62 accuracy) and **over-fill parameters** they were never given. A purpose-built platform with a curated catalog (BioMate) leads both tasks; on routing a good catalog beats raw model scale.

> **Scope note.** RealBio focuses on the non-clinical, objectively-scorable orchestration front-end (route → configure). The clinical-pharmacology tasks (drug-exposure/PBPK, Phase-I dose-finding/BOIN) and QC gating have moved to the companion **DrugDev-Bench**.

## The 2 core tasks

1. **Route** (`cross_domain_routing`, n=200) — turn a plain-English goal into the correct analysis pipeline out of a large catalog (63 distinct target pipelines across every omics domain).
2. **Configure** (`param_prefill`, n=170) — fill the pipeline's parameters from what the user actually said, without inventing settings (143 parameter names, 11 inference categories; scored by F1).

## Results (same items, same deterministic scorer, no AI judge)

| System | Routing | Param (F1) |
|---|---|---|
| **BioMate** (product) | **0.965** | **0.848** |
| Biomni (Stanford A1) | 0.950 | 0.708 |
| Claude Opus 5 | 0.615 | 0.757 |
| Gemini 3.1 Pro | 0.580 | 0.693 |
| GPT-5.6 | 0.530 | 0.671 |
| Kimi K3 | 0.450 | 0.628 |
| DeepSeek V4 | 0.415 | 0.621 |
| GLM-5.2 | 0.400 | 0.641 |
| GPT-5.6-luna | 0.355 | 0.624 |
| Qwen3.8-Max | 0.345 | 0.692 |

## Run your own system

```bash
# produce predictions.jsonl per task — {"id": ..., "prediction": <answer>} — then:
python3 src/score.py cross_domain_routing my_system/cross_domain_routing.jsonl
python3 src/score.py param_prefill        my_system/param_prefill.jsonl
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
