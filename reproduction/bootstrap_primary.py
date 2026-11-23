#!/usr/bin/env python3
"""
compute_bootstrap_cis.py — real paired bootstrap 95% CIs for the RealBio harness-dividend study.

Uses ONLY the committed per-item prediction files and the COMMITTED deterministic scorers
(datasets/public_export/score.py for routing + param; datasets/bioc_method_selection/score.py
for method-selection). No LLM judge, no imputation, no fabrication.

Method
------
For each paired task (bare vs harness) we reconstruct the committed scorer's per-item primitives,
VALIDATE that the reconstruction reproduces the committed scorer's full-set aggregate exactly, and
then resample ITEMS with replacement (paired: the same resampled item ids are used for bare and
harness within an iteration, so the CI is on the paired within-model difference).

 - routing  : per-item binary hit (score_routing logic: norm_wf match vs correct_workflow|acceptable_alts)
 - param    : per-item (tp, fp, fn) (score_param_prefill logic), F1 recomputed on each resample
 - method   : per-item binary hit (bioc score.py logic: norm match vs correct_method|acceptable_alts)

Outputs a JSON blob (stdout) and is imported by nothing — it is the reproducible source of bootstrap_cis.md.

Usage:  python3 compute_bootstrap_cis.py [--iters 5000] [--seed 20261115]
"""
import json, os, sys, random, importlib.util, statistics, glob
from pathlib import Path

EXPORT = str(Path(__file__).resolve().parent / "evaluation/datasets/public_export")
BIOC = str(Path(__file__).resolve().parent / "evaluation/datasets/bioc_method_selection")

def _imp(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

SC = _imp(os.path.join(EXPORT, "score.py"), "realbio_score")  # committed routing/param scorer

def jl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]

def preds_map(path):
    return {r["id"]: r.get("prediction") for r in jl(path)}

# ---------------------------------------------------------------------------
# Per-item primitive builders (faithful to the committed scorers)
# ---------------------------------------------------------------------------
def routing_hits(gt, preds):
    """Return {id: 0/1} using score_routing's exact matching rule."""
    out = {}
    for i, r in gt.items():
        if i not in preds: continue
        gold = {SC.norm_wf(r.get("correct_workflow"))} | {SC.norm_wf(a) for a in (r.get("acceptable_alts") or [])}
        out[i] = 1 if SC.norm_wf(preds[i]) in gold else 0
    return out

def param_prims(gt, preds):
    """Return {id: (tp, fp, fn, viol)} using score_param_prefill's exact rules."""
    out = {}
    for i, r in gt.items():
        if i not in preds: continue
        want = r.get("expected_params", {}) or {}
        got = preds[i] if isinstance(preds[i], dict) else {}
        tp = fp = fn = viol = 0
        for k, v in want.items():
            if k in got and SC.val_eq(v, got[k]): tp += 1
            else: fn += 1
        for k in got:
            if k not in want: fp += 1
        for k in (r.get("must_not_fill") or []):
            if k in got: viol += 1
        out[i] = (tp, fp, fn, viol)
    return out

def method_hits(gt, preds):
    """Return {id: 0/1} using bioc_method_selection/score.py's exact matching rule."""
    def norm(s): return str(s).strip().lower() if s is not None else ""
    out = {}
    for i, r in gt.items():
        if i not in preds: continue
        p = norm(preds[i])
        g = {norm(r["correct_method"])} | {norm(a) for a in r.get("acceptable_alts", [])}
        out[i] = 1 if p in g else 0
    return out

def f1_from(tp, fp, fn):
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0
    return (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0

# ---------------------------------------------------------------------------
# Rosters (clean pairs only: both bare & harness files exist at the SAME slug)
# dir -> display name. Frontier/open models only (on-prem base/sft, biomni, biomate excluded).
# ---------------------------------------------------------------------------
ROUTING_MODELS = {
    "anthropic_claude-opus-5": "Claude Opus 5",
    "anthropic_claude-opus-5.5": "Claude Opus 5.5",
    "openai_gpt-6.1-sol-pro": "GPT-6.1-sol-pro",
    "google_gemini-3.1-pro-preview": "Gemini 3.1 Pro",
    "moonshotai_kimi-k3": "Kimi K3",
    "deepseek_deepseek-v4-pro": "DeepSeek V4-pro",
    "z-ai_glm-5.2": "GLM-5.2",
    "z-ai_glm-5.3-prime": "GLM-5.3-prime",
    "openai_gpt-5.6-luna": "GPT-5.6-luna",
    "qwen_qwen-2.5-72b-instruct": "Qwen2.5-72B",
    "qwen_qwen3.5-27b": "Qwen3.5-27B",
    "qwen_qwen3.8-27b": "Qwen3.8-27B",
    "qwen_qwen-2.5-7b-instruct": "Qwen2.5-7B",
    "qwen_qwen3.5-9b": "Qwen3.5-9B",
}
PARAM_MODELS = {
    "anthropic_claude-opus-5": "Claude Opus 5",
    "qwen_qwen3.5-27b": "Qwen3.5-27B",
    "qwen_qwen3.8-27b": "Qwen3.8-27B",
    "qwen_qwen3.5-9b": "Qwen3.5-9B",
}
METHOD_MODELS = {
    "anthropic_claude-opus-5": "Claude Opus 5",
    "openai_gpt-5.6": "GPT-5.6",
    "google_gemini-3.1-pro-preview": "Gemini 3.1 Pro",
    "moonshotai_kimi-k3": "Kimi K3",
    "qwen_qwen3.8-2.4t-a95b": "Qwen3.8 (2.4T)",
    "z-ai_glm-5.3": "GLM-5.3",
    "deepseek_deepseek-v4-pro": "DeepSeek V4-pro",
    "deepseek_deepseek-v4.1-flash": "DeepSeek V4.1-flash",
}

def ci(sorted_vals, lo=2.5, hi=97.5):
    n = len(sorted_vals)
    def q(p):
        idx = p / 100 * (n - 1)
        lo_i = int(idx); frac = idx - lo_i
        if lo_i + 1 < n: return sorted_vals[lo_i] * (1 - frac) + sorted_vals[lo_i + 1] * frac
        return sorted_vals[lo_i]
    return round(q(lo), 4), round(q(hi), 4)

def main():
    iters = 5000; seed = 20261115
    for a in sys.argv[1:]:
        if a.startswith("--iters"): iters = int(sys.argv[sys.argv.index(a) + 1])
        if a.startswith("--seed"):  seed = int(sys.argv[sys.argv.index(a) + 1])
    rng = random.Random(seed)

    rt_gt  = {r["id"]: r for r in jl(os.path.join(EXPORT, "cross_domain_routing", "data.jsonl"))}
    pf_gt  = {r["id"]: r for r in jl(os.path.join(EXPORT, "param_prefill", "data.jsonl"))}
    ms_gt  = {r["id"]: r for r in jl(os.path.join(BIOC, "data.jsonl"))}

    report = {"iters": iters, "seed": seed, "files_used": {}, "tasks": {}}

    # ---- ROUTING ----
    rt = {"metric": "accuracy", "n_items": len(rt_gt), "harness_condition": "cross_domain_routing_catalog_described.jsonl",
          "bare_condition": "cross_domain_routing_bare.jsonl", "models": []}
    rt_bare_hits, rt_harn_hits = {}, {}
    files = {}
    for d, name in ROUTING_MODELS.items():
        bp = os.path.join(EXPORT, "results", d, "cross_domain_routing_bare.jsonl")
        hp = os.path.join(EXPORT, "results", d, "cross_domain_routing_catalog_described.jsonl")
        bh = routing_hits(rt_gt, preds_map(bp)); hh = routing_hits(rt_gt, preds_map(hp))
        ids = sorted(set(bh) & set(hh))
        rt_bare_hits[name] = bh; rt_harn_hits[name] = hh
        bare = sum(bh[i] for i in ids) / len(ids); harn = sum(hh[i] for i in ids) / len(ids)
        # per-model paired bootstrap over shared item ids
        dd = []
        for _ in range(iters):
            samp = [ids[rng.randrange(len(ids))] for _ in range(len(ids))]
            b = sum(bh[i] for i in samp) / len(samp); h = sum(hh[i] for i in samp) / len(samp)
            dd.append(h - b)
        dd.sort()
        lo, hi = ci(dd)
        # VALIDATION: reconstructed full-set score must equal the committed scorer exactly
        gold_bare = SC.score_routing(rt_gt, preds_map(bp))["accuracy"]
        gold_harn = SC.score_routing(rt_gt, preds_map(hp))["accuracy"]
        assert abs(gold_bare - bare) < 1e-9 and abs(gold_harn - harn) < 1e-9, \
            f"routing reconstruction mismatch for {name}: {gold_bare}/{bare} {gold_harn}/{harn}"
        rt["models"].append({"model": name, "dir": d, "n": len(ids),
                             "bare": round(bare, 4), "harness": round(harn, 4), "delta": round(harn - bare, 4),
                             "delta_ci95": [lo, hi]})
        files[name] = {"bare": bp, "harness": hp, "n": len(ids)}
    report["files_used"]["routing"] = files
    # mean delta across models, item-level shared resample
    r_ids = sorted(set.intersection(*[set(rt_bare_hits[m]) for m in rt_bare_hits]))
    names = [m["model"] for m in rt["models"]]
    md = []
    for _ in range(iters):
        samp = [r_ids[rng.randrange(len(r_ids))] for _ in range(len(r_ids))]
        per = []
        for nm in names:
            b = sum(rt_bare_hits[nm][i] for i in samp) / len(samp)
            h = sum(rt_harn_hits[nm][i] for i in samp) / len(samp)
            per.append(h - b)
        md.append(sum(per) / len(per))
    md.sort(); mlo, mhi = ci(md)
    rt["mean_delta"] = round(statistics.mean([m["delta"] for m in rt["models"]]), 4)
    rt["mean_delta_ci95"] = [mlo, mhi]
    report["tasks"]["routing"] = rt

    # ---- PARAM ----
    pf = {"metric": "param-F1", "n_items": len(pf_gt), "harness_condition": "param_prefill.jsonl",
          "bare_condition": "param_prefill_bare.jsonl", "models": []}
    pf_bare, pf_harn = {}, {}
    files = {}
    for d, name in PARAM_MODELS.items():
        bp = os.path.join(EXPORT, "results", d, "param_prefill_bare.jsonl")
        hp = os.path.join(EXPORT, "results", d, "param_prefill.jsonl")
        bprim = param_prims(pf_gt, preds_map(bp)); hprim = param_prims(pf_gt, preds_map(hp))
        ids = sorted(set(bprim) & set(hprim))
        pf_bare[name] = bprim; pf_harn[name] = hprim
        def agg_f1(prim, samp):
            tp = sum(prim[i][0] for i in samp); fp = sum(prim[i][1] for i in samp); fn = sum(prim[i][2] for i in samp)
            return f1_from(tp, fp, fn)
        bare = agg_f1(bprim, ids); harn = agg_f1(hprim, ids)
        bviol = sum(bprim[i][3] for i in ids); hviol = sum(hprim[i][3] for i in ids)
        dd = []
        for _ in range(iters):
            samp = [ids[rng.randrange(len(ids))] for _ in range(len(ids))]
            dd.append(agg_f1(hprim, samp) - agg_f1(bprim, samp))
        dd.sort(); lo, hi = ci(dd)
        gb = SC.score_param_prefill(pf_gt, preds_map(bp)); gh = SC.score_param_prefill(pf_gt, preds_map(hp))
        assert gb["param_f1"] == round(bare, 4) and gh["param_f1"] == round(harn, 4), \
            f"param reconstruction mismatch for {name}: {gb['param_f1']}/{round(bare,4)} {gh['param_f1']}/{round(harn,4)}"
        assert gb["must_not_fill_violations"] == bviol and gh["must_not_fill_violations"] == hviol
        pf["models"].append({"model": name, "dir": d, "n": len(ids),
                             "bare_f1": round(bare, 4), "harness_f1": round(harn, 4), "delta": round(harn - bare, 4),
                             "delta_ci95": [lo, hi], "viol_bare": bviol, "viol_harness": hviol})
        files[name] = {"bare": bp, "harness": hp, "n": len(ids)}
    report["files_used"]["param"] = files
    p_ids = sorted(set.intersection(*[set(pf_bare[m]) for m in pf_bare]))
    pnames = [m["model"] for m in pf["models"]]
    md = []
    for _ in range(iters):
        samp = [p_ids[rng.randrange(len(p_ids))] for _ in range(len(p_ids))]
        per = []
        for nm in pnames:
            def af1(prim):
                tp = sum(prim[i][0] for i in samp); fp = sum(prim[i][1] for i in samp); fn = sum(prim[i][2] for i in samp)
                return f1_from(tp, fp, fn)
            per.append(af1(pf_harn[nm]) - af1(pf_bare[nm]))
        md.append(sum(per) / len(per))
    md.sort(); mlo, mhi = ci(md)
    pf["mean_delta"] = round(statistics.mean([m["delta"] for m in pf["models"]]), 4)
    pf["mean_delta_ci95"] = [mlo, mhi]
    report["tasks"]["param"] = pf

    # ---- METHOD SELECTION ----
    ms = {"metric": "top1_accuracy", "n_items": len(ms_gt), "harness_condition": "<model>_kb.jsonl",
          "bare_condition": "<model>_bare.jsonl", "models": []}
    ms_bare, ms_harn = {}, {}
    files = {}
    for d, name in METHOD_MODELS.items():
        bp = os.path.join(BIOC, "results", d + "_bare.jsonl")
        hp = os.path.join(BIOC, "results", d + "_kb.jsonl")
        bh = method_hits(ms_gt, preds_map(bp)); hh = method_hits(ms_gt, preds_map(hp))
        ids = sorted(set(bh) & set(hh))
        ms_bare[name] = bh; ms_harn[name] = hh
        bare = sum(bh[i] for i in ids) / len(ids); harn = sum(hh[i] for i in ids) / len(ids)
        dd = []
        for _ in range(iters):
            samp = [ids[rng.randrange(len(ids))] for _ in range(len(ids))]
            dd.append(sum(hh[i] for i in samp) / len(samp) - sum(bh[i] for i in samp) / len(samp))
        dd.sort(); lo, hi = ci(dd)
        ms["models"].append({"model": name, "dir": d, "n": len(ids),
                             "bare": round(bare, 4), "harness": round(harn, 4), "delta": round(harn - bare, 4),
                             "delta_ci95": [lo, hi]})
        files[name] = {"bare": bp, "harness": hp, "n": len(ids)}
    report["files_used"]["method"] = files
    m_ids = sorted(set.intersection(*[set(ms_bare[m]) for m in ms_bare]))
    mnames = [m["model"] for m in ms["models"]]
    md = []
    for _ in range(iters):
        samp = [m_ids[rng.randrange(len(m_ids))] for _ in range(len(m_ids))]
        per = []
        for nm in mnames:
            b = sum(ms_bare[nm][i] for i in samp) / len(samp); h = sum(ms_harn[nm][i] for i in samp) / len(samp)
            per.append(h - b)
        md.append(sum(per) / len(per))
    md.sort(); mlo, mhi = ci(md)
    ms["mean_delta"] = round(statistics.mean([m["delta"] for m in ms["models"]]), 4)
    ms["mean_delta_ci95"] = [mlo, mhi]
    # bootstrap p-value: two-sided, does mean-delta distribution straddle 0
    p_ge0 = sum(1 for x in md if x >= 0) / len(md)
    p_le0 = sum(1 for x in md if x <= 0) / len(md)
    ms["mean_delta_boot_p_two_sided"] = round(2 * min(p_ge0, p_le0), 4)
    ms["mean_delta_ci_contains_0"] = (mlo <= 0 <= mhi)
    report["tasks"]["method"] = ms

    # ---- OPEN vs CLOSED RATIO (the "~9x") ----
    # Each iteration: independently resample routing items, param items, method items; compute mean
    # delta per task; form the ratios. Denominator = method-selection mean delta (can be ~0 or <0).
    def af1s(prim, s):
        tp = sum(prim[i][0] for i in s); fp = sum(prim[i][1] for i in s); fn = sum(prim[i][2] for i in s)
        return f1_from(tp, fp, fn)
    ratios_rt, ratios_pf, ratios_open = [], [], []
    n_method_le0 = 0
    for _ in range(iters):
        rs = [r_ids[rng.randrange(len(r_ids))] for _ in range(len(r_ids))]
        rdelta = statistics.mean([sum(rt_harn_hits[nm][i] for i in rs) / len(rs) - sum(rt_bare_hits[nm][i] for i in rs) / len(rs) for nm in names])
        ps = [p_ids[rng.randrange(len(p_ids))] for _ in range(len(p_ids))]
        pdelta = statistics.mean([af1s(pf_harn[nm], ps) - af1s(pf_bare[nm], ps) for nm in pnames])
        msamp = [m_ids[rng.randrange(len(m_ids))] for _ in range(len(m_ids))]
        mdelta = statistics.mean([sum(ms_harn[nm][i] for i in msamp) / len(msamp) - sum(ms_bare[nm][i] for i in msamp) / len(msamp) for nm in mnames])
        if mdelta <= 0:
            n_method_le0 += 1
        if mdelta != 0:
            ratios_rt.append(rdelta / mdelta)
            ratios_pf.append(pdelta / mdelta)
            ratios_open.append(((rdelta + pdelta) / 2) / mdelta)
    def summ(xs):
        xs2 = sorted(xs); lo, hi = ci(xs2)
        return {"median": round(statistics.median(xs2), 3), "ci95": [round(lo, 3), round(hi, 3)]}
    report["ratio_open_vs_closed"] = {
        "note": ("denominator = method-selection mean delta (point +%.4f). When the denominator "
                 "resample is <=0 the ratio is undefined/negative; its instability is the headline finding." % ms["mean_delta"]),
        "routing_over_method": summ(ratios_rt),
        "param_over_method": summ(ratios_pf),
        "open_avg_over_method": summ(ratios_open),
        "frac_iters_method_delta_le_0": round(n_method_le0 / iters, 4),
        "n_iters_ratio_defined": len(ratios_rt),
    }
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
