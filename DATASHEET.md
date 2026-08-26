# RealBio — Dataset datasheet

Documentation for the RealBio benchmark dataset (following the *Datasheets for Datasets* spirit). The full paper is forthcoming; cite via [biomate.ai/realbio.html](https://biomate.ai/realbio.html).

## Motivation

Most agentic-bio benchmarks are scored by each system's own judge on its own private task set — non-comparable across systems and open to (often unintentional) self-grading. RealBio was built to be **objectively scored, cross-system, and anti-self-grading by construction**: fixed public items, published ground truth, one shared deterministic scorer (`src/score.py`), and no LLM judge for the objective tasks.

## Composition

**505 items across 5 tasks** (3 further tasks re-added as every system is measured on them), each with a machine-checkable answer and (where relevant) an `acceptable_alts` set. No item is drawn from any system's training corpus; each is **generated or adapted from a documented public source with a stated rationale**.

| Task | n | How items were created (source + rationale) | Difficulty strata |
|---|---:|---|---|
| `cross_domain_routing` | 200 | **Adapted from the nf-core catalog documentation** — each query written from a real pipeline's documented use case (item `notes` cite the source page); `disqualified` lists near-miss distractors. Rationale: public, catalog-neutral routing targets. | direct 125 · indirect 36 · adversarial 39 |
| `param_prefill` | 170 | **Constructed by inference category** (genome_inference, …); each pairs a request with parameters that are *clearly stated* and those that must **not** be filled. Rationale: test inference + over-fill avoidance. | easy 61 · medium 72 · hard 37 |
| `protocol_thresholds` | 100 | **Real public datasets** (each item carries a **GEO/PRIDE/EMDB accession**) on specialized library types where a universal QC threshold false-alarms; **expert-labeled** VALID/DEFECTIVE. | — |
| `autofix_benchmark` | 100 | **Deliberately-broken workflow cases** by failure category (genome_mismatch, missing_input, param_type_error, resource_failure, …); each = workflow + buggy params + realistic error log. | — |
| `workflow_generation` | 40 | **Two partitions:** A = in-catalog (route to existing category), B = out-of-catalog (generate from scratch); intent → category / key tools. | easy 6 · medium 16 · hard 18 |
| `boin_benchmark` | 20 (18 scored) | **Original Phase-I dose-escalation scenarios**; MTD **from the published BOIN operating-characteristic tables** (Yuan et al. 2016). 2 undefined-MTD scenarios excluded. | easy 4 · medium 11 · hard 5 |
| `pbpk_benchmark` | 15 | **15 reference compounds** with well-characterized published human PK from **FDA drug labels + DrugBank + Rodgers & Rowland 2007**; each gives physicochemical inputs + per-item published Cmax/AUC/t½. | easy 3 · medium 7 · hard 5 |
| `drug_discovery_e2e` | 15 | **15 PDBbind protein-ligand systems** selected for experimental ΔG (**PDBbind 2020**), an RCSB PDB crystal structure, **multiple ligands per target**, and diverse target classes. | — |

**Withheld internal tasks.** Two internal tasks (`license_gating`, `memory_benchmark`) are excluded from this public release — their ground truth scores one system's product-specific behaviour, not a neutral cross-system task.

## Collection & labeling

Items were authored by the BioMate team from the public sources above. Ground truth is either a published reference value (PBPK, BOIN, ligand affinity), a public catalog name (routing, workflow-gen), an objective category (autofix), or an expert label against a public accession (protocol thresholds).

## Scoring

One committed scorer, `src/score.py` — exact/threshold match against published ground truth, **no LLM judge**. Every leaderboard cell re-scores from committed `results/<system>/*.jsonl`. Non-answers count as failures (they are never silently dropped). Each score reports its n and a 95% Wilson interval.

## Known limitations

- **PBPK endpoint under-specification:** the `reference` records Cmax/AUC/t½; the prompt does not name the target endpoint and scoring uses Cmax, so a valid value for the wrong endpoint scores as a miss. A fixable dataset issue (name the endpoint), flagged rather than silently changed.
- Small-n tasks (`pbpk`, `boin`, `dd`, `workflow_gen`) carry wide confidence intervals — read them with their CIs.

## Uses & distribution

Intended for **cross-system evaluation of bioinformatics AI agents**. Released **CC-BY-4.0**. Run your system on the fixed items, score with `src/score.py`, and your result is directly comparable to the leaderboard.
