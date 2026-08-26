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

### The one-sentence version
Modern drug discovery and genomics run on multi-step **computational pipelines** — pick the right analysis, configure it, quality-control the data, model the drug, choose a safe dose. Teams increasingly want an **AI agent to drive those pipelines**. RealBio asks the blunt question: **can an AI agent actually *run* one correctly end-to-end, or does it only *talk about* biology fluently?**

### Why this is hard — and why we can't just trust the vendors' own scores
A large language model can write a confident paragraph about RNA-seq or pharmacokinetics. That is *not* the same as correctly routing a real request to the right pipeline, filling its parameters without inventing wrong ones, catching a bad sequencing sample, predicting a drug's blood concentration, or picking a safe first-in-human dose — where a mistake wastes real lab money or, in the clinical tasks, is a patient-safety error. Yet almost every agentic-bio benchmark is **scored by each system's own AI judge on its own private task set**, so the numbers are non-comparable and invite (often unintentional) self-grading.

RealBio fixes that: **505 fixed public items across 5 real drug-development / genomics tasks**, each with **objective, published ground truth**, graded by **one shared open scorer** (`src/score.py` — a deterministic checker, **no AI judge**). Same items, same metric, for every system — so any team can run its own agent and land a **directly comparable** number.

**The headline finding:** today's frontier LLMs are strong on biological *knowledge* but **fail at execution** — and they fail worst on the **clinical-pharmacology** tasks (predicting drug exposure, choosing a trial dose), exactly where errors matter most. A purpose-built platform (BioMate) leads every task.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

**🌐 Project:** [biomate.ai](https://biomate.ai) · **🏆 Leaderboard:** [on GitHub](https://github.com/bioMate-AI/realbio-benchmark#results) · **📄 Datasheet:** [`DATASHEET.md`](DATASHEET.md)

> **Growing benchmark.** Three further tasks (execution auto-repair, workflow generation, drug-discovery ligand ranking) are validated and re-added as every system — including BioMate — is measured on the same items with the same metric. We report a task only when the whole board is measured on it.

## Why RealBio exists — and what "running a pipeline" actually means

Taking a therapy from a molecule or a dataset toward the clinic is a **computational relay**. RealBio's five tasks are five real hand-offs in that relay, in order:

1. **Route** — turn a plain-English goal ("call germline variants from whole-genome sequencing") into the correct analysis pipeline, out of hundreds.
2. **Configure** — set that pipeline's parameters from what the user actually said, without inventing settings they didn't specify.
3. **Quality-control** — decide whether the incoming sequencing data is usable, using the rule that fits its specific assay type (a single universal cutoff false-alarms).
4. **Model the drug** — predict how much drug reaches the bloodstream (its pharmacokinetics) from the molecule's chemistry.
5. **Dose the trial** — from emerging toxicity data, recommend the dose to give the next patients in a Phase I clinical trial.

An AI agent that is fluent about biology but gets any of these wrong isn't just unhelpful — it burns real sample and compute budget, and in steps 4–5 it is making **drug-safety** calls. So the question isn't "does it sound knowledgeable," it's "did it get the objectively-checkable answer right." That is what RealBio measures, identically, for every system: **fixed public items, published ground truth, one open deterministic scorer** — no AI judge, no private test set, no self-grading.

## Repository layout

```
├── <task>/data.jsonl        # 5 task datasets (public ground truth) + per-task README
├── results/<system>/*.jsonl # committed predictions per system (re-scorable)
├── src/                     # score.py (the scorer) + run/aggregation harness
├── figures/                 # leaderboard + difficulty figures
├── leaderboard.csv / .md    # the committed leaderboard (regenerates from results/)
└── DATASHEET.md             # dataset documentation (motivation, construction, limitations)
```

## The 5 tasks (in plain language)

Two lifecycle bands — **Orchestration** (set the analysis up) and **Execution** (run the science, including the clinical-pharmacology computations). **Quality control is not a separate band; it is embedded in every task** — route to avoid the wrong pipeline, don't over-fill parameters, gate bad data, monitor trial toxicity, sanity-check drug exposure. BioMate leads both bands.

| Band | Task (code name) | In plain English | Why it matters — and why an error is costly |
|---|---|---|---|
| Orchestration | **Pipeline routing** (`cross_domain_routing`, n=200) | Given a plain-English research request, pick the single correct analysis pipeline from a large catalog (e.g. bulk RNA-seq vs. variant-calling vs. single-cell). | The first decision in any genomics/omics project; the wrong pipeline wastes days of compute and real sample money. |
| Orchestration | **Parameter pre-fill** (`param_prefill`, n=170) | Fill the chosen pipeline's settings from the request — and *only* the settings actually specified, never invented ones. Scored by **F1** (a precision/recall balance). | Over-filling silently corrupts a run; under-filling stalls it. Both can look like success until the results are quietly wrong. |
| Execution | **QC gating** (`protocol_thresholds`, n=100) | Decide PASS / FAIL on a real sequencing sample. One universal quality cutoff *false-alarms* on specialized assays (single-cell, small-RNA, cryo-EM); the agent must apply the assay-specific rule. Each item carries a public data accession (**GEO / PRIDE / EMDB** — the standard genomics / proteomics / cryo-EM repositories), expert-labeled. | Discarding good data — or keeping bad data — corrupts every downstream conclusion. |
| Execution | **Trial dose-finding** (`boin_benchmark`, n=20) | **BOIN** = *Bayesian Optimal INterval* design, a standard **Phase I clinical-trial** method. From emerging toxicity data, recommend the **MTD** (Maximum Tolerated Dose) — the highest dose that isn't too toxic. | A first-in-human patient-safety decision: too high harms patients, too low fails the drug. |
| Execution | **Drug-exposure prediction** (`pbpk_benchmark`, n=15) | **PBPK** = *Physiologically-Based PharmacoKinetic* modeling. From a molecule's chemistry, dose and route, predict how much reaches the blood — peak concentration (**Cmax**), total exposure (**AUC**), half-life. Scored as within **2-fold** of the published human value. | Sets the first-in-human dose and underpins regulatory (FDA) submissions; a wrong exposure estimate mis-doses a trial. |

*Every abbreviation above (BOIN, PBPK, MTD, Cmax, AUC, GEO/PRIDE/EMDB, F1) is a standard drug-development or bioinformatics term, spelled out so the benchmark is readable without prior background.* Items are **original tasks authored from public sources** (the nf-core pipeline catalog, public data accessions, published human pharmacokinetics, and the published BOIN design tables) — **not** drawn from any system's training set. Full per-task construction methodology is in the [`DATASHEET.md`](DATASHEET.md).

### Coverage at a glance (how wide each task reaches)

The items are not five variations of one thing — each task deliberately spans many distinct pipelines, parameters, assays, trial designs, and drugs:

| Task | Items | Distinct coverage inside the task |
|---|---:|---|
| **Pipeline routing** | 200 | **63 distinct target pipelines** spanning every major omics domain (transcriptomics, genomics/variant-calling, epigenomics, single-cell, proteomics, cryo-EM, metagenomics, immunogenomics, therapeutic design) |
| **Parameter pre-fill** | 170 | **11 inference categories** (genome, strandedness, tool-flags, numeric, reference-file, multi-param, single-cell, virtual-cell, drug-discovery, name-disambiguation, negative cases) over **143 distinct parameter names** |
| **QC gating** | 100 | **99 distinct assay / library protocols**; real datasets from **3 major repositories** — GEO (75), PRIDE (3), EMDB (3) + 19 other public sources |
| **Trial dose-finding** | 20 | **20 distinct Phase I trial scenarios** (oncology, antibody-drug conjugates, pediatric, steep/shallow toxicity curves, exposure–response models) |
| **Drug-exposure prediction** | 15 | **15 distinct marketed drugs** (14 oral, 1 IV) across therapeutic classes (analgesic, antidiabetic, statin, antifungal, stimulant, …) |

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

**QC gating** — real public datasets on assays where one universal cutoff misfires:
- `10x_genomics_flex_low_input` (GEO GSE132044) · `cite_seq_low_adt_counts` (GSE164378) · `smart_seq2_plate_based` (GSE118184) · ambient-RNA correction (GSE163530)
- **Domains covered:** single-cell RNA-seq variants · CITE-seq (joint protein+RNA) · plate-based scRNA · plus proteomics (PRIDE) and cryo-EM (EMDB) library types.

**Trial dose-finding** — Phase I scenarios across modalities:
- "Standard oncology — myelosuppression-limited" · "Steep dose-limiting-toxicity curve — MTD at the starting dose" · "Linear exposure–response — antibody-drug conjugate" · "Pediatric oncology — weight-normalized"
- **Domains covered:** oncology Phase I trials · antibody-drug conjugates (ADCs) · pediatric dosing.

**Drug-exposure prediction** — marketed drugs across therapeutic classes, each with published human PK:
- Aspirin (analgesic, 500 mg oral) · Metformin (antidiabetic, 500 mg) · Atorvastatin (statin, 80 mg) · Ketoconazole (antifungal, 200 mg) · Caffeine (stimulant, 200 mg)
- **Domains covered:** clinical pharmacology across analgesics, antidiabetics, statins, antifungals — a deliberate spread of absorption/metabolism behaviors.

![Difficulty strata per task](figures/difficulty.png)
*Figure 1. Deliberate difficulty design — routing spans direct/indirect/adversarial; others grade easy/medium/hard by inference depth.*

## Results

Every cell re-scores from committed `predictions.jsonl` via `src/score.py`. LLMs are evaluated **the way they are actually used** — model + task, no candidate list injected.

![RealBio leaderboard](figures/leaderboard.png)
*Figure 2. BioMate (product) vs frontier LLMs used directly.*

Columns are grouped by capability band: **Orchestration** (Routing, Param) · **Quality control** (Protocol) · **Execution** (PBPK, BOIN).

| System | Routing | Param (F1) | Protocol | PBPK (2×) | BOIN |
|---|---|---|---|---|---|
| **BioMate** (product) | **0.965** | **0.848** | **0.925** | **1.00** | **0.80** |
| Claude Opus 5 | 0.615 | **0.757** | 0.330 | 0.133 | 0.400 |
| Gemini 3.1 Pro | 0.580 | 0.693 | **0.630** | 0.000 | 0.278 |
| GPT-5.6 | 0.530 | 0.671 | 0.460 | **0.200** | **0.500** |
| Kimi K3 | 0.450 | 0.628 | 0.360 | 0.000 | 0.167 |
| DeepSeek V4 | 0.415 | 0.621 | 0.420 | 0.067 | 0.167 |
| GLM-5.2 | 0.400 | 0.641 | 0.440 | 0.000 | 0.111 |
| GPT-5.6-luna | 0.355 | 0.624 | 0.340 | 0.200 | 0.389 |
| Qwen3.8-Max | 0.345 | 0.692 | 0.460 | 0.000 | 0.111 |
| Biomni (Stanford A1) | 0.950 | 0.708 | 0.500 | 0.000 | 0.500 |

Every cell is a same-item, same-scorer result that re-scores from the committed prediction files under `results/`.

### Efficiency & engine (measured)

**Latency** below is the **routing** task (same 200 items) — the *one* metric measured identically for every system, and so the only clean head-to-head. Cost is reported separately (next block), because no single task logged tokens for all systems.

| System | Routing latency (median) | Engine |
|---|---:|---|
| **BioMate** (product) | **2.3 s** | Mixture of LLMs — primary Claude Sonnet 4.5; secondary Claude Haiku 4.5, Gemini 3.5 Flash, Gemini 3.1 Pro, GPT-5.6-luna |
| Claude Opus 5 | 2.7 s | Anthropic Claude Opus 5 |
| Gemini 3.1 Pro | 3.6 s | Google Gemini 3.1 Pro |
| GPT-5.6 | — (subset only) | OpenAI GPT-5.6 |
| GPT-5.6-luna | 1.6 s | OpenAI GPT-5.6-luna |
| Kimi K3 | 3.2 s | Moonshot Kimi K3 |
| DeepSeek V4 | 3.8 s | DeepSeek V4 |
| GLM-5.2 | 0.8 s | Z.ai GLM-5.2 |
| Qwen3.8-Max | 4.0 s | Alibaba Qwen3.8-Max |
| Biomni (A1) | 3.9 s | Agent scaffold — Claude Opus 5 (routing/param/protocol), Claude Sonnet 4.5 (PBPK/BOIN; Opus-5's API rejects Biomni's assistant-prefill loop, removed across Claude ≥ 4.6) |

#### Per-call cost — being revised

> **Note.** The per-call token/cost analysis is temporarily withheld while we make it a clean, same-task comparison across all systems. It will be added back once corrected. Latency above is the one same-task efficiency metric we report in the interim.

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

1. **BioMate leads every task on the board.** Routing **0.965**, parameter-F1 **0.848**, protocol-QC **0.925**, PBPK **1.00**, BOIN **0.80** — first on all five. The nearest competitor differs by task (Biomni ties routing at 0.950; Claude Opus 5 is second on param-F1 at 0.757; Gemini 3.1 Pro is second on protocol at 0.630), so no *single* LLM is BioMate's runner-up — the lead is broad, not a one-task artifact.
2. **LLMs used directly fail *execution*, not knowledge.** They are near-useless at PBPK simulation (mean 0.08 within-2-fold) and mediocre at deterministic BOIN dose-finding (mean 0.24) — the computation/execution tasks — while being competent at knowledge-driven extraction.
3. **Output discipline is a real deployment gap.** Several open-weight models emit long reasoning with *no parseable answer* on PBPK/BOIN — which fails deployment even when the reasoning is sound.
4. **The lead is verifiable, not self-reported.** Open fixed items + one shared deterministic scorer + no LLM judge means you *cannot* self-grade — any team runs its own system and lands directly comparable to the numbers above.
5. **On curated routing, a good catalog beats raw model scale.** The largest cross-system spread is routing: BioMate's product (**0.965**) vs the same frontier LLMs used directly (0.345–0.615).

## Run your own system

```bash
# produce predictions.jsonl per task — {"id": ..., "prediction": <answer>} — then:
python3 src/score.py cross_domain_routing my_system/cross_domain_routing.jsonl
# → objective metric + 95% CI, no LLM judge. Directly comparable to the leaderboard.
```

## Citation

```bibtex
@misc{realbio2026,
  title  = {RealBio: an open, objectively-scored benchmark for bioinformatics AI agents},
  author = {Zhang, Yaoyun and Dike, Andrew},
  year   = {2026},
  note   = {BioMate AI},
  url    = {https://github.com/bioMate-AI/realbio-benchmark}
}
```

## Ground-truth sources (external references)
- **BOIN** — Liu & Yuan, *JRSS-C* 2015, [doi:10.1111/rssc.12089](https://doi.org/10.1111/rssc.12089); Yuan et al., *Clin. Cancer Res.* 2016.
- **PBPK** — FDA drug labels; DrugBank (Wishart et al., *NAR* 2006, [doi:10.1093/nar/gkj067](https://doi.org/10.1093/nar/gkj067)); Rodgers & Rowland, *J. Pharm. Sci.* 2007.
- **Routing** — nf-core (Ewels et al., *Nat. Biotechnol.* 2020, [doi:10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x)).
- **Baseline agent** — Biomni (Huang et al., *Science* 2025, [doi:10.1126/science.adz4351](https://doi.org/10.1126/science.adz4351)).

## License
**CC-BY-4.0** — data, ground truth, scorer, and harness. See [`LICENSE`](LICENSE).

---
Built by **[BioMate AI](https://biomate.ai)** · leaderboard: **[on GitHub](https://github.com/bioMate-AI/realbio-benchmark#results)**
