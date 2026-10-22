#!/usr/bin/env python3
"""Numbers of Sec. 2 of main.tex from the JSON outputs of run_validation.py (validation_nonlinear.json) and run_checks.py (checks_nonlinear.json):
prints 'VALUE <name> <number>' lines.  Output: results_paper_numbers_nl.txt.   Standard library only."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
OUT = []
def val(name, x, fmt='%.6g'):
    s = 'VALUE %s %s' % (name, fmt % x); OUT.append(s); print(s)
V = json.load(open(os.path.join(here, 'validation_nonlinear.json')))
for h, e in V['static']: val('static_err_h%g' % h, e, '%.3e')
val('static_order_min', min(V['static_orders']), '%.4f'); val('static_order_max', max(V['static_orders']), '%.4f')
for row in V['constraint']:
    h = row[0]; val('constraint_u_v0_20_h%g' % h, row[1], '%.3e'); val('constraint_u_v20_60_h%g' % h, row[2], '%.3e'); val('constraint_u_v40_60_h%g' % h, row[3], '%.3e')
val('constraint_u_order_min', min(min(r) for r in V['constraint_orders']), '%.3f'); val('constraint_u_order_max', max(max(r) for r in V['constraint_orders']), '%.3f')
C = json.load(open(os.path.join(here, 'checks_nonlinear.json')))
for h, a, b in C['constraint_v']: val('constraint_v_0_20_h%g' % h, a, '%.3e'); val('constraint_v_20_58_h%g' % h, b, '%.3e')
open(os.path.join(here, 'results_paper_numbers_nl.txt'), 'w').write('\n'.join(OUT) + '\n')
