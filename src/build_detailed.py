#!/usr/bin/env python3
"""Build the COMPLETE per-sample results table: one row per (system, task, item),
with every field that exists in the committed predictions — plus per-item correctness
(recomputed from ground truth) and per-item $ cost (where tokens were logged).

Output:
  results_detailed.csv    — long format, one row per (system, task, item)
  results_detailed.jsonl  — same, JSONL

Columns:
  system, task, id, difficulty, prediction, ground_truth, correct,
  latency_ms, prompt_tokens, completion_tokens, cost_usd, cost_note

Per-item correctness matches src/score.py exactly (routing acceptable_alts, PBPK 2-fold,
BOIN exact-MTD, protocol action, param-prefill per-item F1>=... reported as param_f1).
Per-item cost = (prompt_tokens*price_in + completion_tokens*price_out)/1e6 * 1.05  (OpenRouter fee),
using each system's published price; only boin/pbpk logged per-item tokens, so cost is blank elsewhere.
"""
import json, os, csv, re, glob, ast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# published OpenRouter prices per 1M tokens (see models.yaml); GLM uses glm-5.3, GPT-5.6 standard tier
PRICE = {  # results-dir name -> (in_per_1m, out_per_1m)
    "anthropic_claude-opus-5":        (5.00, 25.00),
    "google_gemini-3.1-pro-preview":  (1.25, 5.00),
    "openai_gpt-5.6":                 (2.00, 10.00),
    "gpt-5.6":                        (2.00, 10.00),   # GPT-5.6 classification-task batch (same system)
    "openai_gpt-5.6-luna":            (0.20, 1.20),
    "moonshotai_kimi-k3":             (3.00, 15.00),
    "deepseek_deepseek-v4-pro":       (1.12, 3.37),
    "z-ai_glm-5.2":                   (1.40, 4.40),
    "qwen_qwen3.8-max":               (2.00, 6.00),
    "biomni_ec2":                     (3.00, 15.00),   # Biomni engine = Claude Sonnet 4.5 on pbpk/boin
}
FEE = 1.05
DISPLAY = {
    "anthropic_claude-opus-5": "Claude Opus 5", "google_gemini-3.1-pro-preview": "Gemini 3.1 Pro",
    "openai_gpt-5.6": "GPT-5.6", "gpt-5.6": "GPT-5.6", "openai_gpt-5.6-luna": "GPT-5.6-luna", "moonshotai_kimi-k3": "Kimi K3",
    "deepseek_deepseek-v4-pro": "DeepSeek V4", "z-ai_glm-5.2": "GLM-5.2", "qwen_qwen3.8-max": "Qwen3.8-Max",
    "biomni_ec2": "Biomni (A1)",
    "biomate_dev": "BioMate (product)",   # routing (engine-free retrieval) only; other tasks are cross-harness (not committed here)
}
TASKS = ["cross_domain_routing", "param_prefill", "protocol_thresholds", "boin_benchmark", "pbpk_benchmark"]

def norm(s): return re.sub(r"\s+", " ", str(s).strip().lower())

def gt_and_correct(task, row, pred):
    """Return (ground_truth_str, correct_bool_or_f1)."""
    if task == "cross_domain_routing":
        gold = {norm(row.get("correct_workflow"))} | {norm(a) for a in (row.get("acceptable_alts") or [])}
        return row.get("correct_workflow"), (norm(pred) in gold)
    if task == "protocol_thresholds":
        g = row.get("expected_correct_action"); return g, (norm(pred) == norm(g))
    if task == "boin_benchmark":
        ref = row.get("reference"); ref = ast.literal_eval(ref) if isinstance(ref, str) else (ref or {})
        gt = ref.get("true_MTD_mg")
        if gt is None: return "(no MTD)", None
        try: return gt, (abs(float(pred) - float(gt)) < 1e-6)
        except Exception: return gt, False
    if task == "pbpk_benchmark":
        ref = row.get("reference");
        try: refv = float(re.search(r"[-+]?\d*\.?\d+", str(ref)).group())
        except Exception: return str(ref), None
        try: p = float(pred); return refv, (refv > 0 and 0.5 <= p/refv <= 2.0)
        except Exception: return refv, False
    if task == "param_prefill":
        want = row.get("expected_params", {}) or {}
        got = pred if isinstance(pred, dict) else {}
        tp = sum(1 for k, v in want.items() if k in got and norm(got[k]) == norm(v))
        fp = sum(1 for k in got if k not in want)
        fn = len(want) - tp
        prec = tp/(tp+fp) if tp+fp else 0; rec = tp/(tp+fn) if tp+fn else 0
        f1 = 2*prec*rec/(prec+rec) if prec+rec else 0
        viol = sum(1 for k in (row.get("must_not_fill") or []) if k in got)
        return json.dumps(want), round(f1, 3) if not viol else f"{round(f1,3)} (must_not_fill viol={viol})"
    return None, None

def main():
    rows_out = []
    gts = {t: {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(ROOT, t, "data.jsonl")))} for t in TASKS}
    for sysdir in sorted(glob.glob(os.path.join(ROOT, "results", "*"))):
        sysname = os.path.basename(sysdir)
        disp = DISPLAY.get(sysname, sysname)
        price = PRICE.get(sysname)
        for t in TASKS:
            f = None
            for c in (f"{t}.jsonl", f"{t}_bare.jsonl", f"{t}_catalog.jsonl", f"{t}_c2ir.jsonl"):
                if os.path.exists(os.path.join(sysdir, c)): f = os.path.join(sysdir, c); break
            if not f: continue
            for l in open(f):
                try: r = json.loads(l)
                except Exception: continue
                iid = r.get("id"); gtrow = gts[t].get(iid, {})
                pred = r.get("prediction")
                gt, correct = gt_and_correct(t, gtrow, pred)
                pt, ct = r.get("prompt_tokens"), r.get("completion_tokens")
                cost, note = "", ""
                if isinstance(pt, (int, float)) and isinstance(ct, (int, float)) and price:
                    cost = round((pt*price[0] + ct*price[1]) / 1e6 * FEE, 6); note = "tokens×price×1.05(OR fee)"
                elif t in ("cross_domain_routing", "param_prefill", "protocol_thresholds"):
                    note = "per-item tokens not logged for this task"
                rows_out.append({
                    "system": disp, "task": t, "id": iid,
                    "difficulty": gtrow.get("difficulty", ""),
                    "prediction": json.dumps(pred) if isinstance(pred, (dict, list)) else pred,
                    "ground_truth": gt, "correct": correct,
                    "latency_ms": r.get("latency_ms", ""),
                    "prompt_tokens": pt if pt is not None else "",
                    "completion_tokens": ct if ct is not None else "",
                    "cost_usd": cost, "cost_note": note,
                })
    cols = ["system", "task", "id", "difficulty", "prediction", "ground_truth", "correct",
            "latency_ms", "prompt_tokens", "completion_tokens", "cost_usd", "cost_note"]
    with open(os.path.join(ROOT, "results_detailed.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows_out)
    with open(os.path.join(ROOT, "results_detailed.jsonl"), "w") as f:
        for r in rows_out: f.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows_out)} per-sample rows -> results_detailed.csv / .jsonl")
    # quick coverage report
    from collections import Counter
    by = Counter((r["system"], r["task"]) for r in rows_out)
    print(f"systems×tasks cells: {len(by)}; total rows: {len(rows_out)}")

if __name__ == "__main__":
    main()
