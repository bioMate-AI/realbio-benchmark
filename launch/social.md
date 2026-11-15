# RealBio — social launch copy

> Do NOT post from here — these need the user's own LinkedIn / X accounts.
> Links: repo = https://github.com/bioMate-AI/realbio-benchmark · site = https://biomate.ai

---

## LinkedIn (single post)

An AI model can write a flawless paragraph about RNA-seq. That's not the same as sending the job
to the right pipeline.

Real genomics isn't an essay — it's a pipeline, and the first two moves decide whether the whole
run is even valid: **route** the request to the right analysis, then **configure** it from what
the user actually said. So we built **RealBio**, an open benchmark that asks the blunt question
most agentic-bio leaderboards dodge: *can an AI agent actually choreograph the pipeline, or does
it only talk about biology?*

What makes it trustworthy:
• 370 fixed, public items across 2 core agentic-execution tasks (routing + parameter pre-fill)
• Published ground truth + one shared, open, deterministic scorer — **no AI judge, no private
  test set**. You cannot self-grade your way up it.

The headline finding: frontier LLMs are strong on biological *knowledge* and weak at
*execution*. Used bare, they route correctly only **0.35–0.62** of the time, and they over-fill
parameters they were never given — silently corrupting runs that still look like they worked.

BioMate (our platform) leads both tasks — routing **0.965**, parameter-F1 **0.848**. On routing,
a curated catalog decisively beats raw model scale (0.965 vs 0.35–0.62 for the same models used
directly).

Fixed items, open scorer, CC-BY-4.0. Run your own system and land a directly comparable number:
🔗 github.com/bioMate-AI/realbio-benchmark

#AIagents #Bioinformatics #Genomics #Benchmarks #LLM #WorkflowAutomation

---

## X / Twitter thread (6 tweets)

**1/**
An LLM can describe RNA-seq perfectly — and still send the job to the wrong pipeline.

Real biology isn't an essay. It's a pipeline you have to *choreograph*: route it to the right
analysis, then configure it correctly.

Introducing RealBio: an open benchmark for whether AI agents can actually do that. 🧵

**2/**
Most agentic-bio benchmarks are scored by each system's *own* AI judge on its *own* private
tasks. Non-comparable, and quietly self-graded.

RealBio: 370 fixed public items · 2 core execution tasks · published ground truth · ONE open
deterministic scorer · no AI judge.

**3/**
The 2 tasks are the moves that gate everything downstream:
• **Route** (n=200) — pick the right pipeline from a large catalog (63 targets, every omics
  domain)
• **Configure** (n=170) — fill its parameters from the request, and NOTHING you weren't given

Objective answer or it's wrong.

**4/**
Headline finding: frontier LLMs are great at biology *knowledge*, weak at *execution*.

Used bare, they route correctly only **0.35–0.62** of the time. On parameters they over-fill
settings they were never given — silently corrupting runs that still look like they worked.

**5/**
BioMate (our platform) leads both tasks: routing **0.965**, parameter-F1 **0.848**.

The biggest gap is routing — a curated catalog (0.965) beats the same frontier models used
directly (0.35–0.62). On the first decision in any project, catalog > raw model scale.

**6/**
The best part: it's auditable. Fixed public items, open scorer, non-answers count as failures,
CC-BY-4.0.

Run your own agent → get a directly comparable number.
🔗 github.com/bioMate-AI/realbio-benchmark

Can your agent choreograph the pipeline?
