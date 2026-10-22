#!/usr/bin/env python3
"""Numbers of Section 4 of Paper G (kernel) that are not printed by one of the table scripts, re-derived from the shipped JSON data sets and
from T_mN5.npy / K_analytic_tau.npy (numpy only; uses analyze.py).  Run from this directory:  python3 paper_numbers_kernel.py   (about 5 s)
Output: results_paper_numbers_kernel.txt with lines 'VALUE <name> <number>' which verify.py compares with main.tex."""
import json, os, warnings
import numpy as np
import analyze
warnings.filterwarnings('ignore')
here = os.path.dirname(os.path.abspath(__file__))
OUT = []
def val(name, x, fmt='%.6g'):
    s = 'VALUE %s %s' % (name, fmt % x); OUT.append(s); print(s)
def load(fn, n=2):
    D = json.load(open(os.path.join(here, fn))); hs = sorted(D['data'], key=float, reverse=True); vq = np.array(D['vq'])
    return vq, analyze.extrap([np.array(D['data'][h]['PV'][n]) for h in hs]), D
def top(fn, n=2):
    vq, T, D = load(fn, n); return vq, T[-1][0], D

# --- Sec. 4.1(c): the compact pulse of horizon flux (B = 0.03, v_s = 10)
fn = 'gen_B0.03_k1.5_A0_U1_w0.3_v110_P10_2.json'
for n, U in enumerate((0.3, 0.6, 1.0, 1.2)):
    vq, P, D = top(fn, n); val('pulse_peak_v_U%g' % U, vq[int(np.nanargmax(np.abs(P[:60])))], '%.0f')
val('pulse_B003_mu_f', D['mu_f'], '%.4f')
rates = []
for n in range(4):
    vq, P, D = top(fn, n); i = int(100 - vq[0]); rates.append(-(np.log(abs(P[i+3])) - np.log(abs(P[i-3])))/(vq[i+3] - vq[i-3]))
val('pulse_rate_spread_v100_percent', 100*(max(rates)/min(rates) - 1), '%.2f')

# --- Sec. 4.3(a): impulse response K(tau) = phi_v(v_s + tau)/(-B), B = 0.003, from the pulses v_s = 3, 10, 30, 60 (width 2)
Ks = {}
for vs, f in ((3, 'gen_B0.003_k1.5_A0_U1_w0.3_v110_P3_2.json'), (10, 'gen_B0.003_k1.5_A0_U1_w0.3_v150_P10_2.json'),
              (30, 'gen_B0.003_k1.5_A0_U1_w0.3_v150_P30_2.json'), (60, 'gen_B0.003_k1.5_A0_U1_w0.3_v150_P60_2.json')):
    for n in (0, 2):
        vq, P, D = top(f, n); Ks[(vs, n)] = (vq, P/(-D['B']))
def Kat(vs, n, tau):
    vq, K = Ks[(vs, n)]; return K[int(round(vs + tau - vq[0]))]
for vs in (3, 10, 30, 60): val('Kpulse_tau60_vs%d_e2' % vs, Kat(vs, 2, 60)*1e2, '%.3f')
val('Kpulse_30_vs_60_max_rel_diff_tau30_80_percent', 100*max(abs(Kat(30, 2, t)/Kat(60, 2, t) - 1) for t in range(30, 81)), '%.2f')
val('Kpulse_vs10_tau60_U0.3_e2', Kat(10, 0, 60)*1e2, '%.3f'); val('Kpulse_vs10_tau60_U1_e2', Kat(10, 2, 60)*1e2, '%.3f')
val('Kpulse_vs10_tau95_U0.3_e3', Kat(10, 0, 95)*1e3, '%.2f'); val('Kpulse_vs10_tau95_U1_e3', Kat(10, 2, 95)*1e3, '%.2f')
val('Kpulse_vs10_tau30_U0.3_e4', Kat(10, 0, 30)*1e4, '%.1f'); val('Kpulse_vs10_tau30_U1', Kat(10, 2, 30), '%.2f')
vq, K = Ks[(60, 2)]
for tau in (30, 40, 50, 60, 70, 80, 85):
    i = int(round(60 + tau - vq[0])); val('Kinf_local_rate_tau%d' % tau, -(np.log(abs(K[i+3])) - np.log(abs(K[i-3])))/(vq[i+3] - vq[i-3]), '%.4f')
val('Kpulse_tau0', Kat(60, 2, 0), '%.2f'); val('Kpulse_tau-2', Kat(60, 2, -2), '%.2f')

# --- Sec. 4.2: high-frequency limit of the transfer function (T_mN5.npy: omega, Re T, Im T from the interior ODE, written by kernel_ft2.py)
w, tr, ti = np.load(os.path.join(here, 'T_mN5.npy'))
i = np.argmin(abs(w - 5.9)); j = np.argmin(abs(w - 4.0))
val('T_re_omega5.9', tr[i], '%.4f'); val('omega_ImT_omega5.9', w[i]*ti[i], '%.3f')
# Re T = T_inf - c/omega^2: Richardson in 1/omega^2 from omega = 4 and 5.9
val('T_inf_extrapolated', (w[i]**2*tr[i] - w[j]**2*tr[j])/(w[i]**2 - w[j]**2), '%.3f')
# K(tau) e^{kappa_+ tau} at tau = 100 (pole term) from the analytic kernel table K_analytic_tau.npy
tau, Kt = np.load(os.path.join(here, 'K_analytic_tau.npy')); kp = 0.048969
i = np.argmin(abs(tau - 100)); val('K_e_kp_tau_at_tau100', Kt[i]*np.exp(kp*tau[i]), '%.3f')

# --- Sec. 4.5: long runs (Table 3) -- the omitted -lambda'/lambda, the level agreement of phi_v, first/last excess
def lam_series(fn):
    vq, T, D = load(fn); P = np.abs(T[-1][0]); S = analyze.extrap([np.abs(np.array(D['data'][h]['sV'][2])) for h in sorted(D['data'], key=float, reverse=True)])[-1][0]
    lam = S + 2*np.gradient(np.log(P), vq); return vq, lam, np.gradient(lam, vq)/lam, T, D
for k, fn, vs in ((0.5, 'gen_B0.003_k0.5_A0_U1_w0.3_v300.json', (100, 140, 290)), (1.5, 'gen_B0.003_k1.5_A0_U1_w0.3_v300.json', (100, 140, 180, 290))):
    vq, lam, lp, T, D = lam_series(fn)
    for v in vs: val('omitted_lamprime_over_lam_k%g_v%d' % (k, v), lp[int(v - vq[0])]*-1, '%.2e')
    pred = D['km'] - 2*(k + 1)/(vq + 1); i = int(290 - vq[0])
    val('omitted_fraction_of_deficit_k%g_v290_percent' % k, 100*abs(lp[i])/abs(lam[i] - pred[i]), '%.1f')
    val('phi_levels_gap_k%g_v290' % k, abs(T[-2][0][i]/T[-1][0][i] - 1), '%.2e')   # second-highest level from the three coarsest grids against the top level
    val('mu_f_k%g_e5' % k, D['mu_f']*1e5, '%.2f')
# --- statistics over the printed tables of other scripts (their stdout logs, regenerated before this script runs)
import re
def lines(fn): return open(os.path.join(here, fn)).read().splitlines()
# kernel_analytic: ratio measured/predicted and local exponents (Sec. 4.3(b))
rr = []; dp = []
for l in lines('results_kernel_analytic.txt'):
    m = re.match(r'^\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+) / (\S+)\s*$', l)
    if m: rr.append(abs(float(m.group(4)) - 1)); dp.append(abs(float(m.group(5)) - float(m.group(6))))
val('kernel_ratio_max_dev', max(rr), '%.1e'); val('kernel_exponent_max_dev', max(dp), '%.3f')
# kernel_sensitivity: change of the six ratios against the baseline row (Sec. 4.3(b), 'at most 1.2e-3')
rowsS = [[float(x) for x in re.findall(r'(\d\.\d{4})', l.split('|', 1)[1])] for l in lines('results_kernel_sensitivity.txt') if l.startswith('sig2=')]
val('kernel_sens_max_change_variants', max(abs(a - b) for r in rowsS[1:5] for a, b in zip(r, rowsS[0])), '%.1e')
val('kernel_sens_max_change_dropped_terms', max(abs(a - b) for r in rowsS[5:] for a, b in zip(r, rowsS[0])), '%.1e')
# kernel_mN: |K_PDE/K_ODE - 1| over all masses and tau (Sec. 4.3(c))
val('kernel_mN_max_dev_percent', 100*max(abs(float(x) - 1) for l in lines('results_kernel_mN.txt') for x in re.findall(r'ratio\s+(\d\.\d+)', l)), '%.2f')
# m_N = 5 pulse kernels against the ODE kernel (tau >= 5)
blk = None; rng = {}
for l in lines('results_kernel_pulse_mN5_B0003.txt'):
    m = re.match(r'== pulse at v_s=(\d+)', l)
    if m: blk = int(m.group(1)); rng[blk] = []
    m = re.match(r'\s+tau=\s*(\d+)\s+K_PDE\s+\S+\s+K_ODE\s+\S+\s+ratio\s+(\S+)', l)
    if m and blk and int(m.group(1)) >= 5: rng[blk].append(100*(float(m.group(2)) - 1))
for b in rng: val('kernel_pulse_mN5_vs%d_min_percent' % b, min(rng[b]), '%.2f'); val('kernel_pulse_mN5_vs%d_max_percent' % b, max(rng[b]), '%.2f')
rb = [float(x) for l in lines('results_kernel_B0003.txt') for x in re.findall(r'ratio\s+(\d\.\d+)', l)]
val('kernel_B0003_ratio_min', min(rb), '%.4f'); val('kernel_B0003_ratio_max', max(rb), '%.4f')
# flux_nl: measured/linear at B = 0.03 (Sec. 4.6): range of the ratio and of the exponent difference for v >= 60
fl = [l for l in lines('results_flux_nl.txt') if re.match(r'^\s+\d+\s+\d\.\d+', l)]
val('flux_nl_ratio_min', min(float(l.split()[1]) for l in fl), '%.4f'); val('flux_nl_ratio_max', max(float(l.split()[1]) for l in fl), '%.4f')
val('flux_nl_exponent_max_dev', max(abs(float(l.split()[2]) - float(l.split()[3])) for l in fl), '%.2f')
# e11 ratios (Sec. 4.3(d)): static-hole kernel (e11_ratio) and final-hole kernel (kernel_mu) at v = 150..290
def ratios_e11():
    d = {}
    for l in lines('results_e11_ratio.txt'):
        m = re.match(r'^(B\S+)\s+(.*)$', l)
        if m: d[m.group(1)] = [float(x) for x in m.group(2).split()]
    return d                                             # columns: v = 100 150 200 250 280 290
def ratios_mu():
    d = {}; cur = None
    for l in lines('results_kernel_mu.txt'):
        m = re.match(r'^k=(\S+) B=(\S+): PDE', l)
        if m: cur = 'B%s_k%s' % (m.group(2), m.group(1)); continue
        if cur and l.strip().startswith('100:'): d[cur] = [float(x) for x in re.findall(r':\s+(\d\.\d+)', l)]; cur = None
    return d                                             # columns: v = 100 150 200 250 280 290
E, Mu = ratios_e11(), ratios_mu()
for t in ('B0.03_k2', 'B0.03_k3', 'B0.03_k1.5'):
    sp = Mu[t][1:]; val('final_kernel_spread_150_290_%s' % t, max(sp) - min(sp), '%.1e')
    sp = Mu[t][2:]; val('final_kernel_spread_200_290_%s' % t, max(sp) - min(sp), '%.1e')
    sp = Mu[t][3:]; val('final_kernel_spread_250_290_%s' % t, max(sp) - min(sp), '%.1e')
val('final_kernel_spread_250_290_max_all', max(max(Mu[t][3:]) - min(Mu[t][3:]) for t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.03_k2', 'B0.03_k3')), '%.1e')
for t, lab in (('B0.03_k1.5', 'k1.5'), ('B0.03_k0.5', 'k0.5')):
    for j, v in ((3, 250), (5, 290)): val('accounted_percent_%s_v%d' % (lab, v), 100*(E[t][j] - Mu[t][j])/(E[t][j] - 1), '%.1f')
for t in ('B0.03_k1.5', 'B0.03_k2', 'B0.03_k3', 'B0.03_k0.5'):
    D_ = json.load(open(os.path.join(here, 'gen3_%s_v300.json' % t.replace('B0.03_', 'B0.03_')))); val('remainder_over_mu_f_%s' % t, (Mu[t][3] - 1)/D_['mu_f'], '%.3f')
D_ = json.load(open(os.path.join(here, 'gen3_B0.003_k0.5_v300.json'))); val('remainder_over_mu_f_B0.003_k0.5', (Mu['B0.003_k0.5'][3] - 1)/D_['mu_f'], '%.2f')
# crossover table (crossover_analytic.py): columns v = 100 150 200 300 500 1000 3000; the k=3 rows are wrapped
txt = ' '.join(lines('results_crossover_analytic.txt')[1:])
for m in re.finditer(r'k=(\S+)\s+ratio\s+\[([^\]]*)\]\s+p\s+\[([^\]]*)\]\s+v_c\(10%\)=(\S+)', txt):
    k, rat, pp, vc = m.group(1), [float(x) for x in m.group(2).split()], [float(x) for x in m.group(3).split()], float(m.group(4))
    val('crossover_vc_k%s' % k, vc, '%.0f'); val('crossover_ratio_v100_k%s' % k, rat[0], '%.4g')
    val('crossover_p_v150_k%s' % k, pp[1], '%.3g'); val('crossover_p_v300_k%s' % k, pp[3], '%.3g'); val('crossover_p_v3000_k%s' % k, pp[6], '%.3g')
open(os.path.join(here, 'results_paper_numbers_kernel.txt'), 'w').write('\n'.join(OUT) + '\n')
