"""E13 (Sec. 5, constraint-projected mass): dependence of ln M_cc on the starting point v0 of the v-constraint integration (r, rho taken from the
extrapolated PDE at v0).  usage: python3 e13_v0.py [gen3_...json] [n]   (default gen3_B0.03_k1.5_v300.json, ray n = 2, v0 = 48, 60, 72, 84)
Prints ln M_cc(v) for v = 100, 200, 280 and its change against v0 = 60; 'VALUE e13_v0_max_change' is the largest change."""
import sys, numpy as np
fn = sys.argv[1] if len(sys.argv) > 1 else 'gen3_B0.03_k1.5_v300.json'; n = sys.argv[2] if len(sys.argv) > 2 else '2'
sys.argv = ['e13_project.py', fn, n]
ns = {}; exec(open('e13_project.py').read().split("if __name__")[0], ns)
vq = ns['vq']; VS = (100, 200, 280)
def lncc(X, v):
    C = X['solC'].sol(float(v)); yc = 0.5 + X['I'][int(v - vq[0])]
    return np.log(C[0]/2) + np.logaddexp(0, np.log(4) + np.log(yc) + np.log(C[1]))
ref = None; worst = 0.0
print('%s ray n=%s: ln M_cc at v = %s for the starting points v0 of the v-constraint' % (fn, n, VS))
for v0 in (60, 48, 72, 84):
    X = ns['run'](None, 60., float(v0)); L = [lncc(X, v) for v in VS]
    if ref is None: ref = L
    d = [a - b for a, b in zip(L, ref)]; worst = max(worst, max(abs(x) for x in d))
    print('  v0=%d  ln M_cc = %s   change against v0=60: %s' % (v0, ' '.join('%.9f' % x for x in L), ' '.join('%+.1e' % x for x in d)))
print('VALUE e13_v0_max_change %.2e' % worst)
