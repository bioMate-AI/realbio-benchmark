# Can your AI agent actually choreograph a bioinformatics pipeline? Introducing RealBio

Ask a frontier language model about RNA-seq or variant calling and you'll get a fluent,
confident paragraph. That is not the same thing as correctly *running* the analysis. Real
genomics and bioinformatics aren't essays — they are **multi-step pipelines**, and a handful of
agentic decisions decide whether the whole run is even valid: route the request to the right
analysis, configure it from what the user actually said, select the method that's statistically
correct for the data, diagnose why a run failed, and generate the workflow. Get any of these
wrong and you burn real sample and compute budget — and the failure is usually *silent* until
the results are quietly wrong.

So we built **RealBio**, an open benchmark that asks the blunt question most agentic-bio
leaderboards dodge: **can an AI agent actually choreograph the pipeline, or does it only talk
about biology?**

## Why another benchmark — and why this one is different

Almost every agentic-bio benchmark is scored by *each system's own AI judge on its own private
task set*. The numbers aren't comparable across systems, and they quietly invite self-grading.
RealBio is built the opposite way, to be anti-self-grading by construction:

- **550 fixed public items** across **5 core agentic-execution tasks**.
- **Objective, published ground truth** for every item.
- **One shared, open, deterministic scorer** (`src/score.py`) — **no AI judge**, no private
  test set.

Same items, same metric, for every system. Any team can run its own agent on the exact items
and land a number that is *directly comparable* to the leaderboard. You cannot self-grade your
way up it.

## The five tasks are five decisions in one pipeline

1. **Route** (`cross_domain_routing`, n=200) — turn "call germline variants from whole-genome
   sequencing" into the correct pipeline out of a large catalog (63 distinct targets across
   transcriptomics, variant calling, epigenomics, single-cell, proteomics, cryo-EM,
   metagenomics and immunogenomics).
2. **Configure** (`param_prefill`, n=170) — fill that pipeline's parameters from what the user
   said, and *only* those: no invented read lengths, no hallucinated aligners (scored by F1).
3. **Select method** (`bioc_method_selection`, n=40) — given an analysis need and a candidate
   list, pick the method that's actually *correct* — over-representation for a discrete gene
   list, not rank-based GSEA — not a plausible-sounding wrong one.
4. **Self-fix** (`autofix_benchmark`, n=100) — read a failed run's error log and classify the
   real root cause (genome mismatch, missing input, resource failure, …) into one of 10
   objective categories.
5. **Generate workflow** (`workflow_generation`, n=40) — turn an intent into the right analysis
   category or the key tools a from-scratch pipeline needs.

Every item is authored from a documented public source — the nf-core catalog and its parameter
schemas, the Bioconductor method catalog, real nf-core failure modes — not pulled from any
model's training set.

## The headline finding: the harder the search space, the worse LLMs do

Here's the pattern that jumps out of the board. Frontier LLMs are already strong when the answer
space is **closed**:

- **Self-fix** (classify the failure into 10 categories): **0.77–0.88**.
- **Select method** (pick from a provided candidate list): **0.82–1.00** — near-ceiling.

But they fall off hard on the **open-ended** decisions:

- **Route** (choose among hundreds of pipelines): **0.35–0.62**. They'll describe RNA-seq
  beautifully and still send the job to the wrong pipeline.
- **Configure** (precision parameter-filling): **F1 0.62–0.76**, dragged down by *over-filling*
  parameters the user never specified — silently corrupting a run that still looks like it
  worked.

The gap isn't biological knowledge. It's that the moment the agent has to search a large space
and commit — rather than classify within a fixed menu — accuracy collapses. That is exactly the
part of "running a pipeline" that matters, and exactly what a candidate-based benchmark that
hands the model its options would hide.

## Where BioMate lands

BioMate — our purpose-built platform — **leads the two open-ended tasks**, the ones that
separate systems the most: routing **0.965** and parameter-F1 **0.848**, first on each. On
routing, a curated catalog (0.965) decisively beats the same frontier models used directly
(0.345–0.615): on the first decision in any genomics project, a good catalog beats raw model
scale. (BioMate's results on the three newly-added tasks are being run on the same items and
will be posted when complete; we show `—` rather than a number we haven't measured.)

And because no single LLM is the all-round runner-up — Claude Opus 5 and GPT-5.6 top
method-selection at 1.0, Gemini tops self-fix among the bare models, Biomni tops self-fix
overall — strength on one execution decision clearly doesn't transfer to the others.

## Run it yourself

That's the part we're proudest of. The items are fixed and public, the scorer is open and
deterministic, and non-answers count as failures — nothing is silently dropped. Clone the repo,
produce `predictions.jsonl` per task, and score:

```bash
python3 src/score.py cross_domain_routing   my_system/cross_domain_routing.jsonl
python3 src/score.py bioc_method_selection  my_system/bioc_method_selection.jsonl
python3 src/leaderboard.py                  # or regenerate the whole board from results/
# → objective metric + 95% CI, no LLM judge. Directly comparable to the leaderboard.
```

RealBio is a **growing** benchmark: we keep it to the non-clinical, objectively-scorable
execution decisions, and we add tasks only once every system is measured on the same items with
the same ruler. (The drug-development evaluation — drug-exposure modeling, Phase-I dose-finding —
lives in our companion DrugDev-Bench.)

The full preprint, the datasheet, every system's committed predictions, and the scorer are in
the repo under CC-BY-4.0: **github.com/bioMate-AI/realbio-benchmark**.

Biology deserves benchmarks you can audit. If your agent can choreograph the pipeline, come
show it — on the same items, with the same ruler.
