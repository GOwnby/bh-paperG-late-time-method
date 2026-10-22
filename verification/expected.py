"""Numbers quoted in main.tex (Paper G) and where verify.py finds the corresponding computed value.

C(id, quantity, loc, paper, src, tol=None, why=None)
  paper : the value as printed in main.tex (a string such as "9.956e-3", so that the printed digits fix the rounding tolerance), or a number.
  src   : V(step, name)            the value of the line "VALUE <name> <x>" printed by the script of that step
          F(file, a1, a2, ..., i=0, g=None, produced_by=None)
                                   file (path relative to the repository root) -> first line matching regex a1; from there the first line
                                   matching a2 (and so on); the i-th number after the end of the last match on that line (negative i
                                   counts from the end), or capture group g of the last regex.  The file is refreshed by step `produced_by`
                                   (default: the step whose output file it is); a shipped file that no step regenerates is read as shipped.
  tol   : None -> "round": |computed - paper| <= half a unit of the last printed digit of the paper value.
          "rel:x" / "abs:x" -> relative / absolute tolerance; "le" / "ge" -> computed must be <= / >= paper (a bound quoted in the paper);
          "eq" -> equal.  Every tolerance other than "round" carries a reason `why`.
  loc   : section / table / equation of main.tex.
  fix   : (optional) value the paper SHOULD say when the computed value disagrees with `paper`; the row is then PASS* ("correction applied/needed").
          No check uses it any more: the 13 values that earlier versions of this file typed from the older text of main.tex (and listed as PASS*)
          are now typed as they stand in the shipped main.tex; the earlier values are kept in the comments "was ... in the earlier version".
  TXT(literal) : 1.0 if the literal string (whitespace-normalized) occurs in main.tex, else 0.0 (checks that the sentences revised after the
          provenance audit are present; skipped if main.tex is not next to verify.py).  textcoverage(): how many `paper` values occur verbatim in main.tex.
"""
import os, re
from decimal import Decimal

CHECKS = []
NUM = re.compile(r'(?<![\w.])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')

class V:
    def __init__(self, step, name, a=False, scale=1.0): self.step, self.name, self.a, self.scale = step, name, a, scale
class F:
    def __init__(self, file, *anchors, i=0, g=None, produced_by=None, a=False, scale=1.0):
        # a=True: absolute value of the number; scale: multiply (unit conversion, e.g. 100 for percent)
        self.file, self.anchors, self.i, self.g, self.by, self.a, self.scale = file, anchors, i, g, produced_by, a, scale
class P:
    """pass flag of a line 'CHECK <name> : PASS|FAIL' printed by the script of `step` (1.0 if PASS)"""
    def __init__(self, step, name): self.step, self.name = step, name

def C(id, quantity, loc, paper, src, tol=None, why=None, fix=None):
    """fix: value that the paper SHOULD say when the computed value disagrees with the printed one (a manuscript correction is then
    listed in REPORT.md and the check passes as PASS* if the computed value matches `fix` to the rounding of the printed digits)."""
    assert tol is None or why, 'tolerance without reason: ' + id
    assert all(c['id'] != id for c in CHECKS), 'duplicate id ' + id
    CHECKS.append(dict(id=id, quantity=quantity, loc=loc, paper=paper, src=src, tol=tol, why=why, fix=fix))

# --------------------------------------------------------------------------------------------------------------------- evaluation
def _read_values(logs):
    vals = {}
    for step, text in logs.items():
        for m in re.finditer(r'^VALUE (\S+) (\S+)\s*$', text, re.M):
            try: vals[(step, m.group(1))] = float(m.group(2))
            except ValueError: pass
    return vals

def _fget(root, f):
    txt = open(os.path.join(root, f.file)).read().splitlines()
    pos = 0; m = None; line = None
    for a in f.anchors:
        rx = re.compile(a)
        for j in range(pos, len(txt)):
            m = rx.search(txt[j])
            if m: line = txt[j]; pos = j; break
        else:
            raise LookupError('anchor %r not found in %s' % (a, f.file))
    if f.g is not None: x = float(m.group(f.g))
    else:
        nums = NUM.findall(line[m.end():])
        if not nums: raise LookupError('no number after anchor %r in %s' % (f.anchors[-1], f.file))
        x = float(nums[f.i])
    return (abs(x) if f.a else x) * f.scale

def _halfulp(p):
    d = Decimal(str(p)) if not isinstance(p, str) else Decimal(p)
    return float(Decimal(5).scaleb(d.as_tuple().exponent - 1))

def _fmt(x):
    if isinstance(x, str): return x
    if x == 0: return '0'
    return ('%.6g' % x)

class TXT:
    def __init__(self, literal): self.literal = literal
class X:
    """derived quantity: fn(*values of the sources), e.g. X(lambda a, b: 100 * (a - b) / (a - 1), F(...), F(...))"""
    def __init__(self, fn, *srcs): self.fn, self.srcs = fn, srcs

class Skip(Exception): pass

def evaluate(root, steps, results, full):
    logs = {sid: r.get('stdout', '') for sid, r in results.items()}
    vals = _read_values(logs)
    produced = {}                       # file -> step id
    for st in steps:
        for p in st['produces']: produced[p] = st['id']

    def get(src):
        if isinstance(src, X): return src.fn(*[get(s) for s in src.srcs])
        if isinstance(src, TXT):
            if not os.path.exists(os.path.join(root, 'main.tex')): raise Skip('main.tex not found')
            return float(re.sub(r'\s+', ' ', src.literal) in re.sub(r'\s+', ' ', open(os.path.join(root, 'main.tex'), encoding='utf-8').read()))
        if isinstance(src, (V, P)):
            r = results.get(src.step)
            if r is None: raise LookupError('unknown step ' + src.step)
            if not r['status'].startswith('OK'): raise Skip(r['status'])
            if isinstance(src, P): return float(bool(re.search(r'^CHECK %s : PASS' % re.escape(src.name), logs[src.step], re.M)))
            if (src.step, src.name) not in vals: raise LookupError('VALUE %s not printed by %s' % (src.name, src.step))
            x = vals[(src.step, src.name)]
            return (abs(x) if src.a else x) * src.scale
        by = src.by or produced.get(src.file.split('/')[-1]) or produced.get(src.file)
        if by is not None and not results[by]['status'].startswith('OK') and results[by]['status'] != 'SKIPPED (full mode only)': raise Skip(results[by]['status'])
        return _fget(root, src)      # a log whose generator runs only in full mode is read as shipped (it is refreshed by `verify.sh --full`)

    rows = []
    for c in CHECKS:
        row = dict(id=c['id'], quantity=c['quantity'], loc=c['loc'], paper=str(c['paper']), computed='', tol='', status='')
        p = c['paper']; tol = c['tol']
        row['tol'] = 'round (half unit of last printed digit)' if tol is None else '%s (%s)' % (tol, c['why'])
        try:
            x = get(c['src'])
            row['computed'] = _fmt(x)
            pv = float(p)
            if tol is None: ok = abs(x - pv) <= _halfulp(p) * (1 + 1e-9) + 1e-12 * abs(pv)
            elif tol == 'le': ok = x <= pv
            elif tol == 'ge': ok = x >= pv
            elif tol == 'eq': ok = x == pv
            elif tol.startswith('rel:'): ok = abs(x - pv) <= float(tol[4:]) * abs(pv)
            elif tol.startswith('abs:'): ok = abs(x - pv) <= float(tol[4:])
            else: raise ValueError('bad tolerance ' + tol)
            row['status'] = 'PASS' if ok else 'FAIL'
            if not ok and c.get('fix') is not None and abs(x - float(c['fix'])) <= _halfulp(c['fix']) * (1 + 1e-9) + 1e-12 * abs(float(c['fix'])):
                row['status'] = 'PASS*'; row['paper'] = '%s (text should read %s)' % (c['paper'], c['fix'])
        except Skip as e:
            row['status'] = 'SKIPPED'; row['computed'] = str(e)
        except Exception as e:
            row['status'] = 'FAIL'; row['computed'] = 'ERROR: %s' % e
        rows.append(row)
    return rows

def _tex_forms(p):
    p = str(p).strip(); out = {p}
    m = re.fullmatch(r'[+]?(-?[0-9.]+)e([+-]?)0*([0-9]+)', p)
    if m:
        a, sg, e = m.groups(); sg = '-' if sg == '-' else ''
        out |= {r'%s\times10^{%s%s}' % (a, sg, e), r'%s\times 10^{%s%s}' % (a, sg, e)}
        out.add(('%.10f' % float(p)).rstrip('0'))
    if p.startswith('+'): out.add(p[1:])
    return out

def textcoverage(root):
    """(n_found, n_total, ids not found): how many of the `paper` values (as typed above) occur verbatim in main.tex, either as typed or in the
    form 1.2\\times10^{-3} (heuristic; a bound or a rounded value may be written differently in the text, so a miss is not an error)."""
    f = os.path.join(root, 'main.tex')
    if not os.path.exists(f): return None
    T = re.sub(r'\s+', ' ', open(f, encoding='utf-8').read()); miss = []
    for c in CHECKS:
        if not any(x in T for x in _tex_forms(c['paper'])): miss.append(c['id'])
    return len(CHECKS) - len(miss), len(CHECKS), miss

# --------------------------------------------------------------------------------------------------------------------- the checks
EH = 'code/eh_init/'

R = lambda name: EH + name          # path of a file in code/eh_init
def NODE(*a, **k): return F(*a, **k)

# =====================================================================================================================================
# Abstract, Sec. 2: the static hole, field equations, symbolic derivations
# =====================================================================================================================================
for nm, lab, p in (('rm', 'r_-', '1.057475'), ('rp', 'r_+', '9.897927'), ('km', 'kappa_-', '0.795649'), ('kp', 'kappa_+', '0.048969')):
    C('static_%s' % nm, '%s of the static hole m_N=5, a_N=10 (50-digit mpmath)' % lab, 'Abstract; Sec. 2', p, V('static_hole', 'mN5_' + nm))
C('static_ratio_rp_rm', 'r_+/r_- (high-frequency gain of the kernel)', 'Sec. 4.2', '9.36', V('static_hole', 'mN5_rp_over_rm'))
for m, p in (('5', '44.30'), ('3', '14.32'), ('2', '5.33'), ('1.6', '2.81'), ('1.4', '1.733')):
    C('T0_mN%s' % m, 'T(0) = (1 + r_+^2/r_-^2)/2, m_N=%s' % m, 'Eq. (T0)', p, V('static_hole', 'mN%s_T0' % m))
for m, p in (('3', '0.07827'), ('2', '0.10541'), ('1.6', '0.1101'), ('1.4', '0.0901')):
    C('kp_mN%s' % m, 'kappa_+ of the hole m_N=%s' % m, 'Sec. 4.3(c)', p, V('static_hole', 'mN%s_kp' % m))
C('km_mN1.4', 'kappa_- at m_N=1.4', 'Sec. 4.5', '0.164', V('static_hole', 'mN1.4_km'))
C('km_minus_2kp_mN1.4', 'kappa_- - 2 kappa_+ at m_N=1.4', 'Sec. 4.5', '-0.016', V('static_hole', 'mN1.4_km_minus_2kp'))
C('M_cross', 'mass at which kappa_- = 2 kappa_+', 'Sec. 4.5', '1.435', V('static_hole', 'M_cross_km_eq_2kp'))
C('eps_cross', 'eps = M/M* - 1 at that mass', 'Sec. 4.5', '0.105', V('static_hole', 'eps_cross'))
C('kappa_over_sqrt_eps', 'kappa_pm / sqrt(eps) as eps -> 0', 'Sec. 4.5', '0.471', V('static_hole', 'kappa_over_sqrt_eps_eps1e-8'))
C('mu_f_hole_rm', 'r_- of the hole of mass parameter mu_f = 9.96e-3', 'Sec. 4.3(d)', '1.04549', V('static_hole', 'B0.03_k1.5_rm_muf'))
C('mu_f_hole_rp', 'r_+ of the same hole', 'Sec. 4.3(d)', '9.91846', V('static_hole', 'B0.03_k1.5_rp_muf'))
C('mu_f_hole_T0', 'T(0) of the same hole', 'Sec. 4.3(d)', '45.500', V('static_hole', 'B0.03_k1.5_T0_muf'))
C('mu_f_hole_T0_percent', 'T(0) of the hole of mass mu_f larger than the static one by (percent)', 'Sec. 4.3(d)', '2.7',
  F(R('results_static_hole.txt'), r'^VALUE B0\.03_k1\.5_T0_muf_over_static', scale=100.0))
C('rminus_B005_k15', 'inner horizon r_- of the final hole at B=0.05, k=3/2 (mu_f=0.0278); 0.0557 is the extra small root r_s ~ 2 mu_f, not the Cauchy horizon',
  'Sec. 4.3(d) (end)', '1.023', V('static_hole', 'B0.05_k1.5_rm_muf'))   # was 0.056 in the earlier version (the spurious root r_s ~ 2 mu_f of the original transfer_mu.py)
for B, p in (('0.03', '1.4'), ('0.04', '2.5'), ('0.05', '4.0')):
    C('shift_percent_B%s' % B, 'predicted shift of kappa_- from the static value at B=%s (percent)' % B, 'Sec. 3', p, V('static_hole', 'shift_percent_B' + B))
C('static_minus_final_km_k15', 'kappa_-^static - kappa_-(mu_f), B=0.003, k=3/2', 'Sec. 4.4 (long runs)', '1.0e-4', V('static_hole', 'static_minus_final_km_B0.003_k1.5'))
C('static_minus_final_km_k05', 'kappa_-^static - kappa_-(mu_f), B=0.003, k=1/2', 'Sec. 4.4 (long runs)', '6.2e-5', V('static_hole', 'static_minus_final_km_B0.003_k0.5'))

# field equations (finite-difference Riemann tensor)
CFE = R('results_check_field_equations.txt')
C('cfe_residual', 'max |G_ab - 8 pi T_ab| with dn1, dn2 and the constraints imposed (E_thth)', 'Sec. 2', '3e-6', F(CFE, r'^equations imposed', i=3, a=True))
C('cfe_perturb_min', 'component departure when its second derivative is changed by 0.1 (smallest)', 'Sec. 2', '0.07', F(CFE, r'^perturbed dr_uu\+=0\.1', i=0, a=True))
C('cfe_perturb_max', 'component departure (largest, E_thth for ds_uv)', 'Sec. 2', '1.6', F(CFE, r'^perturbed ds_uv\+=0\.1', i=3, a=True))
C('cfe_box_phi', 'box phi = 0 against dn3', 'Sec. 2', '1e-15', F(CFE, r'box phi with phi_uv = dn3:', i=0, a=True))
# symbolic derivations (sympy_checks.py)
SYM = [('S1_uu_constraint', 'uu Einstein constraint of ds^2 = -W du dv + r^2 dOmega^2 with the NED+scalar stress tensor', 'Eq. (constraints)'),
       ('S1_vv_constraint', 'vv Einstein constraint', 'Eq. (constraints)'),
       ('S1_dn1', 'Eq. (dn1) = theta-theta/uv Einstein equation', 'Eq. (dn1)'),
       ('S1_dn2', 'Eq. (dn2)', 'Eq. (dn2)'), ('S1_dn3', 'Eq. (dn3) = box phi = 0', 'Eq. (dn3)'),
       ('S1_remaining_components', 'all remaining Einstein components vanish identically', 'Sec. 2'),
       ('S1_misner_sharp', 'Misner-Sharp mass M = (r/2)(1 + 4 r_u r_v/W)', 'Sec. 2'),
       ('S1_negative_control_dn2', 'negative control: wrong coefficient in dn2 is detected', 'Sec. 2'),
       ('S1_negative_control_dn1', 'negative control: wrong coefficient in dn1 is detected', 'Sec. 2'),
       ('S1_negative_control_constraint', 'negative control: wrong constraint is detected', 'Sec. 2'),
       ('S1_scalar_T_uv_vanishes', 'scalar T_uv = 0 (massless, so Eq. dn2 has no phi^2 term)', 'Sec. 2'),
       ('S2_rho_prime', "rho' = sigma_v rho + 4 pi r phi_v^2", 'Eq. (ray)'),
       ('S2_lny_prime', "(ln y)' = rho/r - sigma_v + S/y", 'Eq. (ray)'),
       ('S2_M_of_y_rho', 'M = (r/2)(1 + 4 y rho)', 'Eq. (ray)'),
       ('S2_rayrate', 'd ln(M - r/2)/dv = 4 pi r phi_v^2/rho + S/y', 'Eq. (rayrate)'),
       ('S3_mu_v', 'mu_v = -8 pi r^2 (r_u/W) phi_v^2', 'Eq. (muv)'),
       ('S4_u_constraint_integral', "d_u(r_u/W) = -4 pi r phi_u^2/W, hence y_c = 1/2 + integral", 'Eq. (yc)'),
       ('S5_wave_equation_EF', 'ingoing-EF wave equation (r^2 f F\')\' - 2 i w r (r F)\' = 0', 'Sec. 4.2'),
       ('S5_frobenius_a', 'regular solution F = 1 + a (r_+ - r) + ..., a = -i w/[r_+(kappa_+ - i w)]', 'Sec. 4.2'),
       ('S5_recursion_denominators', 'recursion denominators n(kappa_+ n - i w): poles at w = -i n kappa_+', 'Sec. 4.2'),
       ('S5_static_equation', 'static equation (r^2 f g\')\' + 2 r = 0 for phi = j0 (v + g(r))', 'Sec. 4.2'),
       ('S5_static_solution', 'regular solution r^2 f g\' = r_+^2 - r^2', 'Sec. 4.2'),
       ('S5_T0_gain', 'T(0) = (1 + r_+^2/r_-^2)/2 from the static solution', 'Eq. (T0)'),
       ('S5_outgoing_ray', 'phi_v = j0 [1 + (f/2) g\'] = j0 (1 + r_+^2/r^2)/2 on the outgoing ray', 'Sec. 4.2'),
       ('S6_RN_kappas', 'Reissner-Nordstrom: kappa_pm = (r_+ - r_-)/(2 r_pm^2)', 'Sec. 4.6'),
       ('S6_RN_T0_equals_ori_b0', 'RN: T(0) = (kappa_+ + kappa_-)/(2 kappa_+) = Ori b_0', 'Sec. 4.6'),
       ('S7_filter_a1', 'exponential filtering of a power-law flux: first correction a_1 = p/kappa', 'Sec. 5'),
       ('S7_q_limit_equals_p', 'lim (kappa - d ln M/dv) v = p = 2k+2 for a flux phi_v^2 ~ v^-(2k+2)', 'Sec. 5')]
for nm, q, loc in SYM: C('sym_' + nm, q + ' (exact, sympy)', loc, 1, P('sympy_checks', nm), 'eq', 'exact symbolic statement: the script prints PASS or FAIL')

# =====================================================================================================================================
# Sec. 3: data regular on the event horizon
# =====================================================================================================================================
PN = lambda name: V('paper_numbers', name)
TE = R('results_table_eh.txt')
T1 = [('1.5', '0.03', '3/2, 0.03', ['9.956e-3', '0.784821', '0.78597', '0.78507', '0.78502', '0.78501', '0.78561']),
      ('1.5', '0.05', '3/2, 0.05', ['2.7757e-2', '0.763567', '0.76518', '0.76422', '0.76416', '0.76416', '0.76604']),
      ('0.5', '0.03', '1/2, 0.03', ['5.913e-3', '0.789303', '0.79231', '0.79147', '0.79142', '0.79142', '0.79557']),
      ('0.5', '0.05', '1/2, 0.05', ['1.6461e-2', '0.777349', '0.78443', '0.78364', '0.78359', '0.78358', '0.79669'])]
T1cols = ['mu_f', 'kappa_-(mu_f)', '|sigma_v| h=0.05', '|sigma_v| h=0.0125', '|sigma_v| h=0.003125', '|sigma_v| extrap. U=0.3', '|sigma_v| extrap. U=1']
for k, B, lab, vals in T1:
    for j, (cn, p) in enumerate(zip(T1cols, vals)):
        C('T1_k%s_B%s_%d' % (k, B, j), 'Table 1 (k, B) = (%s): %s' % (lab, cn), 'Table 1', p, F(TE, r'^%s\s+%s\s' % (k.replace('.', r'\.'), B.replace('.', r'\.')), i=j))
for B, k, pu3, pu1, ps in (('0.03', '1.5', '0.024', '0.10', '0.15'), ('0.05', '1.5', '0.077', '0.32', '0.21'), ('0.03', '0.5', '0.27', '0.79', None), ('0.05', '0.5', '0.80', '2.5', None)):
    t = 'B%s_k%s' % (B, k)
    C('T1_pct_U0.3_' + t, 'extrapolated |sigma_v| above kappa_-(mu_f) on U=0.3 (percent), B=%s k=%s' % (B, k), 'Sec. 3', pu3, PN('T1_ext_U0.3_above_pred_percent_' + t))
    C('T1_pct_U1_' + t, 'extrapolated |sigma_v| above kappa_-(mu_f) on U=1 (percent), B=%s k=%s' % (B, k), 'Sec. 3', pu1, PN('T1_ext_U1_above_pred_percent_' + t))
    if ps: C('T1_pct_single_' + t, 'single-grid h=0.05 |sigma_v| above kappa_-(mu_f) on U=0.3 (percent), B=%s k=%s' % (B, k), 'Sec. 3', ps, PN('T1_single_h0.05_above_pred_percent_' + t))
C('T1_B005_k05_U1_exceeds_static', 'k=1/2, B=0.05: extrapolated |sigma_v| on U=1 (0.79669) exceeds the static value 0.795649', 'Sec. 3', '0.795649',
  F(TE, r'^0\.5\s+0\.05\s', i=6), 'ge', 'inequality quoted in the text: computed value must be >= static kappa_-')
for tag in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.05_k1.5'):
    for j, p in enumerate(('3.98', '4.0', '4.0')):
        C('T1_succ_ratio%d_%s' % (j, tag), 'ratio of successive differences of the single-grid |sigma_v| (v=95, U=0.3), number %d, %s' % (j + 1, tag), 'Sec. 3', p,
          PN('T1_ratio_succ_diff%d_%s' % (j, tag)), 'abs:0.05' if j == 0 else 'abs:0.1', 'paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0')

# ---- raw mass function is noise-dominated (Sec. 3)
for j, p, u in (('0', '-9.1', 'e17'), ('1', '-2.6', 'e17'), ('2', '-0.67', 'e17'), ('3', '-0.15', 'e17'), ('4', '-0.018', 'e17')):
    C('rawM_v100_grid%s' % j, 'single-grid M at v=100, B=0.03, k=3/2, U=1, grid %s of 5 (units 1e17)' % j, 'Sec. 3 (raw mass)', p, PN('raw_M_v100_grid%s_e17' % j))
C('rawM_v100_extrap', 'five-grid extrapolated M at v=100 (units 1e15)', 'Sec. 3 (raw mass)', '2.5', PN('raw_M_v100_extrap_e15'))
for v, a, b in ((60, '2', '9'), (80, '18', '71'), (100, '171', '683')):
    C('rawM_finest_off_v%d' % v, 'finest-grid M off from the extrapolant at v=%d (percent)' % v, 'Sec. 3', a, PN('raw_M_finest_off_percent_v%d' % v), None if v != 80 else 'abs:0.5',
      'paper rounds 17.7 to 18' if v == 80 else None)
    C('rawM_next_off_v%d' % v, 'second-finest grid M off from the extrapolant at v=%d (percent)' % v, 'Sec. 3', b, PN('raw_M_next_off_percent_v%d' % v))
for j, p in enumerate(('9.1', '2.7', '0.69', '0.17', '0.044')):
    C('rawM_err_v100_grid%d' % j, 'error of single-grid M against the extrapolant at v=100, grid %d (units 1e17)' % j, 'Sec. 3', p, PN('err_M_v100_grid%d_e17' % j))
for j, p in enumerate(('3.4', '3.9', '4.0', '4.0')):
    C('rawM_err_factor%d' % j, 'successive factor of the errors of single-grid M at v=100, number %d' % (j + 1), 'Sec. 3', p, PN('err_M_v100_factor%d' % j))
C('rawM_rate_extrap', 'rate of the extrapolated M over [84,88], k=3/2', 'Sec. 3', '0.691', PN('rate_84_88_extrapolant'))
C('rawM_rate_finest', 'rate of the finest-grid M over [84,88]', 'Sec. 3', '0.632', PN('rate_84_88_finest'))
C('rawM_rate_undefined', 'grids on which the rate over [84,88] is undefined (M<0)', 'Sec. 3', 4, PN('rate_84_88_n_grids_undefined'), 'eq', 'integer count')
C('rawM_rate_low_percent', 'finest-grid rate low by (percent)', 'Sec. 3', '8.5', PN('rate_84_88_finest_low_percent'))
C('rawM_k05_finest_v100', 'k=1/2: finest-grid M at v=100 (units 1e17)', 'Sec. 3', '2.4', PN('raw_M_k0.5_v100_finest_e17'))
C('rawM_k05_extrap_v100', 'k=1/2: extrapolated M at v=100 (units 1e17)', 'Sec. 3', '2.5', PN('raw_M_k0.5_v100_extrap_e17'), 'abs:0.06',
  'computed 2.55 lies at the rounding boundary between 2.5 and 2.6')
C('rawM_k05_v60_min', 'k=1/2: smallest single-grid M at v=60', 'Sec. 3', '-6e3', PN('raw_M_k0.5_v60_min'))
C('rawM_k05_v60_max', 'k=1/2: largest single-grid M at v=60', 'Sec. 3', '3.2e4', PN('raw_M_k0.5_v60_max'))
C('rawM_B005_k15_finest_off', 'B=0.05, k=3/2: finest-grid M off at v=100 (percent)', 'Sec. 3', '53', PN('B0.05_k1.5_finest_M_v100_off_percent'))
C('rawM_B005_k05_finest_off', 'B=0.05, k=1/2: finest-grid M off at v=100 (percent)', 'Sec. 3', '2', PN('B0.05_k0.5_finest_M_v100_off_percent'))   # the text prints 2% for 2.5 (rounds at the boundary)
C('rawM_levels_main', 'two highest Romberg levels of M agree (relative), v>=60, main series', 'Sec. 3', '1.4e-6', PN('romberg_levels_gap_main_series'))
C('rawM_levels_wide', 'same including the wide-seed run', 'Sec. 3', '1.1e-4', PN('romberg_levels_gap_with_wide_seed'))

# ---- Table 2 (report_stream.py)
RS = R('results_stream_5grid.txt')
T2 = [('tail k=1/2', r'^gen_B0\.03_k0\.5_A0_U1_w0\.3_v110', [('60', '0.7338', '0.7347', '0.7340', '0.8008'), ('84', '0.7457', '0.7463', '0.7457', '0.7967'), ('104', '0.7543', '0.7548', '0.7544', '0.7945')]),
      ('tail k=3/2', r'^gen_B0\.03_k1\.5_A0_U1_w0\.3_v110', [('60', '0.6868', '0.6872', '0.6869', '0.7880'), ('84', '0.6911', '0.6913', '0.6911', '0.7860'), ('104', '0.6947', '0.6950', '0.6947', '0.7853')]),
      ('seed k=1/2', r'^gen_B0\.03_k0\.5_A0\.02_U1_w0\.3_v110', [('60', '0.7086', '0.7077', '0.7079', '0.7635'), ('84', '0.7272', '0.7285', '0.7273', '0.7780'), ('104', '0.7425', '0.7433', '0.7426', '0.7826')]),
      ('seed k=3/2', r'^gen_B0\.03_k1\.5_A0\.02_U1_w0\.3_v110', [('60', '0.6948', '0.6890', '0.6930', '0.7704'), ('84', '0.6861', '0.6866', '0.6861', '0.7803'), ('104', '0.6926', '0.6930', '0.6926', '0.7831')]),
      ('seed k=5/2', r'^gen_B0\.03_k2\.5_A0\.02_U1_w0\.3_v110', [('60', '0.6958', '0.6889', '0.6938', '0.7701'), ('84', '0.6808', '0.6811', '0.6808', '0.7794'), ('104', '0.6838', '0.6840', '0.6838', '0.7819')])]
WIN = {'60': r'\[ 60, 64\] rate', '84': r'\[ 84, 88\] rate', '104': r'\[104,108\] rate'}
for lab, anc, rows in T2:
    for w, rate, lam, lam2, sv in rows:
        for nm, i, p in (('rate', 0, rate), ('lambda', 1, lam), ('lambda-lambda\'/lambda', 2, lam2), ('|sigma_v|', -1, sv)):
            C('T2_%s_%s_%s' % (lab.replace(' ', '').replace('/', ''), w, {'rate': 'rate', 'lambda': 'lam', "lambda-lambda'/lambda": 'lam2', '|sigma_v|': 'sV'}[nm]), 'Table 2 %s, window [%s,%d]: %s' % (lab, w, int(w) + 4, nm), 'Table 2', p, F(RS, anc, WIN[w], i=i))
for tag, anc, p in (('k=1/2', r'^gen_B0\.03_k0\.5_A0_U1_w0\.3_v110', '0.78930'), ('k=3/2', r'^gen_B0\.03_k1\.5_A0_U1_w0\.3_v110', '0.78482'), ('k=5/2', r'^gen_B0\.03_k2\.5_A0\.02_U1_w0\.3_v110', '0.78342')):
    C('T2_km_' + tag.replace('/', ''), 'Table 2 caption: kappa_-(mu_f) for %s' % tag, 'Table 2', p, F(RS, anc + r'.*kappa-\(mu_f\)=([0-9.]+)', g=1))
for k, nm, p, t in (('0.5', 'k=1/2', '44.5', 0.5), ('1.5', 'k=3/2', '46', 1.5), ('2.5', 'k=5/2', '47.5', 0.5)):
    C('seed_node_' + nm.replace('/', ''), 'node of the seeded phi_v on U=1 (%s)' % nm, 'Sec. 3 (Table 2 text)', p, PN('seed_node_k' + k), 'abs:%g' % t,
      'the paper quotes the node range "v ~ 44.5-47.5" (interpolated zeros 44.25, 46.82, 47.37; k=3/2 only has to lie inside the range)')
# ---- rate against the relation (Sec. 3)
C('rel_main_U1_from72', 'max |rate - (lambda - lambda\'/lambda)|, five series, rays U=1 and 1.2, windows from [72,76]', 'Sec. 3', 2e-4, PN('rate_rel_main_U1_U1.2_from72_max'), 'le', 'bound quoted in the text')
C('rel_main_U06_from72', 'same on U=0.6 from [72,76]', 'Sec. 3', 2e-4, PN('rate_rel_main_U0.6_from72_max'), 'le', 'bound quoted in the text')
C('rel_seeded_60_min', 'seeded runs, U=1, [60,64]: smallest difference (+0.7e-3)', 'Sec. 3', '0.7e-3', PN('rate_rel_seeded_U1_at60_min'))
C('rel_seeded_60_max', 'seeded runs, U=1, [60,64]: largest difference (+2.1e-3)', 'Sec. 3', '2.1e-3', PN('rate_rel_seeded_U1_at60_max'))
C('rel_tail_60', 'tail alone, U=1, [60,64]: difference', 'Sec. 3', 2e-4, PN('rate_rel_tail_U1_at60_max'), 'le', 'bound quoted in the text')
C('rel_M_small_min', 'difference on U=0.3, 0.6 while M<~10: smallest', 'Sec. 3', '0.01', PN('rate_rel_M_below_10_min'), 'abs:0.005', 'paper quotes the range "0.01-0.7" to one digit')
C('rel_M_small_max', 'difference on U=0.3, 0.6 while M<~10: largest', 'Sec. 3', '0.7', PN('rate_rel_M_below_10_max'), 'abs:0.05', 'paper quotes the range "0.01-0.7" to one digit (0.747)')
C('rel_example', 'tail only, k=3/2, U=0.3, [84,88]: difference (M=9)', 'Sec. 3', '-1.4e-2', PN('rate_rel_tail_k1.5_U0.3_84_88'))
C('rel_example_M', 'M at v=84 for that example', 'Sec. 3', '9', PN('M_ext_tail_k1.5_U0.3_v84'), 'abs:0.5', 'paper: "M=9"')
C('rel_M_large', 'difference once M >~ 4e2 (all five series, all rays, windows from [72,76])', 'Sec. 3', 4e-4, PN('rate_rel_all_rays_M_over_4e2_max'), 'le', 'bound quoted in the text')
C('rel_B005_60', 'B=0.05 tail only: difference at [60,64] (k=1/2, bound 5e-4)', 'Sec. 3', 5e-4, PN('B0.05_k0.5_rel_at60'), 'le', 'bound quoted in the text')
C('rel_B005_72_k05', 'B=0.05, k=1/2: difference from [72,76] (bound 2e-4)', 'Sec. 3', '2e-4', PN('B0.05_k0.5_rel_from72'))
C('rel_B005_72_k15', 'B=0.05, k=3/2: difference from [72,76] (bound 2e-4)', 'Sec. 3', 2e-4, PN('B0.05_k1.5_rel_from72'), 'le', 'bound quoted in the text')
C('rel_B005_60_k15', 'B=0.05, k=3/2: difference at [60,64] (bound 5e-4)', 'Sec. 3', 5e-4, PN('B0.05_k1.5_rel_at60'), 'le', 'bound quoted in the text')
C('rate_B005_k05_min', 'B=0.05, k=1/2: smallest rate over the windows', 'Sec. 3', '0.746', PN('B0.05_k0.5_rate_min'))
C('rate_B005_k05_max', 'B=0.05, k=1/2: largest rate', 'Sec. 3', '0.753', PN('B0.05_k0.5_rate_max'))
C('rate_B005_k15_min', 'B=0.05, k=3/2: smallest rate', 'Sec. 3', '0.672', PN('B0.05_k1.5_rate_min'))
C('rate_B005_k15_max', 'B=0.05, k=3/2: largest rate', 'Sec. 3', '0.675', PN('B0.05_k1.5_rate_max'))
C('B005_km_k05', 'kappa_-(mu_f) at B=0.05, k=1/2', 'Sec. 3', '0.77735', PN('T1_kappa_mu_f_B0.05_k0.5'), 'abs:6e-6', 'T1 prints six digits (0.777349); paper rounds to five')
C('B005_km_k15', 'kappa_-(mu_f) at B=0.05, k=3/2', 'Sec. 3', '0.76357', PN('T1_kappa_mu_f_B0.05_k1.5'), 'abs:6e-6', 'T1 prints six digits (0.763567); paper rounds to five')
C('lam_corr_seed_k05_72', 'without the lambda\'/lambda correction: rate - lambda, seeded k=1/2, [72,76]', 'Sec. 3', '1.5e-3', V('paper_numbers', 'rate_minus_lambda_seeded_k0.5_72', a=True))
C('lam_corr_seed_k15_60', 'without the correction: rate - lambda, seeded k=3/2, [60,64]', 'Sec. 3', '5.8e-3', PN('rate_minus_lambda_seeded_k1.5_60'))
C('lam_corr_seed_k25_60', 'without the correction: rate - lambda, seeded k=5/2, [60,64]', 'Sec. 3', '7.0e-3', PN('rate_minus_lambda_seeded_k2.5_60'))
# ---- seeds
C('seed01_72', 'seed (0.01,1,0.3): difference for v>=72 (bound 5e-5)', 'Sec. 3', 5e-5, PN('seed_A0.01_rel_from72'), 'le', 'bound quoted in the text')
C('seed01_60', 'seed (0.01,1,0.3): difference at [60,64]', 'Sec. 3', '8e-4', PN('seed_A0.01_rel_60'))
C('seed07_72', 'seed (0.02,0.7,0.2): difference at [72,76]', 'Sec. 3', '5e-4', PN('seed_A0.02_U0.7_rel_72'))
C('seed07_84', 'seed (0.02,0.7,0.2): difference after [72,76] (bound 5e-5)', 'Sec. 3', 5e-5, PN('seed_A0.02_U0.7_rel_from84'), 'le', 'bound quoted in the text')
C('seed07_60', 'seed (0.02,0.7,0.2): difference at [60,64]', 'Sec. 3', '-5.6e-3', PN('seed_A0.02_U0.7_rel_60'))
C('seed07_node1', 'seed (0.02,0.7,0.2): first node of phi_v', 'Sec. 3', '34', PN('seed_A0.02_U0.7_first_node'))
C('seed07_node2', 'seed (0.02,0.7,0.2): second node of phi_v', 'Sec. 3', '54', PN('seed_A0.02_U0.7_second_node'))
C('seed05_node', 'wide seed (0.02,1,0.5): phi_v changes sign at v', 'Sec. 3', '92', PN('wide_seed_phiv_node_v'), 'abs:1', 'grid spacing 1 in vq; paper says "v~92"')
for w, rp, lp, dp in (('72', '0.52', '0.52', '-1.8e-3'), ('84', '0.38', '0.61', '-0.23'), ('96', '1.07', '1.09', '-0.018'), ('104', '0.82', '0.82', '2.0e-3')):
    C('seed05_rate_' + w, 'wide seed: rate of M over [%s,%d]' % (w, int(w) + 4), 'Sec. 3', rp, PN('wide_seed_rate_' + w))
    C('seed05_lam2_' + w, 'wide seed: lambda - lambda\'/lambda over [%s,%d]' % (w, int(w) + 4), 'Sec. 3', lp, PN('wide_seed_lam2_' + w))
    C('seed05_diff_' + w, 'wide seed: difference over [%s,%d]' % (w, int(w) + 4), 'Sec. 3', dp, PN('wide_seed_diff_' + w), None if w != '96' else 'abs:6e-4', None if w != '96' else 'computed -0.0175 lies at the rounding boundary of -0.018')
C('seed03_M_U06_v60', 'A=0.03 seed at U_0=0.6: extrapolated M on U=0.6 at v=60 (units 1e9)', 'Sec. 3', '3.7', PN('seed_A0.03_M_ext_U0.6_v60_e9'))
C('seed03_grids', 'A=0.03 seed: number of grids', 'Sec. 3', 4, PN('seed_A0.03_n_grids'), 'eq', 'integer count')
C('seed03_both_signs', 'A=0.03 seed: the four grids give both signs of M at v=80 (flag)', 'Sec. 3', 1, PN('seed_A0.03_M_v80_both_signs'), 'eq', 'flag')
C('seed03_rneg', 'A=0.03 seed: sigma_v non-finite on U=1 on every grid from v=45 (r<0 between v=40 and 60)', 'Sec. 3', 1, PN('seed_A0.03_U1_nonfinite_all_grids'), 'eq', 'flag')
C('seed03_first_nan', 'A=0.03 seed: first non-finite v on U=1 (between 40 and 60)', 'Sec. 3', 40, PN('seed_A0.03_U1_first_nonfinite_v_min'), 'ge', 'paper: "between v=40 and 60"')
C('seed03_first_nan_le', 'A=0.03 seed: first non-finite v on U=1 (between 40 and 60)', 'Sec. 3', 60, PN('seed_A0.03_U1_first_nonfinite_v_min'), 'le', 'paper: "between v=40 and 60"')

# ---- ingoing flux on the rays (Sec. 3) and late-time sigma_v
for k, anc, rr, ee in (('1/2', r'^gen_B0\.03_k0\.5_A0_U1_w0\.3_v110', ('9.8', '8.2', '7.1'), ('2.0', '2.2', '2.1')),
                       ('3/2', r'^gen_B0\.03_k1\.5_A0_U1_w0\.3_v110', ('91', '69', '47'), ('3.0', '3.8', '4.6'))):
    for j, v in enumerate((60, 80, 100)):
        C('flux_ratio_tail_k%s_v%d' % (k.replace('/', ''), v), 'tail only k=%s: |phi_v| over the tail transported from H+ with r_+/r_- = 9.36, v=%d' % (k, v), 'Sec. 3 (flux)', rr[j],
          F(RS, anc, r'phi_v: v=60:', i=4 * j + 2))
        C('flux_exp_tail_k%s_v%d' % (k.replace('/', ''), v), 'tail only k=%s: local exponent -d ln|phi_v|/d ln v, v=%d' % (k, v), 'Sec. 3 (flux)', ee[j], F(RS, anc, r'phi_v: v=60:', i=4 * j + 1))
C('flux_ratio_min', 'smallest ratio to the transported tail (tail only and seeded k=1/2, 3/2)', 'Sec. 3 (flux)', '7', PN('flux_ratio_to_tail_min_over_main_series'))
C('flux_ratio_max', 'largest ratio to the transported tail (tail only and seeded k=1/2, 3/2)', 'Sec. 3 (flux)', '110', PN('flux_ratio_to_tail_max_over_main_series_excl_k2.5'), 'abs:5', 'quoted to two significant figures (106.7 -> 110)')
C('flux_ratio_k25', 'seeded k=5/2: ratio to the transported tail (~3e3)', 'Sec. 3 (flux)', '3e3', PN('flux_ratio_to_tail_seeded_k2.5_v100'))
C('flux_spread_k05', 'spread of phi_v over the rays U=0.3-1.2 at v=100, k=1/2 (percent)', 'Sec. 3 (flux)', '2.5', PN('flux_ray_spread_percent_k0.5_v100'))
C('flux_spread_k15', 'spread of phi_v over the rays at v=100, k=3/2 (percent)', 'Sec. 3 (flux)', '1', PN('flux_ray_spread_percent_k1.5_v100'), 'abs:0.5', 'paper quotes 1 (computed 1.1)')
C('flux_vs_T0_k05', 'phi_v over T(0) j at v=100, k=1/2', 'Sec. 3 (flux)', '1.4', F(R('results_kernel_analytic.txt'), r'^\s*k=0\.5\s+v_c', r'ratio at v=100:', i=0), 'abs:0.05', 'two-digit rounding of 1.43')
C('flux_vs_T0_k15', 'phi_v over T(0) j at v=100, k=3/2', 'Sec. 3 (flux)', '9.5', F(R('results_kernel_analytic.txt'), r'^\s*k=1\.5\s+v_c', r'ratio at v=100:', i=0), 'abs:0.05', 'two-digit rounding of 9.54')
C('flux_exp_k15_B0003_v140', 'local exponent of phi_v at v=140, k=3/2, B=0.003', 'Sec. 3 (flux)', '5.5', F(R('results_longrun_v300.txt'), r'^gen_B0\.003_k1\.5', r'^\s+140\s', i=2), 'abs:0.05', 'two digits of 5.54')
LS = [('k1.5', '3/2', ('0.7880', '0.7868', '0.7860', '0.7855', '0.7853'), '0.062', '0.06', '2.1', '4.4'), ('k0.5', '1/2', ('0.8008', '0.7986', '0.7967', '0.7953', '0.7945'), '0.659', '0.66', '0.9', '1.7')]
for kk, lab, vals, pct_, pct_p, e60, e100 in LS:
    for v, p in zip((62, 74, 86, 98, 106), vals):
        C('late_sV_%s_v%d' % (kk, v), '|sigma_v| on U=1, tail only k=%s, v~%d' % (lab, v), 'Sec. 3 (late times)', p, PN('late_sV_U1_%s_v%d' % (kk, v)))
    C('late_sV_pct_' + kk, '|sigma_v| above kappa_-(mu_f) at v=106, k=%s (percent)' % lab, 'Sec. 3 (late times)', pct_p, PN('late_sV_U1_%s_above_percent_v106' % kk), None if kk == 'k0.5' else 'abs:0.005',
      None if kk == 'k0.5' else 'paper rounds 0.062 to 0.06')
    C('late_exp60_' + kk, 'local exponent of the excess |sigma_v| - kappa_- at v=60 (U=1), k=%s' % lab, 'Sec. 3 (late times)', e60, PN('late_sV_excess_local_exponent_U1_%s_v60' % kk),
      None if kk == 'k1.5' else 'abs:0.06', None if kk == 'k1.5' else 'computed 0.85 lies on the rounding boundary of 0.9')
    C('late_exp100_' + kk, 'local exponent of the excess at v=100, k=%s' % lab, 'Sec. 3 (late times)', e100, PN('late_sV_excess_local_exponent_U1_%s_v100' % kk))
C('late_U03_min', 'k=1/2, U=0.3: excess |sigma_v| - kappa_- over v=70-100, smallest (1e-3)', 'Sec. 3 (late times)', '2.0', PN('late_sV_excess_U0.3_k0.5_min_v70_100'))
C('late_U03_max', 'same, largest (1e-3)', 'Sec. 3 (late times)', '2.3', PN('late_sV_excess_U0.3_k0.5_max_v70_100'), 'abs:0.05', 'computed 2.26 (paper: 2.0-2.3)')
C('late_U03_fall', 'k=1/2, U=0.3: the excess falls by about 10 percent after v=80', 'Sec. 3 (late times)', '10', PN('late_sV_excess_U0.3_k0.5_fall_after_v80_percent'), 'abs:1.5', 'paper says "about 10%"')
C('late_seeded_k15', 'seeded k=3/2: |sigma_v| at v=106', 'Sec. 3 (late times)', '0.7831', PN('seeded_k1.5_sV_v106'))
C('late_B005_k15_pct', 'B=0.05 k=3/2: excess at v~106 (percent)', 'Sec. 3 (late times)', '0.20', PN('B0.05_k1.5_excess_percent_v106'))
C('late_B005_k15_sV', 'B=0.05 k=3/2: |sigma_v| at v~106', 'Sec. 3 (late times)', '0.7651', PN('B0.05_k1.5_sV_v106'))
C('late_B005_k15_sV62', 'B=0.05 k=3/2: |sigma_v| at v~62', 'Sec. 3 (late times)', '0.7735', PN('B0.05_k1.5_sV_v62'))
C('late_B005_k05_pct', 'B=0.05 k=1/2: excess at v~106 (percent)', 'Sec. 3 (late times)', '2.1', PN('B0.05_k0.5_excess_percent_v106'))
C('late_B005_k05_sV', 'B=0.05 k=1/2: |sigma_v| at v~106', 'Sec. 3 (late times)', '0.7934', PN('B0.05_k0.5_sV_v106'))

# =====================================================================================================================================
# Sec. 4: the interior impulse response
# =====================================================================================================================================
PD = R('results_phidecay.txt'); KP = lambda n: V('paper_numbers_kernel', n)
SEEDF = 'gen_B0_k1.5_A0.02_U1_w0.3_v110.json'; SEED7 = 'gen_B0_k1.5_A0.02_U0.7_w0.2_v110.json'
def PDrow(fn, U): return (r'^' + fn.replace('.', r'\.'), r'^\s+U=%s\s+-dln\|phi_v\|/dv at v=40\.\.100:' % U.replace('.', r'\.'))
C('src_a_seed_min', 'seed alone (B=0): smallest |phi_v|(v=100) on the four rays', 'Sec. 4.1(a)', '4e-7', F(PD, *PDrow(SEED7, '0.3'), i=8))
C('src_a_seed_max', 'seed alone: largest |phi_v|(v=100)', 'Sec. 4.1(a)', '1e-6', F(PD, *PDrow(SEED7, '1.0'), i=8))
C('src_a_tail', 'tail alone: |phi_v|(v=100), B=0.03, k=3/2, U=1', 'Sec. 4.1(a)', '1.9e-4', F(PD, *PDrow('gen_B0.03_k1.5_A0_U1_w0.3_v110.json', '1.0'), i=8))
C('src_a_rate50', 'seed alone: local decay rate at v=50 (U=1, A=0.02, U0=1, w=0.3)', 'Sec. 4.1(a)', '0.27', F(PD, *PDrow(SEEDF, '1.0'), i=1))
C('src_a_rate100', 'seed alone: local decay rate at v=100', 'Sec. 4.1(a)', '0.076', F(PD, *PDrow(SEEDF, '1.0'), i=6))
for V0, fn, p1, p2 in (('0.3', 'gen_B0.03_k1.5_A0_U1_w0.3_v110_T0.3.json', '1.6e-4', '0.0486'), ('1', 'gen_B0.03_k1.5_A0_U1_w0.3_v110.json', '1.9e-4', '0.0459'),
                       ('10', 'gen_B0.03_k1.5_A0_U1_w0.3_v110_T10.json', '9.2e-4', '0.0295')):
    C('src_b_phi_V0_%s' % V0, '|phi_v|(v=100) for phi_H = B(1+v/V0)^-k, V0=%s' % V0, 'Sec. 4.1(b)', p1, F(PD, *PDrow(fn, '1.0'), i=8))
    C('src_b_rate_V0_%s' % V0, 'local rate -d ln|phi_v|/dv at v=100, V0=%s' % V0, 'Sec. 4.1(b)', p2, F(PD, *PDrow(fn, '1.0'), i=6))
PU = 'gen_B0.03_k1.5_A0_U1_w0.3_v110_P10_2.json'
for j, (v, p) in enumerate(zip(range(40, 101, 10), ('0.0589', '0.0565', '0.0534', '0.0514', '0.0502', '0.0494', '0.0489'))):
    C('src_c_rate_v%d' % v, 'pulse of horizon flux: local rate at v=%d on U=1' % v, 'Sec. 4.1(c)', p, F(PD, *PDrow(PU, '1.0'), i=j))
C('src_c_peak_U1', 'pulse flux peaks at v on U=1', 'Sec. 4.1(c)', '34', KP('pulse_peak_v_U1'), 'eq', 'integer grid point of the extrapolated flux')
C('src_c_peak_min', 'pulse flux peak, earliest over the rays (U=1.2)', 'Sec. 4.1(c)', '30', KP('pulse_peak_v_U1.2'), 'eq', 'integer grid point')
C('src_c_peak_max', 'pulse flux peak, latest over the rays (U=0.3)', 'Sec. 4.1(c)', '59', KP('pulse_peak_v_U0.3'), 'eq', 'integer grid point')
C('src_c_rate_spread', 'rates on the four rays agree at v=100 to (percent)', 'Sec. 4.1(c)', '0.2', KP('pulse_rate_spread_v100_percent'))
C('src_c_kappa_plus', 'kappa_+ of the static hole', 'Sec. 4.1(c)', '0.04897', V('static_hole', 'mN5_kp'))
C('src_c_mu_f', 'mu_f of the B=0.03 pulse run', 'Sec. 4.1(c)', '0.088', KP('pulse_B003_mu_f'))
# 4.2
TR5 = R('results_trace_residues_mN5.txt'); TR14 = R('results_trace_residues_mN1.4.txt')
C('res_R1', 'residue R_1 at omega = -i kappa_+ (central difference), m_N=5', 'Sec. 4.2', '0.6442', F(TR5, r'^R1 \(difference.*\):'))
C('res_R1_diff', 'R_1 central difference, 5 digits', 'Sec. 4.2', '0.64423', F(TR5, r'^R1 \(difference.*\):'))
C('res_R1_c03', 'R_1 by contour integral, radius 0.3 kappa_+', 'Sec. 4.2', '0.64422', F(TR5, r'^R1 \(contour, radius 0\.3 kappa\+, 64 points\):'))
C('res_R1_c05', 'R_1 by contour integral, radius 0.5 kappa_+', 'Sec. 4.2', '0.64423', F(TR5, r'^R1 \(contour, radius 0\.5 kappa\+, 64 points\):'))
C('res_K_tau100', 'K(tau) exp(kappa_+ tau) at tau ~ 100', 'Sec. 4.2', '0.65', KP('K_e_kp_tau_at_tau100'))
C('res_T0_numeric', 'numerical A(omega = 1e-3), m_N=5', 'Sec. 4.2', '44.298', F(TR5, r'A\(w=1e-3\) =', i=0))
C('res_T0_corr', 'O(omega^2) difference A(1e-3) - T(0)', 'Sec. 4.2', '0.0066', F(TR5, r'^T\(0\)=.*difference', a=True))
C('T_inf', 'T(omega -> infinity) = r_+/r_- (omega-extrapolated from the ODE transfer function)', 'Sec. 4.2', '9.36', KP('T_inf_extrapolated'))
C('Kreg0', 'K_reg(0+) from omega Im T at omega = 5.9', 'Sec. 4.2', '3.2', KP('omega_ImT_omega5.9'), 'abs:0.05', 'paper: "approximately 3.2"; omega Im T = 3.203 at the largest omega of the table and still decreasing slowly')
C('res14_R1', 'R_1 at m_N=1.4 (residue)', 'Sec. 4.5', '0.0368', F(TR14, r'^R1 \(difference.*\):'))
C('res14_R1_fit', 'R_1 at m_N=1.4 from the three-term fit to the kernel', 'Sec. 4.5', '0.0364', F(R('results_mN1.4_tail250.txt'), r'^m_N=1\.4: T0=[0-9.]+\s+R1=([0-9.]+)', g=1))
C('res14_T0', 'T(0) at m_N=1.4', 'Sec. 4.5', '1.73', V('static_hole', 'mN1.4_T0'))
C('res14_memory', 'memory time 1/kappa_+ at m_N=1.4', 'Sec. 4.5', '11', X(lambda k: 1/k, V('static_hole', 'mN1.4_kp')))
# 4.3 (a)
for vs, p in ((3, '3.567'), (10, '3.624'), (30, '3.670'), (60, '3.684')):
    C('Kpulse_tau60_vs%d' % vs, 'impulse response K(tau=60) from the pulse at v_s=%d, U=1, B=0.003 (1e-2)' % vs, 'Sec. 4.3(a)', p, KP('Kpulse_tau60_vs%d_e2' % vs))
C('Kpulse_30_60', 'kernels from v_s=30 and 60 agree for tau>=30 to (percent)', 'Sec. 4.3(a)', '0.4', KP('Kpulse_30_vs_60_max_rel_diff_tau30_80_percent'))
C('Kpulse_ray_60_a', 'v_s=10, K(tau=60) on U=0.3 (1e-2)', 'Sec. 4.3(a)', '3.624', KP('Kpulse_vs10_tau60_U0.3_e2'))
C('Kpulse_ray_60_b', 'v_s=10, K(tau=60) on U=1 (1e-2)', 'Sec. 4.3(a)', '3.624', KP('Kpulse_vs10_tau60_U1_e2'))
C('Kpulse_ray_95_a', 'v_s=10, K(tau=95) on U=0.3 (1e-3)', 'Sec. 4.3(a)', '6.24', KP('Kpulse_vs10_tau95_U0.3_e3'))
C('Kpulse_ray_95_b', 'v_s=10, K(tau=95) on U=1 (1e-3)', 'Sec. 4.3(a)', '6.24', KP('Kpulse_vs10_tau95_U1_e3'))
C('Kpulse_delay_a', 'v_s=10, K(tau=30) on U=0.3 (1e-4)', 'Sec. 4.3(a)', '7.1', KP('Kpulse_vs10_tau30_U0.3_e4'))
C('Kpulse_delay_b', 'v_s=10, K(tau=30) on U=1', 'Sec. 4.3(a)', '0.19', KP('Kpulse_vs10_tau30_U1'))
for tau, p in ((30, '0.0638'), (40, '0.0571'), (50, '0.0537'), (60, '0.0517'), (70, '0.0506'), (80, '0.0500'), (85, '0.0497')):
    C('Kinf_rate_tau%d' % tau, 'local decay rate of K_infinity at tau=%d' % tau, 'Sec. 4.3(a)', p, KP('Kinf_local_rate_tau%d' % tau))
C('Kpulse_tau0', 'response to the Gaussian pulse at tau=0', 'Sec. 4.3(a)', '4.3', KP('Kpulse_tau0'))
C('Kpulse_taum2', 'smoothed response at tau=-2', 'Sec. 4.3(a)', '1.2', KP('Kpulse_tau-2'))
# 4.3 (b): the convolution with the kernel from the interior ODE
KA = R('results_kernel_analytic.txt')
C('kb_a', 'pole-tail coefficient a fitted to the ODE kernel on 60<=tau<=120', 'Sec. 4.3(b)', '1.063', F(KA, r'^fit tail: a=([0-9.]+)', g=1))
C('kb_b', 'pole-tail coefficient b', 'Sec. 4.3(b)', '0.056', F(KA, r'^fit tail: a=[0-9.]+ b=([0-9.]+)', g=1))
for k, kk in (('0.5', '1/2'), ('1.5', '3/2')):
    pp = {'0.5': ('1.0000', '1.0002', '1.0003'), '1.5': ('0.9996', '0.9998', '1.0003')}[k]
    for v, p in zip((60, 100, 290), pp):
        C('kb_ratio_k%s_v%d' % (k.replace('.', ''), v), 'measured/predicted phi_v, k=%s, v=%d (B=0.003, U=1, four grids)' % (kk, v), 'Sec. 4.3(b)', p,
          F(KA, r'^k=%s\s+v:' % k.replace('.', r'\.'), r'^\s+%d\s' % v, i=2))
C('kb_every_v', 'prediction within this of the measured flux at every v of Table 3', 'Sec. 4.3(b)', '4e-4', KP('kernel_ratio_max_dev'))
C('kb_exponent', 'local exponents agree to', 'Sec. 4.3(b)', 0.01, KP('kernel_exponent_max_dev'), 'le', 'bound quoted in the text')
C('kb_sens', 'change of the prediction by the smoothing variance and the fit window (v=60,100,290), at most', 'Sec. 4.3(b) and Sec. 6, limit 7a', '1.2e-3', KP('kernel_sens_max_change_variants'))
C('kb_sens_drop', 'change of the prediction when the higher pole terms of the tail are dropped (Sec. 4.2: <=1e-3)', 'Sec. 4.2', 1e-3, KP('kernel_sens_max_change_dropped_terms'), 'le', 'bound quoted in the text')
KS = R('results_kernel_sensitivity.txt')
for j, (lab, p) in enumerate((('sig2=0.25', ('0.9992', '0.9986')), ('sig2=1.00', ('0.9990', '0.9993')))):
    pass
# 4.3 (c): other masses
KM = R('results_kernel_mN.txt')
def KMF(m, *a, i=0): return F(KM, r'^m_N=%s\s' % m.replace('.', r'\.'), *a, i=i)
for m, p80, p100, kp in (('3', '0.0784', '0.0783', '0.07827'), ('2', '0.1054', '0.1054', '0.10541'), ('1.6', '0.1102', '0.1102', '0.1101'), ('1.4', '0.0895', '0.0900', '0.0901')):
    C('kc_rate80_mN' + m, 'local decay rate of the pulse kernel at tau=80, m_N=%s' % m, 'Sec. 4.3(c)', p80, KMF(m, r'local decay rate of K_PDE at tau=60,80,100:', i=1))
    C('kc_rate100_mN' + m, 'local decay rate of the pulse kernel at tau=100, m_N=%s' % m, 'Sec. 4.3(c)', p100, KMF(m, r'local decay rate of K_PDE at tau=60,80,100:', i=2))
    C('kc_kp_mN' + m, 'kappa_+ of m_N=%s' % m, 'Sec. 4.3(c)', kp, V('static_hole', 'mN%s_kp' % m))
for m, p in (('3', '14.37'), ('2', '5.33'), ('1.6', '2.81'), ('1.4', '1.733')):
    C('kc_intK_mN' + m, 'integral of the pulse kernel (trapezoid, tail added), m_N=%s' % m, 'Sec. 4.3(c)', p, KMF(m, r'int K_PDE \(all tau, trapezoid, tail e\^\{-kp\}\) =', i=0))
C('kc_dev', 'kernel of Sec. 4.2 reproduces each pulse kernel over -2<=tau<=100 to (percent)', 'Sec. 4.3(c)', '0.5', KP('kernel_mN_max_dev_percent'), 'abs:0.05', 'paper rounds 0.52% to 0.5%')
C('kc_mN5_v30_min', 'm_N=5, v_s=30 pulse kernel above the ODE kernel for tau>=5: smallest (percent)', 'Sec. 4.3(c)', '1.0', KP('kernel_pulse_mN5_vs30_min_percent'))
C('kc_mN5_v30_max', 'same: largest (percent)', 'Sec. 4.3(c)', '1.9', KP('kernel_pulse_mN5_vs30_max_percent'))
C('kc_mN5_v60_min', 'v_s=60: smallest (percent)', 'Sec. 4.3(c)', '1.9', KP('kernel_pulse_mN5_vs60_min_percent'))
C('kc_mN5_v60_max', 'v_s=60: largest (percent)', 'Sec. 4.3(c)', '2.4', KP('kernel_pulse_mN5_vs60_max_percent'))
C('kc_B0003_lo', 'v_s=60 pulse at B=0.0003: ratio PDE/ODE, smallest, quoted as 1.0002 +- 0.0002', 'Sec. 4.3(c)', 1.0000, KP('kernel_B0003_ratio_min'), 'ge', 'range 1.0000-1.0004 implied by 1.0002 +- 0.0002')
C('kc_B0003_hi', 'same, largest', 'Sec. 4.3(c)', 1.0004, KP('kernel_B0003_ratio_max'), 'le', 'range 1.0000-1.0004 implied by 1.0002 +- 0.0002')
C('kc_mu_f_pulse', 'final mass parameter of the v_s=60, B=0.003 pulse run (8.5e-4 in the earlier version of the text is the v_s=10 run)', 'Sec. 4.3(c)', '2.1e-3',
  F(R('results_e11_pulse.txt'), r'^gen_B0\.003_k1\.5_A0_U1_w0\.3_v150_P60_2\.json\s+B=0\.003 mu_f\(PDE\)=([0-9.e+-]+)', g=1))
# 4.3 (e): flux to v = 420
E12 = R('results_e12_ratio.txt')
for v, p in ((60, '0.99964'), (100, '0.99979'), (150, '1.00032'), (200, '1.00032'), (250, '1.00030'), (300, '1.00030'), (350, '1.00031'), (420, '1.00030'), (440, '1.00029')):
    C('ke_ratio_v%d' % v, 'PDE/kernel flux ratio (Romberg top level) at v=%d, B=0.003, k=3/2' % v, 'Sec. 4.3(e)', p, F(E12, r'^\s+%d\s' % v, i=0))
C('ke_const', 'ratio constant over 150<=v<=420 to', 'Sec. 4.3(e)', 2e-5, X(lambda *a: max(a) - min(a), *[F(E12, r'^\s+%d\s' % v, i=0) for v in (150, 200, 250, 300, 350, 420)]), 'le',
  'bound quoted in the text (spread of the six printed ratios)')
C('ke_flux_150', 'flux itself at v=150 (kernel_phi_v column, 1e-6)', 'Sec. 4.3(e)', '2.3', F(E12, r'^\s+150\s', i=3, a=True, scale=1e6), 'abs:0.05', 'paper: "2.3e-6" from 2.2675e-6')
C('ke_flux_420', 'flux at v=420 (1e-8)', 'Sec. 4.3(e)', '5.8', F(E12, r'^\s+420\s', i=3, a=True, scale=1e8))
C('ke_factor40', 'flux falls by a factor ~40 between v=150 and 420', 'Sec. 4.3(e)', '40', X(lambda a, b: a/b, F(E12, r'^\s+150\s', i=3, a=True), F(E12, r'^\s+420\s', i=3, a=True)), 'abs:1.5', 'quoted to one significant figure: 2.3e-6 / 5.8e-8 = 39.7, computed ratio 38.8')
C('ke_finest_150', 'finest-grid ratio at v=150', 'Sec. 4.3(e)', '0.986', F(E12, r'^\s+150\s', i=2))
C('ke_finest_400', 'finest-grid ratio at v=400', 'Sec. 4.3(e)', '0.47', F(E12, r'^\s+400\s', i=2))
C('ke_level2_250', 'second Romberg level departs from the first by (v=250)', 'Sec. 4.3(e)', '5e-4', X(lambda a, b: abs(a - b), F(E12, r'^\s+250\s', i=0), F(E12, r'^\s+250\s', i=1)))
C('ke_level2_400', 'second Romberg level departs from the first by (v=400)', 'Sec. 4.3(e)', '6e-3', X(lambda a, b: abs(a - b), F(E12, r'^\s+400\s', i=0), F(E12, r'^\s+400\s', i=1)))
# 4.3 (d): nonlinear excess and the final-hole kernel
E11 = R('results_e11_ratio.txt'); KMU = R('results_kernel_mu.txt')
cols = {100: 0, 150: 1, 200: 2, 250: 3, 280: 4, 290: 5}
for t, tl in (('B0.03_k1.5', 'B=0.03 k=3/2'), ('B0.03_k0.5', 'B=0.03 k=1/2')):
    for v, p in ((250, {'B0.03_k1.5': '1.0354', 'B0.03_k0.5': '1.0351'}[t]), (290, {'B0.03_k1.5': '1.0346', 'B0.03_k0.5': '1.0349'}[t])):
        C('kd_static_%s_v%d' % (t, v), 'PDE/kernel(static hole) flux ratio, %s, v=%d' % (tl, v), 'Sec. 4.3(d)', p, F(E11, r'^%s\s' % t.replace('.', r'\.'), i=cols[v]))
for t in ('B0.003_k1.5', 'B0.003_k0.5'):
    C('kd_static_%s' % t, 'PDE/kernel(static hole) ratio at v=250, %s' % t, 'Sec. 4.3(d)', '1.0003', F(E11, r'^%s\s' % t.replace('.', r'\.'), i=3))
C('kd_final_k15', 'PDE/kernel(final hole), B=0.03 k=3/2, v=250', 'Sec. 4.3(d)', '1.0067', F(KMU, r'^k=1\.5 B=0\.03: PDE', r'^\s+100:', i=6))
C('kd_final_k15_const', 'same: constant over 150<=v<=290 to (the spread is 7e-5 from v=150, 1e-5 from v=200; the earlier text said 1e-5)', 'Sec. 4.3(d)', '7e-5', KP('final_kernel_spread_150_290_B0.03_k1.5'))
C('kd_final_k05_290', 'PDE/kernel(final hole), B=0.03 k=1/2, v=290', 'Sec. 4.3(d)', '1.0186', F(KMU, r'^k=0\.5 B=0\.03: PDE', r'^\s+100:', i=10))
C('kd_final_k05_100', 'same at v=100', 'Sec. 4.3(d)', '1.0211', F(KMU, r'^k=0\.5 B=0\.03: PDE', r'^\s+100:', i=0))
C('kd_final_B0003_k15', 'PDE/kernel(final hole) at B=0.003, k=3/2, v=250', 'Sec. 4.3(d)', '1.0000', F(KMU, r'^k=1\.5 B=0\.003: PDE', r'^\s+100:', i=6))
C('kd_final_B0003_k05', 'same, k=1/2', 'Sec. 4.3(d)', '1.0002', F(KMU, r'^k=0\.5 B=0\.003: PDE', r'^\s+100:', i=6))
C('kd_account_k15', 'displacement of the horizons accounts for (percent of the excess), k=3/2', 'Sec. 4.3(d)', '81', KP('accounted_percent_k1.5_v250'))
C('kd_account_k05', 'displacement of the horizons accounts for (percent), k=1/2', 'Sec. 4.3(d)', '47', KP('accounted_percent_k0.5_v250'))   # was 46
for k, t, a, b, c1, c2 in (('2', 'B0.03_k2', '1.0440', '1.0386', '1.0058', '1.0058'), ('3', 'B0.03_k3', '1.0639', '1.0672', '1.0056', '1.0055')):
    C('kd_static_k%s_250' % k, 'PDE/kernel(static hole), k=%s, B=0.03, v=250' % k, 'Sec. 4.3(d)', a, F(E11, r'^%s\s' % t.replace('.', r'\.'), i=3))
    C('kd_static_k%s_290' % k, 'same at v=290', 'Sec. 4.3(d)', b, F(E11, r'^%s\s' % t.replace('.', r'\.'), i=5))
    C('kd_final_k%s_290' % k, 'PDE/kernel(final hole), k=%s, B=0.03, v=290' % k, 'Sec. 4.3(d)', c1, F(KMU, r'^k=%s B=0\.03: PDE' % k, r'^\s+100:', i=10))
    C('kd_final_k%s_250' % k, 'PDE/kernel(final hole), k=%s, B=0.03, v=250 (Sec. 5: matching factor r_b)' % k, 'Sec. 5', c2, F(KMU, r'^k=%s B=0\.03: PDE' % k, r'^\s+100:', i=6))
C('kd_final_const_k2k3', 'final-hole ratio constant over 150<=v<=290 for k=2, 3 (spreads are 1.5e-4 and 4e-5; the earlier text said 1e-5)', 'Sec. 4.3(d)', '1.4e-4',
  X(max, KP('final_kernel_spread_150_290_B0.03_k2'), KP('final_kernel_spread_150_290_B0.03_k3')))
C('kd_rem_low', 'remainder of the tails k>=3/2 in units of mu_f: smallest (k=3)', 'Sec. 4.3(d)', '0.48', KP('remainder_over_mu_f_B0.03_k3'))
C('kd_rem_high', 'remainder in units of mu_f: largest (k=3/2)', 'Sec. 4.3(d)', '0.67', KP('remainder_over_mu_f_B0.03_k1.5'))
C('kd_rem_k05', 'remainder in units of mu_f for k=1/2', 'Sec. 4.3(d)', '3', KP('remainder_over_mu_f_B0.03_k0.5'), 'abs:0.2', 'paper: "3 mu_f" (computed 3.17); the later text says 3-4 mu_f')
ES = R('results_e11_scaling.txt')
C('kd_scal_B003', 'k=1/2, B=0.03: remainder at v=100', 'Sec. 4.3(d)', '2.12e-2', F(ES, r'^gen_B0\.03_k0\.5.*ratio-1 at v=', r'100:', i=0))
C('kd_scal_B005', 'k=1/2, B=0.05: remainder at v=100', 'Sec. 4.3(d)', '6.67e-2', F(ES, r'^gen_B0\.05_k0\.5.*ratio-1 at v=', r'100:', i=0))
C('kd_scal_mu03', 'k=1/2, B=0.03: remainder in units of mu_f', 'Sec. 4.3(d)', '3.6', X(lambda e, m: e/m, F(ES, r'^gen_B0\.03_k0\.5.*ratio-1 at v=', r'100:', i=0), V('paper_numbers', 'T1_mu_f_B0.03_k0.5')))
C('kd_scal_mu05', 'k=1/2, B=0.05: remainder in units of mu_f', 'Sec. 4.3(d)', '4.1', X(lambda e, m: e/m, F(ES, r'^gen_B0\.05_k0\.5.*ratio-1 at v=', r'100:', i=0), V('paper_numbers', 'T1_mu_f_B0.05_k0.5')))
C('kd_scal_ratio', 'ratio of the remainders B=0.05 / B=0.03', 'Sec. 4.3(d)', '3.15', X(lambda a, b: a/b, F(ES, r'^gen_B0\.05_k0\.5.*ratio-1 at v=', r'100:', i=0), F(ES, r'^gen_B0\.03_k0\.5.*ratio-1 at v=', r'100:', i=0)))
C('kd_scal_B4', 'excess of the remainder ratio over B^2 scaling, eps(0.05)/eps(0.03) / (0.05/0.03)^2 - 1 (percent)', 'Sec. 4.3(d)', '13',
  X(lambda e3, e5: 100 * (e5/e3 / (0.05/0.03)**2 - 1), F(ES, r'^gen_B0\.03_k0\.5.*ratio-1 at v=', r'100:', i=0), F(ES, r'^gen_B0\.05_k0\.5.*ratio-1 at v=', r'100:', i=0)),
  'abs:1', 'the text calls this a "B^4 term of ~13%"; the quantity is 13.5%')
C('kd_scal_k15_B003', 'k=3/2, B=0.03: remainder at v=100', 'Sec. 4.3(d)', '7.1e-3', F(ES, r'^gen_B0\.03_k1\.5.*ratio-1 at v=', r'100:', i=0))
C('kd_scal_k15_B0003', 'k=3/2, B=0.003: remainder at v=100', 'Sec. 4.3(d)', '-5.5e-4', F(ES, r'^gen_B0\.003_k1\.5.*ratio-1 at v=', r'100:', i=0))
C('kd_scal_k15_B0003_v290', 'k=3/2, B=0.003: ratio - 1 at v=290', 'Sec. 4.3(d)', '3e-5', X(lambda a: a - 1, F(KMU, r'^k=1\.5 B=0\.003: PDE', r'^\s+100:', i=10)))
C('kd_scal_k05_B0003', 'k=1/2, B=0.003: remainder at v>=250', 'Sec. 4.3(d)', '1.6e-4', X(lambda a: a - 1, F(KMU, r'^k=0\.5 B=0\.003: PDE', r'^\s+100:', i=6)))
C('kd_scal_k05_B0003_mu', 'same in units of mu_f', 'Sec. 4.3(d)', '2.7', KP('remainder_over_mu_f_B0.003_k0.5'))
# pulses (e11_pulse_all.py): rows of the SUMMARY table, columns after (v_s, B, v1): mu_f, ratio-1 (static kernel), ratio-1 (final-hole kernel), eps/mu_f, eps/B^2
EP = R('results_e11_pulse.txt')
def EPs(vs, B, v1, col): return F(EP, r'^v_s\s+B\s+v1', r'^\s*%s\s+%s\s+%s\s' % (vs, B.replace('.', r'\.'), v1), i=col)
for vs, B, e_p in ((60, '0.0003', '1.2e-4'), (60, '0.003', '1.25e-2'), (30, '0.0003', '9.9e-5'), (30, '0.003', '1.0e-2')):
    C('kd_pulse_eps_vs%d_B%s' % (vs, B), 'pulse v_s=%d, B=%s: PDE response at tau=60 exceeds the final-hole kernel by' % (vs, B), 'Sec. 4.3(d)', e_p, EPs(vs, B, '150', 2))
C('kd_pulse_eps_range_lo', 'eps/mu_f for v_s=30, 60: smallest', 'Sec. 4.3(d)', '5.8', X(min, *[EPs(vs, B, '150', 3) for vs in (30, 60) for B in ('0.0003', '0.003')]))
C('kd_pulse_eps_range_hi', 'eps/mu_f for v_s=30, 60: largest', 'Sec. 4.3(d)', '6.0', X(max, *[EPs(vs, B, '150', 3) for vs in (30, 60) for B in ('0.0003', '0.003')]))
C('kd_pulse_eps_vs10_B0003', 'pulse v_s=10, B=3e-4: excess over the final-hole kernel', 'Sec. 4.3(d)', '2.2e-6', EPs(10, '0.0003', '110', 2))
C('kd_pulse_eps_vs10_B003', 'pulse v_s=10, B=3e-3: excess over the final-hole kernel', 'Sec. 4.3(d)', '2.2e-4', EPs(10, '0.003', '150', 2))
C('kd_pulse_eps_vs10_mu', 'pulse v_s=10: eps/mu_f', 'Sec. 4.3(d)', '0.25', EPs(10, '0.003', '150', 3))
C('kd_pulse_v1', 'pulse v_s=10, B=3e-3: same excess at v1=110 and 150', 'Sec. 4.3(d)', '2.2e-4', EPs(10, '0.003', '110', 2))
C('kd_pulse_B2_vs60', 'eps/B^2 of the v_s=60 pulse at B=3e-4 against B=3e-3 (the text says: scale as B^2 to within 3 percent; the earlier text said "to three digits")', 'Sec. 4.3(d)', '3',
  X(lambda a, b: 100*abs(a/b - 1), EPs(60, '0.0003', '150', 4), EPs(60, '0.003', '150', 4)))   # the text prints 3% for 2.8%
C('kd_pulse_removes_35', 'replacing the static-hole kernel by the final-hole kernel removes (percent of the deviation), v_s=30, B=3e-3', 'Sec. 4.3(d)', '35',
  X(lambda s_, f_: 100*(1 - f_/s_), EPs(30, '0.003', '150', 1), EPs(30, '0.003', '150', 2)))
C('kd_pulse_static_coeff', 'static-hole kernel deviation of the v_s=30,60 pulses in units of mu_f (paper: 9.3 -> 6.0)', 'Sec. 4.3(d)', '9.3',
  X(lambda a, m, b, n: (a/m + b/n)/2, EPs(30, '0.003', '150', 1), EPs(30, '0.003', '150', 0), EPs(60, '0.003', '150', 1), EPs(60, '0.003', '150', 0)), 'abs:0.2', 'computed mean of the two pulses 9.17; the log prints 9.14 and 9.20')
C('kd_pulse_removes_93', 'same for v_s=10 (percent)', 'Sec. 4.3(d)', '93', X(lambda s_, f_: 100*(1 - f_/s_), EPs(10, '0.003', '150', 1), EPs(10, '0.003', '150', 2)))
C('kd_pulse_vs3', 'pulse at v_s=3 (B=3e-3 only): excess over the final-hole kernel', 'Sec. 4.3(d)', '-1.4e-2', EPs(3, '0.003', '110', 2))
C('kd_const_factor', 'matching factor constant in v between 250 and 290 to (bound 1e-3), all four B=0.03 tails', 'Sec. 4.3(d)', 1e-3, KP('final_kernel_spread_250_290_max_all'), 'le', 'bound quoted in the text')
# crossover (crossover_analytic.py, parsed in paper_numbers_kernel.py)
for k, vc, r100, kk in (('0.5', '200', '1.4', '1/2'), ('1.5', '310', '9.5', '3/2'), ('2.0', '370', '61', '2'), ('3.0', '500', '3.9e3', '3')):
    C('xo_vc_k%s' % k, 'crossover v at which phi_v is within 10%% of T(0) j(v), k=%s' % kk, 'Sec. 4.4', vc, KP('crossover_vc_k' + k))
    C('xo_ratio100_k%s' % k, 'phi_v/(T(0) j) at v=100, k=%s' % kk, 'Sec. 4.4', r100, KP('crossover_ratio_v100_k' + k), 'rel:0.04', 'the log prints three significant digits (1.43, 9.54, 60.94, 3899); the text rounds to two')
C('xo_exp150_k15', 'local exponent at v=150, k=3/2', 'Sec. 4.4', '5.55', KP('crossover_p_v150_k1.5'))
C('xo_exp300_k3', 'local exponent at v=300, k=3', 'Sec. 4.4', '14.1', KP('crossover_p_v300_k3.0'), 'abs:0.05', 'two-digit rounding of 14.06')
for k, p in (('1.5', '2.51'), ('2.0', '3.01'), ('3.0', '4.01')): C('xo_exp3000_k' + k, 'local exponent at v=3000, k=%s (-> k+1)' % k, 'Sec. 4.4', p, KP('crossover_p_v3000_k' + k))
for k, kk, p in (('0.5', '1/2', '160'), ('1.5', '3/2', '250'), ('2.0', '2', '290'), ('3.0', '3', '400')):
    C('xo_kv_k' + k, 'kappa_- v at the crossover, k=%s' % kk, 'Sec. 4.4', p, X(lambda k_, v: k_*v, V('static_hole', 'mN5_km'), KP('crossover_vc_k' + k)), 'abs:6', 'the text rounds kappa_- v to the nearest 10 (159, 247, 294, 398)')

# ---- Ori rate against the measured rate (Sec. 4.4)
C('ori_rate_pred', 'Ori rate kappa_-(mu_f) - 2 kappa_+ for k=3/2, B=0.03', 'Sec. 4.4', '0.6869',
  X(lambda km, kp: km - 2*kp, V('paper_numbers', 'T1_kappa_mu_f_B0.03_k1.5'), V('static_hole', 'mN5_kp')))
C('ori_rate_meas_60', 'measured rate of M at [60,64], k=3/2, tail only (B=0.03)', 'Sec. 4.4', '0.6868', F(RS, T2[1][1], WIN['60'], i=0))
C('ori_rate_meas_84', 'same at [84,88]', 'Sec. 4.4', '0.6911', F(RS, T2[1][1], WIN['84'], i=0))
C('ori_rate_meas_104', 'same at [104,108]', 'Sec. 4.4', '0.6947', F(RS, T2[1][1], WIN['104'], i=0))
C('ori_excess_sV', 'excess of |sigma_v| over kappa_-(mu_f) at [60,64] (k=3/2, B=0.03)', 'Sec. 4.4', '3.2e-3',
  X(lambda sv, km: sv - km, F(RS, T2[1][1], WIN['60'], i=-1), V('paper_numbers', 'T1_kappa_mu_f_B0.03_k1.5')), 'abs:5e-5', 'the table value |sigma_v| = 0.7880 is printed to 4 digits')
C('ori_dlnphi', 'd ln|phi_v|/dv at [60,64], k=3/2 tail only (from lambda and |sigma_v|)', 'Sec. 4.4', '-0.0504',
  X(lambda lam, sv: (lam - sv)/2, F(RS, T2[1][1], WIN['60'], i=1), F(RS, T2[1][1], WIN['60'], i=-1)), 'abs:5e-5', 'lambda and |sigma_v| are printed to 4 digits')
C('ori_dlnphi_minus_kp', 'departure of d ln|phi_v|/dv from -kappa_+', 'Sec. 4.4', '-1.4e-3',
  X(lambda lam, sv, kp: (lam - sv)/2 + kp, F(RS, T2[1][1], WIN['60'], i=1), F(RS, T2[1][1], WIN['60'], i=-1), V('static_hole', 'mN5_kp')), 'abs:1e-4', 'built from 4-digit table entries')
C('ori_dlnphi_contrib', 'its contribution to lambda (twice the departure)', 'Sec. 4.4', '-2.9e-3',
  X(lambda lam, sv, kp: (lam - sv) + 2*kp, F(RS, T2[1][1], WIN['60'], i=1), F(RS, T2[1][1], WIN['60'], i=-1), V('static_hole', 'mN5_kp')), 'abs:2e-4', 'built from 4-digit table entries')

# ---- long runs and Table 3 (longrun.py, kernel_analytic.py)
LR = R('results_longrun_v300.txt')
LRK = {'0.5': r'^gen_B0\.003_k0\.5_A0_U1_w0\.3_v300', '1.5': r'^gen_B0\.003_k1\.5_A0_U1_w0\.3_v300'}
T3 = [(100, '0.5', '0.02127', '2.15', '5.5e-5', '-1.3e-2'), (180, '0.5', '0.00941', '1.70', '2.1e-5', '-2.2e-3'), (290, '0.5', '0.00538', '1.57', '1.1e-5', '-4.5e-4'),
      (100, '1.5', '0.04588', '4.63', '5.9e-6', '-4.2e-2'), (140, '1.5', '0.03930', '5.54', '1.1e-6', '-4.3e-2'), (180, '1.5', '0.02755', '4.99', '2.9e-7', '-2.7e-2'),
      (220, '1.5', '0.01675', '3.70', '1.2e-7', '-1.1e-2'), (260, '1.5', '0.01133', '2.96', '7.0e-8', '-3.5e-3'), (290, '1.5', '0.00940', '2.74', '5.1e-8', '-1.6e-3')]
for v, k, r_, b_, s_, l_ in T3:
    t = 'T3_k%s_v%d_' % (k, v); loc = 'Table 3 (k=%s, v=%d)' % (k, v)
    row = (LRK[k], r'^\s+%d\s' % v)
    C(t + 'rate', '-d ln|phi_v|/dv, ' + loc, 'Table 3', r_, F(LR, *row, i=0))
    C(t + 'beta', 'beta (measured), ' + loc, 'Table 3', b_, F(LR, *row, i=2))
    C(t + 'beta_kernel', 'beta (kernel from the interior ODE), ' + loc, 'Table 3', b_, F(KA, r'^k=%s\s+v:' % k.replace('.', r'\.'), r'^\s+%d\s' % v, i=4))
    C(t + 'sV', '|sigma_v| - kappa_-(mu_f), ' + loc, 'Table 3', s_, F(LR, *row, i=3))
    C(t + 'lam', 'lambda - [kappa_- - 2(k+1)/(v+1)], ' + loc, 'Table 3', l_, F(LR, *row, i=7))
C('T3_km_k05', 'Table 3 caption: kappa_-(mu_f), k=1/2', 'Table 3', '0.795587', F(LR, LRK['0.5'] + r'.*kappa-\(mu_f\)=([0-9.]+)', g=1))
C('T3_km_k15', 'Table 3 caption: kappa_-(mu_f), k=3/2', 'Table 3', '0.795545', F(LR, LRK['1.5'] + r'.*kappa-\(mu_f\)=([0-9.]+)', g=1))
C('T3_km_static', 'Table 3 caption: static kappa_-', 'Table 3', '0.795649', V('static_hole', 'mN5_km'))
C('lr_mu_f_k05', 'long run k=1/2: mu_f (units 1e-5)', 'Sec. 4.4 (long runs)', '5.9', F(LR, LRK['0.5'] + r'.*mu_f=([0-9.e+-]+)', g=1, scale=1e5))
C('lr_mu_f_k15', 'long run k=3/2: mu_f (units 1e-5)', 'Sec. 4.4 (long runs)', '9.9', F(LR, LRK['1.5'] + r'.*mu_f=([0-9.e+-]+)', g=1, scale=1e5))
C('lr_levels_gap', 'two highest Romberg levels of phi_v agree at v=290, k=3/2', 'Sec. 4.4 (long runs)', '2.4e-3', KP('phi_levels_gap_k1.5_v290'))
C('lr_beta_above_k15', 'beta at v=290 above k+1 (percent), k=3/2', 'Sec. 4.4 (long runs)', '10',
  X(lambda b: 100*(b/2.5 - 1), F(LR, LRK['1.5'], r'^\s+290\s', i=2)), 'abs:1', 'the text quotes 2.74/2.5 - 1 = 9.6 percent as 10')
C('lr_beta_above_k05', 'beta at v=290 above k+1 (percent), k=1/2', 'Sec. 4.4 (long runs)', '5',
  X(lambda b: 100*(b/1.5 - 1), F(LR, LRK['0.5'], r'^\s+290\s', i=2)), 'abs:0.6', '1.567/1.5 - 1 = 4.5 percent, quoted as 5')
C('lr_sV_k05_v60', '|sigma_v| - kappa_-(mu_f) at v=60, k=1/2', 'Sec. 4.4 (long runs)', '1.1e-4', F(LR, LRK['0.5'], r'^\s+60\s', i=3))
C('lr_sV_k05_v290', 'same at v=290', 'Sec. 4.4 (long runs)', '1.1e-5', F(LR, LRK['0.5'], r'^\s+290\s', i=3))
C('lr_sV_k15_v60', 'same at v=60, k=3/2', 'Sec. 4.4 (long runs)', '3.2e-5', F(LR, LRK['1.5'], r'^\s+60\s', i=3))
C('lr_sV_k15_v290', 'same at v=290', 'Sec. 4.4 (long runs)', '5.1e-8', F(LR, LRK['1.5'], r'^\s+290\s', i=3))
C('lr_sV_k15_v290_lower', 'same, next-lower Romberg level', 'Sec. 4.4 (long runs)', '5.2e-8', F(LR, LRK['1.5'], r'^\s+290\s', i=4))
for k, kk, p in (('0.5', '1/2', '-6.8e-4'), ):
    pass
for v, p in ((100, '-6.8e-4'), (140, '-3.6e-4'), (290, '-5e-5')):
    C('lr_omit_k05_v%d' % v, 'omitted -lambda\'/lambda, k=1/2, v=%d' % v, 'Sec. 4.4 (long runs)', p, KP('omitted_lamprime_over_lam_k0.5_v%d' % v), None if v != 290 else 'abs:5e-6', None if v != 290 else 'one significant figure of 5.04e-5')
for v, p in ((100, '-3.2e-4'), (140, '-6.5e-4'), (180, '-8.7e-4'), (290, '-1.2e-4')):
    C('lr_omit_k15_v%d' % v, 'omitted -lambda\'/lambda, k=3/2, v=%d' % v, 'Sec. 4.4 (long runs)', p, KP('omitted_lamprime_over_lam_k1.5_v%d' % v))
C('lr_omit_frac_lo', 'omitted term as a share of the deficit at v=290, k=3/2 (percent)', 'Sec. 4.4 (long runs)', '8', KP('omitted_fraction_of_deficit_k1.5_v290_percent'), 'abs:0.5', 'quoted as "8-11%"; computed 7.6')
C('lr_omit_frac_hi', 'same, k=1/2', 'Sec. 4.4 (long runs)', '11', KP('omitted_fraction_of_deficit_k0.5_v290_percent'))
C('lr_twobeta', 'effective exponent of M at the flux level, 2 beta at v=290, k=3/2', 'Sec. 4.4 (long runs)', '5.5', X(lambda b: 2*b, F(LR, LRK['1.5'], r'^\s+290\s', i=2)), 'abs:0.05', '2 x 2.737 = 5.47')

# ---- Sec. 4.5: the conjecture near M* (kernel_general.py, m_N = 1.4)
M14 = R('results_mN1.4_tail250.txt'); A14 = r'^k=1\.5 B=0\.003 U=1\.0'
for v, p in ((40, '0.7'), (60, '0.3'), (80, '0.13'), (100, '0.1')):
    C('c14_ratio_v%d' % v, 'kernel prediction of the measured flux at v=%d, m_N=1.4 (percent)' % v, 'Sec. 4.5', p,
      X(lambda r: 100*abs(r - 1), F(M14, A14, r'^\s+%d\s+-' % v, i=2)), 'abs:0.06', 'the log prints the ratio to 4 digits (0.9932, 0.9974, 1.0013, 1.0011)')
C('c14_ratio_v120', 'kernel prediction of the measured flux for v>=120, m_N=1.4: largest deviation', 'Sec. 4.5', 4e-4,
  X(lambda *r: max(abs(x - 1) for x in r), *[F(M14, A14, r'^\s+%d\s+-' % v, i=2) for v in (120, 150, 180, 210, 240)]), 'le', 'bound quoted in the text (4e-4 or better)')
for v, lam, beta in ((40, '0.016', '3.0'), (100, '0.09', '3.7'), (240, '0.143', '2.53')):
    C('c14_lam_v%d' % v, 'flux-level rate lambda at v=%d, m_N=1.4' % v, 'Sec. 4.5', lam, F(M14, A14, r'^\s+%d\s+-' % v, i=4), None if v != 100 else 'abs:0.002', None if v != 100 else 'the log prints 0.0915; the text rounds to 0.09')
    C('c14_beta_v%d' % v, 'beta at v=%d, m_N=1.4' % v, 'Sec. 4.5', beta, F(M14, A14, r'^\s+%d\s+-' % v, i=3), None if v != 100 else 'abs:0.05', None if v != 100 else '3.66 rounded to 3.7')
C('c14_lam_neg', 'analytic lambda is negative only for v up to (zero crossing, linear interpolation between the printed v=10 and 15)', 'Sec. 4.5', '14',
  X(lambda b, d: 10 + 5*(-b)/(d - b), F(M14, r'^early windows', r'^\s+10\s', i=1), F(M14, r'^early windows', r'^\s+15\s', i=1)), 'abs:1', 'the text says v<~14; the printed windows give 14.6')
C('c14_R1_mN5', 'R_1 at m_N=5 (fit; compare 44.3)', 'Sec. 4.5', '0.644', F(TR5, r'^R1 \(difference.*\):'), 'abs:0.0005', 'rounded to 3 digits')
C('c14_Tstatic_mN5', 'T(0) at m_N=5', 'Sec. 4.5', '44.3', V('static_hole', 'mN5_T0'))

# ---- Sec. 4.7: the Ori shell model with the filtered flux (shell_kernel.py, flux_nl.py)
SK = R('results_shell_kernel.txt')
SKH = {'3/2': r'^k=1\.5 B=0\.03\s+windows', '1/2': r'^k=0\.5 B=0\.03\s+windows'}
SKR = (('PDE', r'^\s+PDE \(Romberg M\)'), ('shell', r'^\s+shell, kernel-filtered'), ('shellx', r'^\s+shell\(filtered\) \+ \[\|sigma_v\| - kappa_-\(mu_f\)\] \(measured\)'),
       ('power', r'^\s+power-law formula .* at window mid'), ('excess', r'^\s+\|sigma_v\|-kappa_-\(mu_f\) \(PDE, U=1, window mean\)'))
def SKF(k, row, j): return F(SK, SKH[k], dict(SKR)[row], i=j)
TAB = {'3/2': {'PDE': ('0.6868', '0.6892', '0.6911', '0.6931', '0.6947'), 'shell': ('0.6832', '0.6867', '0.6891', '0.6914', '0.6930'), 'shellx': ('0.6864', '0.6886', '0.6903', '0.6921', '0.6935'), 'power': ('0.7055', '0.7182', '0.7273', '0.7343', '0.7381')},
       '1/2': {'PDE': ('0.7338', '0.7400', '0.7457', '0.7510', '0.7543'), 'shell': ('0.7213', '0.7298', '0.7375', '0.7444', '0.7486'), 'shellx': ('0.7328', '0.7391', '0.7449', '0.7504', '0.7538'), 'power': ('0.7417', '0.7493', '0.7548', '0.7590', '0.7613')}}
VW = (60, 72, 84, 96, 104)
for k in ('3/2', '1/2'):
    for row, lab in (('PDE', 'PDE'), ('shell', 'shell, filtered flux'), ('shellx', 'shell + (|sigma_v| - kappa_-(mu_f))'), ('power', 'power law kappa_- - (2k+2)/(v+1)')):
        for j, v in enumerate(VW):
            C('T4s_k%s_%s_v%d' % (k.replace('/', ''), row, v), 'shell table, k=%s, %s, window at v=%d' % (k, lab, v), 'Sec. 4.7 table', TAB[k][row][j], SKF(k, row, j))
for k, ex in (('3/2', ('3.2e-3', '2.0e-3', '1.2e-3', '0.7e-3', '0.5e-3')), ('1/2', ('11.5e-3', '9.3e-3', '7.4e-3', '6.0e-3', '5.2e-3'))):
    for j, (v, p) in enumerate(zip(VW, ex)):
        C('T4s_excess_k%s_v%d' % (k.replace('/', ''), v), '|sigma_v| - kappa_-(mu_f) of the PDE, k=%s, window at v=%d' % (k, v), 'Sec. 4.7', p, SKF(k, 'excess', j))
def _maxdiff(*a):
    n = len(a)//2
    return max(abs(x - y) for x, y in zip(a[:n], a[n:]))
for k in ('3/2', '1/2'):
    C('T4s_agree_%s' % k.replace('/', ''), 'shell + excess against the PDE rate, largest difference over the five windows, k=%s' % k, 'Sec. 4.7', 1.2e-3,
      X(_maxdiff, *[SKF(k, 'shellx', j) for j in range(5)], *[SKF(k, 'PDE', j) for j in range(5)]), 'le', 'bound quoted in the text (1.2e-3 or better)')
C('T4s_agree_pct', 'same, as a fraction of the rate (percent, at most)', 'Sec. 4.7', '0.17',
  X(lambda *a: 100*max(abs(x - y)/y for x, y in zip(a[:10], a[10:])), *[SKF(k, 'shellx', j) for k in ('3/2', '1/2') for j in range(5)], *[SKF(k, 'PDE', j) for k in ('3/2', '1/2') for j in range(5)]))
C('T4s_power_k32_lo', 'power-law input against the PDE, k=3/2: smallest misfit', 'Sec. 4.7', '1.9e-2', X(lambda *a: min(abs(x - y) for x, y in zip(a[:5], a[5:])), *[SKF('3/2', 'power', j) for j in range(5)], *[SKF('3/2', 'PDE', j) for j in range(5)]))
C('T4s_power_k32_hi', 'same: largest misfit', 'Sec. 4.7', '4.3e-2', X(lambda *a: max(abs(x - y) for x, y in zip(a[:5], a[5:])), *[SKF('3/2', 'power', j) for j in range(5)], *[SKF('3/2', 'PDE', j) for j in range(5)]))
C('T4s_power_k12_lo', 'power-law input against the PDE, k=1/2: smallest misfit', 'Sec. 4.7', '0.7e-2', X(lambda *a: min(abs(x - y) for x, y in zip(a[:5], a[5:])), *[SKF('1/2', 'power', j) for j in range(5)], *[SKF('1/2', 'PDE', j) for j in range(5)]), 'abs:5e-4', 'one significant figure (0.0070)')
C('T4s_power_k12_hi', 'same: largest misfit', 'Sec. 4.7', '0.9e-2', X(lambda *a: max(abs(x - y) for x, y in zip(a[:5], a[5:])), *[SKF('1/2', 'power', j) for j in range(5)], *[SKF('1/2', 'PDE', j) for j in range(5)]), 'abs:5e-4', 'one significant figure (0.0093)')
for v, j, ps, pp in ((60, 0, '1.25e-2', '0.8e-2'), (72, 1, '1.0e-2', '0.9e-2')):
    C('T4s_ex_shell_v%d' % v, 'k=1/2 without the measured excess: |shell - PDE| at v=%d' % v, 'Sec. 4.7', ps, X(lambda a, b: abs(a - b), SKF('1/2', 'shell', j), SKF('1/2', 'PDE', j)), 'abs:6e-4', 'rate columns are printed to 4 digits; 0.0125 and 0.0102')
    C('T4s_ex_power_v%d' % v, 'k=1/2: |power law - PDE| at v=%d' % v, 'Sec. 4.7', pp, X(lambda a, b: abs(a - b), SKF('1/2', 'power', j), SKF('1/2', 'PDE', j)), 'abs:6e-4', 'one significant figure')
C('T4s_k12_better_84', 'k=1/2 without the excess the filtered shell beats the power law from v=84 (|shell-PDE| < |power-PDE|), all of 84, 96, 104', 'Sec. 4.7', 1,
  X(lambda *a: float(all(abs(a[j] - a[10+j]) < abs(a[5+j] - a[10+j]) for j in (2, 3, 4))), *[SKF('1/2', 'shell', j) for j in range(5)], *[SKF('1/2', 'power', j) for j in range(5)], *[SKF('1/2', 'PDE', j) for j in range(5)]), 'eq', 'boolean statement')
FN = R('results_flux_nl.txt')
C('fnl_ratio', 'measured phi_v at B=0.03 over the linear one: range of the printed ratios (1.033-1.042)', 'Sec. 4.7', '1.04', KP('flux_nl_ratio_max'), 'abs:0.005', 'ratios 1.0329 to 1.0419 quoted as 1.04')
C('fnl_exponent', 'same exponents to', 'Sec. 4.7', '0.06', KP('flux_nl_exponent_max_dev'))
C('fnl_expo_effect', 'a change of 0.06 in the local exponent changes 2 beta/(v+1) by (at v = 100)', 'Sec. 4.7', '1.2e-3', X(lambda d: 2*d/101, KP('flux_nl_exponent_max_dev')))

# =====================================================================================================================================
# Sec. 5: exact integration along the ray (ray_mass.py, ray_stability.py, ray_long.py, e13_*.py, ray_extend.py, ray_rate_only.py)
# =====================================================================================================================================
RY = lambda n, a=False: V('paper_numbers_ray', n, a=a)
RMF = {'1.5': R('results_ray_mass_B0.03_k1.5.txt'), '0.5': R('results_ray_mass_B0.03_k0.5.txt')}
# --- test against the extrapolated PDE
C('ray_A_k15', 'max |M_ODE/M_PDE - 1| over v0 < v <= 108, tail k=3/2, B=0.03, v0 = 48, 60, 72, 84', 'Sec. 5', '6.1e-5', RY('rm_B0.03_k1.5_A_maxdev'))
C('ray_A_k05', 'same, k=1/2', 'Sec. 5', '2.1e-6', RY('rm_B0.03_k0.5_A_maxdev'))
C('ray_A_v0_indep', 'the maximum is the same for the four starting points (spread of the four maxima)', 'Sec. 5', 0, RY('rm_B0.03_k1.5_A_spread_over_v0'), 'eq', 'the printed maxima are identical to two digits')
for k, kk, m1, m2 in (('1.5', '3/2', '1.2', '6.6e17'), ('0.5', '1/2', '5.6', '1.1e20')):
    C('ray_A_growth_lo_k' + k, 'M_PDE at v0=48, k=%s' % kk, 'Sec. 5', m1, F(RMF[k], r'^\s+v0=48\s+M_ext\(v0\)='), None if k == '1.5' else 'abs:0.05', None if k == '1.5' else '5.62 rounds to 5.6')
    C('ray_A_growth_hi_k' + k, 'M_PDE at v=108, k=%s' % kk, 'Sec. 5', m2, F(RMF[k], r'^\s+v0=48\s+M_ext\(v0\)=\S+\s+M_ext\(108\)=([0-9.e+]+)', g=1))
C('ray_A_levels_s_v100', 'sigma_v: two highest Romberg levels agree at v=100 (k=3/2, relative)', 'Sec. 5', '2e-13', F(R('results_ray_long_B0.03_k1.5.txt'), r'^\(a\) PDE', r'^\s+100\s', i=5))
C('ray_A_levels_phi_v100', 'phi_v: same', 'Sec. 5', '3e-11', F(R('results_ray_long_B0.03_k1.5.txt'), r'^\(a\) PDE', r'^\s+100\s', i=6))
C('ray_A_levels_M', 'level spread of M_PDE (v <= 108)', 'Sec. 5', '1e-7', X(max, *[F(RMF['1.5'], r'^\[B\]', r'^\s+%d\s' % v, i=2) for v in (84, 100, 108)]), 'abs:2e-8', 'quoted to one significant figure: the printed spreads are 3.3e-8, 7.4e-8, 1.1e-7')
C('ray_A_underestimate_k15', 'M_PDE error divided by the level spread over the rows of Table 4 (smallest over k=3/2 and 1/2; the text says: at least 8 at the v of Table 4; an earlier version said 10^2-10^3 at every v)', 'Sec. 5 and Fig. 4 caption', '8',
  X(min, RY('rm_B0.03_k1.5_B_min_dev_over_levels_table'), RY('rm_B0.03_k0.5_B_min_dev_over_levels_table')), 'ge', 'lower bound quoted in the text, for the rows of Table 4 only (all integer v: see rr_* below)')
C('ray_A_underestimate_max', 'same, largest ratio over the rows', 'Sec. 5 (not quoted in the current text; kept as a record of the earlier "10^2-10^3")', '1000', X(max, RY('rm_B0.03_k1.5_B_max_dev_over_levels_table'), RY('rm_B0.03_k0.5_B_max_dev_over_levels_table')), 'le', 'upper end 10^3 of the earlier range (computed 554)')
# --- Table 4
T4 = {'1.5': [(108, '6.58e17', '1.1e-7', '+1.9e-5', '0.69513', '9.78'), (140, '3.50e27', '4.1e-7', '+1.0e-4', '0.70565', '11.16'), (180, '9.81e39', '2.3e-5', '-2.6e-3', '0.72870', '10.16'),
             (240, '2.47e59', '8.0e-5', '+2.9e-2', None, None), (290, '9.8e75', '2.3e-3', '-6.6e-2', '0.76587', '5.51')],
      '0.5': [(108, '1.06e20', '4.2e-9', '-1.2e-6', '0.75508', '3.73'), (140, '3.93e30', '8.5e-9', '+7e-8', '0.76533', '3.38'), (180, '9.10e43', '1.3e-8', '+7.2e-6', '0.77250', '3.04'),
             (240, '1.45e64', '1.1e-7', '-1.2e-5', None, None), (290, '1.17e81', '4.4e-7', '-6.6e-6', '0.77959', '2.83')]}
for k, rows in T4.items():
    for v, M_, lv, dv, rt, qm in rows:
        t = 'T4_k%s_v%d_' % (k, v); rowB = (r'^\[B\]', r'^\s+%d\s' % v); rowC = (r'^\[C\]', r'^\s+%d\s' % v)
        C(t + 'M', 'Table 4 (k=%s) M_PDE at v=%d' % (k, v), 'Table 4', M_, F(RMF[k], *rowB, i=1))
        C(t + 'levels', 'Table 4 (k=%s) Romberg levels at v=%d' % (k, v), 'Table 4', lv, F(RMF[k], *rowB, i=2))
        C(t + 'dev', 'Table 4 (k=%s) M_ODE/M_PDE - 1 at v=%d' % (k, v), 'Table 4', dv, F(RMF[k], *rowB, i=3))
        if rt:
            C(t + 'rate', 'Table 4 (k=%s) rate_ODE at v=%d' % (k, v), 'Table 4', rt, F(RMF[k], *rowC, i=0))
            C(t + 'qM', 'Table 4 (k=%s) q_M at v=%d' % (k, v), 'Table 4', qm, F(RMF[k], *rowC, i=-1))
# --- beyond v = 110: which mass is converged
RM3 = R('results_ray_mass_B0.003_k1.5.txt'); RM3h = R('results_ray_mass_B0.003_k0.5.txt')
C('ray_b_k05_agree', 'k=1/2, B=0.03: ODE and PDE mass agree up to v=290 to', 'Sec. 5', '1.2e-5', RY('rm_B0.03_k0.5_B_maxabsdev_to290'))
C('ray_b_k05_lnM', 'ln M at v=290, k=1/2, B=0.03', 'Sec. 5', '186.7', RY('rm_B0.03_k0.5_lnM_ode_v290'))
for v, d, sp in ((84, '9e-6', '3e-8'), (180, '2.6e-3', '2e-5'), (290, '7e-2', '2e-3')):
    C('ray_b_k15_dev_v%d' % v, 'k=3/2, B=0.03: |M_ODE/M_PDE - 1| at v=%d' % v, 'Sec. 5', d, F(RMF['1.5'], r'^\[B\]', r'^\s+%d\s' % v, i=3, a=True))
    C('ray_b_k15_spread_v%d' % v, 'k=3/2, B=0.03: spread of the two highest Romberg levels at v=%d' % v, 'Sec. 5', sp, F(RMF['1.5'], r'^\[B\]', r'^\s+%d\s' % v, i=2))
STB = 'rs_B0.03_k1.5_'
C('ray_stab_finest4', 'ln M_ODE changes by at most (four finest grids), k=3/2, B=0.03, 84<=v<=290', 'Sec. 5', '2e-8', RY(STB + 'ode_max_finest4'))
C('ray_stab_coarsest4', 'same, four coarsest grids', 'Sec. 5', '5e-6', RY(STB + 'ode_max_coarsest4'))
C('ray_stab_finest3', 'same, three finest grids', 'Sec. 5', '1.2e-6', RY(STB + 'ode_max_finest3'))
C('ray_stab_pde_v140', 'extrapolated PDE ln M changes by (v=140), k=3/2', 'Sec. 5', '1e-4', RY(STB + 'pde_change_v140'), 'abs:5e-5', 'one significant figure (1.2e-4)')
C('ray_stab_pde_v290_lo', 'extrapolated PDE ln M changes at v=290 from one subset to another: smallest', 'Sec. 5', '0.07', RY(STB + 'pde_abs_v290_min'))
C('ray_stab_pde_v290_hi', 'same: largest', 'Sec. 5', '0.6', RY(STB + 'pde_abs_v290_max'), 'abs:0.05', 'one significant figure (0.56)')
C('ray_stab_k05_ode', 'k=1/2: ODE ln M changes by at most (both amplitudes)', 'Sec. 5', '1.4e-7', X(max, RY('rs_B0.03_k0.5_ode_max_all_subsets'), RY('rs_B0.003_k0.5_ode_max_all_subsets')))
C('ray_stab_k05_pde003', 'k=1/2, B=0.03: PDE mass changes by up to', 'Sec. 5', '1e-4', RY('rs_B0.03_k0.5_pde_change_max'), 'abs:5e-5', 'one significant figure (1.2e-4)')
C('ray_stab_k05_pde0003', 'k=1/2, B=0.003: PDE mass changes by up to', 'Sec. 5', '0.2', RY('rs_B0.003_k0.5_pde_change_max'), 'abs:0.05', 'one significant figure (0.22)')
C('ray_stab_converged', 'ray-integrated mass converged in the grid in ln M over the whole range (all runs and subsets), at most', 'Sec. 5', 1e-5,
  X(max, RY('rs_B0.03_k1.5_ode_max_all_subsets'), RY('rs_B0.003_k1.5_ode_max_all_subsets'), RY('rs_B0.03_k0.5_ode_max_all_subsets'), RY('rs_B0.003_k0.5_ode_max_all_subsets')), 'le', 'bound quoted in the text')
C('ray_levels_sV', 'sigma_v: two highest Romberg levels agree to (relative, v<=290, k=3/2 B=0.03)', 'Sec. 5', '2e-13', RY('rl_B0.03_k1.5_levels_sV_max'))
C('ray_levels_phiv', 'phi_v: same', 'Sec. 5', '1.2e-8', RY('rl_B0.03_k1.5_levels_PV_max'))
C('ray_rate_exact', 'ODE rate against 4 pi r phi_v^2/rho, k=3/2, B=0.03, v>=84', 'Sec. 5', '5e-6', RY('rm_B0.03_k1.5_C_ode_vs_exact_max'))
C('ray_rate_lamlam_k15', 'ODE rate against lambda - lambda\'/lambda, k=3/2', 'Sec. 5', '2e-5', RY('rm_B0.03_k1.5_C_ode_vs_lamlam_max'))
C('ray_rate_lamlam_k05', 'same, k=1/2', 'Sec. 5', '4e-5', RY('rm_B0.03_k0.5_C_ode_vs_lamlam_max'))
# --- which factor carries the error (e13_errconst.py)
EC = 'ec_B0.03_k1.5_'; ECh = 'ec_B0.03_k0.5_'
C('ec_hratio', 'ratio of the errors of the two finest grids, every v listed', 'Sec. 5', '4.00', X(lambda a, b: min(a, b), RY(EC + 'hratio_min'), RY(ECh + 'hratio_min')))
for v, a, b in ((40, '-1.8e2', '-87'), (60, '-2.0e3', '-4.4e2'), (100, '-9.2e4', '-4.0e3')):
    C('ec_Crho_k15_v%d' % v, 'C_rho at v=%d, k=3/2, B=0.03' % v, 'Sec. 5', a, RY(EC + 'Crho_v%d' % v))
    C('ec_Crho_k05_v%d' % v, 'C_rho at v=%d, k=1/2, B=0.03' % v, 'Sec. 5', b, RY(ECh + 'Crho_v%d' % v))
C('ec_dlnC_k15', 'C_rho grows like exp(x v) at v ~ 100, k=3/2: x', 'Sec. 5', '0.09', RY(EC + 'dlnC_v100'))
C('ec_dlnC_k05', 'same, k=1/2', 'Sec. 5', '0.05', RY(ECh + 'dlnC_v100'))
C('ec_Cy_k15_lo', 'C_y range over v=40..100, k=3/2: smallest (abs)', 'Sec. 5', '70', RY(EC + 'Cy_min_v40_100'))
C('ec_Cy_k15_hi', 'same: largest', 'Sec. 5', '77', RY(EC + 'Cy_max_v40_100'), 'abs:0.6', '76.5 rounded to 77')
C('ec_Cy_k05_lo', 'C_y range, k=1/2: smallest', 'Sec. 5', '37', RY(ECh + 'Cy_min_v40_100'))
C('ec_Cy_k05_hi', 'same: largest', 'Sec. 5', '40', RY(ECh + 'Cy_max_v40_100'), 'abs:0.6', '40.5 rounded to 40')
for v, p in ((40, '0.2'), (60, '1.9'), (100, '90')):
    C('ec_rho_err_v%d' % v, 'relative error of the evolved rho at h=0.003125, v=%d (percent), k=3/2' % v, 'Sec. 5', p, RY(EC + 'rho_err_percent_v%d' % v), None if v != 40 else 'abs:0.03', None if v != 40 else '0.18 rounded to 0.2')
C('ec_y_err', 'relative error of y at h=0.003125 (percent)', 'Sec. 5', '0.07', RY(EC + 'Cy_err_percent'))
C('ec_Cy_B0003', 'C_y at B=0.003, v=60', 'Sec. 5', '-8.3e3', RY('ec_B0.003_k1.5_Cy_v60'))
C('ec_Cy_B2', 'C_y(B=0.003)/C_y(B=0.03) against B^-2 (percent deviation, "up to 10%")', 'Sec. 5', '10', RY('ec_Cy_ratio_B0003_to_B003_k1.5_percent_v60'), 'abs:0.5', '10.4 percent')
C('ec_Crho_B0003', 'C_rho at B=0.003, v=60', 'Sec. 5', '-2.1e5', RY('ec_B0.003_k1.5_Crho_v60'))
# --- constraint-projected mass (Table 5, e13_table.py, e13_all.py, e13_v0.py)
E13 = ('B0.03_k0.5', 'B0.03_k1.5', 'B0.03_k2', 'B0.03_k3', 'B0.003_k0.5', 'B0.003_k1.5')
T5 = (('B0.03_k0.5', ('-1.3e-9', '-1.0e-9', '+6.3e-9', '+2.2e-9'), '1.4e-8', '3.6e-10', '360', '179', '2.5e-6'),
      ('B0.03_k1.5', ('+1.9e-10', '-3.6e-9', '-9.2e-9', '-3.3e-7'), '3.3e-7', '1.2e-8', '337', '167', '1.1e-5'),
      ('B0.03_k2', ('-5.8e-9', '-9.7e-9', '-1.4e-8', '-1.1e-6'), '1.1e-6', '1.1e-7', '327', '162', '1.3e-5'),
      ('B0.03_k3', ('+7.7e-10', '-3.0e-9', '+1.3e-8', '-1.4e-6'), '1.4e-6', '7.8e-7', '319', '158', '1.4e-5'),
      ('B0.003_k0.5', ('+3.7e-8', '+3.1e-8', '+2.6e-8', '+1.6e-8'), '3.7e-8', '1.3e-10', '343', '170', '2.0e-4'),
      ('B0.003_k1.5', ('-9.8e-8', '-9.9e-8', '-4.5e-7', '-2.3e-6'), '2.3e-6', '4.5e-9', '323', '161', '7.6e-4'))
for tag, d4, mx, sp, lk, lm, u3 in T5:
    for v, p in zip((84, 140, 200, 280), d4):
        C('T5_%s_v%d' % (tag, v), 'Table 5 %s: ln M_cc - ln M_ODE at v=%d' % (tag, v), 'Table 5', p, V('e13_table', 'e13_%s_dlnM_v%d' % (tag, v)))
    C('T5_%s_max' % tag, 'Table 5 %s: max |Delta ln M| over 84<=v<=280' % tag, 'Table 5 and Result paragraph', mx, V('e13_table', 'e13_%s_max_dlnM' % tag, a=True))
    C('T5_%s_spread' % tag, 'Table 5 %s: spread of ln M_cc, four finest grids' % tag, 'Table 5 and Result paragraph', sp, V('e13_table', 'e13_%s_spread_4finest' % tag, a=True))
    C('T5_%s_lnK' % tag, 'Table 5 %s: ln K bound at v=280' % tag, 'Table 5', lk, V('e13_table', 'e13_%s_lnK_v280' % tag))
    C('T5_%s_lnM280' % tag, 'Table 5 caption: ln M_ODE(v=280), %s' % tag, 'Table 5 caption', lm, V('e13_table', 'e13_%s_lnM_ODE_v280' % tag), 'abs:0.5', 'rounded to integers (the value 160.5 is printed to 0.1)')
    C('T5_%s_U03' % tag, 'Table 5 caption: max |Delta ln M| on U=0.3, %s' % tag, 'Table 5 caption', u3, V('e13_table', 'e13_%s_max_dlnM_U0.3' % tag, a=True))
for v, p in ((84, '24'), (140, '63'), (200, '107')):
    C('T5_lnM_B003k15_v%d' % v, 'Table 5 caption: ln M_ODE(v=%d), k=3/2, B=0.03' % v, 'Table 5 caption', p, V('e13_table', 'e13_B0.03_k1.5_lnM_ODE_v%d' % v), 'abs:0.5', 'rounded to integers')
C('e13_growth_lo', 'growth of M over the six runs: smallest ln M_ODE(280) -> decimal exponent', 'Result paragraph', '69', X(lambda *a: min(a)/2.302585, *[V('e13_table', 'e13_%s_lnM_ODE_v280' % t) for t in E13]), 'abs:0.5', 'e^158 = 10^68.6')
C('e13_growth_hi', 'same, largest', 'Result paragraph', '78', X(lambda *a: max(a)/2.302585, *[V('e13_table', 'e13_%s_lnM_ODE_v280' % t) for t in E13]), 'abs:0.5', 'e^179 = 10^77.7')
C('e13_le160', 'B=0.003, k=3/2: |Delta ln M| <= 1e-7 for v <= 160', 'Result paragraph', 1e-7, RY('e13_B0.003_k1.5_U1_dlnM_max_to160'), 'le', 'bound quoted in the text')
C('e13_dsigma_003', 'implied extrapolation error of sigma_v for B=0.03 (max |Delta ln M|/220, k=3/2)', 'Result paragraph', '1.5e-9', X(lambda d: d/220, V('e13_table', 'e13_B0.03_k1.5_max_dlnM', a=True)))
C('e13_dsigma_0003', 'same for B=0.003 (k=3/2)', 'Result paragraph', '1e-8', X(lambda d: d/220, V('e13_table', 'e13_B0.003_k1.5_max_dlnM', a=True)), 'abs:1e-9', 'one significant figure (1.07e-8)')
C('e13_sV_levels_quote', 'level spread of sigma_v at the printed v (the earlier text quoted 1.2e-8, which is the spread of phi_v; every integer v: rr_B0.03_k1.5_levels_sV below)', 'Result paragraph', '2e-13', RY('rl_B0.03_k1.5_levels_sV_max'))
C('e13_levels_I_200', 'Romberg levels of the profile integral agree to (v<=200, relative, all runs)', 'Sec. 5', 2e-9, RY('e13all_I_levels_max_to200'), 'le', 'bound quoted in the text')
C('e13_levels_I_280', 'same up to v=280', 'Sec. 5', '8.3e-9', RY('e13all_I_levels_max_to280'))   # was the bound 8e-9
C('e13_v0_change', 'starting at v0 = 48..84 changes ln M_cc by (v=100, 200, 280; B=0.03, k=3/2)', 'Sec. 5', 1e-10, V('e13_v0', 'e13_v0_max_change'), 'le', 'bound quoted in the text')
C('e13_U03_B0003', 'on U=0.3 the ODE calibrated on the evolved y is off by (B=0.003, k=3/2)', 'Result paragraph', '7.6e-4', V('e13_table', 'e13_B0.003_k1.5_max_dlnM_U0.3', a=True))
C('e13_U03_B003', 'same at B=0.03', 'Result paragraph', '1.1e-5', V('e13_table', 'e13_B0.03_k1.5_max_dlnM_U0.3', a=True))
C('e13_pde_wrong', 'evolved PDE mass wrong at v=290 (B=0.03, k=3/2)', 'Result paragraph', '7e-2', RY('rm_B0.03_k1.5_B_maxabsdev_to290'), 'abs:0.005', 'one significant figure (6.6e-2)')
C('e13_M_v0_B0003', 'M(v0=60) at B=0.003, k=3/2 (marginal)', 'Caveats', '0.85', F(RM3, r'^\s+v0=60\s+M_ext\(v0\)='))
# --- the tail exponent in M (Table 4 [C])
def QM(k, v): return F(RMF[k], r'^\[C\]', r'^\s+%d\s' % v, i=-1)
C('qM_k15_v140', 'q_M at v=140, k=3/2', 'Sec. 5 (tail exponent)', '11.2', QM('1.5', 140))
C('qM_k15_v260', 'q_M at v=260, k=3/2', 'Sec. 5 (tail exponent)', '5.99', QM('1.5', 260))
C('qM_k15_v290', 'q_M at v=290, k=3/2', 'Sec. 5 (tail exponent)', '5.51', QM('1.5', 290))
C('qM_k05_v84', 'q_M at v=84, k=1/2', 'Sec. 5 (tail exponent)', '3.79', QM('0.5', 84))
C('qM_k05_v290', 'q_M at v=290, k=1/2', 'Sec. 5 (tail exponent)', '2.83', QM('0.5', 290))
C('qM_k05_excess', '|sigma_v| - kappa_-(mu_f) at v=290, k=1/2', 'Sec. 5 (tail exponent)', '1.1e-3', F(RMF['0.5'], r'^\[C\]', r'^\s+290\s', i=3))
C('qM_k05_contrib', '-(|sigma_v| - kappa_-)(v+1) at v=290, k=1/2', 'Sec. 5 (tail exponent)', '-0.32', X(lambda e: -e*291, F(RMF['0.5'], r'^\[C\]', r'^\s+290\s', i=3)))
# --- kernel-driven extension (ray_extend.py, results_ray_extend_*.txt)
XT = {t: R('results_ray_extend_%s.txt' % t) for t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5')}
XD = lambda B, k: R('results_ray_extend_ext_def_B%s_k%s.txt' % (B, k)); XM = lambda B, k: R('results_ray_extend_ext_mu_B%s_k%s.txt' % (B, k))
def XR(fn, v, col): return F(fn, r'^\s+v\s+ln M', r'^\s+%d\s' % v, i=col)
C('ext_eb_k05', 'excess |sigma_v| - kappa_- at v_b = 250, k=1/2, B=0.03', 'Sec. 5 (extension)', '1.4e-3', F(XT['B0.03_k0.5'], r'^excess \|sV\|-km at v_b=([0-9.e+-]+)', g=1))
C('ext_eb_k15', 'same, k=3/2', 'Sec. 5 (extension)', '8.3e-6', F(XT['B0.03_k1.5'], r'^excess \|sV\|-km at v_b=([0-9.e+-]+)', g=1))
C('ext_q_k05', 'fitted power q of the excess, k=1/2', 'Sec. 5 (extension)', '1.48', F(XT['B0.03_k0.5'], r'^excess .*fitted power q=([0-9.]+)', g=1))
C('ext_q_k15', 'same, k=3/2', 'Sec. 5 (extension)', '4.42', F(XT['B0.03_k1.5'], r'^excess .*fitted power q=([0-9.]+)', g=1))
C('ext_rb', 'calibration factor r_b = PDE/kernel flux at v_b = 250 (static-hole kernel), k=3/2, B=0.03', 'Sec. 5 (extension)', '1.035', F(XT['B0.03_k1.5'], r'^PDE/kernel phi_v ratio at v_b:'), 'abs:0.0005', '1.0354 rounded to 1.035')
for k, p in (('1.5', '1.0067'), ('0.5', '1.0188')):
    C('ext_rb_final_k' + k, 'r_b with the kernel of the final hole, k=%s, B=0.03' % k, 'Sec. 5 (extension)', p, F(XM('0.03', k), r'^PDE/kernel phi_v ratio at v_b:'))
for k, p in (('2', '1.0058'), ('3', '1.0055')):
    C('ext_rb_final_k' + k, 'r_b with the kernel of the final hole, k=%s, B=0.03' % k, 'Sec. 5 (extension)', p, F(XM('0.03', k), r'^PDE/kernel phi_v ratio at v_b:'))
C('ext_final_effect', 'the final-hole kernel changes ln M(v=2500) by at most (all four tails, B=0.03)', 'Sec. 5 (extension)', '0.05', X(lambda *a: max(abs(x) for x in a), *[RY('ex_B0.03_k%s_mu_minus_def_lnM_v2500' % k) for k in ('0.5', '1.5', '2', '3')]), 'abs:0.002', 'computed 0.051')
C('ext_cmp_k15', 'kernel-driven against PDE-driven ln M at v=290, k=3/2, B=0.03 (174.908 against 174.906)', 'Sec. 5 (extension)', '1.5e-3', RY('ex_gen2_B0.03_k1.5_kernel_minus_pde_lnM_v290'), 'abs:6e-4', 'both ln M are printed to 3 decimals')
C('ext_cmp_k05', 'same, k=1/2', 'Sec. 5 (extension)', '2e-4', RY('ex_gen2_B0.03_k0.5_kernel_minus_pde_lnM_v290'), 'abs:5e-4', 'both ln M are printed to 3 decimals (difference below the printing)')
for k, rows in (('1.5', ((290, '174.91', '5.51'), (400, '259.55', '5.175'), (1000, '725.77', '5.058'), (2000, '1507.10', '5.028'), (2500, '1898.39', '5.022'))),
                ('0.5', ((290, '186.67', '2.83'), (400, '272.59', '2.82'), (1000, '743.57', '2.86'), (2000, '1530.87', '2.89'), (2500, '1924.88', '2.90')))):
    for v, lm, qm in rows:
        C('ext_tab_lnM_k%s_v%d' % (k, v), 'extension table ln M, k=%s, v=%d' % (k, v), 'Sec. 5 (extension table)', lm, XR(XT['B0.03_k' + k], v, 0))
        C('ext_tab_q_k%s_v%d' % (k, v), 'extension table q_M, k=%s, v=%d' % (k, v), 'Sec. 5 (extension table)', qm, XR(XT['B0.03_k' + k], v, 2))
C('ext_C_2500', 'ln M - kappa_- v + 5 ln(v+1) at v=2500, k=3/2', 'Sec. 5 (extension)', '-24.541', XR(XT['B0.03_k1.5'], 2500, 3))
C('ext_C_change', 'its change between v=2000 and 2500', 'Sec. 5 (extension)', '5e-3', X(lambda a, b: abs(a - b), XR(XT['B0.03_k1.5'], 2500, 3), XR(XT['B0.03_k1.5'], 2000, 3)))
C('ext_treat_k15', 'the three treatments of the excess differ by at most (ln M, v=2500, k=3/2)', 'Sec. 5 (extension)', '0.02', X(lambda a, b: max(abs(a), abs(b)), XR(XT['B0.03_k1.5'], 2500, 4), XR(XT['B0.03_k1.5'], 2500, 5)), 'abs:0.005', '0.018 rounded to 0.02')
C('ext_k05_zero', 'k=1/2: treatment e=0 against the power-law treatment, ln M at v=2500', 'Sec. 5 (extension)', '-0.48', XR(XT['B0.03_k0.5'], 2500, 4))
C('ext_k05_const', 'k=1/2: treatment e=e(v_b) held, ln M at v=2500', 'Sec. 5 (extension)', '+2.6', XR(XT['B0.03_k0.5'], 2500, 5))
C('ext_k05_q2500', 'k=1/2: q_M at v=2500 (still rising)', 'Sec. 5 (extension)', '2.90', XR(XT['B0.03_k0.5'], 2500, 2))
C('ext_k05_rate_change', 'k=1/2: the three treatments change the rate by at most (finite differences of the printed treatment columns, v>=1000)', 'Sec. 5 (extension)', '1.4e-3',
  X(lambda *a: max(abs((a[i+1] - a[i])/dv) for i, dv in ((0, 500), (1, 500), (2, 500))) , *[XR(XT['B0.03_k0.5'], v, 5) for v in (1000, 1500, 2000, 2500)]))   # estimated from the printed rows (ln M to 3 decimals); an earlier version of the text said 1e-3
# rate-only (full mode)
RO = R('results_ray_rate_only.txt')
for k, kk, cr, qs in (('0.5', '1/2', '197', '3.012'), ('1.5', '3/2', '309', '5.019'), ('2.0', '2', '368', '6.023'), ('3.0', '3', '495', '8.030')):
    C('ro_q3000_k' + k, 'rate-only q_M at v=3000, k=%s' % kk, 'Sec. 5 (extension)', qs, F(RO, r'^\s+%s\s' % k.replace('.', r'\.'), i=4))
    C('ro_cross_k' + k, 'rate-only 10%% crossover of the flux, k=%s' % kk, 'Sec. 5 (extension)', cr, F(RO, r'^\s+%s\s' % k.replace('.', r'\.'), i=0))
# B = 0.003
C('b3_k05_A', 'B=0.003, k=1/2: ray integration against M_PDE for v<=108', 'Sec. 5 (B=0.003)', '4.8e-4', RY('rm_B0.003_k0.5_A_maxdev'))
C('b3_k05_v240', 'same at v=240', 'Sec. 5 (B=0.003)', '8.5e-4', F(RM3h, r'^\[B\]', r'^\s+240\s', i=3, a=True))
C('b3_k15_v100', 'B=0.003, k=3/2: difference at v=100', 'Sec. 5 (B=0.003)', '1.0e-2', F(RM3, r'^\[B\]', r'^\s+100\s', i=3, a=True))
C('b3_k15_levels', 'two highest Romberg levels at v=100', 'Sec. 5 (B=0.003)', '5e-6', F(RM3, r'^\[B\]', r'^\s+100\s', i=2))
C('b3_k15_v180', 'difference at v=180', 'Sec. 5 (B=0.003)', '-0.19', F(RM3, r'^\[B\]', r'^\s+180\s', i=3), 'abs:0.005', 'two digits (-1.9e-1)')
C('b3_k15_negative', 'M_PDE < 0 at v=200 (B=0.003, k=3/2)', 'Sec. 5 (B=0.003)', 1, X(lambda m: float(m < 0), F(RM3, r'^\[B\]', r'^\s+200\s', i=1)), 'eq', 'boolean statement')
C('b3_v100_k05', 'B=0.003: difference from the ray integration at v=100, k=1/2', 'Sec. 5 (B=0.003)', '5e-5', F(RM3h, r'^\[B\]', r'^\s+100\s', i=3, a=True), 'abs:5e-5', 'the log prints 3.0e-7 for B=0.03 and 4.5e-5 for B=0.003 (one significant figure in the text)')
C('b3_v100_k15', 'same for k=3/2', 'Sec. 5 (B=0.003)', '1e-2', F(RM3, r'^\[B\]', r'^\s+100\s', i=3, a=True), 'abs:5e-4', 'one significant figure (9.7e-3)')
C('b3_v100_B003_k05', 'B=0.03: difference at v=100, k=1/2', 'Sec. 5 (B=0.003)', '3e-7', F(RMF['0.5'], r'^\[B\]', r'^\s+100\s', i=3, a=True))
C('b3_v100_B003_k15', 'B=0.03: difference at v=100, k=3/2', 'Sec. 5 (B=0.003)', '7e-6', F(RMF['1.5'], r'^\[B\]', r'^\s+100\s', i=3, a=True))
C('b3_M108_k05', 'M(v=108) at B=0.03 over B=0.003, k=1/2', 'Sec. 5 (B=0.003)', '1.2e4', RY('rm_M108_ratio_B003_to_B0003_k0.5'))
C('b3_M108_k15', 'same, k=3/2', 'Sec. 5 (B=0.003)', '5e3', RY('rm_M108_ratio_B003_to_B0003_k1.5'), 'abs:2e2', 'one significant figure (5.2e3)')
C('b3_rate_exact', 'ODE rate against 4 pi r phi_v^2/rho at B=0.003, k=3/2, v=290', 'Sec. 5 (B=0.003)', '5e-6', RY('rm_B0.003_k1.5_C_ode_vs_exact_v290'), 'le', 'bound quoted in the text')
C('b3_rate_lamlam', 'ODE rate against lambda - lambda\'/lambda at v=140, B=0.003, k=3/2', 'Sec. 5 (B=0.003)', '2e-5', RY('rm_B0.003_k1.5_C_ode_vs_lamlam_v140'), 'abs:3e-6', 'one significant figure (1.8e-5)')
C('b3_q290_k05', 'B=0.003, k=1/2: q_M at v=290', 'Sec. 5 (B=0.003)', '3.145', XR(XT['B0.003_k0.5'], 290, 2))
C('b3_q2500_k05', 'same at v=2500', 'Sec. 5 (B=0.003)', '3.012', XR(XT['B0.003_k0.5'], 2500, 2))
C('b3_q290_k15', 'B=0.003, k=3/2: q_M at v=290', 'Sec. 5 (B=0.003)', '5.509', XR(XT['B0.003_k1.5'], 290, 2))
C('b3_q2500_k15', 'same at v=2500', 'Sec. 5 (B=0.003)', '5.022', XR(XT['B0.003_k1.5'], 2500, 2))
C('b3_Cchange_k05', 'change of ln M - kappa_- v + (2k+2) ln(v+1) between v=2000 and 2500, k=1/2', 'Sec. 5 (B=0.003)', '3e-3', X(lambda a, b: abs(a - b), XR(XT['B0.003_k0.5'], 2500, 3), XR(XT['B0.003_k0.5'], 2000, 3)))
C('b3_Cchange_k15', 'same, k=3/2', 'Sec. 5 (B=0.003)', '6e-3', X(lambda a, b: abs(a - b), XR(XT['B0.003_k1.5'], 2500, 3), XR(XT['B0.003_k1.5'], 2000, 3)), 'abs:1e-3', '5.5e-3 rounded to 6e-3')
C('b3_treat', 'the three treatments change ln M by at most (v=2500, B=0.003, k=1/2)', 'Sec. 5 (B=0.003)', '0.025', X(lambda a, b: max(abs(a), abs(b)), XR(XT['B0.003_k0.5'], 2500, 4), XR(XT['B0.003_k0.5'], 2500, 5)))
C('b3_lnM_2500', 'ln M at v=2500, B=0.003, k=1/2 (out of "1930")', 'Sec. 5 (B=0.003)', '1930', XR(XT['B0.003_k0.5'], 2500, 0), 'abs:1', 'three significant figures')
C('b3_eb_k05', 'B=0.003: excess at v_b, k=1/2 (v=290 value quoted: 1.1e-5)', 'Sec. 5 (B=0.003)', '1.1e-5', F(R('results_longrun_v300.txt'), LRK['0.5'], r'^\s+290\s', i=3))
# --- physical tails
for k, mu, km in (('2', '1.070e-2', '0.783979'), ('3', '1.154e-2', '0.783028')):
    C('pt_muf_k' + k, 'mu_f of the k=%s tail, B=0.03' % k, 'Sec. 5 (physical tails)', mu, V('static_hole', 'muf_gen3_B0.03_k%s_v300' % k))
    C('pt_km_k' + k, 'kappa_-(mu_f) of the k=%s tail, B=0.03' % k, 'Sec. 5 (physical tails)', km, V('static_hole', 'km_muf_gen3_B0.03_k%s_v300' % k))
for k, mu, km in (('2', '1.068e-4', '0.795537'), ('3', '1.151e-4', '0.795528')):
    C('pt3_muf_k' + k, 'mu_f of the k=%s tail, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', mu, V('static_hole', 'muf_gen3_B0.003_k%s_v300' % k))
    C('pt3_km_k' + k, 'kappa_-(mu_f) of the k=%s tail, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', km, V('static_hole', 'km_muf_gen3_B0.003_k%s_v300' % k))
for k, d, g in (('2', '1.1e-6', '162'), ('3', '1.4e-6', '158')):
    C('pt_e13_k' + k, 'projected mass against the ray integration, k=%s, B=0.03' % k, 'Sec. 5 (physical tails)', d, V('e13_table', 'e13_B0.03_k%s_max_dlnM' % k, a=True))
for k, eb, tr in (('2', '9.6e-7', '2.1e-3'), ('3', '3.1e-7', '6.9e-4')):
    C('pt_eb_k' + k, 'excess of |sigma_v| at v_b, k=%s, B=0.03' % k, 'Sec. 5 (physical tails)', eb, F(XD('0.03', k), r'^excess \|sV\|-km at v_b=([0-9.e+-]+)', g=1))
    C('pt_treat_k' + k, 'three treatments differ by at most (ln M, v=2500), k=%s, B=0.03' % k, 'Sec. 5 (physical tails)', tr, X(lambda a, b: max(abs(a), abs(b)), XR(XD('0.03', k), 2500, 4), XR(XD('0.03', k), 2500, 5)))
for k, p in (('2', '1.0440'), ('3', '1.0639')):
    C('pt_rb_static_k' + k, 'matching factor of the static-hole kernel at v_b, k=%s, B=0.03' % k, 'Sec. 5 (physical tails)', p, F(XD('0.03', k), r'^PDE/kernel phi_v ratio at v_b:'))
C('pt_drift_k2', 'drift of the static-kernel matching factor between v=250 and 290, k=2 (percent)', 'Sec. 5 (physical tails)', '0.5',
  X(lambda a, b: 100*(a - b)/a, F(R('results_e11_ratio.txt'), r'^B0\.03_k2\s', r'', i=3), F(R('results_e11_ratio.txt'), r'^B0\.03_k2\s', r'', i=5)))   # was 0.6
C('pt_drift_k3', 'same, k=3 (percent)', 'Sec. 5 (physical tails)', '0.3',
  X(lambda a, b: 100*(b - a)/a, F(R('results_e11_ratio.txt'), r'^B0\.03_k3\s', r'', i=3), F(R('results_e11_ratio.txt'), r'^B0\.03_k3\s', r'', i=5)))
C('pt_final_k2', 'matching factor of the final-hole kernel at v_b, k=2 (constant)', 'Sec. 5 (physical tails)', '1.0058', F(XM('0.03', '2'), r'^PDE/kernel phi_v ratio at v_b:'))
C('pt_final_k3', 'same, k=3', 'Sec. 5 (physical tails)', '1.0055', F(XM('0.03', '3'), r'^PDE/kernel phi_v ratio at v_b:'))
for k, p in (('2', '1.0e-2'), ('3', '-5.6e-3'), ('1.5', '1.7e-3'), ('0.5', '5.8e-4')):
    C('pt_static_cmp_k' + k, 'kernel-driven (static kernel) minus PDE-driven ln M at v=290, k=%s, B=0.03' % k, 'Sec. 5 (physical tails)', p, RY('ex_B0.03_k%s_kernel_minus_pde_lnM_v290' % k), 'abs:6e-4', 'the log values are printed to 4 decimals (+0.0105, -0.0056, +0.0017, +0.0006)')
C('pt_final_cmp', 'with the final-hole kernel all four agree at v=290 to', 'Sec. 5 (physical tails)', 1e-3, X(lambda *a: max(abs(x) for x in a), *[RY('ex_B0.03_k%s_kernel_final_minus_pde_lnM_v290' % k) for k in ('0.5', '1.5', '2', '3')]), 'le', 'bound quoted in the text')
for k, q, c, ch in (('2', '6.026', '-24.112', '7e-3'), ('3', '8.035', '-23.332', '9e-3')):
    C('pt_q2500_k' + k, 'q_M at v=2500, k=%s, B=0.03 (static-hole kernel)' % k, 'Sec. 5 (physical tails)', q, XR(XD('0.03', k), 2500, 2))
    C('pt_C2500_k' + k, 'ln M - kappa_- v + (2k+2) ln(v+1) at v=2500, k=%s' % k, 'Sec. 5 (physical tails)', c, XR(XD('0.03', k), 2500, 3))
    C('pt_Cchange_k' + k, 'its change since v=2000, k=%s' % k, 'Sec. 5 (physical tails)', ch, X(lambda a, b: abs(a - b), XR(XD('0.03', k), 2500, 3), XR(XD('0.03', k), 2000, 3)), 'abs:6e-4', 'one significant figure (6.7e-3, 9.0e-3)')
for k, rt, q4, q40 in (('2', '0.7540', '8.73', '6.27'), ('3', '0.6882', '27.6', '16.8')):
    C('pt_rate290_k' + k, 'rate at v=290, k=%s' % k, 'Sec. 5 (physical tails)', rt, XR(XD('0.03', k), 290, 1))
    C('pt_q290_k' + k, 'q_M at v=290, k=%s' % k, 'Sec. 5 (physical tails)', q4, XR(XD('0.03', k), 290, 2))
    C('pt_q400_k' + k, 'q_M at v=400, k=%s' % k, 'Sec. 5 (physical tails)', q40, XR(XD('0.03', k), 400, 2))
for k, d, d3, g in (('2', '2.3e-6', '8.7e-4', '156'), ('3', '5.4e-7', '9.6e-4', '152')):
    C('pt3_e13_k' + k, 'projected mass against the ray integration at v=280, k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', d, RY('e13_B0.003_k%s_U1_dlnM_v280' % k, a=True))
    C('pt3_e13_U03_k' + k, 'same on U=0.3', 'Sec. 5 (physical tails at B=0.003)', d3, RY('e13_B0.003_k%s_U03_dlnM_v280' % k, a=True))
    C('pt3_e13_le200_k' + k, 'same for 84<=v<=200', 'Sec. 5 (physical tails at B=0.003)', 1e-6, RY('e13_B0.003_k%s_U1_dlnM_max_84_200' % k), 'le', 'bound quoted in the text')
    C('pt3_lnM_k' + k, 'growth of M, ln M_ODE(280), k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', g, RY('e13_B0.003_k%s_lnM_ode_v280' % k))
for k, fl in (('2', '0.99993'), ('3', '0.99947')):
    C('pt3_flux_k' + k, 'flux over the final-hole kernel at v=280, k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', fl, F(KMU, r'^k=%s B=0\.003: PDE' % k, r'^\s+100:', i=8))
for k, rb in (('2', '0.99982'), ('3', '0.99947')):
    C('pt3_rb_k' + k, 'matching factor of the final-hole kernel at v_b, k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', rb, F(XM('0.003', k), r'^PDE/kernel phi_v ratio at v_b:'))
for k, eb, tr in (('2', '9e-9', '2e-5'), ('3', '3e-9', '7e-6')):
    C('pt3_eb_k' + k, 'excess of |sigma_v| at v_b, k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', eb, F(XM('0.003', k), r'^excess \|sV\|-km at v_b=([0-9.e+-]+)', g=1))
    C('pt3_treat_k' + k, 'three treatments differ by at most (ln M, v=2500), k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', tr, X(lambda a, b: max(abs(a), abs(b)), XR(XM('0.003', k), 2500, 4), XR(XM('0.003', k), 2500, 5)))
for k, q, c, ch in (('2', '6.0261', '-33.834', '6.6e-3'), ('3', '8.0352', '-33.104', '8.9e-3')):
    C('pt3_q2500_k' + k, 'q_M at v=2500, k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', q, XR(XM('0.003', k), 2500, 2))
    C('pt3_C2500_k' + k, 'ln M - kappa_- v + (2k+2) ln(v+1) at v=2500, k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', c, XR(XM('0.003', k), 2500, 3))
    C('pt3_Cchange_k' + k, 'its change since v=2000, k=%s, B=0.003' % k, 'Sec. 5 (physical tails at B=0.003)', ch, X(lambda a, b: abs(a - b), XR(XM('0.003', k), 2500, 3), XR(XM('0.003', k), 2000, 3)), 'abs:6e-4', 'two digits of 6.5e-3, 8.8e-3')
# --- caveats
SY = R('results_static_y_noise.txt')
for v, p in ((40, '-0.8'), (50, '-3.7e3'), (60, '-1.1e7')):
    C('sy_single_v%d' % v, 'static interior, single-grid y on the coarsest grid at v=%d' % v, 'Sec. 5 (caveats)', p, F(SY, r'^v=\s*%d\s+single grids' % v), None if v != 60 else 'abs:5e5', None if v != 60 else 'two digits of -1.06e7')
C('sy_romberg60', 'three-grid Romberg value of y at v=60 is wrong by', 'Sec. 5 (caveats)', '7', X(lambda a: abs(a - 0.5), F(SY, r'^v=\s*60\s+single grids.*3 grids')), 'abs:0.5', '|-6.52 - 0.5| = 7.0')

# =====================================================================================================================================
# Sec. 2 (validation of the scheme: code/nonlinear/run_validation.py, run_checks.py)
# =====================================================================================================================================
NLV = lambda n, a=False: V('paper_numbers_nl', n, a=a)
for h, p in (('0.08', '1.1e-3'), ('0.04', '2.8e-4'), ('0.02', '6.9e-5'), ('0.01', '1.7e-5')):
    C('val_static_h' + h, 'static interior: error of the evolution at h=%s' % h, 'Sec. 2 (validation)', p, NLV('static_err_h' + h))
C('val_static_order_lo', 'static interior: measured order, smallest', 'Sec. 2 (validation)', '1.998', NLV('static_order_min'))
C('val_static_order_hi', 'static interior: measured order, largest', 'Sec. 2 (validation)', '2.000', NLV('static_order_max'))
for h, a, b, c, d in (('0.08', '2.2e-3', '5.3e-3', '1.2e-3', '3.4e-4'), ('0.04', '5.4e-4', '1.3e-3', '2.9e-4', '8.4e-5'), ('0.02', '1.4e-4', '3.3e-4', '7.3e-5', '2.1e-5')):
    C('val_cu1_h' + h, 'relative Raychaudhuri residual in u, v<=20, h=%s' % h, 'Sec. 2 (validation)', a, NLV('constraint_u_v0_20_h' + h))
    C('val_cu2_h' + h, 'same, 20<v<=60', 'Sec. 2 (validation)', b, NLV('constraint_u_v20_60_h' + h))
    C('val_cv1_h' + h, 'relative Raychaudhuri residual in v, v<=20, h=%s' % h, 'Sec. 2 (validation)', c, NLV('constraint_v_0_20_h' + h), None if h != '0.02' else 'abs:1e-6', None if h != '0.02' else '7.35e-5 at the rounding boundary of 7.3e-5/7.4e-5')
    C('val_cv2_h' + h, 'same, 20<v<=58', 'Sec. 2 (validation)', d, NLV('constraint_v_20_58_h' + h))
C('val_cu_order', 'order of the u residual (quoted as 2.00)', 'Sec. 2 (validation)', '2.00', X(lambda a, b: (a + b)/2, NLV('constraint_u_order_min'), NLV('constraint_u_order_max')), 'abs:0.005', 'measured 1.998 to 2.000')

# =====================================================================================================================================
# Sec. 3: remaining historical numbers (paper_numbers_hist.py)
# =====================================================================================================================================
PH = lambda n, a=False: V('paper_numbers_hist', n, a=a)
for h, p in (('0.2', '2.0e-2'), ('0.1', '5.6e-3'), ('0.05', '1.4e-3')):
    C('hist_static_dsV_h' + h, 'static run: sigma_v error at U=1, v=100 for h_s=h_v=%s' % h, 'Sec. 3', p, PH('static_dsV_U1_v100_h' + h))
C('hist_B004_richardson', 'B=0.04, two grids: Richardson value of |sigma_v|', 'Sec. 3', '0.77622', PH('B0.04_richardson'))
C('hist_B004_pred', 'B=0.04: kappa_-(mu_f) prediction', 'Sec. 3', '0.775856', PH('B0.04_kappa_mu_f'))
C('hist_muloc_v40', 'mu_loc at U=0.1, v=40 (B=0.03, k=3/2)', 'Sec. 3', '9.959e-3', PH('muloc_U0.1_v40'))
C('hist_muloc_muf', 'mu_f of that run', 'Sec. 3', '9.956e-3', PH('muloc_mu_f'))
C('hist_muloc_rel_lo', 'mu_loc against mu_f on U=0.1, 40<=v<=65: smallest relative difference', 'Sec. 3', '3e-4', PH('muloc_U0.1_rel_min'), 'abs:5e-5', 'one significant figure (3.4e-4)')
C('hist_muloc_rel_hi', 'same: largest', 'Sec. 3', '7e-4', PH('muloc_U0.1_rel_max'), 'abs:5e-5', 'one significant figure (7.4e-4)')
C('hist_muloc_U03_lo', 'mu_loc against mu_f on U=0.3 (percent): smallest', 'Sec. 3', '0.3', PH('muloc_U0.3_percent_min'), 'abs:0.05', 'one significant figure (0.33)')
C('hist_muloc_U03_hi', 'same: largest', 'Sec. 3', '0.9', PH('muloc_U0.3_percent_max'), 'abs:0.05', 'one significant figure (0.93)')
C('hist_kappa_shift', 'change of kappa_- from the difference mu_loc - mu_f, at most', 'Sec. 3', '1e-4', PH('muloc_kappa_shift_max'), 'abs:2e-5', 'one significant figure (1.0e-4)')
for B, p in (('0.03', '3.6'), ('0.04', '3.3'), ('0.05', '2.9')):
    C('hist_Uc_B' + B, 'U_c(B=%s) from the first NaN column' % B, 'Sec. 3', p, PH('Uc_B' + B))
C('hist_aniso_lo', 'spurious mu/(h_s^2+h_v^2) at U=0.3, v=40, B=0: smallest of five combinations', 'Sec. 3', '1.5e-3', PH('aniso_ratio_min'))
C('hist_aniso_hi', 'same: largest', 'Sec. 3', '1.7e-3', PH('aniso_ratio_max'))
C('hist_aniso_a', 'anisotropic pair (0.1, 0.025)', 'Sec. 3', '1.7e-3', PH('aniso_ratio_hs0.1_hv0.025'))
C('hist_aniso_b', 'anisotropic pair (0.025, 0.1)', 'Sec. 3', '1.5e-3', PH('aniso_ratio_hs0.025_hv0.1'))
C('hist_muid_a1', 'mu_v identity on seeded data: ratio of the two sides at v=5, U=0.5, h=0.05', 'Sec. 3', '1.0016', PH('muid_U0.5_v5_h0.05'))
C('hist_muid_a2', 'same, h=0.025', 'Sec. 3', '1.0004', PH('muid_U0.5_v5_h0.025'))
C('hist_muid_b1', 'ratio at v=30, U=1, h=0.05', 'Sec. 3', '0.994', PH('muid_U1_v30_h0.05'), 'abs:5e-4', 'paper prints 0.994 for 0.9940')
C('hist_muid_b2', 'same, h=0.025', 'Sec. 3', '0.9985', PH('muid_U1_v30_h0.025'))
C('hist_uniform_nan_a', 'uniform U grid, h_U=0.04: first NaN at v', 'Sec. 3', '56', PH('uniform_nan_v_hU0.04'), 'abs:0.5', 'integer v of 55.8')
C('hist_uniform_nan_b', 'uniform U grid, h_U=0.02: first NaN at v', 'Sec. 3', '70', PH('uniform_nan_v_hU0.02'), 'abs:0.5', 'integer v of 70.2')

# =====================================================================================================================================
# Abstract and Sec. 6 (summary statements: each is a restatement of a check above, recomputed here)
# =====================================================================================================================================
C('abs_ray_decades_k15', 'growth of M over which the ray integration is tested, k=3/2 (decades, v0=48 to v=108)', 'Abstract; Sec. 5', '17',
  X(lambda a, b: __import__('math').log10(b/a), F(RMF['1.5'], r'^\s+v0=48\s+M_ext\(v0\)='), F(RMF['1.5'], r'^\s+v0=48\s+M_ext\(v0\)=\S+\s+M_ext\(108\)=([0-9.e+]+)', g=1)), 'abs:1', 'the text counts whole decades ("seventeen to nineteen"): 17.7')
C('abs_ray_decades_k05', 'same, k=1/2 (decades)', 'Abstract; Sec. 5', '19',
  X(lambda a, b: __import__('math').log10(b/a), F(RMF['0.5'], r'^\s+v0=48\s+M_ext\(v0\)='), F(RMF['0.5'], r'^\s+v0=48\s+M_ext\(v0\)=\S+\s+M_ext\(108\)=([0-9.e+]+)', g=1)), 'abs:1', 'whole decades: 19.3')
C('abs_underestimate', 'level spread of M_PDE understates its error by (smallest factor over Table 4 rows; the text says: at least 8 at the tabulated v; an earlier version "two to three orders of magnitude")', 'Abstract; Sec. 5', '8',
  X(min, RY('rm_B0.03_k1.5_B_min_dev_over_levels_table'), RY('rm_B0.03_k0.5_B_min_dev_over_levels_table')), 'ge', 'lower bound quoted in the text, for the rows of Table 4 only (all integer v: see rr_* below)')
C('abs_flux_B0003', 'abstract: B=0.003, k=3/2 flux agreement (ratio - 1, v=150..420)', 'Abstract; Sec. 6', '3e-4', X(lambda *a: max(abs(x - 1) for x in a), *[F(E12, r'^\s+%d\s' % v, i=0) for v in (150, 200, 250, 300, 350, 420)]), 'abs:1e-4', 'one significant figure (3.0e-4 to 3.2e-4)')
C('abs_range_kv', 'kappa_- v at v = 110 (Sec. 6: "approximately 87")', 'Sec. 6', '87', X(lambda k: k*110, V('static_hole', 'mN5_km')), 'abs:1', '0.7956 x 110 = 87.5; kappa_-(mu_f) x 110 = 86.3')
C('abs_k15_excess_le', 'k=3/2: excess of |sigma_v| over kappa_-(mu_f) at v_b = 250 is <= 1e-5', 'Sec. 6', 1e-5, F(XT['B0.03_k1.5'], r'^excess \|sV\|-km at v_b=([0-9.e+-]+)', g=1), 'le', 'bound quoted in the text')

# =====================================================================================================================================
# remaining single numbers found by the coverage pass over main.tex
# =====================================================================================================================================
C('gap_static_y_v80', 'static interior, single-grid y on the coarsest grid at v=80', 'Sec. 3 (construction)', '-8.7e13', F(SY, r'^v=\s*80\s+single grids'))
C('gap_T0_static', 'T(0) of the static hole (Sec. 4.4(d) text)', 'Sec. 4.3(d)', '44.304', V('static_hole', 'mN5_T0'))
C('gap_muf_k15', 'mu_f at B=0.03, k=3/2', 'Sec. 4.3(d)', '9.96e-3', V('paper_numbers', 'T1_mu_f_B0.03_k1.5'))
C('gap_muf_B005_k15', 'mu_f at B=0.05, k=3/2', 'Sec. 4.3(d)', '0.0278', V('paper_numbers', 'T1_mu_f_B0.05_k1.5'))
C('gap_muf_k05', 'mu_f at B=0.03, k=1/2', 'Sec. 4.3(d)', '5.91e-3', V('paper_numbers', 'T1_mu_f_B0.03_k0.5'))
C('gap_muf_B005_k05', 'mu_f at B=0.05, k=1/2', 'Sec. 4.3(d)', '1.65e-2', V('paper_numbers', 'T1_mu_f_B0.05_k0.5'))
C('gap_B2', '(0.05/0.03)^2, the B^2 scaling of mu_f', 'Sec. 4.3(d)', '2.78', X(lambda: (0.05/0.03)**2))
for k, p in (('1.5', '3e-3'), ('0.5', '0'), ('2', '0.017'), ('3', '0.05')):
    C('gap_kernel_choice_k' + k, 'ln M(v=2500) changes by (final-hole against static-hole kernel), B=0.03, k=%s' % k, 'Sec. 4.3(d)', p,
      RY('ex_B0.03_k%s_mu_minus_def_lnM_v2500' % k, a=True), 'abs:2e-3' if k == '3' else ('abs:5e-4' if k != '2' else None), ('0.051 rounded to 0.05' if k == '3' else ('printed to 3 decimals' if k != '2' else None)))
C('gap_kernel_choice_B0003', 'same at B=0.003: largest change over the four tails (the logs print ln M to 3 decimals, k=3: 1893.123 against 1893.121; the earlier text said <=1e-5)', 'Sec. 4.3(d)', '2e-3',
  X(lambda *a: max(abs(x) for x in a), *[RY('ex_B0.003_k%s_mu_minus_def_lnM_v2500' % k, a=True) for k in ('0.5', '1.5', '2', '3')]))
C('gap_qM_choice', 'q_M changes by at most (final-hole against static-hole kernel, B=0.03, all four tails, v>=1000)', 'Sec. 4.3(d)', 1e-3,
  X(lambda *a: max(abs(a[i] - a[i+1]) for i in range(0, len(a), 2)), *[s for k in ('0.5', '1.5', '2', '3') for v in (1000, 1500, 2000, 2500) for s in (XR(XD('0.03', k), v, 2), XR(XM('0.03', k), v, 2))]), 'le', 'bound quoted in the text')
C('gap_rays_s0', 'ray positions s_q of the profile integral: first', 'Sec. 5', '246.70', RY('rays_sq_n0'))
C('gap_rays_s2', 'ray positions s_q: last (U ~ 1)', 'Sec. 5', '271.25', RY('rays_sq_n2'))
C('gap_rays_U0', 'U at the first ray position', 'Sec. 5', '0.3003', RY('rays_Uq_n0'))
C('gap_rays_U2', 'U at the last ray position', 'Sec. 5', '0.9993', RY('rays_Uq_n2'))
C('gap_seed03_M', 'wide seed A=0.03: extrapolated M on U=0.6 at v=60 (units 1e9)', 'Sec. 3', '3.7', PN('seed_A0.03_M_ext_U0.6_v60_e9'))
C('gap_2kp_mN14', '2 kappa_+ at m_N=1.4 (exceeds kappa_-=0.164)', 'Sec. 4.2', '0.18', X(lambda k: 2*k, V('static_hole', 'mN1.4_kp')))
C('gap_beta_v60', 'beta at v=60, k=3/2, B=0.003', 'Sec. 4.4 (long runs)', '3.1', F(LR, LRK['1.5'], r'^\s+60\s', i=2))

# B=0.05, k=3/2 of Sec. 4.3(d): the computed remainder replaces the earlier sentence "excluded ... we did not compute"; transfer_mu.py selects the correct roots
C('kd_scal_k15_B005', 'k=3/2, B=0.05: remainder at v=100 (this run is valid; its inner horizon is r_-=1.0233; the earlier text excluded it, the shipped log had the wrong root)', 'Sec. 4.3(d)', '2.37e-2', F(ES, r'^gen_B0\.05_k1\.5.*ratio-1 at v=', r'100:', i=0))
C('kd_scal_k15_B005_mu', 'same in units of mu_f', 'Sec. 4.3(d)', '0.85', X(lambda e, m: e/m, F(ES, r'^gen_B0\.05_k1\.5.*ratio-1 at v=', r'100:', i=0), V('paper_numbers', 'T1_mu_f_B0.05_k1.5')))
C('kd_scal_k15_B005_ratio', 'ratio of the remainders B=0.05 / B=0.03, k=3/2 (B^2 scaling: 2.78)', 'Sec. 4.3(d)', '3.3',
  X(lambda a, b: a/b, F(ES, r'^gen_B0\.05_k1\.5.*ratio-1 at v=', r'100:', i=0), F(ES, r'^gen_B0\.03_k1\.5.*ratio-1 at v=', r'100:', i=0)))

# =====================================================================================================================================
# Added after the provenance audit (2026-10): the ratio of the ray-ODE deviation to the Romberg level spread at EVERY integer v = 84..290
# (ray_ratio_all_v.py, NEW script; the printed rows of Table 4 are the 10 values checked above).  The statements "at least 8 at every v" of the
# earlier text held for those rows only; the text now gives these statistics.
# =====================================================================================================================================
RR = lambda n: V('ray_ratio_all_v', n)
for t, kk, med, p05, mn, vmn in (('B0.03_k1.5', '3/2', '154', '11.7', '0.23', 272), ('B0.03_k0.5', '1/2', '136', '6.1', '0.77', 223)):
    C('rr_median_' + t, 'ratio |M_ODE/M_PDE-1| / level spread, median over integer v=84..290, B=0.03, k=%s' % kk, 'Abstract; Sec. 5', med, RR('rr_%s_p50' % t))
    C('rr_p05_' + t, 'same, fifth percentile', 'Sec. 5', p05, RR('rr_%s_p05' % t))
    C('rr_min_' + t, 'same, minimum', 'Sec. 5', mn, RR('rr_%s_min' % t))
    C('rr_vmin_' + t, 'v of the minimum', 'Sec. 5', vmn, RR('rr_%s_vmin' % t), 'eq', 'integer')
    C('rr_nlt1_' + t, 'number of integer v (of 207) at which the ratio is below 1', 'Abstract; Sec. 5', 1, RR('rr_%s_n_lt1' % t), 'eq', 'integer')
    C('rr_ntot_' + t, 'number of integer v, 84..290', 'Abstract', 207, RR('rr_%s_n_total' % t), 'eq', 'integer')
    C('rr_signchange_' + t, 'the minimum lies within 2 of a sign change of M_ODE-M_PDE (distance in v)', 'Sec. 5', 2, RR('rr_%s_min_dist_signchange' % t), 'le', 'bound quoted in the text ("next to a sign change")')
for t, kk, med in (('B0.003_k1.5', '3/2', '4.3'), ('B0.003_k0.5', '1/2', '8.3')):
    C('rr_median_' + t, 'same, median, B=0.003, k=%s' % kk, 'Abstract; Sec. 5', med, RR('rr_%s_p50' % t))
C('rr_sV_levels_k15', 'sigma_v: two highest Romberg levels, largest relative difference over every integer 60<=v<=290, B=0.03, k=3/2', 'Sec. 5', '5.1e-13', RR('rr_B0.03_k1.5_levels_sV_max_60_290'))
C('rr_sV_levels_k05', 'same, k=1/2', 'Sec. 5', '1.1e-12', RR('rr_B0.03_k0.5_levels_sV_max_60_290'))
C('rr_sV_levels_B0003', 'same, B=0.003 (k=3/2; k=1/2 gives 2.50e-12)', 'Sec. 5', '2.5e-12', RR('rr_B0.003_k1.5_levels_sV_max_60_290'))
C('rr_PV_levels_k15', 'phi_v: same, B=0.03, k=3/2', 'Sec. 5', '1.2e-8', RR('rr_B0.03_k1.5_levels_PV_max_60_290'))
C('rr_PV_levels_k05', 'phi_v: same, B=0.03, k=1/2', 'Sec. 5', '3.1e-10', RR('rr_B0.03_k0.5_levels_PV_max_60_290'))
C('kb_worst_variant', 'worst agreement of the kernel variants (smoothing variance, fit window) with the measured flux, k=3/2, v=100 (1 - ratio)', 'Sec. 4.3(b)', '1.4e-3',
  X(lambda a: 1 - a, F(R('results_kernel_sensitivity.txt'), r'^sig2=0\.25 .*k=3/2: v=60,100,290: \S+ (\S+)', g=1)))
C('hist_muid_regen', 'muid.py regenerated (results_muid_regen.txt): ratio at v=30, U=1, h=0.05 equals the original log (0.994)', 'Sec. 3', '0.994',
  F(R('results_muid_regen.txt'), r'^h 0\.05$', r'U=1\.00 v=30\s', i=2), 'abs:5e-4', 'paper prints 0.994 for 0.9940')
# sentences of main.tex that were revised after the provenance audit (present in the shipped main.tex)
for i, (lit, what) in enumerate((
    (r'numerical choices in the kernel change the prediction by up to $1.2\times10^{-3}$', 'abstract: kernel sensitivity'),
    (r'a median factor of $1.4$--$1.5\times10^{2}$ at $B=0.03$ and $4$--$8$ at $B=0.003$', 'abstract: level spread'),
    (r'a median factor of $1.4$--$1.5\times10^{2}$ ($B=0.03$) and $4$--$8$ ($B=0.003$)', 'Sec. 3: level spread'),
    (r'has median $154$ ($k=3/2$) and $136$ ($k=1/2$)', 'Sec. 5: all-v statistics'),
    (r'by a median factor of $1.5\times10^{2}$ ($k=3/2$) and $1.4\times10^{2}$ ($k=1/2$) over all integer $v=84$--$290$', 'Sec. 5: which mass is converged'),
    (r'is not an error bound, so it neither excludes nor demonstrates errors of this size', 'Sec. 5: sigma_v level spread'),
    (r'over all integer $v=84$--$290$ the median factor is $1.5\times10^{2}$', 'Fig. 4 caption'),
    (r'the worst of the variants agrees to $1.4\times10^{-3}$', 'Sec. 4.3(b): kernel variants'),
    (r'its tail coefficients are fitted to the ODE kernel itself', 'Sec. 5: kernel parameters'),
    (r'the remainder at $v=100$ is $2.37\times10^{-2}$', 'Sec. 4.3(d): B=0.05, k=3/2'))):
    C('txt_revised_%d' % i, 'sentence present in main.tex: ' + what, 'main.tex', 1, TXT(lit), 'eq', 'wording revised after the provenance audit; the numbers in it are checked by the rr_*, kb_* and kd_scal_* rows')
