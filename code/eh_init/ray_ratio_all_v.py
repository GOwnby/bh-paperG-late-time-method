#!/usr/bin/env python3
"""Ratio of the ray-ODE deviation to the Romberg level spread of the PDE mass at EVERY integer v (Paper G, Sec. 5, Table 4 / Fig. 4a).
NEW script (written for the provenance audit; no counterpart in the author's archive).  It repeats, for every integer v = 84..290 instead of the
printed rows of ray_mass.py [B], exactly the computation of ray_mass.py: five-grid Romberg-extrapolated r, r_v, y, M, sigma_v, phi_v (analyze.extrap),
ODE of raylib.integrate from v0 = 60, ratio R(v) = |M_ODE/M_ext - 1| / |M_next/M_ext - 1|  (M_next = second-highest Romberg level).
Also prints the largest relative difference of the two highest Romberg levels of sigma_v and phi_v over 60 <= v <= 290.
usage: python3 ray_ratio_all_v.py [gen2_...json ...]   (default: the four v=300 gen2 files; about 12 s; output: results_ray_ratio_all_v.txt)
Prints 'VALUE <name> <number>' lines compared by verify.py with main.tex."""
import json, sys, numpy as np
from scipy.interpolate import CubicSpline
import raylib as R, analyze
files = sys.argv[1:] or ['gen2_B%s_A0_U1_w0.3_v300.json' % t for t in ('0.03_k1.5', '0.03_k0.5', '0.003_k1.5', '0.003_k0.5')]
n = 2
for fn in files:
    D = json.load(open(fn)); hs = sorted(D['data'], key=float, reverse=True); vq = np.array(D['vq'])
    tag = 'B%g_k%g' % (D['B'], D['k'])
    def fld(name):
        arr = []
        for h in hs:
            d = D['data'][h]; arr.append(np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n])) if name == 'Y' else np.array(d[name][n]))
        T = analyze.extrap(arr); return T[-1][0], T[-2][1]
    F = {nm: fld(nm) for nm in ('r', 'rv', 'Y', 'M', 'sV', 'PV')}
    r, rv, Y, M = [F[x][0] for x in ('r', 'rv', 'Y', 'M')]; Mn = F['M'][1]
    sV = CubicSpline(vq, F['sV'][0]); Pv = CubicSpline(vq, F['PV'][0])
    i0 = int(60 - vq[0]); sol = R.integrate(60., vq[-1], r[i0], -rv[i0], np.log(-Y[i0]), sV, Pv)
    vs = np.arange(84, 291); rat = []; dif = []
    for v in vs:
        i = int(v - vq[0]); lm = R.lnMof(*sol.sol(float(v))); dif.append(np.exp(lm)/M[i] - 1); rat.append(abs(dif[-1])/abs(Mn[i]/M[i] - 1))
    rat = np.array(rat); dif = np.array(dif); j = int(np.argmin(rat)); p = np.percentile(rat, [5, 25, 50, 75, 95])
    sc = vs[:-1][dif[:-1]*dif[1:] < 0]          # integers v where M_ODE/M_ext-1 changes sign between v and v+1
    near = int(np.min(np.abs(sc - vs[j]))) if len(sc) else -1
    print('%s %s: ratio |M_ODE/M_ext-1| / (level spread of M_ext) at every integer v = 84..290' % (fn, tag))
    print('  min %.3g at v=%d; percentiles 5,25,50,75,95: %s; fraction of v with ratio < 8: %.3f, < 1: %.3f' % (rat[j], vs[j], ' '.join('%.3g' % x for x in p), (rat < 8).mean(), (rat < 1).mean()))
    print('  sign changes of M_ODE/M_ext-1 between consecutive integer v: %d, at v=%s; distance of the minimum from the nearest one: %d' % (len(sc), ','.join(map(str, sc)), near))
    print('VALUE rr_%s_min %.3g' % (tag, rat[j])); print('VALUE rr_%s_vmin %d' % (tag, vs[j])); print('VALUE rr_%s_nsignchange %d' % (tag, len(sc))); print('VALUE rr_%s_min_dist_signchange %d' % (tag, near))
    for q, x in zip((5, 25, 50, 75, 95), p): print('VALUE rr_%s_p%02d %.3g' % (tag, q, x))
    print('VALUE rr_%s_frac_lt8 %.3f' % (tag, (rat < 8).mean())); print('VALUE rr_%s_frac_lt1 %.3f' % (tag, (rat < 1).mean()))
    print('VALUE rr_%s_n_lt1 %d' % (tag, (rat < 1).sum())); print('VALUE rr_%s_n_total %d' % (tag, len(rat)))
    sel = (vq >= 60) & (vq <= 290)
    for key, nm in (('sV', 'sigma_v'), ('PV', 'phi_v')):
        T = analyze.extrap([np.array(D['data'][h][key][n]) for h in hs]); lev = np.abs(T[-2][1]/T[-1][0] - 1)[sel]
        print('  max relative difference of the two highest Romberg levels of %s over 60<=v<=290: %.2e (at v=%d)' % (nm, lev.max(), vq[sel][int(np.argmax(lev))]))
        print('VALUE rr_%s_levels_%s_max_60_290 %.2e' % (tag, key, lev.max()))
