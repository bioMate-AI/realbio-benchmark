> **22 November 2026 scope correction:** This is retained historical component documentation. The current root README and DATASHEET define the evaluated task version and its limits. Historical labels such as self-fix, PBPK or BOIN do not establish successful repair, physiological simulation or sequential trial execution.

---
license: cc-by-4.0
---
# RealBio Benchmark — autofix_benchmark

*Part of **RealBio Benchmark**: real-world execution benchmarks for bioinformatics AI agents (see the suite README).*

**Task.** Given a failed pipeline run and its error log, classify the failure into one of 10 objective fix categories (genome_mismatch, resource_failure, container_error, dependency_mismatch, missing_input, param_type_error, param_scope_error, data_format_error, output_assertion_error, cloud_storage_error). A free-text 'expected_fix' reference is provided as a secondary signal.

**Items.** 100  ·  **Ground-truth field(s).** `category`  ·  **Scoring.** objective (see src/score.py) — no LLM judge required.

Any system can run this benchmark and be scored on the same items. 


