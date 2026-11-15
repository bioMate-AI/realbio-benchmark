# RealBio leaderboard

Five agentic-execution tasks, in pipeline order — **Route** (pick the pipeline, n=200), **Configure**
(parameter pre-fill, F1, n=170), **Select method** (Bioconductor method top-1, n=40), **Self-fix**
(failure-category accuracy, n=100), **Generate workflow** (category/key-tool, n=40). Same fixed
items, one open deterministic scorer (`src/score.py`), no AI judge. `—` = no committed result on
that task yet.

| System | Routing | Param (F1) | Method (top-1) | Self-fix | Workflow-gen |
|---|---|---|---|---|---|
| **BioMate** | 0.965 | 0.848 | — | — | — |
| Biomni (A1) | 0.95 | 0.708 | — | 0.95 | 0.5 |
| Claude Opus 5 | 0.615 | 0.757 | 1.0 | 0.87 | 0.5 |
| Gemini 3.1 Pro | 0.58 | 0.693 | 0.975 | 0.88 | 0.5 |
| GPT-5.6 | 0.53 | 0.671 | 1.0 | 0.86 | 0.5 |
| Kimi K3 | 0.45 | 0.628 | 0.975 | 0.77 | 0.45 |
| DeepSeek V4 | 0.415 | 0.621 | 0.825 | 0.8 | 0.5 |
| GLM-5.2 | 0.4 | 0.641 | — | 0.83 | 0.5 |
| GPT-5.6-luna | 0.355 | 0.624 | — | 0.83 | 0.5 |
| Qwen3.8-Max | 0.345 | 0.692 | — | 0.86 | 0.5 |

**Notes.** BioMate's committed results cover routing + parameter pre-fill (it tops both); its
numbers on the three newly-added tasks are pending (not yet run on the same items). `bioc`
(method-selection) results are the `bare` condition and currently cover five systems; the rest are
`—`. `workflow_gen` saturates near 0.50 for most systems (weak discrimination) and is reported for
breadth. Every non-`—` cell re-scores from the committed prediction files under `results/`.
