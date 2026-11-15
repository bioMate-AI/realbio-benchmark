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

> **Can your AI agent actually *choreograph* a bioinformatics pipeline — start by routing the request to the right analysis, then configuring it correctly — or does it only *talk about* biology?** That is the question RealBio scores.

### The one-sentence version
Genomics and bioinformatics run on multi-step **computational pipelines**, and the first two moves decide whether the whole run is even valid: **pick the right analysis** for the request, then **configure it** from what the user actually said. Teams increasingly want an **AI agent to drive those pipelines**. RealBio asks the blunt question: **can an AI agent get those execution decisions right, or does it only sound knowledgeable?**

### Why this is hard — and why we can't just trust the vendors' own scores
A large language model can write a confident paragraph about RNA-seq or variant calling. That is *not* the same as correctly **routing** a real request to the right pipeline out of hundreds, or **filling its parameters** without inventing wrong ones. A wrong pipeline wastes days of compute and real sample money; an over-filled or under-filled parameter set silently corrupts a run that still *looks* like it succeeded. Yet almost every agentic-bio benchmark is **scored by each system's own AI judge on its own private task set**, so the numbers are non-comparable and invite (often unintentional) self-grading.

RealBio fixes that: **370 fixed public items across 2 core agentic-execution tasks**, each with **objective, published ground truth**, graded by **one shared open scorer** (`src/score.py` — a deterministic checker, **no AI judge**). Same items, same metric, for every system — so any team can run its own agent and land a **directly comparable** number.

**The headline finding:** today's frontier LLMs are strong on biological *knowledge* but **weak at execution** — used directly they **misroute requests** (0.35–0.62 accuracy) and **over-fill parameters** they were never given. A purpose-built platform with a curated catalog (BioMate) leads both tasks, and on routing a good catalog beats raw model scale.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

**🌐 Project:** [biomate.ai](https://biomate.ai) · **🏆 Leaderboard:** [on GitHub](https://github.com/bioMate-AI/realbio-benchmark#results) · **📄 Datasheet:** [`DATASHEET.md`](DATASHEET.md) · **📝 Paper:** [`paper/RealBio_benchmark.pdf`](paper/RealBio_benchmark.pdf)

> **Scope note.** RealBio focuses on the **non-clinical, objectively-scorable orchestration front-end** of the pipeline (route → configure). The clinical-pharmacology tasks that used to appear here (drug-exposure / PBPK, Phase-I dose-finding / BOIN) and QC gating have moved to the companion **DrugDev-Bench**, where they belong with the rest of the drug-development evaluation. RealBio is a clean execution benchmark; it is also a **growing** one — additional non-clinical agentic tasks are re-added as every system is measured on the same items with the same metric.

## Why RealBio exists — and what "running a pipeline" actually means

Taking a dataset toward an answer is a **computational relay**, and RealBio measures its first two hand-offs — the ones that gate everything downstream:

1. **Route** — turn a plain-English goal ("call germline variants from whole-genome sequencing") into the correct analysis pipeline, out of hundreds.
2. **Configure** — set that pipeline's parameters from what the user actually said, without inventing settings they didn't specify.

An AI agent that is fluent about biology but gets either of these wrong isn't just unhelpful — it burns real sample and compute budget, and the failure is often *silent* until the results are quietly wrong. So the question isn't "does it sound knowledgeable," it's "did it get the objectively-checkable answer right." That is what RealBio measures, identically, for every system: **fixed public items, published ground truth, one open deterministic scorer** — no AI judge, no private test set, no self-grading.

## Repository layout

```
├── <task>/data.jsonl        # 2 task datasets (public ground truth) + per-task README
├── results/<system>/*.jsonl # committed predictions per system (re-scorable)
├── src/                     # score.py (the scorer) + run/aggregation harness
├── leaderboard.csv / .md    # the committed leaderboard (regenerates from results/)
├── paper/                   # the preprint (RealBio_benchmark.pdf)
└── DATASHEET.md             # dataset documentation (motivation, construction, limitations)
```

## The 2 tasks (in plain language)

Both tasks live in the **Orchestration** band — set the analysis up correctly before a single CPU-hour is spent. Quality discipline is embedded in both: route to avoid the wrong pipeline, and don't over-fill parameters. BioMate leads both.

| Task (code name) | In plain English | Why it matters — and why an error is costly |
|---|---|---|
| **Pipeline routing** (`cross_domain_routing`, n=200) | Given a plain-English research request, pick the single correct analysis pipeline from a large catalog (e.g. bulk RNA-seq vs. variant-calling vs. single-cell). | The first decision in any genomics/omics project; the wrong pipeline wastes days of compute and real sample money. |
| **Parameter pre-fill** (`param_prefill`, n=170) | Fill the chosen pipeline's settings from the request — and *only* the settings actually specified, never invented ones. Scored by **F1** (a precision/recall balance). | Over-filling silently corrupts a run; under-filling stalls it. Both can look like success until the results are quietly wrong. |

*Every abbreviation above (F1) is a standard term, spelled out so the benchmark is readable without prior background.* Items are **original tasks authored from public sources** (the nf-core pipeline catalog and its documented parameter schemas) — **not** drawn from any system's training set. Full per-task construction methodology is in the [`DATASHEET.md`](DATASHEET.md).

### Coverage at a glance (how wide each task reaches)

The items are not variations of one thing — each task deliberately spans many distinct pipelines and parameters:

| Task | Items | Distinct coverage inside the task |
|---|---:|---|
| **Pipeline routing** | 200 | **63 distinct target pipelines** spanning every major omics domain (transcriptomics, genomics/variant-calling, epigenomics, single-cell, proteomics, cryo-EM, metagenomics, immunogenomics, therapeutic design) |
| **Parameter pre-fill** | 170 | **11 inference categories** (genome, strandedness, tool-flags, numeric, reference-file, multi-param, single-cell, virtual-cell, drug-discovery, name-disambiguation, negative cases) over **143 distinct parameter names** |

### Examples & the domains each task covers

Real items from the benchmark (not toy prompts), to show the breadth:

**Pipeline routing** — spans essentially every omics domain:
- *"Run standard RNA-seq analysis on my paired-end FASTQ files from a mouse study"* → `nf-core/rnaseq` *(transcriptomics)*
- *"Whole-genome bisulfite sequencing to profile CpG methylation"* → `nf-core/methylseq` *(epigenomics)*
- *"AIRR-compliant V(D)J gene-usage analysis for an immunology clinical study"* → `nf-core/airrflow` *(immune-repertoire / clinical immunology)*
- *"Recommend 2′-OMe chemical modifications to reduce siRNA immunogenicity"* → `sirna_offtarget_analysis` *(therapeutic-oligonucleotide design)*
- **Domains covered:** transcriptomics · epigenomics · variant calling · single-cell · proteomics · cryo-EM · metagenomics · immunogenomics · therapeutic design.

**Parameter pre-fill** — extract the right settings, and *only* those:
- *"RNA-seq differential expression on human lung adenocarcinoma"* → `{genome: GRCh38}` (nothing else — don't invent a read length or aligner)
- *"WES human GATK best-practices germline variant calling"* → `{genome: GRCh38, wes: true, tools: haplotypecaller}`
- *"Synergy analysis: trametinib (MEK inhibitor) + palbociclib (CDK4/6 inhibitor)"* → structured drug/target params
- **Domains covered:** oncology genomics · gene regulation (ChIP-seq) · clinical genetics (WES/WGS) · combination pharmacology.

## Results

Every cell re-scores from committed `predictions.jsonl` via `src/score.py`. LLMs are evaluated **the way they are actually used** — model + task, no candidate list injected.

| System | Routing | Param (F1) |
|---|---|---|
| **BioMate** (product) | **0.965** | **0.848** |
| Biomni (Stanford A1) | 0.950 | 0.708 |
| Claude Opus 5 | 0.615 | **0.757** |
| Gemini 3.1 Pro | 0.580 | 0.693 |
| GPT-5.6 | 0.530 | 0.671 |
| Kimi K3 | 0.450 | 0.628 |
| DeepSeek V4 | 0.415 | 0.621 |
| GLM-5.2 | 0.400 | 0.641 |
| GPT-5.6-luna | 0.355 | 0.624 |
| Qwen3.8-Max | 0.345 | 0.692 |

Every cell is a same-item, same-scorer result that re-scores from the committed prediction files under `results/`. (A refreshed figure for the two-task board is being regenerated; the committed table and `leaderboard.csv` are authoritative.)

### Efficiency (measured)

**Latency** below is the **routing** task (same 200 items) — the *one* metric measured identically for every system, and so the only clean head-to-head.

| System | Routing latency (median) | Engine |
|---|---:|---|
| **BioMate** (product) | **2.3 s** | Mixture of LLMs — primary Claude Sonnet 4.5; secondary Claude Haiku 4.5, Gemini 3.5 Flash, Gemini 3.1 Pro, GPT-5.6-luna |
| Claude Opus 5 | 2.7 s | Anthropic Claude Opus 5 |
| Gemini 3.1 Pro | 3.6 s | Google Gemini 3.1 Pro |
| GPT-5.6-luna | 1.6 s | OpenAI GPT-5.6-luna |
| Kimi K3 | 3.2 s | Moonshot Kimi K3 |
| DeepSeek V4 | 3.8 s | DeepSeek V4 |
| GLM-5.2 | 0.8 s | Z.ai GLM-5.2 |
| Qwen3.8-Max | 4.0 s | Alibaba Qwen3.8-Max |
| Biomni (A1) | 3.9 s | Agent scaffold — Claude Opus 5 (routing/param) |

## Participating systems

Every system was run on the **same fixed items** and scored by the **same** `src/score.py`. Frontier and open-weight LLMs were run the way they are actually deployed (model + task); BioMate was run as the product; Biomni is run as its published agent scaffold.

| System | Organization | Link | Reference |
|---|---|---|---|
| **BioMate** (product) | BioMate AI | [biomate.ai](https://biomate.ai) · [leaderboard](https://github.com/bioMate-AI/realbio-benchmark#results) | This benchmark — see [Citation](#citation) |
| Claude Opus 5 | Anthropic | [anthropic.com/claude](https://www.anthropic.com/claude) | — |
| Gemini 3.1 Pro | Google DeepMind | [deepmind.google/models/gemini](https://deepmind.google/models/gemini/) | — |
| GPT-5.6 · GPT-5.6-luna | OpenAI | [openai.com](https://openai.com/) | — |
| Kimi K3 | Moonshot AI | [moonshot.ai](https://www.moonshot.ai/) | — |
| DeepSeek V4 | DeepSeek | [deepseek.com](https://www.deepseek.com/) | — |
| GLM-5.2 | Z.ai (Zhipu AI) | [z.ai](https://z.ai/) | — |
| Qwen3.8-Max | Alibaba Qwen | [qwen.ai](https://qwen.ai/) | — |
| Biomni (A1) | Stanford (Zou Lab) | [biomni.stanford.edu](https://biomni.stanford.edu/) | Huang et al., *Science* 2025, [doi:10.1126/science.adz4351](https://doi.org/10.1126/science.adz4351) |

## Key takeaways for the community

1. **BioMate leads both tasks on the board.** Routing **0.965**, parameter-F1 **0.848** — first on both. Biomni ties routing closely at 0.950; Claude Opus 5 is second on param-F1 at 0.757 — so no *single* LLM is BioMate's runner-up across both.
2. **LLMs used directly fail *execution*, not knowledge.** Used bare, frontier and open-weight models route correctly only 0.35–0.62 of the time and over-fill parameters they were never given, while sounding fluent throughout. The gap is doing the step right, not knowing the biology.
3. **On curated routing, a good catalog beats raw model scale.** The largest cross-system spread is routing: BioMate's product (**0.965**) vs the same frontier LLMs used directly (0.345–0.615).
4. **The lead is verifiable, not self-reported.** Open fixed items + one shared deterministic scorer + no LLM judge means you *cannot* self-grade — any team runs its own system and lands directly comparable to the numbers above.

## Run your own system

```bash
# produce predictions.jsonl per task — {"id": ..., "prediction": <answer>} — then:
python3 src/score.py cross_domain_routing my_system/cross_domain_routing.jsonl
python3 src/score.py param_prefill        my_system/param_prefill.jsonl
# → objective metric + 95% CI, no LLM judge. Directly comparable to the leaderboard.
```

## Citation

The full preprint is included in this repo: [`paper/RealBio_benchmark.pdf`](paper/RealBio_benchmark.pdf) — *RealBio evaluates the decisions underlying bioinformatics workflow automation* (Zhang & Dike, 2026).

```bibtex
@misc{realbio2026,
  title  = {RealBio: evaluating the decisions underlying bioinformatics workflow automation},
  author = {Zhang, Yaoyun and Dike, Andrew},
  year   = {2026},
  note   = {BioMate AI. Preprint},
  url    = {https://github.com/bioMate-AI/realbio-benchmark}
}
```

## Ground-truth sources (external references)
- **Routing & parameters** — nf-core pipeline catalog and documented parameter schemas (Ewels et al., *Nat. Biotechnol.* 2020, [doi:10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x)).
- **Baseline agent** — Biomni (Huang et al., *Science* 2025, [doi:10.1126/science.adz4351](https://doi.org/10.1126/science.adz4351)).

## License
**CC-BY-4.0** — data, ground truth, scorer, and harness. See [`LICENSE`](LICENSE).

---
Built by **[BioMate AI](https://biomate.ai)** · leaderboard: **[on GitHub](https://github.com/bioMate-AI/realbio-benchmark#results)**
