#!/usr/bin/env python3
"""Build and check both implementations using disposable local profiles."""
import json, pathlib, shutil, subprocess
from reproduce import run
root = pathlib.Path(__file__).resolve().parent
sdk = root / 'sdk'
shutil.copy2(root / 'profile_precedence_test.go', sdk / 'internal/cli/profile_precedence_test.go')
results = {}
for mode in ['before', 'fixed']:
    if mode == 'fixed':
        subprocess.run(['git', 'apply', str(root / 'fix.patch')], cwd=sdk, check=True)
    with (root / f'{mode}-unit.log').open('w') as output:
        unit = subprocess.run(['go', 'test', './internal/cli', '-run', 'TestProfilesRespectProfileFlag', '-count=1', '-v'], cwd=sdk, stdout=output, stderr=subprocess.STDOUT)
    assert unit.returncode == (1 if mode == 'before' else 0)
    binary = root / f'rc-{mode}'
    subprocess.run(['go', 'build', '-o', str(binary), './cmd/rc'], cwd=sdk, check=True)
    result = run(binary)
    (root / f'{mode}-results.json').write_text(json.dumps(result, indent=2))
    assert result['failed'] == (2 if mode == 'before' else 0)
    results[mode] = {'passed': result['passed'], 'failed': result['failed']}
subprocess.run(['go', 'test', './...'], cwd=sdk, check=True)
print(json.dumps(results, indent=2))
