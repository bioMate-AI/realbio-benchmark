# Per-model paired results

Archived endpoint labels; conditions and item versions are fixed in the reproduction manifest. These are decision predictions, not executed workflows or product rankings.

## routing

| Endpoint | Bare | Guided | Difference | Difference 95% interval |
|---|---:|---:|---:|---|
| Claude Opus 5 | 0.6150 | 0.9900 | +0.3750 | [+0.3050, +0.4400] |
| Claude Opus 5.5 | 0.6100 | 0.8850 | +0.2750 | [+0.2050, +0.3450] |
| GPT-6.1-sol-pro | 0.5900 | 0.9850 | +0.3950 | [+0.3300, +0.4650] |
| Gemini 3.1 Pro | 0.5800 | 0.9750 | +0.3950 | [+0.3250, +0.4650] |
| Kimi K3 | 0.4950 | 0.9700 | +0.4750 | [+0.4000, +0.5450] |
| DeepSeek V4-pro | 0.4150 | 0.8500 | +0.4350 | [+0.3600, +0.5100] |
| GLM-5.2 | 0.4000 | 0.9500 | +0.5500 | [+0.4800, +0.6250] |
| GLM-5.3-prime | 0.3750 | 0.9550 | +0.5800 | [+0.5100, +0.6500] |
| GPT-5.6-luna | 0.3550 | 0.9500 | +0.5950 | [+0.5200, +0.6700] |
| Qwen2.5-72B | 0.2450 | 0.8950 | +0.6500 | [+0.5800, +0.7200] |
| Qwen3.5-27B | 0.2400 | 0.9350 | +0.6950 | [+0.6300, +0.7550] |
| Qwen3.8-27B | 0.1750 | 0.8750 | +0.7000 | [+0.6300, +0.7650] |
| Qwen2.5-7B | 0.1400 | 0.7350 | +0.5950 | [+0.5250, +0.6650] |
| Qwen3.5-9B | 0.1200 | 0.8300 | +0.7100 | [+0.6450, +0.7750] |

## param

| Endpoint | Bare | Guided | Difference | Difference 95% interval |
|---|---:|---:|---:|---|
| Claude Opus 5 | 0.1408 | 0.8049 | +0.6641 | [+0.6188, +0.7056] |
| Qwen3.5-27B | 0.0637 | 0.7190 | +0.6553 | [+0.6050, +0.6995] |
| Qwen3.8-27B | 0.0630 | 0.6816 | +0.6186 | [+0.5598, +0.6709] |
| Qwen3.5-9B | 0.0481 | 0.6000 | +0.5519 | [+0.4875, +0.6094] |

## method

| Endpoint | Bare | Guided | Difference | Difference 95% interval |
|---|---:|---:|---:|---|
| Claude Opus 5 | 1.0000 | 0.9750 | -0.0250 | [-0.0750, +0.0000] |
| GPT-5.6 | 1.0000 | 1.0000 | +0.0000 | [+0.0000, +0.0000] |
| Gemini 3.1 Pro | 0.9750 | 1.0000 | +0.0250 | [+0.0000, +0.0750] |
| Kimi K3 | 0.9750 | 1.0000 | +0.0250 | [+0.0000, +0.0750] |
| Qwen3.8 (2.4T) | 0.9250 | 1.0000 | +0.0750 | [+0.0000, +0.1750] |
| GLM-5.3 | 0.9000 | 1.0000 | +0.1000 | [+0.0250, +0.2000] |
| DeepSeek V4-pro | 0.8250 | 0.9500 | +0.1250 | [+0.0000, +0.2500] |
| DeepSeek V4.1-flash | 0.8000 | 0.9750 | +0.1750 | [+0.0750, +0.3000] |

Full QC condition matrices and supplementary parameter endpoints are in the reproduction analysis files. Joint-success intervals use the separately recorded seed 20261122; historical F1 intervals above use seed 20261115.
