#!/usr/bin/env python3
"""Numbers quoted in the text of Paper G (Sections 3-5) that are not printed by one of the table scripts, re-derived from the shipped JSON
data sets (numpy only; uses analyze.py).  Run from this directory:  python3 paper_numbers.py     (about 10 s; output: results_paper_numbers.txt)
Every line 'VALUE <name> <number>' is compared by verify.py with the number in main.tex (see verification/REPORT.md)."""
import json, os, sys, warnings
import numpy as np
import analyze
warnings.filterwarnings('ignore')
here = os.path.dirname(os.path.abspath(__file__))
OUT = []
def val(name, x, fmt='%.6g'):
    s = 'VALUE %s %s' % (name, fmt % x); OUT.append(s); print(s)
def load(fn):
    D = json.load(open(os.path.join(here, fn))); hs = sorted(D['data'], key=float, reverse=True); return D, hs, np.array(D['vq'])
def sig(D, hs, key, n):             # signed arrays per grid for ray n
    return [np.array(D['data'][h][key][n]) for h in hs]
def ext(D, hs, key, n, level=-1):   # Romberg extrapolant (top level) of the signed series
    T = analyze.extrap(sig(D, hs, key, n)); return T[-1][0] if level == -1 else T[level][0]
def at(vq, v): return int(v - vq[0])
def pct(a, b): return 100*(a/b - 1)

# ------------------------------------------------------------------ Section 3 (event-horizon data), Table 1 and the text around it
V = 95
for B, k in ((0.03, 1.5), (0.05, 1.5), (0.03, 0.5), (0.05, 0.5)):
    D, hs, vq = load('gen_B%g_k%g_A0_U1_w0.3_v110.json' % (B, k)); i = at(vq, V); km = D['km']; tag = 'B%g_k%g' % (B, k)
    S = sig(D, hs, 'sV', 0); s0 = [abs(s[i]) for s in S]
    d = [s0[j] - s0[j+1] for j in range(4)]
    for j in range(3): val('T1_ratio_succ_diff%d_%s' % (j, tag), d[j]/d[j+1], '%.3f')
    e0 = abs(ext(D, hs, 'sV', 0)[i]); e2 = abs(ext(D, hs, 'sV', 2)[i])
    val('T1_ext_U0.3_above_pred_percent_%s' % tag, pct(e0, km), '%.4f'); val('T1_ext_U1_above_pred_percent_%s' % tag, pct(e2, km), '%.4f')
    val('T1_single_h0.05_above_pred_percent_%s' % tag, pct(s0[0], km), '%.4f')
    val('T1_kappa_mu_f_%s' % tag, km, '%.6f'); val('T1_mu_f_%s' % tag, D['mu_f'], '%.5e')
val('T1_static_kappa_minus', 0.795649, '%.6f')

# raw and extrapolated M at v = 100 (Sec. 3, "raw mass function is noise-dominated")
D, hs, vq = load('gen_B0.03_k1.5_A0_U1_w0.3_v110.json')
M = sig(D, hs, 'M', 2); Mx = analyze.extrap(M)[-1][0]
for v in (60, 80, 100):
    i = at(vq, v)
    val('raw_M_finest_off_percent_v%d' % v, 100*abs(M[-1][i]/Mx[i] - 1), '%.1f'); val('raw_M_next_off_percent_v%d' % v, 100*abs(M[-2][i]/Mx[i] - 1), '%.1f')
i = at(vq, 100)
for j, h in enumerate(hs): val('raw_M_v100_grid%d_e17' % j, M[j][i]/1e17, '%.4g')
val('raw_M_v100_extrap_e15', Mx[i]/1e15, '%.4g')
err = [abs(M[j][i] - Mx[i]) for j in range(5)]
for j in range(5): val('err_M_v100_grid%d_e17' % j, err[j]/1e17, '%.3g')
for j in range(4): val('err_M_v100_factor%d' % j, err[j]/err[j+1], '%.2f')
i = at(vq, 84)
val('rate_84_88_extrapolant', np.log(Mx[i+4]/Mx[i])/4, '%.4f'); val('rate_84_88_finest', np.log(M[-1][i+4]/M[-1][i])/4, '%.4f')
val('rate_84_88_n_grids_undefined', sum(1 for m in M if not (m[i] > 0 and m[i+4] > 0)), '%d')
val('rate_84_88_finest_low_percent', 100*(1 - np.log(M[-1][i+4]/M[-1][i])/np.log(Mx[i+4]/Mx[i])), '%.1f')
D5, hs5, vq5 = load('gen_B0.03_k0.5_A0_U1_w0.3_v110.json'); M5 = sig(D5, hs5, 'M', 2); M5x = analyze.extrap(M5)[-1][0]
val('raw_M_k0.5_v100_finest_e17', M5[-1][at(vq5, 100)]/1e17, '%.3g'); val('raw_M_k0.5_v100_extrap_e17', M5x[at(vq5, 100)]/1e17, '%.4g')
val('raw_M_k0.5_v60_min', min(m[at(vq5, 60)] for m in M5), '%.3g'); val('raw_M_k0.5_v60_max', max(m[at(vq5, 60)] for m in M5), '%.3g')
for k in (1.5, 0.5):
    Db, hb, vb = load('gen_B0.05_k%g_A0_U1_w0.3_v110.json' % k); Mb = sig(Db, hb, 'M', 2); Mbx = analyze.extrap(Mb)[-1][0]
    val('B0.05_k%g_finest_M_v100_off_percent' % k, 100*abs(Mb[-1][at(vb, 100)]/Mbx[at(vb, 100)] - 1), '%.1f')

# agreement of the two highest Romberg levels of M (relative), v >= 60, all four rays, five main series; and with the wide-seed run
main = ['gen_B0.03_k0.5_A0_U1_w0.3_v110.json', 'gen_B0.03_k1.5_A0_U1_w0.3_v110.json', 'gen_B0.03_k0.5_A0.02_U1_w0.3_v110.json',
        'gen_B0.03_k1.5_A0.02_U1_w0.3_v110.json', 'gen_B0.03_k2.5_A0.02_U1_w0.3_v110.json']
def level_gap(fn):
    D, hs, vq = load(fn); g = 0
    for n in range(4):
        T = analyze.extrap(sig(D, hs, 'M', n)); Mb, Mp = T[-1][0], T[-2][1]; sel = (vq >= 60) & (Mb > 0)
        g = max(g, np.max(np.abs(Mp[sel]/Mb[sel] - 1)))
    return g
val('romberg_levels_gap_main_series', max(level_gap(f) for f in main), '%.2e')
val('romberg_levels_gap_with_wide_seed', max(max(level_gap(f) for f in main), level_gap('gen_B0.03_k1.5_A0.02_U1_w0.5_v110.json')), '%.2e')

# rate against lambda - lambda'/lambda: statements of Sec. 3 ("Rate against the relation", "Robustness to the seed")
import io, contextlib
def rows(fn, n, t0s=(60, 72, 84, 96, 104), w=4):
    f = io.StringIO()
    with contextlib.redirect_stdout(f): r = analyze.analyze(fn, n=n, t0s=t0s)
    return r              # (t0, rate, lam, lam2, dis, rate_p, sV)
allrows = {fn: {n: rows(fn, n) for n in range(4)} for fn in main}
def dif2(r): return r[1] - r[3]
def dif1(r): return r[1] - r[2]
late = lambda r: [x for x in r if x[0] >= 72]
val('rate_rel_main_U1_U1.2_from72_max', max(abs(dif2(x)) for fn in main for n in (2, 3) for x in late(allrows[fn][n])), '%.2e')
val('rate_rel_main_U0.6_from72_max', max(abs(dif2(x)) for fn in main for x in late(allrows[fn][1])), '%.2e')
sd = [fn for fn in main if 'A0.02' in fn]
val('rate_rel_seeded_U1_at60_min', min(dif2(x) for fn in sd for x in allrows[fn][2] if x[0] == 60), '%.2e')
val('rate_rel_seeded_U1_at60_max', max(dif2(x) for fn in sd for x in allrows[fn][2] if x[0] == 60), '%.2e')
val('rate_rel_tail_U1_at60_max', max(abs(dif2(x)) for fn in main[:2] for x in allrows[fn][2] if x[0] == 60), '%.2e')
def rel_when_M_large(thr):
    g = 0
    for fn in main:
        D, hs, vq = load(fn)
        for n in range(4):
            Mb = ext(D, hs, 'M', n)
            for x in allrows[fn][n]:
                if x[0] >= 72 and Mb[at(vq, x[0])] >= thr: g = max(g, abs(dif2(x)))
    return g
val('rate_rel_all_rays_M_over_4e2_max', rel_when_M_large(4e2), '%.2e')
def rel_when_M_small(thr):
    g = []
    for fn in main:
        D, hs, vq = load(fn)
        for n in (0, 1):
            Mb = ext(D, hs, 'M', n)
            for x in allrows[fn][n]:
                if 0 < Mb[at(vq, x[0])] <= thr: g.append(abs(dif2(x)))
    return min(g), max(g)
lo, hi = rel_when_M_small(10.0)
val('rate_rel_M_below_10_min', lo, '%.2e'); val('rate_rel_M_below_10_max', hi, '%.2e')
# U = 0.3 / 0.6 early windows: difference 0.01-0.7 while M < 10
val('rate_rel_tail_k1.5_U0.3_84_88', dif2([x for x in allrows[main[1]][0] if x[0] == 84][0]), '%.3e')
Dm, hm, vm = load(main[1]); val('M_ext_tail_k1.5_U0.3_v84', ext(Dm, hm, 'M', 0)[at(vm, 84)], '%.2f')
# correction lambda'/lambda matters: without it (dif1) up to ... at [72,76] seeded k=1/2 and at [60,64] seeded k=3/2, 5/2
val('rate_minus_lambda_seeded_k0.5_72', dif1([x for x in allrows[main[2]][2] if x[0] == 72][0]), '%.2e')
val('rate_minus_lambda_seeded_k1.5_60', dif1([x for x in allrows[main[3]][2] if x[0] == 60][0]), '%.2e')
val('rate_minus_lambda_seeded_k2.5_60', dif1([x for x in allrows[main[4]][2] if x[0] == 60][0]), '%.2e')
# B = 0.05
for k in (0.5, 1.5):
    fn = 'gen_B0.05_k%g_A0_U1_w0.3_v110.json' % k; r = rows(fn, 2, t0s=(60, 72, 84, 96, 104))
    val('B0.05_k%g_rel_at60' % k, max(abs(dif2(x)) for x in r if x[0] == 60), '%.2e'); val('B0.05_k%g_rel_from72' % k, max(abs(dif2(x)) for x in r if x[0] >= 72), '%.2e')
    val('B0.05_k%g_rate_min' % k, min(x[1] for x in r), '%.4f'); val('B0.05_k%g_rate_max' % k, max(x[1] for x in r), '%.4f')
# seeds
def seedrows(fn, t0s=(60, 72, 84, 96, 104)): return rows(fn, 2, t0s=t0s)
for tag, fn in (('A0.01', 'gen_B0.03_k1.5_A0.01_U1_w0.3_v110.json'), ('A0.02_U0.7', 'gen_B0.03_k1.5_A0.02_U0.7_w0.2_v110.json')):
    r = seedrows(fn)
    val('seed_%s_rel_from72' % tag, max(abs(dif2(x)) for x in r if x[0] >= 72), '%.2e'); val('seed_%s_rel_from96' % tag, max(abs(dif2(x)) for x in r if x[0] >= 96), '%.2e'); val('seed_%s_rel_72' % tag, abs(dif2([x for x in r if x[0] == 72][0])), '%.2e')
    val('seed_%s_rel_from84' % tag, max(abs(dif2(x)) for x in r if x[0] >= 84), '%.2e'); val('seed_%s_rel_60' % tag, dif2([x for x in r if x[0] == 60][0]), '%.2e')
r = seedrows('gen_B0.03_k1.5_A0.02_U1_w0.5_v110.json', t0s=(72, 84, 96, 104))
for x in r: val('wide_seed_rate_%d' % x[0], x[1], '%.2f'); val('wide_seed_lam2_%d' % x[0], x[3], '%.2f'); val('wide_seed_diff_%d' % x[0], dif2(x), '%.5f')
Dw, hw, vw = load('gen_B0.03_k1.5_A0.02_U1_w0.5_v110.json'); Pw = ext(Dw, hw, 'PV', 2)
val('wide_seed_phiv_node_v', [float(vw[i]) for i in range(len(vw)-1) if Pw[i]*Pw[i+1] < 0][0], '%.0f')
Dn, hn, vn = load('gen_B0.03_k1.5_A0.02_U0.7_w0.2_v110.json'); Pn = ext(Dn, hn, 'PV', 2)
nodes = [float(vn[i]) for i in range(len(vn)-1) if Pn[i]*Pn[i+1] < 0]
val('seed_A0.02_U0.7_first_node', nodes[0], '%.0f'); val('seed_A0.02_U0.7_second_node', nodes[1], '%.0f')
Ds, hsd, vs_ = load('gen_B0.03_k1.5_A0.03_U0.6_w0.3_v110.json')
val('seed_A0.03_M_ext_U0.6_v60_e9', ext(Ds, hsd, 'M', 1)[at(vs_, 60)]/1e9, '%.2f')
val('seed_A0.03_n_grids', len(hsd), '%d')
ms = [np.array(Ds['data'][h]['M'][1])[at(vs_, 80)] for h in hsd]
val('seed_A0.03_M_v80_both_signs', int(min(ms) < 0 < max(ms)), '%d')
Pm = [np.array(Ds['data'][h]['sV'][2]) for h in hsd]; nanrow = [bool(np.any(~np.isfinite(p))) for p in Pm]
val('seed_A0.03_U1_nonfinite_all_grids', int(all(nanrow)), '%d')
val('seed_A0.03_U1_first_nonfinite_v_min', min(float(vs_[int(np.where(~np.isfinite(p))[0][0])]) for p in Pm), '%.0f')

# nodes of the seeded phi_v on U = 1 by linear interpolation (Sec. 3: 'node at v = 44.5-47.5')
def node(fn):
    D, hs, vq = load(fn); P = ext(D, hs, 'PV', 2)
    return [float(vq[i] - P[i]*(vq[i+1] - vq[i])/(P[i+1] - P[i])) for i in range(len(vq)-1) if P[i]*P[i+1] < 0]
for k, fn in ((0.5, main[2]), (1.5, main[3]), (2.5, main[4])): val('seed_node_k%g' % k, node(fn)[0], '%.2f')

# the ingoing flux on the rays (Sec. 3, "observations")
rt = 9.36
def ratio_to_tail(fn, k, v, n=2):
    D, hs, vq = load(fn); P = ext(D, hs, 'PV', n); return abs(P[at(vq, v)])/(k*D['B']*(1 + v)**(-k-1)*rt)
for k in (0.5, 1.5):
    fn = 'gen_B0.03_k%g_A0_U1_w0.3_v110.json' % k
    for v in (60, 80, 100): val('flux_ratio_to_transported_tail_k%g_v%d' % (k, v), ratio_to_tail(fn, k, v), '%.1f')
    D, hs, vq = load(fn)
    Ps = [abs(ext(D, hs, 'PV', n)[at(vq, 100)]) for n in range(4)]
    val('flux_ray_spread_percent_k%g_v100' % k, 100*(max(Ps) - min(Ps))/min(Ps) if False else 100*(max(Ps)/min(Ps) - 1), '%.1f')
r_all = []
for fn, k in [(f, kk) for f, kk in zip(main, (0.5, 1.5, 0.5, 1.5, 2.5))] + [('gen_B0.03_k1.5_A0.02_U1_w0.3_v110.json', 1.5)]:
    for v in (60, 80, 100): r_all.append(ratio_to_tail(fn, k, v, 2))
val('flux_ratio_to_tail_min_over_main_series', min(r_all), '%.1f'); val('flux_ratio_to_tail_max_over_main_series_excl_k2.5', max(x for x, f in zip(r_all, [m for m in (main[:5]) for _ in range(3)]+['x']*3) if 'k2.5' not in f), '%.1f')
val('flux_ratio_to_tail_seeded_k2.5_v100', ratio_to_tail(main[4], 2.5, 100), '%.0f')

# |sigma_v| approaching kappa_-(mu_f) at late times on U = 1 (Sec. 3, "late times")
for k, fn in ((1.5, main[1]), (0.5, main[0])):
    D, hs, vq = load(fn); S = np.abs(ext(D, hs, 'sV', 2)); km = D['km']
    for v in (62, 74, 86, 98, 106): val('late_sV_U1_k%g_v%d' % (k, v), S[at(vq, v)], '%.4f')
    val('late_sV_U1_k%g_above_percent_v106' % k, pct(S[at(vq, 106)], km), '%.3f')
    ex = S - km
    p = lambda v: -(np.log(ex[at(vq, v+4)]) - np.log(ex[at(vq, v-4)]))/(np.log(vq[at(vq, v+4)]) - np.log(vq[at(vq, v-4)]))
    val('late_sV_excess_local_exponent_U1_k%g_v60' % k, p(60), '%.3f'); val('late_sV_excess_local_exponent_U1_k%g_v100' % k, p(100), '%.3f')
D, hs, vq = load(main[0]); S0 = np.abs(ext(D, hs, 'sV', 0)); ex0 = S0 - D['km']
val('late_sV_excess_U0.3_k0.5_min_v70_100', min(ex0[at(vq, 70):at(vq, 100)+1])*1e3, '%.2f'); val('late_sV_excess_U0.3_k0.5_max_v70_100', max(ex0[at(vq, 70):at(vq, 100)+1])*1e3, '%.2f')
val('late_sV_excess_U0.3_k0.5_fall_after_v80_percent', 100*(1 - ex0[at(vq, 100)]/ex0[at(vq, 80)]), '%.0f')
D, hs, vq = load('gen_B0.03_k1.5_A0.02_U1_w0.3_v110.json'); val('seeded_k1.5_sV_v106', abs(ext(D, hs, 'sV', 2)[at(vq, 106)]), '%.4f')
for k in (1.5, 0.5):
    D, hs, vq = load('gen_B0.05_k%g_A0_U1_w0.3_v110.json' % k); S = np.abs(ext(D, hs, 'sV', 2))
    val('B0.05_k%g_sV_v106' % k, S[at(vq, 106)], '%.4f'); val('B0.05_k%g_excess_percent_v106' % k, pct(S[at(vq, 106)], D['km']), '%.2f')
    val('B0.05_k%g_sV_v62' % k, S[at(vq, 62)], '%.4f')

open(os.path.join(here, 'results_paper_numbers.txt'), 'w').write('\n'.join(OUT) + '\n')
