# Can your AI agent actually choreograph a drug-development pipeline? Introducing RealBio

Ask a frontier language model about RNA-seq or pharmacokinetics and you'll get a fluent,
confident paragraph. That is not the same thing as correctly *running* the analysis. Real
drug discovery and genomics are not essays — they are **multi-step pipelines** that have to
be choreographed in order: route the request to the right analysis, configure its parameters,
quality-control the incoming data, model the drug, and choose a safe first-in-human dose. Get
any step wrong and you burn real sample and compute budget — and in the last two steps, you're
making a patient-safety call.

So we built **RealBio**, an open benchmark that asks the blunt question most agentic-bio
leaderboards dodge: **can an AI agent actually choreograph the pipeline, or does it only talk
about biology?**

## Why another benchmark — and why this one is different

Almost every agentic-bio benchmark is scored by *each system's own AI judge on its own private
task set*. The numbers aren't comparable across systems, and they quietly invite self-grading.
RealBio is built the opposite way, to be anti-self-grading by construction:

- **505 fixed public items** across **5 real drug-development / genomics tasks**.
- **Objective, published ground truth** for every item.
- **One shared, open, deterministic scorer** (`src/score.py`) — **no AI judge**, no private
  test set.

Same items, same metric, for every system. Any team can run its own agent on the exact items
and land a number that is *directly comparable* to the leaderboard. You cannot self-grade your
way up it.

## The five tasks are five hand-offs in one relay

1. **Route** — turn "call germline variants from whole-genome sequencing" into the correct
   pipeline out of a large catalog (200 items, 63 distinct target pipelines).
2. **Configure** — fill that pipeline's parameters from what the user actually said, and *only*
   those — no invented settings (170 items, scored by F1).
3. **QC** — decide PASS/FAIL on a real sequencing sample using the assay-specific rule, because
   one universal cutoff false-alarms on specialized assays (100 items, real GEO/PRIDE/EMDB data).
4. **Model the drug** — predict how much drug reaches the blood (Cmax, AUC, half-life) within
   2-fold of the published human value (15 marketed drugs).
5. **Dose the trial** — recommend the Phase-I maximum tolerated dose from emerging toxicity data
   using the BOIN design (20 oncology scenarios).

Every abbreviation is a standard drug-development term, spelled out, so the benchmark reads
without prior background. Every item is authored from a documented public source — the nf-core
catalog, public data accessions, published human pharmacokinetics, published BOIN tables — not
pulled from any model's training set.

## The headline finding: fluent about biology, weak at execution

Today's frontier LLMs are strong on biological *knowledge* and genuinely weak at *execution* —
and they're weakest exactly where mistakes cost the most: the clinical-pharmacology tasks.

- On **drug-exposure prediction (PBPK)**, the eight frontier LLMs average **0.08 within-2-fold**.
  This is the hardest task on the board — *no* system we tested exceeds **0.200**. Models will
  write pages of plausible reasoning and still miss the number.
- On **BOIN dose-finding** — a deterministic, table-defined calculation — the LLM mean is **0.24**.
  Several open-weight models emit long reasoning with *no parseable answer at all*, which fails
  deployment even when the thinking is sound.
- Meanwhile the same models are competent at the knowledge-driven extraction tasks (parameter
  F1 clusters in the 0.62–0.76 band).

The gap isn't knowledge. It's the ability to execute the step correctly and return a usable
answer. That is the whole point of measuring choreography instead of conversation.

## Where BioMate lands

BioMate — our purpose-built platform — **leads the orchestration and QC tasks outright**:
routing **0.965**, parameter-F1 **0.848**, protocol-QC **0.925**, BOIN **0.80**. On the hardest
task, PBPK, BioMate scores **0.200**, *tied for the best result on the board* alongside GPT-5.6
and GPT-5.6-luna — because PBPK is simply not solved by anyone yet, and we report it honestly
rather than crowning a winner. (An earlier BioMate "1.00" came from a different, non-comparable
task; the same-item score is 0.200, and we've corrected it everywhere.)

The lead that matters is the broad one: on curated routing, a good catalog beats raw model
scale — BioMate's 0.965 vs the same frontier LLMs at 0.35–0.62 used directly — and no single
LLM is the runner-up across the board.

## Run it yourself

That's the part we're proudest of. The items are fixed and public, the scorer is open and
deterministic, and non-answers count as failures — nothing is silently dropped. Clone the repo,
produce `predictions.jsonl` per task, and score:

```bash
python3 src/score.py cross_domain_routing my_system/cross_domain_routing.jsonl
# → objective metric + 95% CI, no LLM judge. Directly comparable to the leaderboard.
```

The full preprint, the datasheet, every system's committed predictions, and the scorer are in
the repo under CC-BY-4.0: **github.com/bioMate-AI/realbio-benchmark**.

Biology deserves benchmarks you can audit. If your agent can choreograph the pipeline, come
show it — on the same items, with the same ruler.
