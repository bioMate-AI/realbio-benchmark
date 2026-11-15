---
license: cc-by-4.0
---
# RealBio Benchmark — bioc_method_selection

*Part of **RealBio Benchmark**: real-world execution benchmarks for bioinformatics AI agents (see the suite README).*

**Task.** Given an analysis need and a candidate list of Bioconductor / workflow methods, pick the one that is **statistically correct for the data** — the fine-grained analogue of RealBio's coarse `cross_domain_routing`. The query states the observable discriminator (data shape / assay / input artifact) but never names a method, so it tests context interpretation, not keyword matching.

**Items.** 40 · **Ground-truth field(s).** `correct_method` (+ `acceptable_alts`), with `invalid_picks` (methods that are a *correctness* failure in context) · **Scoring.** objective (`python3 src/score.py bioc_method_selection <preds.jsonl>`) — no LLM judge.

Each item: `{id, query, candidates[], correct_method, acceptable_alts[], invalid_picks[], discriminator}`. The prediction is a single method name chosen from `candidates`.

**Regimes covered** (confusable-sibling method choices):
- **ORA vs GSEA** — discrete gene list → over-representation (ORA); genome-wide ranked statistic → GSEA; GO/KEGG vs Reactome vs GMT.
- **microarray vs RNA-seq DE** — two-colour intensity → limma; integer counts → DESeq2/edgeR.
- **input-stage DE** — count matrix vs Salmon quant vs multi-method report.
- **proteomics labeling** — TMT / LiP / PTM / label-free DDA.
- **single-cell object format** — SingleCellExperiment → scran; h5ad → scanpy/scdownstream; Seurat → Seurat tools.
- plus additional held-out confusable-sibling cases.

**Metrics** (from `score.py`):
- **top-1 accuracy** — prediction ∈ {`correct_method`} ∪ `acceptable_alts`.
- **invalid_regime_failure_rate** — prediction ∈ `invalid_picks` (a correctness failure, e.g. ORA on ranked data, limma on counts, a TMT method on label-free data) — reported separately so wrong-regime picks are visible, not just suboptimal ones.
- **wrong_but_real_rate** / **hallucination_rate** — prediction is a real candidate but wrong / not among candidates.

Any system can run this benchmark and be scored on the same items.
