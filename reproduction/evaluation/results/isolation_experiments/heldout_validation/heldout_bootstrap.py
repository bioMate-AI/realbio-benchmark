#!/usr/bin/env python3
"""Paired item bootstrap CIs for the held-out protocol-QC improvement (v7->v8).

Design (answers the round-6 DeepSeek "no uncertainty" blocker):
  * The resampling unit is the ITEM (one of the 60 held-out protocols), not the
    row. On each iteration we resample the 60 item ids WITH REPLACEMENT, and the
    SAME resampled item set is applied to every condition (bare / card_v1 /
    card_v2) and every model -- so each delta is PAIRED on items and the item
    clustering across the 5 models is respected (an item drawn k times carries
    all 5 of its model rows k times).
  * Metrics are pooled across the 5 models exactly as analyze.py pools them:
    balanced accuracy = mean of present-class recalls over the pooled 3x3
    confusion; WARN recall = WARN-diagonal / WARN-support, pooled.
  * Correctness uses the COMMITTED scorer's norm() exact-match (score.py::norm),
    identical to analyze.py -- nothing here redefines correctness.

Reproduction gate: the point estimates computed here (full set, each item once)
MUST equal the committed analysis.json values before any CI is reported; this is
asserted. Then we report 95% percentile CIs and a bootstrap sign test.
"""
import json, os, importlib.util, random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SCORE_PY = os.path.normpath(os.path.join(HERE, "..", "..", "..", "datasets", "public_export", "score.py"))
DATA = os.path.join(HERE, "heldout_protocol_thresholds.jsonl")

spec = importlib.util.spec_from_file_location("committed_score", SCORE_PY)
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)

CLASSES = ["PASS", "WARN", "FAIL"]
MODELS = ["anthropic/claude-opus-5.5", "openai/gpt-6.1-sol-pro", "google/gemini-3.8-flash",
          "deepseek/deepseek-v4-pro", "z-ai/glm-5.3-prime"]
CONDS = ["bare", "card_v1", "card_v2"]

GT = {r["id"]: r for r in (json.loads(l) for l in open(DATA))}
GOLD = {i: r["expected_correct_action"] for i, r in GT.items()}
ITEM_IDS = list(GOLD.keys())           # the 60 held-out items (resampling unit)
N_ITEMS = len(ITEM_IDS)

def load_preds(model, cond):
    return S.load_preds(os.path.join(HERE, model.replace("/", "_"), f"{cond}.jsonl"))

# PRED[cond][model] = {id: predicted_label_norm_upper}
PRED = {c: {} for c in CONDS}
for c in CONDS:
    for m in MODELS:
        raw = load_preds(m, c)
        lab = {}
        for i, p in raw.items():
            pu = S.norm(p).upper()
            lab[i] = pu if pu in CLASSES else ("EMPTY" if pu in ("", "NONE") else "OTHER")
        PRED[c][m] = lab

def pooled_metrics(cond, counts):
    """counts: {item_id: multiplicity}. Pool the 3x3 confusion across all 5 models
    (each item contributes its 5 model rows x multiplicity). Return balanced acc
    and per-class recall. Mirrors analyze.py exactly on the full set (all mult=1)."""
    diag = Counter(); support = Counter()
    for i, k in counts.items():
        if not k:
            continue
        g = GOLD[i]
        support[g] += 5 * k
        for m in MODELS:
            if PRED[cond][m].get(i) == g:
                diag[g] += k
    recalls = {c: (diag[c] / support[c] if support[c] else None) for c in CLASSES}
    present = [c for c in CLASSES if support[c]]
    bal = sum(recalls[c] for c in present) / len(present) if present else None
    return bal, recalls

def point(cond):
    bal, rec = pooled_metrics(cond, {i: 1 for i in ITEM_IDS})
    return bal, rec

# ---- reproduction gate: match committed analysis.json before reporting CIs ----
pt = {c: point(c) for c in CONDS}
v2_bal, v2_rec = pt["card_v2"]; v1_bal, v1_rec = pt["card_v1"]; bare_bal, bare_rec = pt["bare"]
d_bal_v1 = v2_bal - v1_bal; d_bal_bare = v2_bal - bare_bal
d_warn_v1 = v2_rec["WARN"] - v1_rec["WARN"]

def approx(a, b, tol=1e-3): return abs(a - b) <= tol
assert approx(round(v2_bal, 3), 0.834), f"card-v2 bal-acc {v2_bal} != 0.834"
assert approx(round(d_bal_v1, 3), 0.102), f"delta bal-acc vs v1 {d_bal_v1} != +0.102"
assert approx(round(v2_rec['WARN'], 3), 0.552), f"card-v2 WARN recall {v2_rec['WARN']} != 0.552"
assert approx(round(d_warn_v1, 3), 0.238), f"delta WARN recall vs v1 {d_warn_v1} != +0.238"
print("[gate] committed point estimates reproduced:")
print(f"       card-v2 bal-acc={v2_bal:.4f}  dvs-v1={d_bal_v1:+.4f}  dvs-bare={d_bal_bare:+.4f}")
print(f"       card-v2 WARN recall={v2_rec['WARN']:.4f}  dvs-v1={d_warn_v1:+.4f}")
print(f"       card-v1 bal-acc={v1_bal:.4f}  bare bal-acc={bare_bal:.4f}")

# ---- paired item bootstrap ----
B = 10000
random.seed(20261118)
samp = defaultdict(list)
for _ in range(B):
    counts = Counter(random.choices(ITEM_IDS, k=N_ITEMS))   # resample 60 items w/ replacement
    b2, r2 = pooled_metrics("card_v2", counts)
    b1, r1 = pooled_metrics("card_v1", counts)
    b0, r0 = pooled_metrics("bare", counts)
    samp["v2_bal"].append(b2)
    samp["v1_bal"].append(b1)
    samp["bare_bal"].append(b0)
    samp["d_bal_v2_v1"].append(b2 - b1)
    samp["d_bal_v2_bare"].append(b2 - b0)
    samp["v2_warn"].append(r2["WARN"])
    samp["v1_warn"].append(r1["WARN"])
    samp["d_warn_v2_v1"].append(r2["WARN"] - r1["WARN"])

def ci(xs, lo=2.5, hi=97.5):
    s = sorted(xs); n = len(s)
    def q(p):
        idx = p / 100 * (n - 1); f = int(idx); c = min(f + 1, n - 1)
        return s[f] + (s[c] - s[f]) * (idx - f)
    return q(lo), q(hi)

point_map = {
    "v2_bal": v2_bal, "v1_bal": v1_bal, "bare_bal": bare_bal,
    "d_bal_v2_v1": d_bal_v1, "d_bal_v2_bare": d_bal_bare,
    "v2_warn": v2_rec["WARN"], "v1_warn": v1_rec["WARN"], "d_warn_v2_v1": d_warn_v1,
}
labels = {
    "v2_bal": "card-v2 balanced accuracy",
    "v1_bal": "card-v1 balanced accuracy",
    "bare_bal": "bare balanced accuracy",
    "d_bal_v2_v1": "Δ balanced acc  card-v2 − card-v1",
    "d_bal_v2_bare": "Δ balanced acc  card-v2 − bare",
    "v2_warn": "card-v2 WARN recall",
    "v1_warn": "card-v1 WARN recall",
    "d_warn_v2_v1": "Δ WARN recall  card-v2 − card-v1",
}
print(f"\n[bootstrap] paired item bootstrap, B={B}, n_items={N_ITEMS}, pooled over {len(MODELS)} models, seed=20261118\n")
out = {"B": B, "n_items": N_ITEMS, "models": MODELS, "seed": 20261118, "metrics": {}}
for k in ["v2_bal", "v1_bal", "bare_bal", "d_bal_v2_v1", "d_bal_v2_bare",
          "v2_warn", "v1_warn", "d_warn_v2_v1"]:
    lo, hi = ci(samp[k])
    print(f"  {labels[k]:<38} = {point_map[k]:+.4f}   95% CI [{lo:+.4f}, {hi:+.4f}]")
    out["metrics"][k] = {"point": round(point_map[k], 4), "ci95": [round(lo, 4), round(hi, 4)], "label": labels[k]}

frac_bal = sum(1 for d in samp["d_bal_v2_v1"] if d > 0) / B
frac_warn = sum(1 for d in samp["d_warn_v2_v1"] if d > 0) / B
frac_bal_bare = sum(1 for d in samp["d_bal_v2_bare"] if d > 0) / B
out["bootstrap_sign"] = {
    "frac_iters_d_bal_v2_v1_gt0": round(frac_bal, 4),
    "frac_iters_d_warn_v2_v1_gt0": round(frac_warn, 4),
    "frac_iters_d_bal_v2_bare_gt0": round(frac_bal_bare, 4),
}
print(f"\n  P(Δ bal-acc card-v2>card-v1) over iters = {frac_bal:.4f}  (bootstrap one-sided p ≈ {1-frac_bal:.4f})")
print(f"  P(Δ WARN recall card-v2>card-v1)        = {frac_warn:.4f}")
print(f"  P(Δ bal-acc card-v2>bare)               = {frac_bal_bare:.4f}")

for k, exclude in [("d_bal_v2_v1", "card-v2 > card-v1 balanced acc"),
                   ("d_warn_v2_v1", "card-v2 > card-v1 WARN recall"),
                   ("d_bal_v2_bare", "card-v2 > bare balanced acc")]:
    lo, hi = out["metrics"][k]["ci95"]
    print(f"  [{'EXCLUDES 0' if lo > 0 else 'INCLUDES 0'}] {exclude}: 95% CI [{lo:+.4f}, {hi:+.4f}]")

with open(os.path.join(HERE, "bootstrap_cis.json"), "w") as f:
    json.dump(out, f, indent=2)
print("\nwrote bootstrap_cis.json")
