# RealBio — social launch copy

> Do NOT post from here — these need the user's own LinkedIn / X accounts.
> Links: repo = https://github.com/bioMate-AI/realbio-benchmark · site = https://biomate.ai

---

## LinkedIn (single post)

An AI model can write a flawless paragraph about RNA-seq. That's not the same as sending the job
to the right pipeline.

Real genomics isn't an essay — it's a pipeline you have to **choreograph**: route the request,
configure it, select the right method, self-fix a failed run, generate the workflow. So we built
**RealBio**, an open benchmark that asks the question most agentic-bio leaderboards dodge: *can
an AI agent actually run those steps, or does it only talk about biology?*

What makes it trustworthy:
• 550 fixed, public items across 5 core agentic-execution tasks
• Published ground truth + one shared, open, deterministic scorer — **no AI judge, no private
  test set**. You cannot self-grade your way up it.

The finding that jumps out: **the harder the search space, the worse LLMs do.** On closed-choice
tasks they're already strong — classifying a failed run's root cause (0.77–0.88) and picking a
method from a candidate list (0.82–1.0). But on open-ended execution they fall off: used directly
they route correctly only 0.35–0.62 of the time and over-fill parameters they were never given.

BioMate (our platform) leads the two open-ended tasks — routing **0.965**, parameter-F1 **0.848**
— where a curated catalog beats raw model scale (0.965 vs 0.35–0.62 for the same models direct).

Fixed items, open scorer, CC-BY-4.0. Run your own system and land a directly comparable number:
🔗 github.com/bioMate-AI/realbio-benchmark

#AIagents #Bioinformatics #Genomics #Benchmarks #LLM #WorkflowAutomation

---

## X / Twitter thread (6 tweets)

**1/**
An LLM can describe RNA-seq perfectly — and still send the job to the wrong pipeline.

Real biology isn't an essay. It's a pipeline you have to *choreograph*: route → configure →
select method → self-fix → generate.

Introducing RealBio: an open benchmark for whether AI agents can actually do that. 🧵

**2/**
Most agentic-bio benchmarks are scored by each system's *own* AI judge on its *own* private
tasks. Non-comparable, and quietly self-graded.

RealBio: 550 fixed public items · 5 core execution tasks · published ground truth · ONE open
deterministic scorer · no AI judge.

**3/**
The 5 tasks = 5 decisions in one pipeline:
• Route (n=200) — pick the pipeline from a large catalog
• Configure (n=170) — fill params, nothing you weren't given
• Select method (n=40) — correct Bioconductor method, not a plausible one
• Self-fix (n=100) — classify a failed run's root cause
• Generate workflow (n=40)

**4/**
The finding that jumps out: **the harder the search space, the worse LLMs do.**

Closed-choice tasks — classify a failure (0.77–0.88), pick from a candidate list (0.82–1.0) —
they're already strong. Open-ended — route across hundreds of pipelines — they drop to 0.35–0.62.

**5/**
BioMate (our platform) leads the two open-ended tasks: routing **0.965**, parameter-F1 **0.848**
— the tasks that separate systems the most.

On routing, a curated catalog (0.965) beats the same frontier models used directly (0.35–0.62).

**6/**
The best part: it's auditable. Fixed public items, open scorer, non-answers count as failures,
CC-BY-4.0.

Run your own agent → get a directly comparable number.
🔗 github.com/bioMate-AI/realbio-benchmark

Can your agent choreograph the pipeline?
