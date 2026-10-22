#!/usr/bin/env python3
"""Symbolic (computer-algebra) verification of the analytic statements of Paper G.  Needs sympy only (no scipy, no numpy).
Run from this directory:  python3 sympy_checks.py      (about 1-2 min; output: results_sympy_checks.txt)

Each block prints a line 'CHECK <id> : PASS/FAIL' that verify.py collects.

 S1  Field equations (Sec. 2, Eqs. dn1-dn3 and the constraints): the Einstein tensor of ds^2 = -W du dv + r(u,v)^2 dOmega^2 is computed with
     sympy and G_ab - 8 pi T_ab = 0 (massless scalar + NED monopole, M_N = m r^3/(r^3+a)) is shown to be equivalent to
     dn1, dn2 and the u- and v-constraints, and Box phi = 0 to dn3.
 S2  Ray equations (Sec. 5, Eq. ray, rayrate): from dn1, the v-constraint and M = r/2 (1+4 r_u r_v/W) by algebra.
 S3  mu_v = -8 pi r^2 (r_u/W) phi_v^2 (Eq. muv).
 S4  y_c identity (Eq. yc): d_u (r_u/W) = -4 pi r phi_u^2 / W  from the u-constraint.
 S5  Wave equation in ingoing EF coordinates (Sec. 4.2): (r^2 f F')' - 2 i w r (rF)' = 0, the Frobenius coefficient a at r_+ and the denominators
     n (kappa_+ n - i w) of the recursion (poles at w = -i n kappa_+), and the zero-frequency gain T(0) = (1 + r_+^2/r_-^2)/2 (Eq. T0).
 S6  Reissner-Nordstrom: T(0) = (r_-^2 + r_+^2)/(2 r_-^2) = (kappa_+ + kappa_-)/(2 kappa_+)  (Ori's b_0).
 S7  Rate-only / filtering statement: rho' = -kappa rho + c v^-p  =>  d ln(flux/rho)/dv ... : (kappa - dlnM/dv)(v+1) -> p  (q_M -> 2k+2).
"""
import sympy as sp
import sys

results = []
def report(name, ok, extra=''):
    results.append((name, bool(ok)))
    print('CHECK %s : %s %s' % (name, 'PASS' if ok else 'FAIL', extra), flush=True)

# ---------------------------------------------------------------- S1
u, v, th, ph_ = sp.symbols('u v theta varphi', real=True)
m, a = sp.symbols('m a', positive=True)
r = sp.Function('r')(u, v)
sig = sp.Function('sigma')(u, v)            # W = exp(sigma)
phi = sp.Function('phi')(u, v)
W = sp.exp(sig)
X = [u, v, th, ph_]
g = sp.zeros(4, 4)
g[0, 1] = g[1, 0] = -W / 2
g[2, 2] = r**2
g[3, 3] = r**2 * sp.sin(th)**2
ginv = g.inv()

def christoffel(g, ginv, X):
    n = len(X)
    G = [[[0]*n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                G[i][j][k] = sp.simplify(sum(ginv[i, l]*(sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(n))/2)
    return G
Gam = christoffel(g, ginv, X)

def ricci(Gam, X):
    n = len(X)
    Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(n):
            e = 0
            for i in range(n):
                e += sp.diff(Gam[i][j][k], X[i]) - sp.diff(Gam[i][j][i], X[k])
                for l in range(n):
                    e += Gam[i][i][l]*Gam[l][j][k] - Gam[i][k][l]*Gam[l][j][i]
            Ric[j, k] = sp.simplify(e)
    return Ric
Ric = ricci(Gam, X)
Rs = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(4) for j in range(4)))
Gt = (Ric - Rs*g/2).applyfunc(sp.simplify)          # Einstein tensor G_ab

rr = sp.Symbol('rr', positive=True)
MN = m*rr**3/(rr**3 + a)
MNp = sp.diff(MN, rr); MNpp = sp.diff(MNp, rr)
rho = MNp/(4*sp.pi*rr**2)
pt = -rho - rr*sp.diff(rho, rr)/2
at_r = lambda e: e.subs(rr, r)
# stress tensor with lower indices.  Scalar: T_ab = phi_a phi_b - g_ab (d phi)^2/2.  NED monopole: T^u_u = T^v_v = -rho, T^th_th = T^ph_ph = p_t.
dphi = [sp.diff(phi, x) for x in X]
dphi2 = sum(ginv[i, j]*dphi[i]*dphi[j] for i in range(4) for j in range(4))
Tsc = sp.Matrix(4, 4, lambda i, j: dphi[i]*dphi[j] - g[i, j]*dphi2/2)
Tup = sp.diag(-at_r(rho), -at_r(rho), at_r(pt), at_r(pt))      # mixed T^a_b
Tned = (g*Tup).applyfunc(sp.simplify)                           # T_ab = g_ac T^c_b
E = (Gt - 8*sp.pi*(Tsc + Tned)).applyfunc(sp.simplify)

ru, rv, su, sv = sp.diff(r, u), sp.diff(r, v), sp.diff(sig, u), sp.diff(sig, v)
phu, phv = dphi[0], dphi[1]
# (a) u-constraint:  E_uu = -(2/r)(r_uu - sigma_u r_u + 4 pi r phi_u^2)
cu = sp.diff(r, u, 2) - su*ru + 4*sp.pi*r*phu**2
cv = sp.diff(r, v, 2) - sv*rv + 4*sp.pi*r*phv**2
report('S1_uu_constraint', sp.simplify(E[0, 0] + 2*cu/r) == 0)
report('S1_vv_constraint', sp.simplify(E[1, 1] + 2*cv/r) == 0)
# (b) dn1:  r_uv = -r_u r_v/r - W/(4r)(1-2 M_N'(r)).  Solve E_uv = 0 for r_uv and compare.
ruv_sym, suv_sym = sp.symbols('ruv suv')
rep = {sp.diff(r, u, v): ruv_sym, sp.diff(sig, u, v): suv_sym}
Euv = sp.simplify(E[0, 1].subs(rep)); Eth = sp.simplify(E[2, 2].subs(rep))
sol_ruv = sp.solve(Euv, ruv_sym)[0]
dn1 = -ru*rv/r - W/(4*r)*(1 - 2*at_r(MNp))
report('S1_dn1', sp.simplify(sol_ruv - dn1) == 0)
sol_suv = sp.solve(Eth.subs(ruv_sym, dn1), suv_sym)[0]
dn2 = -2*dn1/r - 8*sp.pi*phu*phv + W*at_r(MNpp)/(2*r)
report('S1_dn2', sp.simplify(sol_suv - dn2) == 0)
# (c) dn3: Box phi = 0  <=>  phi_uv = -(r_u phi_v + r_v phi_u)/r
box = sum(ginv[i, j]*(sp.diff(phi, X[i], X[j]) - sum(Gam[k][i][j]*sp.diff(phi, X[k]) for k in range(4))) for i in range(4) for j in range(4))
phuv_sym = sp.Symbol('phuv')
box_s = sp.simplify(box.subs(sp.diff(phi, u, v), phuv_sym))
sol_phuv = sp.solve(box_s, phuv_sym)[0]
report('S1_dn3', sp.simplify(sol_phuv + (ru*phv + rv*phu)/r) == 0)
# (d) the remaining components (E_uv, E_theta-theta, E_phi-phi) vanish identically once dn1, dn2 are imposed; E_uth = E_vth = 0 identically
rem = [sp.simplify(E[0, 1].subs(rep).subs(ruv_sym, dn1)), sp.simplify(E[2, 2].subs(rep).subs({ruv_sym: dn1, suv_sym: dn2})),
       sp.simplify(E[3, 3].subs(rep).subs({ruv_sym: dn1, suv_sym: dn2})), E[0, 2], E[1, 2], E[0, 3], E[1, 3], E[2, 3]]
report('S1_remaining_components', all(sp.simplify(e) == 0 for e in rem))
# (e) Misner-Sharp mass: 1 - 2M/r = g^{ab} r_a r_b = -4 r_u r_v / W
Msharp = r/2*(1 + 4*ru*rv/W)
report('S1_misner_sharp', sp.simplify(1 - 2*Msharp/r - (ginv[0, 1]*ru*rv*2)) == 0)

# negative controls: the same comparisons with a wrong sign / wrong coefficient must NOT vanish
report('S1_negative_control_dn2', sp.simplify(sol_suv - (-2*dn1/r + 8*sp.pi*phu*phv + W*at_r(MNpp)/(2*r))) != 0)
report('S1_negative_control_dn1', sp.simplify(sol_ruv - (-ru*rv/r - W/(4*r)*(1 - 3*at_r(MNp)))) != 0)
report('S1_negative_control_constraint', sp.simplify(E[0, 0] + 2*(sp.diff(r, u, 2) - su*ru - 4*sp.pi*r*phu**2)/r) != 0)
report('S1_scalar_T_uv_vanishes', sp.simplify(Tsc[0, 1]) == 0)

# ---------------------------------------------------------------- S2, S3, S4 : jets
R_, Ru, Rv, Wj, Sv, Pv, Pu, Mp, Mpp = sp.symbols('R Ru Rv W Sv Pv Pu Mp Mpp')     # r, r_u, r_v, W, sigma_v, phi_v, phi_u, M_N'(r), M_N''(r)
Ruv = -Ru*Rv/R_ - Wj/(4*R_)*(1 - 2*Mp)                                           # dn1
Rvv = Sv*Rv - 4*sp.pi*R_*Pv**2                                                  # v-constraint
Wv = Wj*Sv
rho_ = -Rv; y_ = -Ru/Wj; S_ = (1 - 2*Mp)/(4*R_)
# S2.1  rho' = sigma_v rho + 4 pi r phi_v^2
report('S2_rho_prime', sp.simplify(-Rvv - (Sv*rho_ + 4*sp.pi*R_*Pv**2)) == 0)
# S2.2  (ln y)' = rho/r - sigma_v + S/y     (y_v = -(r_uv)/W + r_u W_v/W^2)
yv = -Ruv/Wj + Ru*Wv/Wj**2
report('S2_lny_prime', sp.simplify(yv/y_ - (rho_/R_ - Sv + S_/y_)) == 0)
# S2.3  M = r/2 (1 + 4 y rho)
report('S2_M_of_y_rho', sp.simplify(R_/2*(1 + 4*Ru*Rv/Wj) - R_/2*(1 + 4*y_*rho_)) == 0)
# S2.4  d/dv ln(M - r/2) = 4 pi r phi_v^2/rho + S/y
rp_ = Rv; rhop = -Rvv
dlnM = rp_/R_ + yv/y_ + rhop/rho_
report('S2_rayrate', sp.simplify(dlnM - (4*sp.pi*R_*Pv**2/rho_ + S_/y_)) == 0)
# S3  mu_v = M_v - M_N'(r) r_v = -8 pi r^2 (r_u/W) phi_v^2
Mj = R_/2*(1 + 4*Ru*Rv/Wj)
Mv = sp.diff(Mj, R_)*Rv + sp.diff(Mj, Ru)*Ruv + sp.diff(Mj, Rv)*Rvv + sp.diff(Mj, Wj)*Wv
muv = Mv - Mp*Rv
report('S3_mu_v', sp.simplify(muv - (-8*sp.pi*R_**2*(Ru/Wj)*Pv**2)) == 0)
# S4  u-constraint => d_u (r_u/W) = -4 pi r phi_u^2/W   (so y_c = 1/2 + int 4 pi r phi_u^2/W du)
Ruu = sp.Symbol('Ruu'); Su = sp.Symbol('Su')
Ruu_c = Su*Ru - 4*sp.pi*R_*Pu**2
d_u_ruW = Ruu_c/Wj - Ru*(Wj*Su)/Wj**2
report('S4_u_constraint_integral', sp.simplify(d_u_ruW - (-4*sp.pi*R_*Pu**2/Wj)) == 0)

# ---------------------------------------------------------------- S5 : wave equation and kernel
vv_, rv_ = sp.symbols('v r_', real=True)
fun = sp.Function('f')(rv_)
gE = sp.Matrix([[-fun, 1], [1, 0]])                              # ingoing EF, coordinates (v, r)
# Box on the (v,r) part plus the sphere: Box phi = r^-2 [ d_a (r^2 sqrt(-g2) g^{ab} d_b phi) ], sqrt(-g2) = 1
gi = gE.inv(); Xe = [vv_, rv_]
def boxE(P):
    return sp.simplify(sum(sp.diff(rv_**2*sum(gi[i, j]*sp.diff(P, Xe[j]) for j in range(2)), Xe[i]) for i in range(2))/rv_**2)
w = sp.Symbol('omega')
F = sp.Function('F')(rv_)
lhs = sp.simplify(boxE(sp.exp(-sp.I*w*vv_)*F)*rv_**2*sp.exp(sp.I*w*vv_))
target = sp.diff(rv_**2*fun*sp.diff(F, rv_), rv_) - 2*sp.I*w*rv_*sp.diff(rv_*F, rv_)
report('S5_wave_equation_EF', sp.simplify(lhs - target) == 0)
# Frobenius at r_+: f = 2 kp x + f2 x^2 + f3 x^3 (x = r - r_+), F = 1 + c1 x + c2 x^2 + c3 x^3
kp, rp, x, f2, f3 = sp.symbols('kappa_p r_p x f2 f3')
c1, c2, c3 = sp.symbols('c1 c2 c3')
Fs = 1 + c1*x + c2*x**2 + c3*x**3
fs = 2*kp*x + f2*x**2 + f3*x**3
rr_ = rp + x
ode = sp.diff(rr_**2*fs*sp.diff(Fs, x), x) - 2*sp.I*w*rr_*sp.diff(rr_*Fs, x)
ode = sp.expand(ode)
co = [ode.coeff(x, k) for k in range(3)]
s1 = sp.solve(co[0], c1)[0]
a_paper = -sp.I*w/(rp*(kp - sp.I*w))                              # F = 1 + a (r_+ - r)  =>  c1 = -a
report('S5_frobenius_a', sp.simplify(s1 + a_paper) == 0)
# leading coefficient of c_n at order x^(n-1):  2 r_p^2 n (kp n - i w) c_n  (+ lower c_j): the factor n (kp n - i w) gives poles at w = -i n kp
ok_den = True
for n in (1, 2, 3):
    cn = [c1, c2, c3][n-1]
    cofn = sp.expand(ode).coeff(x, n-1)
    lead = sp.simplify(sp.diff(cofn, cn) - 2*rp**2*n*(kp*n - sp.I*w))
    ok_den = ok_den and lead == 0
report('S5_recursion_denominators', ok_den)
# static solution phi = j0 (v + g(r)):  Box phi = 0  <=>  (r^2 f g')' + 2 r = 0 ; r^2 f g' = r_+^2 - r^2 is the regular solution (f(r_+) = 0)
gg = sp.Function('g')(rv_)
box_static = sp.simplify(boxE(vv_ + gg)*rv_**2 - (sp.diff(rv_**2*fun*sp.diff(gg, rv_), rv_) + 2*rv_))
report('S5_static_equation', box_static == 0)
rP, f_ = sp.symbols('r_P f_')
gp = (rP**2 - rv_**2)/(rv_**2*fun)                               # g' from r^2 f g' = r_+^2 - r^2
report('S5_static_solution', sp.simplify(sp.diff(rv_**2*fun*gp, rv_) + 2*rv_) == 0)
# phi_v along the outgoing ray dr/dv = f/2 at fixed U:  d/dv [v + g(r(v))] = 1 + (f/2) g'  = (1 + r_+^2/r^2)/2
report('S5_T0_gain', sp.simplify(1 + fun/2*gp - (1 + rP**2/rv_**2)/2) == 0)
report('S5_outgoing_ray', sp.simplify(sp.Matrix([1, fun/2]).T*gE*sp.Matrix([1, fun/2])) == sp.zeros(1, 1))

# ---------------------------------------------------------------- S6 : Reissner-Nordstrom
rm_, rp2 = sp.symbols('r_m r_p2', positive=True)
fRN = (1 - rp2/rv_)*(1 - rm_/rv_)
kap_p = sp.simplify(sp.diff(fRN, rv_).subs(rv_, rp2)/2); kap_m = sp.simplify(-sp.diff(fRN, rv_).subs(rv_, rm_)/2)
T0_RN = (1 + rp2**2/rm_**2)/2
report('S6_RN_kappas', sp.simplify(kap_p - (rp2 - rm_)/(2*rp2**2)) == 0 and sp.simplify(kap_m - (rp2 - rm_)/(2*rm_**2)) == 0)
report('S6_RN_T0_equals_ori_b0', sp.simplify(T0_RN - (rm_**2 + rp2**2)/(2*rm_**2)) == 0 and sp.simplify(T0_RN - (kap_p + kap_m)/(2*kap_p)) == 0)

# ---------------------------------------------------------------- S7 : filtering a power-law flux
V, kappa, c0, p = sp.symbols('V kappa c0 p', positive=True)
a1 = sp.Symbol('a1')
# rho' = -kappa rho + c0 V^-p, particular solution rho = (c0 V^-p / kappa)(1 + a1/V + O(V^-2)); d ln M/dv = c0 V^-p / rho  (M >> r)
rho_ser = c0*V**(-p)/kappa*(1 + a1/V)
resid = sp.simplify((sp.diff(rho_ser, V) + kappa*rho_ser - c0*V**(-p))/(c0*V**(-p-1)))   # = -a1 - p/kappa*(1+a1/V) - ... ; leading term at V -> oo
lead = sp.limit(resid, V, sp.oo)
a1_val = sp.solve(lead, a1)[0]
rate = c0*V**(-p)/rho_ser.subs(a1, a1_val)                                                  # = kappa/(1 + a1/V)
q = sp.limit((kappa - rate)*V, V, sp.oo)
report('S7_filter_a1', sp.simplify(a1_val - p/kappa) == 0, '(a1 = %s)' % a1_val)
report('S7_q_limit_equals_p', sp.simplify(q - p) == 0, '(lim (kappa - dlnM/dv) v = %s; p = 2k+2 for a flux phi_v^2 ~ v^-(2k+2))' % q)

nfail = sum(1 for _, ok in results if not ok)
print('SUMMARY sympy_checks: %d checks, %d failed' % (len(results), nfail))
sys.exit(1 if nfail else 0)
