# HuggingFace update — manual steps (do this once you're logged in)

**Status:** PREPARED, NOT UPLOADED. The `hf` CLI on this machine is **not logged in**
(`hf auth whoami` → *Not logged in*), so nothing was pushed to HuggingFace. The updated
dataset card is ready at `hf_update/README.md`.

**No rename needed.** The benchmark name stays **RealBio** (the earlier "BioChore" rename was
reversed). You are only **updating the dataset card** (latest results + the choreography
framing + the PBPK correction). There is **no `hf repo move` step**.

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
  --commit-message "Update card: latest results (PBPK correction), choreography framing"
```

That single `upload` replaces the card in place. Verify at
`https://huggingface.co/datasets/DATASET_ID`.

## 2. (Optional) Sync the task data + scorer to match the GitHub release

If the HF dataset also mirrors the task files, sync the 5 task folders, `src/score.py`,
`leaderboard.csv`, and `paper/RealBio_benchmark.pdf` so HF and GitHub agree:

```bash
hf upload DATASET_ID leaderboard.csv leaderboard.csv --repo-type dataset
hf upload DATASET_ID src/score.py src/score.py --repo-type dataset
hf upload DATASET_ID paper/RealBio_benchmark.pdf paper/RealBio_benchmark.pdf --repo-type dataset
# task data (repeat per task folder, or upload-large-folder for the whole repo):
hf upload DATASET_ID cross_domain_routing cross_domain_routing --repo-type dataset
hf upload DATASET_ID param_prefill param_prefill --repo-type dataset
hf upload DATASET_ID protocol_thresholds protocol_thresholds --repo-type dataset
hf upload DATASET_ID pbpk_benchmark pbpk_benchmark --repo-type dataset
hf upload DATASET_ID boin_benchmark boin_benchmark --repo-type dataset
```

## 3. What changed vs. the previous card

- `pretty_name` stays **RealBio Benchmark** (no rename).
- Results table updated to match the preprint's Supplementary Table S1:
  - **BioMate PBPK 1.00 → 0.200** (same-item 3/15; the old 1.00 was a different, non-comparable task).
  - **Claude Opus 5 BOIN 0.400 → 0.444** (fixes a stale value; GitHub leaderboard already had 0.444).
- Added the choreography tagline (route → configure → QC → model → dose).
- Added a pointer to the in-repo preprint `paper/RealBio_benchmark.pdf`.

> Tip: if you want HF and GitHub to show identical numbers, this card already matches
> the corrected GitHub `leaderboard.csv`.
