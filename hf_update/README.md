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

> **Can your AI agent actually *choreograph* a bioinformatics pipeline — route the request, configure it, select the right method, self-fix a failed run, and generate the workflow — or does it only *talk about* biology?** That is the question RealBio scores.

Genomics and bioinformatics run on multi-step **computational pipelines**, and a handful of agentic decisions decide whether the whole run is even valid: **route → configure → select method → self-fix → generate**. RealBio asks the blunt question: can an AI agent get those execution decisions right, or does it only sound knowledgeable?

Almost every agentic-bio benchmark is **scored by each system's own AI judge on its own private task set**, so the numbers are non-comparable and invite self-grading. RealBio fixes that: **550 fixed public items across 5 core agentic-execution tasks**, each with **objective, published ground truth**, graded by **one shared open deterministic scorer** (`src/score.py` — **no AI judge**). Same items, same metric, for every system — so any team can run its own agent and land a **directly comparable** number.

**Headline finding:** frontier LLMs are strong where the answer space is **closed** — classifying a failure's root cause (0.77–0.88) and picking a method from a candidate list (0.82–1.0) — but **fall off on open-ended execution**: used directly they misroute requests (0.35–0.62) and over-fill parameters they were never given (F1 0.62–0.76). The harder the search space, the worse they do. A purpose-built platform (BioMate) leads the two open-ended tasks (routing, parameter pre-fill); on routing a curated catalog beats raw model scale.

> **Scope note.** RealBio covers the non-clinical, objectively-scorable agentic-execution tasks (route → configure → select method → self-fix → generate). The clinical-pharmacology tasks (drug-exposure/PBPK, Phase-I dose-finding/BOIN) and QC gating have moved to the companion **DrugDev-Bench**.

## The 5 core tasks

1. **Route** (`cross_domain_routing`, n=200) — pick the correct pipeline out of a large catalog (63 targets, every omics domain).
2. **Configure** (`param_prefill`, n=170) — fill parameters from the request, without inventing settings (143 parameter names; scored by F1).
3. **Select method** (`bioc_method_selection`, n=40) — pick the statistically correct Bioconductor method from a candidate list (top-1 accuracy).
4. **Self-fix** (`autofix_benchmark`, n=100) — classify a failed run's root cause into 1 of 10 objective categories.
5. **Generate workflow** (`workflow_generation`, n=40) — intent → analysis category (A) or key tools (B).

## Results (same items, same deterministic scorer, no AI judge)

Columns in pipeline order; `—` = no committed result on that task yet.

| System | Routing | Param (F1) | Method (top-1) | Self-fix | Workflow-gen |
|---|---|---|---|---|---|
| **BioMate** (product) | **0.965** | **0.848** | — | — | — |
| Biomni (Stanford A1) | 0.950 | 0.708 | — | 0.950 | 0.500 |
| Claude Opus 5 | 0.615 | 0.757 | 1.000 | 0.870 | 0.500 |
| Gemini 3.1 Pro | 0.580 | 0.693 | 0.975 | 0.880 | 0.500 |
| GPT-5.6 | 0.530 | 0.671 | 1.000 | 0.860 | 0.500 |
| Kimi K3 | 0.450 | 0.628 | 0.975 | 0.770 | 0.450 |
| DeepSeek V4 | 0.415 | 0.621 | 0.825 | 0.800 | 0.500 |
| GLM-5.2 | 0.400 | 0.641 | — | 0.830 | 0.500 |
| GPT-5.6-luna | 0.355 | 0.624 | — | 0.830 | 0.500 |
| Qwen3.8-Max | 0.345 | 0.692 | — | 0.860 | 0.500 |

BioMate tops the two open-ended tasks (routing, parameter pre-fill); its results on the three newly-added tasks are pending. `bioc` (method-selection) currently covers five systems.

## Run your own system

```bash
# produce predictions.jsonl per task — {"id": ..., "prediction": <answer>} — then:
python3 src/score.py cross_domain_routing   my_system/cross_domain_routing.jsonl
python3 src/score.py param_prefill          my_system/param_prefill.jsonl
python3 src/score.py bioc_method_selection  my_system/bioc_method_selection.jsonl
python3 src/score.py autofix_benchmark      my_system/autofix_benchmark.jsonl
python3 src/score.py workflow_generation    my_system/workflow_generation.jsonl
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
