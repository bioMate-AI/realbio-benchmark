# RealBio leaderboard

Two agentic execution tasks — **Routing** (pick the right pipeline, n=200) and **Parameter
pre-fill** (configure it without inventing settings, n=170, scored by F1). Same fixed items,
one open deterministic scorer (`src/score.py`), no AI judge.

| System | Routing | Param (F1) |
|---|---|---|
| **BioMate** | 0.965 | 0.848 |
| Biomni (A1) | 0.95 | 0.708 |
| Claude Opus 5 | 0.615 | 0.757 |
| Gemini 3.1 Pro | 0.58 | 0.693 |
| GPT-5.6 | 0.53 | 0.671 |
| Kimi K3 | 0.45 | 0.628 |
| DeepSeek V4 | 0.415 | 0.621 |
| GLM-5.2 | 0.4 | 0.641 |
| GPT-5.6-luna | 0.355 | 0.624 |
| Qwen3.8-Max | 0.345 | 0.692 |
