#!/usr/bin/env python3
"""Statistics quoted in Sec. 5 of main.tex (exact ray integration, constraint-projected mass, kernel-driven extension) that are not a single entry of a printed table:
maxima, minima and differences over the rows of the logs of ray_mass.py, ray_stability.py, ray_long.py, e13_errconst.py, e13_all.py, ray_extend.py.
Reads the result logs in this directory (verify.py regenerates the quick ones before running this script; the logs of the full-mode runs are read as shipped).
Prints 'VALUE <name> <number>' lines; output: results_paper_numbers_ray.txt.   Needs numpy only."""
import os, re, json
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
NUM = re.compile(r'(?<![\w.])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')
OUT = []
def val(name, x, fmt='%.6g'):
    s = 'VALUE %s %s' % (name, fmt % x); OUT.append(s); print(s)
def lines(fn): return open(os.path.join(here, fn)).read().splitlines()
def nums(l): return [float(x) for x in NUM.findall(l)]
def block(L, start, stop=None):
    i = next(j for j, l in enumerate(L) if l.startswith(start))
    k = next((j for j in range(i + 1, len(L)) if stop and L[j].startswith(stop)), len(L))
    return L[i + 1:k]

TAGS = ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5')
# ------------------------------------------------------------------------------------------------ ray_mass.py: blocks [A], [B], [C]
for t in TAGS:
    L = lines('results_ray_mass_%s.txt' % t)
    A = [float(re.search(r'max dev \(v<=108\):\s+(\S+)', l).group(1)) for l in block(L, '[A]', '[B]') if l.strip().startswith('v0=')]
    val('rm_%s_A_maxdev' % t, max(A), '%.1e'); val('rm_%s_A_spread_over_v0' % t, max(A) - min(A), '%.1e')
    B = {int(nums(l)[0]): nums(l) for l in block(L, '[B]', '[C]') if re.match(r'\s+\d+\s', l)}      # v, ln M_ode, M_ext, levels, dev, ydev, rhodev
    C = {int(nums(l)[0]): nums(l) for l in block(L, '[C]') if re.match(r'\s+\d+\s', l)}              # v, ode, exact, lam-lam', |sV|-km, power, ode-pred, q_M
    val('rm_%s_B_maxabsdev_to290' % t, max(abs(r[4]) for r in B.values()), '%.1e')
    tab = (108, 140, 180, 240, 290)
    val('rm_%s_B_min_dev_over_levels_table' % t, min(abs(B[v][4])/B[v][3] for v in tab), '%.2f')
    val('rm_%s_B_max_dev_over_levels_table' % t, max(abs(B[v][4])/B[v][3] for v in tab), '%.0f')
    ge84 = [r for v, r in C.items() if v >= 84]
    val('rm_%s_C_ode_vs_exact_max' % t, max(abs(r[1] - r[2]) for r in ge84), '%.1e')
    val('rm_%s_C_ode_vs_lamlam_max' % t, max(abs(r[1] - r[3]) for r in ge84), '%.1e')
    val('rm_%s_C_ode_vs_exact_v290' % t, abs(C[290][1] - C[290][2]), '%.1e'); val('rm_%s_C_ode_vs_lamlam_v290' % t, abs(C[290][1] - C[290][3]), '%.1e')
    val('rm_%s_C_ode_vs_lamlam_v140' % t, abs(C[140][1] - C[140][3]), '%.1e')
    val('rm_%s_lnM_ode_v290' % t, B[290][1], '%.3f')
val('rm_M108_ratio_B003_to_B0003_k0.5', float(re.search(r'M_ext\(108\)=(\S+)', lines('results_ray_mass_B0.03_k0.5.txt')[4]).group(1)) / float(re.search(r'M_ext\(108\)=(\S+)', lines('results_ray_mass_B0.003_k0.5.txt')[4]).group(1)), '%.3g')
val('rm_M108_ratio_B003_to_B0003_k1.5', float(re.search(r'M_ext\(108\)=(\S+)', lines('results_ray_mass_B0.03_k1.5.txt')[4]).group(1)) / float(re.search(r'M_ext\(108\)=(\S+)', lines('results_ray_mass_B0.003_k1.5.txt')[4]).group(1)), '%.3g')

# ------------------------------------------------------------------------------------------------ ray_stability.py (concatenated blocks)
L = lines('results_ray_stability.txt'); i = 0
while i < len(L):
    m = re.match(r'gen2_(\S+)_A0_U1_w0\.3_v300\.json\s+k=', L[i])
    if not m: i += 1; continue
    t = m.group(1); rows = {}
    for l in L[i + 2:i + 10]:
        v = int(l.split('|')[0]); cols = l.split('|')[1:]
        rows[v] = [(float(re.search(r'ODE-ODE5 (\S+)', c).group(1)), float(re.search(r'PDE/ODE5 (\S+)', c).group(1))) for c in cols]
    for j, nm in ((1, 'finest4'), (2, 'coarsest4'), (3, 'finest3')):
        val('rs_%s_ode_max_%s' % (t, nm), max(abs(r[j][0]) for r in rows.values()), '%.1e')
    val('rs_%s_ode_max_all_subsets' % t, max(abs(r[j][0]) for r in rows.values() for j in (1, 2, 3)), '%.1e')
    ch = lambda v: max([abs(rows[v][j][1] - rows[v][0][1]) for j in (1, 2, 3) if np.isfinite(rows[v][j][1]) and np.isfinite(rows[v][0][1])] or [np.nan])
    val('rs_%s_pde_change_v140' % t, ch(140), '%.1e'); val('rs_%s_pde_change_max' % t, np.nanmax([ch(v) for v in rows]), '%.1e')
    a290 = [abs(c[1]) for c in rows[290] if np.isfinite(c[1])]
    val('rs_%s_pde_abs_v290_min' % t, min(a290), '%.2f'); val('rs_%s_pde_abs_v290_max' % t, max(a290), '%.2f')
    i += 10

# ------------------------------------------------------------------------------------------------ ray_long.py on the gen2 files (Romberg levels of the extrapolated fields) and on the gen3 files (PDE-driven ODE to v = 290)
for t in TAGS:
    L = lines('results_ray_long_%s.txt' % t)
    a = [nums(l) for l in block(L, '(a)', '(b)') if re.match(r'\s+\d+\s', l)]          # v, M_ext, levels: M, y, rho, r, sigma_v, phi_v
    val('rl_%s_levels_sV_max' % t, max(r[6] for r in a), '%.1e'); val('rl_%s_levels_PV_max' % t, max(r[7] for r in a), '%.1e')
for t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.03_k2', 'B0.03_k3'):
    L = lines('results_ray_long_gen3_%s.txt' % t)
    m = next(re.search(r'v= 290\s+lnM_ode=\s*(\S+)', l) for l in L if re.search(r'v= 290\s+lnM_ode', l))
    val('rl3_%s_lnM_ode_v290' % t, float(m.group(1)), '%.4f')

# ------------------------------------------------------------------------------------------------ ray_extend.py logs
def extend(fn):
    L = lines(fn); d = {}
    d['ratio'] = float(re.search(r'ratio at v_b: (\S+)', ' '.join(L)).group(1)); d['excess_vb'] = float(re.search(r'excess \|sV\|-km at v_b=(\S+),', ' '.join(L)).group(1))
    d['q'] = float(re.search(r'fitted power q=(\S+)', ' '.join(L)).group(1))
    rows = {int(nums(l)[0]): nums(l) for l in block(L, '    v      ln M') if re.match(r'\s+\d+\s', l)}
    d['rows'] = rows; return d
G2 = {t: extend('results_ray_extend_%s.txt' % t) for t in TAGS}
for t, d in G2.items():
    r = d['rows']
    val('re_%s_lnM_v290' % t, r[290][1], '%.3f'); val('re_%s_q_v290' % t, r[290][3], '%.3f'); val('re_%s_q_v2500' % t, r[2500][3], '%.3f'); val('re_%s_lnM_v2500' % t, r[2500][1], '%.2f')
    val('re_%s_C_change_2000_2500' % t, abs(r[2500][4] - r[2000][4]), '%.1e'); val('re_%s_treatments_max_at_2500' % t, max(abs(r[2500][5]), abs(r[2500][6])), '%.3f')
    val('re_%s_zero_minus_power_at_2500' % t, r[2500][5], '%.2f'); val('re_%s_const_minus_power_at_2500' % t, r[2500][6], '%.2f')
    val('re_%s_excess_vb' % t, d['excess_vb'], '%.2e'); val('re_%s_ratio_vb' % t, d['ratio'], '%.4f'); val('re_%s_q_fit' % t, d['q'], '%.2f')
    for v in (400, 1000, 2000, 2500): val('re_%s_lnM_v%d' % (t, v), r[v][1], '%.2f'); val('re_%s_qM_v%d' % (t, v), r[v][3], '%.4g'); val('re_%s_C_v%d' % (t, v), r[v][4], '%.3f')
EXT = {}
for kind in ('def', 'mu'):
    for B in ('0.03', '0.003'):
        for k in ('0.5', '1.5', '2', '3'):
            fn = 'results_ray_extend_ext_%s_B%s_k%s.txt' % (kind, B, k)
            if os.path.exists(os.path.join(here, fn)): EXT[(kind, B, k)] = extend(fn)
for (kind, B, k), d in EXT.items():
    r = d['rows']; t = '%s_B%s_k%s' % (kind, B, k)
    val('ex_%s_lnM_v2500' % t, r[2500][1], '%.3f'); val('ex_%s_q_v2500' % t, r[2500][3], '%.4f'); val('ex_%s_C_v2500' % t, r[2500][4], '%.3f')
    val('ex_%s_C_change_2000_2500' % t, abs(r[2500][4] - r[2000][4]), '%.1e'); val('ex_%s_treatments_max_at_2500' % t, max(abs(r[2500][5]), abs(r[2500][6])), '%.1e')
    val('ex_%s_excess_vb' % t, d['excess_vb'], '%.1e'); val('ex_%s_ratio_vb' % t, d['ratio'], '%.5f')
for B in ('0.03', '0.003'):
    for k in ('0.5', '1.5', '2', '3'):
        if ('def', B, k) in EXT and ('mu', B, k) in EXT:
            val('ex_B%s_k%s_mu_minus_def_lnM_v2500' % (B, k), EXT[('mu', B, k)]['rows'][2500][1] - EXT[('def', B, k)]['rows'][2500][1], '%.4f')
# kernel-driven against PDE-driven ln M at v = 290 (static-hole kernel, B = 0.03, gen3 inputs)
for k in ('1.5', '0.5', '2', '3'):
    val('ex_B0.03_k%s_kernel_minus_pde_lnM_v290' % k, EXT[('def', '0.03', k)]['rows'][290][1] - float(next(x for x in OUT if x.startswith('VALUE rl3_B0.03_k%s_lnM_ode_v290 ' % k)).split()[2]), '%.4f')
    val('ex_B0.03_k%s_kernel_final_minus_pde_lnM_v290' % k, EXT[('mu', '0.03', k)]['rows'][290][1] - float(next(x for x in OUT if x.startswith('VALUE rl3_B0.03_k%s_lnM_ode_v290 ' % k)).split()[2]), '%.4f')
for k in ('1.5', '0.5'):
    val('ex_gen2_B0.03_k%s_kernel_minus_pde_lnM_v290' % k, G2['B0.03_k' + k]['rows'][290][1] - float(next(x for x in OUT if x.startswith('VALUE rm_B0.03_k%s_lnM_ode_v290 ' % k)).split()[2]), '%.4f')

# ------------------------------------------------------------------------------------------------ e13_errconst.py
L = lines('results_e13_errconst.txt'); i = 0
while i < len(L):
    m = re.match(r'gen3_(\S+)_v300\.json k=\S+ B=\S+ ray s=(\S+): C_rho', L[i])
    if not m: i += 1; continue
    t, s = m.group(1), m.group(2); rows = {}
    j = i + 1
    while j < len(L) and L[j].startswith('  v='):
        n = nums(L[j]); rows[int(n[0])] = n; j += 1                              # v, C_rho, h-ratio, C_y, [dlnC/dv]
    if s.startswith('271'):
        val('ec_%s_hratio_min' % t, min(r[2] for r in rows.values()), '%.2f'); val('ec_%s_hratio_max' % t, max(r[2] for r in rows.values()), '%.2f')
        val('ec_%s_Cy_min_v40_100' % t, min(abs(rows[v][3]) for v in range(40, 101, 10)), '%.1f'); val('ec_%s_Cy_max_v40_100' % t, max(abs(rows[v][3]) for v in range(40, 101, 10)), '%.1f')
        for v in (40, 60, 100): val('ec_%s_Crho_v%d' % (t, v), rows[v][1], '%.4g'); val('ec_%s_rho_err_percent_v%d' % (t, v), 100*abs(rows[v][1])*0.003125**2, '%.2g')
        val('ec_%s_Cy_err_percent' % t, 100*abs(rows[60][3])*0.003125**2, '%.2g')
        val('ec_%s_Cy_v60' % t, rows[60][3], '%.4g'); val('ec_%s_dlnC_v100' % t, rows[100][4], '%.3f')
    i = j
val('ec_Cy_ratio_B0003_to_B003_k1.5_percent_v60', 100*(next(float(x.split()[2]) for x in OUT if x.startswith('VALUE ec_B0.003_k1.5_Cy_v60 '))/(100*next(float(x.split()[2]) for x in OUT if x.startswith('VALUE ec_B0.03_k1.5_Cy_v60 '))) - 1), '%.1f')

# ------------------------------------------------------------------------------------------------ e13_all.py outputs (eight runs, two rays) : next-level difference of the profile integral, differences projected-ODE
Imax200 = Imax280 = 0.0
for B in ('0.03', '0.003'):
    for k in ('0.5', '1.5', '2', '3'):
        L = lines('results_e13_B%s_k%s.txt' % (B, k)); cur = None
        for l in L:
            if l.startswith('gen3_'): cur = l
            elif re.match(r'\s+\d+\s', l) and cur is not None:
                n = nums(l)
                if len(n) < 10: continue
                v, Idiff = int(n[0]), n[8]
                if v <= 280: Imax280 = max(Imax280, Idiff)
                if v <= 200: Imax200 = max(Imax200, Idiff)
val('e13all_I_levels_max_to200', Imax200, '%.1e'); val('e13all_I_levels_max_to280', Imax280, '%.1e')
L = lines('results_e13_B0.003_k1.5.txt')
rowsU1 = [nums(l) for l in block(L, 'gen3_B0.003_k1.5_v300.json: k=1.5 B=0.003, ray s=271.25', 'gen3_B0.003_k1.5_v300.json: k=1.5 B=0.003, ray s=246') if re.match(r'\s+\d+\s', l)]
val('e13_B0.003_k1.5_U1_dlnM_max_to160', max(abs(r[2]) for r in rowsU1 if 84 <= r[0] <= 160), '%.1e'); val('e13_B0.003_k1.5_U1_dlnM_v280', abs(rowsU1[-1][2]), '%.2e')
# physical tails at B = 0.003: projected-minus-ODE at v = 280 on the rays U ~ 1 and U ~ 0.3 and the largest value over 84 <= v <= 200 on U ~ 1
for k in ('2', '3'):
    L = lines('results_e13_B0.003_k%s.txt' % k)
    b1 = [nums(l) for l in block(L, 'gen3_B0.003_k%s_v300.json: k=%s B=0.003, ray s=271.25' % (k, k), 'gen3_B0.003_k%s_v300.json: k=%s B=0.003, ray s=246' % (k, k)) if re.match(r'\s+\d+\s', l)]
    b0 = [nums(l) for l in block(L, 'gen3_B0.003_k%s_v300.json: k=%s B=0.003, ray s=246' % (k, k)) if re.match(r'\s+\d+\s', l)]
    val('e13_B0.003_k%s_U1_dlnM_v280' % k, abs(b1[-1][2]), '%.2e'); val('e13_B0.003_k%s_U03_dlnM_v280' % k, abs(b0[-1][2]), '%.2e')
    val('e13_B0.003_k%s_U1_dlnM_max_84_200' % k, max(abs(r[2]) for r in b1 if 84 <= r[0] <= 200), '%.1e'); val('e13_B0.003_k%s_lnM_ode_v280' % k, b1[-1][1], '%.0f')
# ------------------------------------------------------------------------------------------------ positions of the rays
D = json.load(open(os.path.join(here, 'gen3_B0.03_k1.5_v300.json')))
for n in (0, 2): val('rays_sq_n%d' % n, D['sq'][n], '%.2f'); val('rays_Uq_n%d' % n, D['Uq'][n], '%.4f')

open(os.path.join(here, 'results_paper_numbers_ray.txt'), 'w').write('\n'.join(OUT) + '\n')
