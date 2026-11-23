#!/usr/bin/env python3
"""Paired item-bootstrap 95% CIs for the SERVING-MATCHED card Δ (protocol/PBPK/BOIN).

Uses the committed scorer logic (datasets/public_export/score.py) to score each item per
matched model, asserts the pooled point estimate reproduces partC_serving_matched_scores.json,
then paired item-bootstraps (resample items with replacement; same resampled items applied to
bare and card and to every matched model; pooled mean Δ over model×item). Item-sampling CIs.
"""
import json, os, re, ast, random

HERE = os.path.dirname(os.path.abspath(__file__))
GT_DIR = os.path.normpath(os.path.join(HERE, "../../datasets/public_export"))
PRED_DIR = os.path.join(HERE, "partC_serving_matched")
PARTC = json.load(open(os.path.join(HERE, "partC_serving_matched_scores.json")))
random.seed(20261118)
N_BOOT = 10000

def norm(s): return re.sub(r"\s+", " ", str(s).strip().lower())
# protocol uses the committed 100-item design set; PBPK/BOIN matched runs used data_v2_generated (n=15/20).
GT_FILE = {"protocol_thresholds": "protocol_thresholds/data.jsonl",
           "pbpk_benchmark": "pbpk_benchmark/data_v2_generated.jsonl",
           "boin_benchmark": "boin_benchmark/data_v2_generated.jsonl"}
def load_gt(task): return {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(GT_DIR, GT_FILE[task])))}
def load_preds(path): return {r["id"]: r.get("prediction") for r in (json.loads(l) for l in open(path))}

def correct_protocol(gold, pred): return norm(pred) == norm(gold.get("expected_correct_action"))
def correct_pbpk(gold, pred):
    try:
        ep = gold.get("target_endpoint"); rb = gold["reference"]
        ref = float(rb[ep]) if ep and isinstance(rb, dict) and ep in rb else float(re.search(r"[-+]?\d*\.?\d+", str(rb)).group())
    except Exception:
        return None  # unscoreable
    try: p = float(pred)
    except Exception: return False
    return bool(ref > 0 and 0.5 <= p / ref <= 2.0)
def correct_boin(gold, pred):
    try:
        ref = gold["reference"]; ref = ast.literal_eval(ref) if isinstance(ref, str) else ref
        gt_val = ref.get("true_MTD_mg")
    except Exception:
        gt_val = None
    if gt_val is None: return None
    try: return abs(float(pred) - float(gt_val)) < 1e-6
    except Exception: return False

SCORE = {"protocol_thresholds": correct_protocol, "pbpk_benchmark": correct_pbpk, "boin_benchmark": correct_boin}

def build(task):
    gt = load_gt(task); fn = SCORE[task]; models = PARTC[task]["models"]
    # per item id -> list of (bare_correct, card_correct) over matched models (scoreable items only)
    item_pairs = {}
    per_model_acc = {}
    for m in models:
        bp = load_preds(os.path.join(PRED_DIR, m, f"{task}_bare.jsonl"))
        cp = load_preds(os.path.join(PRED_DIR, m, f"{task}_harness.jsonl"))
        nb = cb = n = 0
        for i, g in gt.items():
            b = fn(g, bp.get(i)); c = fn(g, cp.get(i))
            if b is None or c is None:  # unscoreable GT -> excluded from denominator for both
                continue
            item_pairs.setdefault(i, []).append((int(b), int(c)))
            nb += int(b); cb += int(c); n += 1
        per_model_acc[m] = (round(nb / n, 3), round(cb / n, 3), n)
    return item_pairs, per_model_acc, models

def pooled_delta(item_pairs, ids):
    sb = sc = k = 0
    for i in ids:
        for b, c in item_pairs[i]:
            sb += b; sc += c; k += 1
    return (sc - sb) / k, sb / k, sc / k

out = {}
for task in ["protocol_thresholds", "pbpk_benchmark", "boin_benchmark"]:
    item_pairs, per_model_acc, models = build(task)
    ids = list(item_pairs.keys())
    d_hat, bare_hat, card_hat = pooled_delta(item_pairs, ids)
    exp = PARTC[task]
    # assert reproduction of committed pooled numbers
    assert abs(bare_hat - exp["bare"]) < 0.02, (task, "bare", bare_hat, exp["bare"])
    assert abs(card_hat - exp["card"]) < 0.02, (task, "card", card_hat, exp["card"])
    assert abs(d_hat - exp["delta"]) < 0.02, (task, "delta", d_hat, exp["delta"])
    deltas = []
    for _ in range(N_BOOT):
        samp = [random.choice(ids) for _ in ids]
        deltas.append(pooled_delta(item_pairs, samp)[0])
    deltas.sort()
    lo = deltas[int(0.025 * N_BOOT)]; hi = deltas[int(0.975 * N_BOOT)]
    frac_pos = sum(1 for d in deltas if d > 0) / N_BOOT
    out[task] = {"n_items": len(ids), "n_models": len(models),
                 "bare": round(bare_hat, 3), "card": round(card_hat, 3),
                 "delta": round(d_hat, 3), "ci95": [round(lo, 3), round(hi, 3)],
                 "frac_boot_delta_gt0": round(frac_pos, 4)}
    print(f"{task}: Δ={d_hat:+.3f} [{lo:+.3f}, {hi:+.3f}]  (n_items={len(ids)}, n_models={len(models)}, bare={bare_hat:.3f}, card={card_hat:.3f}, frac>0={frac_pos:.3f})")

json.dump(out, open(os.path.join(HERE, "serving_matched_bootstrap_cis.json"), "w"), indent=2)
print("\nWROTE serving_matched_bootstrap_cis.json")
