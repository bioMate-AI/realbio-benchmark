REALBIO / REALDRUG OFFLINE REPRODUCTION SNAPSHOT — 22 NOVEMBER 2026

Run: python3 -I reproduce.py
This checks SHA-256 integrity and exact ID coverage for all 110 paired prediction
files and 22 supporting historical files, then prints the historical endpoint
scores. It makes no network calls. Supporting files are not additional independent
task items or a new model population.

Run: python3 -I bootstrap_primary.py > primary-bootstrap.json
This reproduces the original routing, parameter-F1 and method-selection bootstrap
statistics. File paths in its JSON reflect the current package location.

Run: python3 -I supplementary_analysis.py --output supplementary-recomputed.json
This recomputes parameter joint success and key-count stratification and verifies
the saved LLM-reannotation sensitivity analysis, including its paired bootstrap.
It uses 180 EXISTING annotations on the SAME 60 items, not 180 new scientific cases.
Model-based annotation does not establish independent expert label validity.

Run: python3 -I verify_generated_references.py --output references-recomputed.json
This regenerates the 15/20 synthetic task sets in temporary directories, checks
all stored fields, and computes the exact oracle bound for constant exposure
predictions. It does not validate the references against clinical measurements.

The original parameter scorer is retained unchanged. Candidate-key construction
uses per-item annotations. Routing uses a benchmark-wide label vocabulary.
The method condition looks up descriptions for pre-supplied candidates.
The archive is sufficient for offline scoring of the paired core. It is not a
complete replay of historical provider calls or database metadata. Supplementary
analysis files record the newer joint bootstrap and required-key stratification.
Code that contains model-call helpers is archived for provenance only; reproduce.py
does not import or execute those helpers. No credentials or private database is included.
The historical harness credential loader is replaced with a failing stub in this
archival copy; the source and packaged hashes are in provenance-transformations.json.

The existing CC BY 4.0 project notices are preserved under notices/ for attribution.
They do not supersede any upstream third-party terms or grant rights in material
not covered by those notices. This snapshot supports the reported component analyses. Final preprint author metadata
is separate from this data/code release. Use the repository commit SHA to identify
the exact version, and retain the per-file integrity manifest.
