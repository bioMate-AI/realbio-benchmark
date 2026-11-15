# RealBio — social launch copy

> Do NOT post from here — these need the user's own LinkedIn / X accounts.
> Links: repo = https://github.com/bioMate-AI/realbio-benchmark · site = https://biomate.ai

---

## LinkedIn (single post)

An AI model can write a flawless paragraph about pharmacokinetics. That's not the same as
getting the dose right.

Real drug discovery and genomics aren't essays — they're multi-step pipelines you have to
**choreograph** in order: route → configure → QC → model → dose. So we built **RealBio**, an
open benchmark that asks the blunt question most agentic-bio leaderboards dodge: *can an AI
agent actually run the pipeline, or does it only talk about biology?*

What makes it trustworthy:
• 505 fixed, public items across 5 real drug-development / genomics tasks
• Published ground truth + one shared, open, deterministic scorer — **no AI judge, no private
  test set**. You cannot self-grade your way up it.

The headline finding: frontier LLMs are strong on biological *knowledge* and weak at
*execution* — weakest exactly where errors cost the most. On drug-exposure prediction (PBPK),
the frontier-LLM average is **0.08 within-2-fold**, and *no system we tested exceeds 0.200*. On
deterministic BOIN dose-finding, the LLM mean is **0.24** — some models never return a
parseable answer at all.

BioMate (our platform) leads the orchestration and QC tasks — routing 0.965, parameter-F1
0.848, QC 0.925 — and ties for the best score on the hardest task, PBPK, which nobody has
solved yet.

Fixed items, open scorer, CC-BY-4.0. Run your own system and land a directly comparable number:
🔗 github.com/bioMate-AI/realbio-benchmark

#AIagents #DrugDiscovery #Bioinformatics #Benchmarks #LLM #Genomics

---

## X / Twitter thread (6 tweets)

**1/**
An LLM can write a perfect paragraph about pharmacokinetics — and still pick the wrong dose.

Real biology isn't an essay. It's a pipeline you have to *choreograph*: route → configure → QC
→ model → dose.

Introducing RealBio: an open benchmark for whether AI agents can actually run it. 🧵

**2/**
Most agentic-bio benchmarks are scored by each system's *own* AI judge on its *own* private
tasks. Non-comparable, and quietly self-graded.

RealBio: 505 fixed public items · 5 real tasks · published ground truth · ONE open
deterministic scorer · no AI judge.

**3/**
The 5 tasks = 5 hand-offs in one relay:
• Route the request to the right pipeline
• Configure its parameters (no inventing)
• QC the sequencing data
• Model the drug (PBPK)
• Dose the Phase-I trial (BOIN)

Objective answer or it's wrong.

**4/**
Headline finding: frontier LLMs are great at biology *knowledge*, weak at *execution* —
weakest where it matters most.

PBPK (drug exposure): frontier-LLM avg = 0.08 within-2-fold. No system we tested beats 0.200.
BOIN dose-finding: LLM mean = 0.24. Some never return a parseable answer.

**5/**
BioMate (our platform) leads the orchestration + QC tasks: routing 0.965, parameter-F1 0.848,
QC 0.925, BOIN 0.80 — and ties for the best PBPK score (0.200), because nobody has solved that
one yet. We report it honestly, no crowned winner on the hardest task.

**6/**
The best part: it's auditable. Fixed public items, open scorer, non-answers count as failures,
CC-BY-4.0.

Run your own agent → get a directly comparable number.
🔗 github.com/bioMate-AI/realbio-benchmark

Can your agent choreograph the pipeline?
