#!/usr/bin/env python3
"""Compare a freshly generated data set (gen.py / gen2.py / gen3.py output, written to the current directory) with the shipped one, grid by grid.
usage: regen_compare.py <new.json> <shipped.json>    prints 'VALUE regen_max_rel_diff <x>' (largest elementwise relative difference of M, sigma_v, phi_v over the grids
present in the new file, rays and v), 'VALUE regen_mu_f_rel_diff <x>' and the number of grids compared.  Needs numpy only."""
import json, sys
import numpy as np
new = json.load(open(sys.argv[1])); old = json.load(open(sys.argv[2]))
worst = 0.0; n = 0
for h, d in new['data'].items():
    if h not in old['data']: print('grid %s not in the shipped file' % h); continue
    n += 1
    for fld in ('M', 'sV', 'PV'):
        a = np.array(d[fld]); b = np.array(old['data'][h][fld])
        rel = np.abs(a - b)/np.maximum(np.abs(b), 1e-300); w = float(np.nanmax(rel)); worst = max(worst, w)
        print('h=%-9s %-3s max relative difference %.2e' % (h, fld, w))
print('VALUE regen_grids_compared %d' % n)
print('VALUE regen_max_rel_diff %.1e' % worst)
print('VALUE regen_mu_f_rel_diff %.1e' % abs(new['mu_f']/old['mu_f'] - 1))
