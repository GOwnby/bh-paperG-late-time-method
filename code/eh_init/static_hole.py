#!/usr/bin/env python3
"""Horizons, surface gravities and zero-frequency gain T(0) = (1 + r_+^2/r_-^2)/2 of the static holes used in Paper G, in 50-digit mpmath arithmetic
(independent of the numpy/scipy root finders used by the evolution code).  Needs mpmath and the standard library only.
Run from this directory:  python3 static_hole.py        (1 s; output: results_static_hole.txt)

f(r) = 1 - 2(mu + M_N(r))/r,  M_N = m r^3/(r^3 + a),  a = 2 m (ell = 1).  Roots of the quartic  r^4 - 2(m+mu) r^3 + a r - 2 mu a = 0
(for mu = 0 the cubic r^3 - 2 m r^2 + a = 0); kappa_pm = |f'(r_pm)|/2.
Prints 'VALUE <name> <number>' lines which verify.py compares with the numbers quoted in main.tex.
"""
import json, glob, os, sys
import mpmath as mp
mp.mp.dps = 50

def hole(m, mu=0, a=None):
    m = mp.mpf(m); mu = mp.mpf(mu); a = 2*m if a is None else mp.mpf(a)
    Q = [1, -2*(m+mu), 0, a, -2*mu*a]
    roots = [z.real for z in mp.polyroots(Q, maxsteps=500, extraprec=200) if abs(z.imag) < mp.mpf(10)**-30 and z.real > 0]
    roots.sort()
    D = lambda r: r*(r**3 + a)
    dQ = lambda r: 4*r**3 - 6*(m+mu)*r**2 + a
    # mu > 0 adds a third, small root r_s ~ 2 mu (Schwarzschild-like horizon of the accumulated mass); the Cauchy horizon is the second-largest root
    rs = roots[0] if len(roots) > 2 else None
    rm, rp = roots[-2], roots[-1]
    km = abs(dQ(rm)/D(rm))/2; kp = abs(dQ(rp)/D(rp))/2
    return dict(rm=rm, rp=rp, km=km, kp=kp, T0=(1 + (rp/rm)**2)/2, roots=roots, rs=rs)

out = []
def val(name, x, fmt='%.10g'):
    s = 'VALUE %s %s' % (name, fmt % x)
    print(s); out.append(s)

# (1) the main hole m_N = 5, a_N = 10  (abstract, Sec. 2)
h5 = hole(5)
for k in ('rm', 'rp', 'km', 'kp', 'T0'): val('mN5_' + k, h5[k])
val('mN5_ratio_km_over_kp', h5['km']/h5['kp'])
val('mN5_rp_over_rm', h5['rp']/h5['rm'])
# (2) T(0) for the other profiles (Eq. T0), kappa table (Sec. 4.5)
for mN in ('3', '2', '1.6', '1.4'):
    h = hole(mN)
    for k in ('rm', 'rp', 'km', 'kp', 'T0'): val('mN%s_%s' % (mN, k), h[k])
    val('mN%s_km_minus_2kp' % mN, h['km'] - 2*h['kp'])
# (3) near the extremal limit: kappa_- = 2 kappa_+ at M = 1.435 ell;  M* = 3 sqrt(3)/4 ell;  kappa_pm -> 0.471 sqrt(eps)/ell
Mstar = 3*mp.sqrt(3)/4
val('Mstar', Mstar)
f = lambda M: (lambda h: h['km'] - 2*h['kp'])(hole(M))
Mc = mp.findroot(f, mp.mpf('1.435'))
val('M_cross_km_eq_2kp', Mc)
val('eps_cross', Mc/Mstar - 1)
for eps in ('1e-6', '1e-8'):
    h = hole(Mstar*(1 + mp.mpf(eps)))
    val('kappa_over_sqrt_eps_eps%s' % eps, (h['km'] + h['kp'])/2/mp.sqrt(mp.mpf(eps)), '%.6g')

# (4) holes of the accumulated mass mu_f of the shipped runs: kappa_-(mu_f) of the tables, T(0), r_-
here = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(here, 'gen3_B*_k*_v300.json')) + glob.glob(os.path.join(here, 'gen_B0.0[35]*_A0_U1_w0.3_v110.json')))
for fn in files:
    D = json.load(open(fn)); mu = D['mu_f']
    h = hole(5, mu)
    tag = os.path.basename(fn).replace('.json', '')
    val('km_muf_%s' % tag, h['km']); val('muf_%s' % tag, mu)
    val('km_muf_json_minus_mp_%s' % tag, D['km'] - h['km'], '%.3e')
    if abs(mu - 9.955525e-3) < 2e-6:
        val('B0.03_k1.5_rm_muf', h['rm']); val('B0.03_k1.5_rp_muf', h['rp']); val('B0.03_k1.5_T0_muf', h['T0'])
        val('B0.03_k1.5_T0_muf_over_static', h['T0']/h5['T0'] - 1)
# B = 0.05, k = 3/2: inner horizon of the final hole (Sec. 4.4(d): r_- = 0.056)
for fn in files:
    if 'gen_B0.05_k1.5' in fn:
        h = hole(5, json.load(open(fn))['mu_f']); val('B0.05_k1.5_rs_small_root', h['rs']); val('B0.05_k1.5_rm_muf', h['rm']); val('B0.05_k1.5_km_muf', h['km'])
# static-minus-final surface gravity (Sec. 4.5 text): kappa_-^static - kappa_-(mu_f) for the B = 0.003 runs
for t in ('B0.003_k1.5', 'B0.003_k0.5'):
    fn = os.path.join(here, 'gen_%s_A0_U1_w0.3_v300.json' % t)
    if os.path.exists(fn):
        mu = json.load(open(fn))['mu_f']; val('static_minus_final_km_%s' % t, h5['km'] - hole(5, mu)['km'], '%.4e')
# predicted shifts from the static value (Sec. 3): B = 0.03 -> 1.4 %, 0.05 -> 4.0 %, 0.04 (mu_f = 1.7727e-2 from results_eh_init.txt) -> 2.5 %
for B, mu in (('0.03', 9.955525e-3), ('0.04', 1.7727e-2), ('0.05', 2.7757016e-2)):
    h = hole(5, mu); val('shift_percent_B%s' % B, 100*(1 - h['km']/h5['km']), '%.3f')
open(os.path.join(here, 'results_static_hole.txt'), 'w').write('\n'.join(out) + '\n')
