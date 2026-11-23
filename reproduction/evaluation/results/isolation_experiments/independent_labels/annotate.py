#!/usr/bin/env python3
"""STEP 1 -- Independent second-annotator re-labelling of the 60 held-out protocol-QC items.

Each independent annotator (a committee model) is shown ONLY the item's `protocol` and
`universal_threshold_problem` -- NEVER the original authored label (`expected_correct_action`),
`notes`, `ground_truth`, or ANY KB card (v1 or v2). The annotator is given a NEUTRAL
QC-analyst codebook (domain definitions of PASS/WARN/FAIL) that is NOT card-v2's 3-step
STEP1/STEP2/STEP3 rubric. This is a standard second-annotator / inter-rater design, not
"objective ground truth".

Reuses the COMMITTED harness (results/realpharma_harness_v1/run_harness.py) only for its
transport (`call_openrouter`, `_read_key`) and the `_passfail` token extractor -- nothing
about correctness/scoring is redefined here.

max_tokens forced >=8000 (serving-matched). Per-call cost, finish_reason, raw text and
empties are all logged.

Usage: python3 annotate.py --model <id> [--limit N] [--max-tokens 8000]
Writes: annotations/<model_sanitized>.jsonl  +  annotations/<model_sanitized>.usage.json
"""
import json, os, sys, argparse, time, re

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "realpharma_harness_v1"))
DATA = os.path.join(HERE, "..", "heldout_validation", "heldout_protocol_thresholds.jsonl")

sys.path.insert(0, HARNESS_DIR)
import run_harness as H  # call_openrouter, _read_key, _passfail

# ---- NEUTRAL second-annotator codebook (NOT card-v2's text; no protocol-specific rules) ----
NEUTRAL_RUBRIC = (
    "You are a sequencing-core / assay QC analyst reviewing ONE sample. You are given the "
    "PROTOCOL that produced the sample and a FLAGGED METRIC (a quality number that fell "
    "outside a generic one-size-fits-all threshold). Using your own domain knowledge of how "
    "this assay/protocol behaves, decide the correct QC call for the sample:\n"
    "  PASS  = the flagged deviation is a normal, EXPECTED consequence of THIS protocol's "
    "design, and its value is within the range this protocol normally produces; the data are valid.\n"
    "  WARN  = the data are still usable, but the deviation is unusually SEVERE for this "
    "protocol, or the result is only PARTIALLY valid (e.g. trustworthy for only a subset).\n"
    "  FAIL  = a genuine technical / quality DEFECT (contamination, instrument/run failure, "
    "barcode collision, sample swap, etc.) -- something this protocol would NOT normally produce.\n"
    "Judge by domain fact about the assay, NOT by the generic threshold quoted and NOT by any "
    "supplied rulebook. Reason briefly (2-4 sentences), then on the FINAL line output EXACTLY "
    "one word and nothing else: PASS, WARN, or FAIL."
)

def annot_input(r):
    # ONLY protocol + the flagged-metric text. No label, no notes, no ground_truth, no card.
    return f"Protocol: {r['protocol']}\nFlagged metric / QC situation: {r['universal_threshold_problem']}"

def build_prompt(r):
    return f"{NEUTRAL_RUBRIC}\n\nITEM:\n{annot_input(r)}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-tokens", type=int, default=8000)
    args = ap.parse_args()
    assert args.max_tokens >= 8000, "max_tokens must be >=8000"

    key = H._read_key()
    rows = [json.loads(l) for l in open(DATA)]
    if args.limit:
        rows = rows[:args.limit]

    outdir = os.path.join(HERE, "annotations")
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, f"{args.model.replace('/', '_')}.jsonl")

    tot_in = tot_out = n = n_usage = n_empty = 0
    tot_usd = 0.0
    lat = []
    with open(outpath, "w") as f:
        for r in rows:
            prompt = build_prompt(r)
            label, raw, in_tok, out_tok, dt, fr, usd = "", "", None, None, None, None, None
            for attempt in range(4):
                try:
                    t0 = time.time()
                    resp = H.call_openrouter(key, args.model, prompt, args.max_tokens)
                    dt = int((time.time() - t0) * 1000)
                    ch = (resp.get("choices") or [{}])[0]
                    raw = (ch.get("message") or {}).get("content") or ""
                    fr = ch.get("finish_reason")
                    label = H._passfail(raw)  # committed last-token PASS/WARN/FAIL extractor
                    u = resp.get("usage") or {}
                    in_tok = u.get("prompt_tokens"); out_tok = u.get("completion_tokens")
                    usd = u.get("cost")
                    break
                except Exception as e:
                    msg = getattr(e, "read", lambda: b"")()
                    if attempt == 3:
                        sys.stderr.write(f"[{r['id']}] ERR {e} {msg[:200] if msg else ''}\n")
                    else:
                        time.sleep(3 * (attempt + 1))
            rec = {"id": r["id"], "label": label, "raw": raw}
            if fr is not None: rec["finish_reason"] = fr
            if in_tok is not None:
                rec["prompt_tokens"] = in_tok; rec["completion_tokens"] = out_tok
                tot_in += in_tok or 0; tot_out += out_tok or 0; n_usage += 1
            if usd is not None:
                rec["usd"] = usd; tot_usd += usd
            if dt is not None: rec["latency_ms"] = dt; lat.append(dt)
            if label in ("", None):
                n_empty += 1
                sys.stderr.write(f"[EMPTY] {args.model} {r['id']} fr={fr} raw={raw[:120]!r}\n")
            f.write(json.dumps(rec) + "\n"); n += 1
    summary = {
        "task": "independent_annotation", "model": args.model, "n": n,
        "n_with_usage": n_usage, "n_empty_label": n_empty, "max_tokens": args.max_tokens,
        "input_tokens_total": tot_in or None, "output_tokens_total": tot_out or None,
        "latency_ms_mean": round(sum(lat)/len(lat)) if lat else None,
        "usd_total": round(tot_usd, 6) if tot_usd else None,
    }
    with open(os.path.join(outdir, f"{args.model.replace('/', '_')}.usage.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[{args.model}] wrote {n} -> {outpath}  (in={tot_in} out={tot_out} tok; "
          f"empty={n_empty}; ${summary.get('usd_total','?')})")

if __name__ == "__main__":
    main()
