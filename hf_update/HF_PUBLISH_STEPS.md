# HuggingFace update — manual steps (do this once you're logged in)

**Status:** PREPARED, NOT UPLOADED. The `hf` CLI on this machine is **not logged in**
(`hf auth whoami` → *Not logged in*), so nothing was pushed to HuggingFace. The updated
dataset card is ready at `hf_update/README.md`.

**No rename needed.** The benchmark name stays **RealBio**. You are **updating the dataset card**
(now a clean 2-task routing + parameter benchmark) and should **delete the removed task folders**
on HF so it matches the re-scoped GitHub repo. There is **no `hf repo move` step**.

---

## 0. Confirm the dataset id

Replace `DATASET_ID` below with your real id, e.g. `biomate-ai/realbio` or `BioMate-AI/RealBio`.
If unsure, list your datasets after logging in:

```bash
hf auth login            # paste a WRITE token from https://huggingface.co/settings/tokens
hf auth whoami           # confirm the account + that the token has write scope
hf repo list --repo-type dataset   # find the exact RealBio dataset id
```

## 1. Push the updated dataset card

The card is the dataset's `README.md` (YAML front-matter sets `pretty_name: RealBio Benchmark`).

```bash
# from the repo root:
hf upload DATASET_ID hf_update/README.md README.md --repo-type dataset \
  --commit-message "Update to 5-task board (550 items); refresh results + choreography framing"
```

That single `upload` replaces the card in place. Verify at
`https://huggingface.co/datasets/DATASET_ID`.

## 2. Sync the task data + scorer, and DELETE the removed tasks

RealBio is now a **2-task** benchmark. Sync the two task folders + scorer + leaderboard + paper:

```bash
hf upload DATASET_ID leaderboard.csv leaderboard.csv --repo-type dataset
hf upload DATASET_ID src/score.py src/score.py --repo-type dataset
hf upload DATASET_ID paper/RealBio_benchmark.pdf paper/RealBio_benchmark.pdf --repo-type dataset
hf upload DATASET_ID cross_domain_routing cross_domain_routing --repo-type dataset
hf upload DATASET_ID param_prefill param_prefill --repo-type dataset
hf upload DATASET_ID bioc_method_selection bioc_method_selection --repo-type dataset
hf upload DATASET_ID autofix_benchmark autofix_benchmark --repo-type dataset
hf upload DATASET_ID workflow_generation workflow_generation --repo-type dataset
hf upload DATASET_ID results results --repo-type dataset   # refreshed per-system predictions
```

Then remove the clinical/QC tasks that moved to DrugDev-Bench (they will otherwise linger on HF):

```bash
# delete the removed task folders + their result files on the HF dataset
hf repo-files DATASET_ID delete pbpk_benchmark --repo-type dataset
hf repo-files DATASET_ID delete boin_benchmark --repo-type dataset
hf repo-files DATASET_ID delete protocol_thresholds --repo-type dataset
# also delete each removed-task prediction file under results/<system>/ if the HF dataset mirrors results/
```

> `hf repo-files ... delete` accepts a path or glob; confirm the exact paths with
> `hf repo-files DATASET_ID list --repo-type dataset` first.

## 3. What changed vs. the previous card

- `pretty_name` stays **RealBio Benchmark** (no rename).
- **Scoped to 5 core tasks** — routing (200) + parameter pre-fill (170) + method-selection
  (40) + self-fix (100) + workflow-gen (40) = **550 items**. The clinical-pharmacology tasks
  (PBPK, BOIN) and QC gating (protocol_thresholds) moved to **DrugDev-Bench**.
- Results table is the **5-task board** (Routing, Param-F1, Method top-1, Self-fix,
  Workflow-gen); `—` marks systems with no committed result on a task.
- Headline reframed around the closed-choice-vs-open-ended finding; choreography tagline
  extended (route → configure → select method → self-fix → generate).
- Points to the in-repo preprint `paper/RealBio_benchmark.pdf`.

> Tip: this card already matches the re-scoped GitHub `leaderboard.csv`.
