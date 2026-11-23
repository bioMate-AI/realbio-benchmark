#!/usr/bin/env python3
"""Portable offline parameter and LLM-reannotation analyses; no model/API imports."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import re
import statistics

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--root', type=Path, default=HERE if (HERE / 'manifest.json').exists() else HERE.parents[1])
ap.add_argument('--output', type=Path)
args = ap.parse_args()
ROOT = args.root.resolve()
PUB = ROOT / 'evaluation/datasets/public_export'
EXP = ROOT / 'evaluation/results/isolation_experiments'
spec = importlib.util.spec_from_file_location('historical_score', PUB / 'score.py')
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)
hashes = {}


def rows(path):
    data = path.read_bytes()
    hashes[str(path.relative_to(ROOT))] = hashlib.sha256(data).hexdigest()
    rs = [json.loads(s) for s in data.decode().splitlines() if s.strip()]
    assert len({r['id'] for r in rs}) == len(rs), f'Duplicate IDs: {path}'
    return {r['id']: r for r in rs}


def predictions(path, gold, field='prediction'):
    rs = rows(path)
    assert set(rs) == set(gold), f'Incomplete or extra IDs: {path}'
    return {i: r.get(field) for i, r in rs.items()}


def interval(values):
    vs = sorted(values)
    def q(p):
        x = (len(vs)-1)*p
        n = int(x)
        return vs[n]+(vs[min(n+1,len(vs)-1)]-vs[n])*(x-n)
    return [q(.025), q(.975)]


PARAM = [('anthropic_claude-opus-5', 'Claude Opus 5'), ('qwen_qwen3.5-27b', 'Qwen3.5-27B'),
         ('qwen_qwen3.8-27b', 'Qwen3.8-27B'), ('qwen_qwen3.5-9b', 'Qwen3.5-9B')]
pg = rows(PUB / 'param_prefill/data.jsonl')
joint, summary = {}, {}
for slug, name in PARAM:
    joint[name], summary[name] = {}, {}
    for condition, suffix in [('bare', '_bare'), ('harness', '')]:
        ps = predictions(PUB / 'results' / slug / f'param_prefill{suffix}.jsonl', pg)
        success, exact, strata = {}, {}, {}
        empty_false_matches, invalid_objects = [], []
        for i, r in pg.items():
            want = r.get('expected_params') or {}
            obj = ps[i]
            if not isinstance(obj, dict):
                invalid_objects.append(i)
            got = obj if isinstance(obj, dict) else {}
            all_correct = all(k in got and score.val_eq(v, got[k]) for k,v in want.items())
            success[i] = int(all_correct and not set(got).intersection(r.get('must_not_fill') or []))
            exact[i] = int(all_correct and set(got) == set(want))
            for k,v in want.items():
                if k in got and score.norm(got[k]) == '' and score.norm(v) != '' and score.val_eq(v, got[k]):
                    empty_false_matches.append({'id':i,'key':k})
            strata.setdefault(len(want), []).append(i)
        joint[name][condition] = success
        summary[name][condition] = dict(joint=statistics.mean(success.values()),
            exact_object=statistics.mean(exact.values()), empty_string_false_matches=empty_false_matches,
            invalid_objects=invalid_objects, historical_metrics=score.score_param_prefill(pg,ps),
            by_required_key_count={str(k): dict(n=len(ids),joint=statistics.mean(success[i] for i in ids),
                exact_object=statistics.mean(exact[i] for i in ids)) for k,ids in sorted(strata.items())})
ids = sorted(pg)
rng = random.Random(20261122)
dist = {name: [] for _,name in PARAM};dist['mean'] = []
for _ in range(5000):
    sample = [ids[rng.randrange(len(ids))] for _ in ids]
    ds = []
    for _,name in PARAM:
        d = statistics.mean(joint[name]['harness'][i]-joint[name]['bare'][i] for i in sample)
        dist[name].append(d);ds.append(d)
    dist['mean'].append(statistics.mean(ds))
jb = {'seed':20261122,'iterations':5000,'models':{}}
for _,name in PARAM:
    b,h = summary[name]['bare']['joint'],summary[name]['harness']['joint']
    jb['models'][name] = dict(bare=b,harness=h,delta=h-b,delta_ci95=interval(dist[name]))
jb['mean'] = {k:statistics.mean(jb['models'][name][k] for _,name in PARAM) for k in ['bare','harness','delta']}
jb['mean']['delta_ci95'] = interval(dist['mean'])

ANNOTATORS = ['anthropic_claude-opus-5.5','openai_gpt-6.1-sol-pro','google_gemini-3.8-flash']
MODELS = ANNOTATORS+['deepseek_deepseek-v4-pro','z-ai_glm-5.3-prime']
CONDS = ['bare','card_v1','card_v2']
CLASSES = ['PASS','WARN','FAIL']
hg = rows(EXP / 'heldout_validation/heldout_protocol_thresholds.jsonl')
original = {i:r['expected_correct_action'] for i,r in hg.items()}
ann,majority = {},{}
for model in ANNOTATORS:
    raw = rows(EXP / 'independent_labels/annotations' / f'{model}.jsonl')
    assert set(raw) == set(hg)
    ann[model] = {}
    for i,r in raw.items():
        label = str(r.get('label') or '').strip().upper()
        assert label in CLASSES
        words = re.findall(r'\b(PASS|WARN|FAIL)\b', r.get('raw','').upper())
        assert words and words[-1] == label, (model,i,'raw/stored label mismatch')
        ann[model][i] = label
for i in hg:
    votes = Counter(ann[m][i] for m in ANNOTATORS)
    label,n = votes.most_common(1)[0]
    assert n >= 2, f'No majority: {i}'
    majority[i] = label
observed = sum(majority[i] == original[i] for i in hg)/len(hg)
og,ng = Counter(original.values()),Counter(majority.values())
chance = sum(og[c]*ng[c] for c in CLASSES)/len(hg)**2
kappa = (observed-chance)/(1-chance)
preds = {c:{m:predictions(EXP/'heldout_validation'/m/f'{c}.jsonl',hg) for m in MODELS} for c in CONDS}


def qc_metrics(labels, models, condition, multiplicities):
    hit,support = Counter(),Counter()
    for i,k in multiplicities.items():
        c = labels[i]
        support[c] += k*len(models)
        hit[c] += k*sum(score.norm(preds[condition][m][i]) == score.norm(c) for m in models)
    recalls = {c:hit[c]/support[c] if support[c] else None for c in CLASSES}
    present = [v for v in recalls.values() if v is not None]
    return dict(accuracy=sum(hit.values())/sum(support.values()),
                balanced_accuracy=statistics.mean(present),recall=recalls)


ones = Counter({i:1 for i in hg})
panels = {}
for label_name, labels in [('original',original),('LLM_majority',majority)]:
    panels[label_name] = {}
    for cohort,models in [('all_five',MODELS),('non_annotators',MODELS[3:])]:
        panels[label_name][cohort] = {c:qc_metrics(labels,models,c,ones) for c in CONDS}
saved = json.loads((EXP/'independent_labels/indep_bootstrap_cis.json').read_text())
pts = panels['LLM_majority']['all_five']
assert round(pts['card_v2']['balanced_accuracy'],4) == saved['metrics']['v2_bal']['point']
assert round(pts['card_v2']['balanced_accuracy']-pts['card_v1']['balanced_accuracy'],4) == saved['metrics']['d_bal_v2_v1']['point']
rng = random.Random(20261118)
distributions = {k:[] for k in saved['metrics']}
for _ in range(10000):
    counts = Counter(rng.choices(list(hg),k=len(hg)))
    p = {c:qc_metrics(majority,MODELS,c,counts) for c in CONDS}
    b,v1,v2 = p['bare'],p['card_v1'],p['card_v2']
    vals = dict(v2_bal=v2['balanced_accuracy'],v1_bal=v1['balanced_accuracy'],bare_bal=b['balanced_accuracy'],
        d_bal_v2_v1=v2['balanced_accuracy']-v1['balanced_accuracy'],d_bal_v2_bare=v2['balanced_accuracy']-b['balanced_accuracy'],
        v2_warn=v2['recall']['WARN'],v1_warn=v1['recall']['WARN'],d_warn_v2_v1=(v2['recall']['WARN'] or 0)-(v1['recall']['WARN'] or 0))
    for k,v in vals.items():distributions[k].append(v)
ci = {k:[round(v,4) for v in interval(vs)] for k,vs in distributions.items()}
assert all(ci[k] == saved['metrics'][k]['ci95'] for k in ci), 'Alternative-label bootstrap mismatch'
report = dict(status='pass',new_inference_calls=0,parameter=dict(summary=summary,joint_bootstrap=jb),
    LLM_reannotation=dict(items=len(hg),annotation_files=3,annotations=3*len(hg),
        original_class_counts=og,alternative_class_counts=ng,agreement=observed,kappa=kappa,
        disagreements=[dict(id=i,original=original[i],alternative=majority[i]) for i in hg if original[i] != majority[i]],
        unanimous_items=sum(len({ann[m][i] for m in ANNOTATORS}) == 1 for i in hg),
        scores=panels,bootstrap_seed=20261118,bootstrap_iterations=10000,reproduced_ci95=ci,
        limits='Three model annotators use a related author-supplied codebook and overlap with the evaluation roster. This is sensitivity to alternative labels, not independent expert validation or proof against construction bias.'),
    input_sha256=hashes)
text = json.dumps(report,indent=2)+'\n'
if args.output:
    args.output.write_text(text)
print(json.dumps({'status':report['status'],'parameter_joint':jb['mean'],
    'LLM_reannotation':{k:report['LLM_reannotation'][k] for k in ['items','annotations','agreement','kappa','unanimous_items','alternative_class_counts','reproduced_ci95']}},indent=2))
