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

> **Can your AI agent actually *choreograph* a bioinformatics pipeline — route the request to the right analysis, configure it, select the right method, self-fix a failed run, and generate the workflow — or does it only *talk about* biology?** That is the question RealBio scores.

### The one-sentence version
Genomics and bioinformatics run on multi-step **computational pipelines**, and a handful of agentic decisions decide whether the whole run is even valid: **route** the request to the right analysis, **configure** it from what the user actually said, **select** the right method for the data, **self-fix** a run that failed, and **generate** the workflow. Teams increasingly want an **AI agent to drive those pipelines**. RealBio asks the blunt question: **can an AI agent get those execution decisions right, or does it only sound knowledgeable?**

### Why this is hard — and why we can't just trust the vendors' own scores
A large language model can write a confident paragraph about RNA-seq or variant calling. That is *not* the same as correctly **routing** a real request to the right pipeline out of hundreds, **filling its parameters** without inventing wrong ones, **picking the correct analysis method** for the data (not a plausible-sounding wrong one), or **diagnosing why a run failed**. A wrong pipeline wastes days of compute and real sample money; an over-filled parameter set silently corrupts a run that still *looks* like it succeeded. Yet almost every agentic-bio benchmark is **scored by each system's own AI judge on its own private task set**, so the numbers are non-comparable and invite (often unintentional) self-grading.

RealBio fixes that: **550 fixed public items across 5 core agentic-execution tasks**, each with **objective, published ground truth**, graded by **one shared open scorer** (`src/score.py` — a deterministic checker, **no AI judge**). Same items, same metric, for every system — so any team can run its own agent and land a **directly comparable** number.

**The headline finding:** today's frontier LLMs are strong where the answer space is **closed** — they classify a failure's root cause (0.77–0.88) and pick the right method from a candidate list (0.82–1.0) well — but **fall off on open-ended execution**: used directly they **misroute requests** (0.35–0.62) and **over-fill parameters** they were never given (F1 0.62–0.76). The harder the search space, the worse they do. A purpose-built platform with a curated catalog (BioMate) leads the two open-ended tasks (routing, parameter pre-fill), where a good catalog beats raw model scale.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

**🌐 Project:** [biomate.ai](https://biomate.ai) · **🏆 Leaderboard:** [on GitHub](https://github.com/bioMate-AI/realbio-benchmark#results) · **📄 Datasheet:** [`DATASHEET.md`](DATASHEET.md) · **📝 Paper:** [`paper/RealBio_benchmark.pdf`](paper/RealBio_benchmark.pdf)

> **Scope note.** RealBio covers the **non-clinical, objectively-scorable agentic-execution** tasks of the pipeline (route → configure → select method → self-fix → generate). The clinical-pharmacology tasks that used to appear here (drug-exposure / PBPK, Phase-I dose-finding / BOIN) and QC gating have moved to the companion **DrugDev-Bench**, where they belong with the rest of the drug-development evaluation. RealBio is a **growing** benchmark — tasks are added only once systems are measured on the same items with the same metric.

## Why RealBio exists — and what "running a pipeline" actually means

Taking a dataset toward an answer is a **computational relay**, and RealBio measures five hand-offs that gate everything downstream:

1. **Route** — turn a plain-English goal ("call germline variants from whole-genome sequencing") into the correct analysis pipeline, out of hundreds.
2. **Configure** — set that pipeline's parameters from what the user actually said, without inventing settings they didn't specify.
3. **Select method** — given a specific analysis need and a candidate list, pick the method that is actually *correct* for the data (e.g. over-representation vs. rank-based enrichment), not a plausible-sounding wrong one.
4. **Self-fix** — read a failed run's error log and classify the real root cause (genome mismatch, missing input, resource failure, …) so it can be repaired.
5. **Generate workflow** — turn an intent into the right analysis category or the key tools a from-scratch pipeline needs.

An AI agent that is fluent about biology but gets any of these wrong isn't just unhelpful — it burns real sample and compute budget, and the failure is often *silent* until the results are quietly wrong. So the question isn't "does it sound knowledgeable," it's "did it get the objectively-checkable answer right." That is what RealBio measures, identically, for every system: **fixed public items, published ground truth, one open deterministic scorer** — no AI judge, no private test set, no self-grading.

## Repository layout

```
├── <task>/data.jsonl        # 5 task datasets (public ground truth) + per-task README
├── results/<system>/*.jsonl # committed predictions per system (re-scorable)
├── src/                     # score.py (the scorer) + run/aggregation harness
├── leaderboard.csv / .md    # the committed leaderboard (regenerates from results/)
├── paper/                   # the preprint (RealBio_benchmark.pdf)
└── DATASHEET.md             # dataset documentation (motivation, construction, limitations)
```

## The 5 tasks (in plain language)

Five agentic-execution decisions in pipeline order. Each has an objective, machine-checkable answer and is scored by the same open scorer.

| Task (code name) | In plain English | Why it matters — and why an error is costly |
|---|---|---|
| **Route** (`cross_domain_routing`, n=200) | Given a plain-English research request, pick the single correct analysis pipeline from a large catalog (e.g. bulk RNA-seq vs. variant-calling vs. single-cell). | The first decision in any genomics/omics project; the wrong pipeline wastes days of compute and real sample money. |
| **Configure** (`param_prefill`, n=170) | Fill the chosen pipeline's settings from the request — and *only* the settings actually specified, never invented ones. Scored by **F1** (a precision/recall balance). | Over-filling silently corrupts a run; under-filling stalls it. Both can look like success until the results are quietly wrong. |
| **Select method** (`bioc_method_selection`, n=40) | Given an analysis need and a candidate list of Bioconductor methods, pick the one that is *correct* for the data — e.g. over-representation (ORA) for a discrete gene list, not rank-based GSEA. Scored by **top-1 accuracy**; statistically-wrong picks are tracked separately. | Picking a plausible-but-wrong method produces confident, invalid results that pass silently into a paper or a decision. |
| **Self-fix** (`autofix_benchmark`, n=100) | Read a failed nf-core run (workflow + params + error log) and classify the real root cause into one of **10 objective categories** (genome_mismatch, missing_input, resource_failure, …). | Misdiagnosing a failure sends an agent down the wrong repair path; the right category is the first step to an automated fix. |
| **Generate workflow** (`workflow_generation`, n=40) | Turn an intent into the right analysis **category** (in-catalog) or the **key tools** a from-scratch pipeline needs (out-of-catalog). | Tests whether an agent can specify a pipeline, not just route to a named one. |

*Every abbreviation above (F1, ORA, GSEA) is a standard term, spelled out so the benchmark is readable without prior background.* Items are **original tasks authored from public sources** (the nf-core pipeline catalog, its documented parameter schemas, and the Bioconductor method catalog) — **not** drawn from any system's training set. Full per-task construction methodology is in the [`DATASHEET.md`](DATASHEET.md).

### Coverage at a glance (how wide each task reaches)

The items are not variations of one thing — each task deliberately spans many distinct pipelines, parameters, methods and failure modes:

| Task | Items | Distinct coverage inside the task |
|---|---:|---|
| **Route** | 200 | **63 distinct target pipelines** spanning every major omics domain (transcriptomics, genomics/variant-calling, epigenomics, single-cell, proteomics, cryo-EM, metagenomics, immunogenomics, therapeutic design) |
| **Configure** | 170 | **11 inference categories** (genome, strandedness, tool-flags, numeric, reference-file, multi-param, single-cell, virtual-cell, drug-discovery, name-disambiguation, negative cases) over **143 distinct parameter names** |
| **Select method** | 40 | Bioconductor method choices across distinct analysis regimes, each with a `correct_method`, valid `acceptable_alts`, and `invalid_picks` (methods that are statistically wrong for the context) |
| **Self-fix** | 100 | **10 objective failure categories** across nf-core pipelines, with realistic error logs and a difficulty stratum per case |
| **Generate workflow** | 40 | **2 partitions** — A (in-catalog → analysis category, 20) and B (out-of-catalog → key tools, 20) |

### Examples & the domains each task covers

Real items from the benchmark (not toy prompts), to show the breadth:

**Route** — spans essentially every omics domain:
- *"Run standard RNA-seq analysis on my paired-end FASTQ files from a mouse study"* → `nf-core/rnaseq` *(transcriptomics)*
- *"Whole-genome bisulfite sequencing to profile CpG methylation"* → `nf-core/methylseq` *(epigenomics)*
- *"AIRR-compliant V(D)J gene-usage analysis for an immunology clinical study"* → `nf-core/airrflow` *(immune-repertoire / clinical immunology)*

**Configure** — extract the right settings, and *only* those:
- *"RNA-seq differential expression on human lung adenocarcinoma"* → `{genome: GRCh38}` (nothing else — don't invent a read length or aligner)
- *"WES human GATK best-practices germline variant calling"* → `{genome: GRCh38, wes: true, tools: haplotypecaller}`

**Select method** — pick the statistically correct method, not a plausible one:
- *"I have 284 DE genes at FDR<0.05 and want GO/KEGG over-representation"* → `clusterprofiler` (ORA) — **not** rank-based GSEA / `fgsea` on an unranked list.

**Self-fix** — classify the real root cause of a failed run:
- STAR aborts with "no valid exon lines in the GTF; index built with GRCh38, GTF uses hg19 naming" → `genome_mismatch` (not a generic `data_format_error`).

## Results

Every cell re-scores from committed `predictions.jsonl` via `src/score.py`. For routing / configure / self-fix / generate, LLMs are evaluated **the way they are actually used** — model + task, no candidate list injected. Method-selection (`bioc`) inherently supplies a candidate list in the item, and is reported in the **bare** condition (no extra retrieval). Columns are in pipeline order; `—` = no committed result on that task yet.

| System | Routing | Param (F1) | Method (top-1) | Self-fix | Workflow-gen |
|---|---|---|---|---|---|
| **BioMate** (product) | **0.965** | **0.848** | — | — | — |
| Biomni (Stanford A1) | 0.950 | 0.708 | — | **0.950** | 0.500 |
| Claude Opus 5 | 0.615 | **0.757** | **1.000** | 0.870 | 0.500 |
| Gemini 3.1 Pro | 0.580 | 0.693 | 0.975 | **0.880** | 0.500 |
| GPT-5.6 | 0.530 | 0.671 | **1.000** | 0.860 | 0.500 |
| Kimi K3 | 0.450 | 0.628 | 0.975 | 0.770 | 0.450 |
| DeepSeek V4 | 0.415 | 0.621 | 0.825 | 0.800 | 0.500 |
| GLM-5.2 | 0.400 | 0.641 | — | 0.830 | 0.500 |
| GPT-5.6-luna | 0.355 | 0.624 | — | 0.830 | 0.500 |
| Qwen3.8-Max | 0.345 | 0.692 | — | 0.860 | 0.500 |

Every non-`—` cell is a same-item, same-scorer result that re-scores from the committed prediction files under `results/`. **Reading the board:** the *open-ended* tasks (routing, parameter pre-fill) separate systems the most and are where BioMate leads; the *closed-choice* tasks (method-selection from a candidate list, 10-class failure classification) are already near-ceiling for frontier LLMs; `workflow_gen` saturates near 0.50 for most systems and is kept for breadth. BioMate's committed results cover routing + parameter pre-fill (it tops both); its numbers on the three newly-added tasks are pending, and `bioc` currently covers five systems. (A refreshed board figure is being regenerated; the committed table and `leaderboard.csv` are authoritative.)

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
| Biomni (A1) | 3.9 s | Agent scaffold — Claude Opus 5 (routing/param/self-fix/workflow-gen) |

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

1. **The harder the search space, the worse LLMs do.** On *closed-choice* tasks — classifying a failure's root cause (0.77–0.88) or picking a method from a candidate list (0.82–1.0) — frontier LLMs are already strong. On *open-ended* execution — routing across hundreds of pipelines (0.35–0.62) and precision parameter-filling (F1 0.62–0.76) — they fall off. The gap is not biological knowledge; it is doing the open-ended step right.
2. **BioMate leads the open-ended tasks.** Routing **0.965** and parameter-F1 **0.848** — first on both, exactly the two tasks that separate systems the most. On routing, a curated catalog (0.965) decisively beats the same frontier LLMs used directly (0.345–0.615). BioMate's results on the three newly-added tasks are pending.
3. **No single LLM is the all-round runner-up.** The best bare model differs by task (Claude Opus 5 / GPT-5.6 top method-selection at 1.0; Gemini 3.1 Pro tops self-fix among LLMs at 0.88; Biomni tops self-fix overall at 0.95), so strength on one execution decision does not transfer to the others.
4. **`workflow_gen` is near-saturated.** Most systems tie at 0.50 — it adds breadth, not separation, and should be read with that caveat.
5. **The numbers are verifiable, not self-reported.** Open fixed items + one shared deterministic scorer + no LLM judge means you *cannot* self-grade — any team runs its own system and lands directly comparable to the numbers above.

## Run your own system

```bash
# produce predictions.jsonl per task — {"id": ..., "prediction": <answer>} — then:
python3 src/score.py cross_domain_routing   my_system/cross_domain_routing.jsonl
python3 src/score.py param_prefill          my_system/param_prefill.jsonl
python3 src/score.py bioc_method_selection  my_system/bioc_method_selection.jsonl
python3 src/score.py autofix_benchmark      my_system/autofix_benchmark.jsonl
python3 src/score.py workflow_generation    my_system/workflow_generation.jsonl
# → objective metric + 95% CI, no LLM judge. Directly comparable to the leaderboard.
# or regenerate the whole board from results/:  python3 src/leaderboard.py
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
- **Routing, parameters, self-fix, workflow-gen** — nf-core pipeline catalog and documented parameter schemas (Ewels et al., *Nat. Biotechnol.* 2020, [doi:10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x)); failure cases are authored against real nf-core error modes.
- **Method selection** — the Bioconductor project method catalog (Huber et al., *Nat. Methods* 2015, [doi:10.1038/nmeth.3252](https://doi.org/10.1038/nmeth.3252)).
- **Baseline agent** — Biomni (Huang et al., *Science* 2025, [doi:10.1126/science.adz4351](https://doi.org/10.1126/science.adz4351)).

## License
**CC-BY-4.0** — data, ground truth, scorer, and harness. See [`LICENSE`](LICENSE).

---
Built by **[BioMate AI](https://biomate.ai)** · leaderboard: **[on GitHub](https://github.com/bioMate-AI/realbio-benchmark#results)**
