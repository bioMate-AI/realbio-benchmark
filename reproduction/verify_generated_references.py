#!/usr/bin/env python3
"""Rebuild synthetic references in temporary directories; prove constant-exposure bound."""
import argparse
from collections import Counter
from decimal import Decimal
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--root',type=Path,default=HERE if (HERE/'manifest.json').exists() else HERE.parents[1])
ap.add_argument('--output',type=Path)
args=ap.parse_args()
PUB=args.root.resolve()/'evaluation/datasets/public_export'


def rows(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


generated={}
for task,script in [('pbpk_benchmark','generate_pk_v2.py'),('boin_benchmark','generate_dose_v2.py')]:
    original=rows(PUB/task/'data_v2_generated.jsonl')
    with tempfile.TemporaryDirectory(prefix='benchmark-reference-check-') as directory:
        temp=Path(directory)
        shutil.copyfile(PUB/task/script,temp/script)
        subprocess.run([sys.executable,'-I',str(temp/script)],check=True,capture_output=True,text=True)
        rebuilt=rows(temp/'data_v2_generated.jsonl')
    assert rebuilt==original,f'Generator does not reproduce stored items: {task}'
    generated[task]={'items':len(original),'generator_reproduces_all_fields':True}

pk=rows(PUB/'pbpk_benchmark/data_v2_generated.jsonl')
refs=[Decimal(str(r['reference'][r['target_endpoint']])) for r in pk]
assert all(r>0 for r in refs)
endpoints=sorted({r/2 for r in refs}|{r*2 for r in refs})
coverage=[(sum(r/2<=x<=r*2 for r in refs),x) for x in endpoints]
maximum=max(n for n,_ in coverage)
witness=next(x for n,x in coverage if n==maximum)
historical=Decimal('2.2387')
assert sum(r/2<=historical<=r*2 for r in refs)==maximum
dose=rows(PUB/'boin_benchmark/data_v2_generated.jsonl')
lowest_hits=sum(r['reference'].get('true_MTD_mg')==min(json.loads(r['inputs']['dose_levels_json'])) for r in dose)
counts=Counter(r['reference'].get('true_MTD_mg') for r in dose)
assert counts[None]==0 and lowest_hits==5
report=dict(status='pass',new_model_calls=0,synthetic_generators=generated,
    exposure_constant=dict(maximum_hits=maximum,n_items=len(refs),maximum_agreement=maximum/len(refs),
        witness_uM=str(witness),historical_constant_uM=str(historical),historical_constant_is_optimal=True,
        method='Maximum overlap of closed [reference/2, 2*reference] intervals evaluated at all endpoints using Decimal arithmetic; no grid approximation.'),
    dose=dict(n_items=len(dose),null_references=counts[None],lowest_dose_hits=lowest_hits,
        lowest_dose_accuracy=lowest_hits/len(dose),reference_distribution=dict(counts)),
    limitation='Rebuilding synthetic labels verifies internal consistency, not agreement with observed pharmacology or clinical decisions.')
if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
