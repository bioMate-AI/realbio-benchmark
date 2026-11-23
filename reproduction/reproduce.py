#!/usr/bin/env python3
"""Offline integrity, coverage and historical-score reproduction for this package."""
from pathlib import Path
import collections
import hashlib
import importlib.util
import json
import statistics

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'manifest.json').read_text())
for relative, expected in manifest['sha256'].items():
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative
spec = importlib.util.spec_from_file_location('score', ROOT / 'evaluation/datasets/public_export/score.py')
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)


def rows(path):
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    assert len({r['id'] for r in records}) == len(records), f'Duplicate IDs: {path}'
    return {r['id']: r for r in records}


scores = []
for cell in manifest['cells'] + manifest.get('auxiliary_cells', []):
    gold = rows(ROOT / cell['gold'])
    raw = rows(ROOT / cell['file'])
    assert set(gold) == set(raw), cell['file']
    pred = {i: r.get('prediction') for i, r in raw.items()}
    task = cell['task']
    if task == 'routing':
        result = score.score_routing(gold, pred)
    elif task == 'param':
        result = score.score_param_prefill(gold, pred)
    elif task == 'method':
        correct = sum(str(pred[i]).strip().lower() in {str(x).strip().lower() for x in [r['correct_method']]+r.get('acceptable_alts', [])} for i, r in gold.items())
        result = {'accuracy': correct / len(gold)}
    elif task == 'QC':
        support, hits = collections.Counter(), collections.Counter()
        for i, r in gold.items():
            label = r['expected_correct_action']
            support[label] += 1
            hits[label] += score.norm(pred[i]) == score.norm(label)
        recalls = {c: hits[c]/support[c] for c in ['PASS', 'WARN', 'FAIL']}
        result = {'accuracy': sum(hits.values())/len(gold), 'balanced_accuracy': sum(recalls.values())/3, 'recalls': recalls}
    elif task == 'pbpk_benchmark':
        result = score.score_pbpk(gold, pred)
    elif task == 'boin_benchmark':
        result = score.score_boin(gold, pred)
    else:
        raise ValueError(task)
    scores.append({'file': cell['file'], 'task': task, 'n': len(gold), 'scores': result})
lookup = {s['file']:s['scores'] for s in scores}
ladder = {'all_ten':{},'nonempty_names_nine':{}}
names_cells = [c for c in manifest.get('auxiliary_cells',[]) if c['task']=='routing']
assert len(names_cells)==10
nonempty = [c for c in names_cells if any(r.get('prediction') for r in rows(ROOT/c['file']).values())]
assert len(nonempty)==9
for label,cells in [('all_ten',names_cells),('nonempty_names_nine',nonempty)]:
    for condition,suffix in [('bare','bare'),('names','catalog'),('described','catalog_described')]:
        paths=[str(Path(c['file']).parent/f'cross_domain_routing_{suffix}.jsonl') for c in cells]
        ladder[label][condition]=statistics.mean(lookup[path]['accuracy'] for path in paths)
for label,expected in [('all_ten',[.461,.816,.939]),('nonempty_names_nine',[.493,.906,.946])]:
    assert all(abs(ladder[label][k]-v)<.00051 for k,v in zip(['bare','names','described'],expected)),ladder
historical_qc={}
for condition in ['bare','harness']:
    rs=[lookup[c['file']] for c in manifest.get('auxiliary_cells',[]) if c['task']=='QC' and c['file'].endswith(f'_{condition}.jsonl')]
    assert len(rs)==6
    historical_qc[condition]={c:statistics.mean(r['recalls'][c] for r in rs) for c in ['PASS','WARN','FAIL']}
for condition,expected in [('bare',[.469,.680,1.0]),('harness',[.969,.060,1.0])]:
    assert all(abs(historical_qc[condition][k]-v)<.00051 for k,v in zip(['PASS','WARN','FAIL'],expected)),historical_qc
print(json.dumps({'status': 'pass', 'primary_prediction_files':len(manifest['cells']),
    'auxiliary_prediction_files':len(manifest.get('auxiliary_cells',[])), 'prediction_files': len(scores),
    'supporting_comparison_checks':{'routing_ladder':ladder,'original_six_model_QC':historical_qc},'scores': scores}, indent=2))
