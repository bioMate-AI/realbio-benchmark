# Can your AI agent actually choreograph a bioinformatics pipeline? Introducing RealBio

Ask a frontier language model about RNA-seq or variant calling and you'll get a fluent,
confident paragraph. That is not the same thing as correctly *running* the analysis. Real
genomics and bioinformatics aren't essays — they are **multi-step pipelines**, and the first
two moves decide whether the whole run is even valid: route the request to the right analysis,
then configure that analysis from what the user actually said. Get either wrong and you burn
real sample and compute budget — and the failure is usually *silent* until the results are
quietly wrong.

So we built **RealBio**, an open benchmark that asks the blunt question most agentic-bio
leaderboards dodge: **can an AI agent actually choreograph the pipeline — route it, then
configure it — or does it only talk about biology?**

## Why another benchmark — and why this one is different

Almost every agentic-bio benchmark is scored by *each system's own AI judge on its own private
task set*. The numbers aren't comparable across systems, and they quietly invite self-grading.
RealBio is built the opposite way, to be anti-self-grading by construction:

- **370 fixed public items** across **2 core agentic-execution tasks**.
- **Objective, published ground truth** for every item.
- **One shared, open, deterministic scorer** (`src/score.py`) — **no AI judge**, no private
  test set.

Same items, same metric, for every system. Any team can run its own agent on the exact items
and land a number that is *directly comparable* to the leaderboard. You cannot self-grade your
way up it.

## The two tasks are the two moves that gate everything downstream

1. **Route** (`cross_domain_routing`, n=200) — turn "call germline variants from whole-genome
   sequencing" into the correct pipeline out of a large catalog. The items span 63 distinct
   target pipelines across transcriptomics, variant calling, epigenomics, single-cell,
   proteomics, cryo-EM, metagenomics and immunogenomics — this is deliberately not five
   variations of one thing.
2. **Configure** (`param_prefill`, n=170) — fill that pipeline's parameters from what the user
   actually said, and *only* those: no invented read lengths, no hallucinated aligners. Scored
   by F1 across 143 distinct parameter names and 11 inference categories, including negative
   cases where the right answer is to fill *nothing*.

Every item is authored from a documented public source — the nf-core catalog and its parameter
schemas — not pulled from any model's training set.

## The headline finding: fluent about biology, weak at execution

Today's frontier LLMs are strong on biological *knowledge* and genuinely weak at *execution* —
the plumbing that decides whether a run is valid.

- Used **bare**, frontier and open-weight models route correctly only **0.35–0.62** of the
  time. They will describe RNA-seq beautifully and still send the job to the wrong pipeline.
- On **parameter pre-fill**, the same models **over-fill settings they were never given** —
  inventing parameters that silently corrupt a run that still *looks* like it succeeded. F1
  clusters in the **0.62–0.76** band, held down as much by over-filling as by misses.

The gap isn't knowledge. It's doing the step right — and returning an answer a pipeline can
actually execute. That is the whole point of measuring choreography instead of conversation.

## Where BioMate lands

BioMate — our purpose-built platform — **leads both tasks**: routing **0.965** and
parameter-F1 **0.848**, first on each. Biomni, the Stanford agent scaffold, ties routing
closely at 0.950; Claude Opus 5 is the best bare model on parameters at 0.757 — so no single
LLM is BioMate's runner-up across both.

The lead that matters most is routing, where the cross-system spread is largest: a curated
catalog (0.965) decisively beats the same frontier models used directly (0.345–0.615). On the
first decision in any genomics project, a good catalog beats raw model scale.

## Run it yourself

That's the part we're proudest of. The items are fixed and public, the scorer is open and
deterministic, and non-answers count as failures — nothing is silently dropped. Clone the repo,
produce `predictions.jsonl` per task, and score:

```bash
python3 src/score.py cross_domain_routing my_system/cross_domain_routing.jsonl
python3 src/score.py param_prefill        my_system/param_prefill.jsonl
# → objective metric + 95% CI, no LLM judge. Directly comparable to the leaderboard.
```

RealBio is a **growing** benchmark: we keep it to the non-clinical, objectively-scorable
orchestration front-end, and we add tasks only once every system is measured on the same items
with the same ruler. (The drug-development evaluation — drug-exposure modeling, Phase-I
dose-finding — lives in our companion DrugDev-Bench.)

The full preprint, the datasheet, every system's committed predictions, and the scorer are in
the repo under CC-BY-4.0: **github.com/bioMate-AI/realbio-benchmark**.

Biology deserves benchmarks you can audit. If your agent can choreograph the pipeline, come
show it — on the same items, with the same ruler.
