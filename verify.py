#!/usr/bin/env python3
"""verify.py -- self-verification of the repository of Paper G (late-time mass inflation, method paper).

    verify.sh [--quick|--full]        (calls this script)

quick (default): runs every cheap generator script from the shipped data (JSON files, result logs), refreshes the result logs and
                 compares the computed numbers with the numbers quoted in main.tex (verification/expected.py).
full           : quick + the heavy runs (finest-grid regeneration of one data set, kernel-driven extension to v = 3000, rate-only
                 extension, nonlinear/run_checks.py, figures, ...), also compared with the paper.

Output: verification/REPORT.md (environment, step table, one row per check: quantity, location in main.tex, paper value, computed
value, tolerance with its reason, PASS/FAIL), verification/logs/<step>.log (command, return code, stdout, stderr of every script).
Exit code 0 only if no check and no step failed.  Steps whose Python/C requirements are missing (scipy, mpmath, sympy, matplotlib, gcc)
are SKIPPED (and so are the checks that read their output); SKIPPED checks are listed and not counted as passed.
In quick mode the steps marked `full` are SKIPPED too, but the checks that read their logs use the logs as shipped (written by the last --full run)
and are counted as passed; the report states the number of SKIPPED steps next to the number of SKIPPED checks.
Needs: Python >= 3.10, numpy >= 2, scipy >= 1.11, sympy, mpmath, matplotlib, gcc.  No network.  Relative paths only.
"""
import os, sys, re, json, time, subprocess, platform, shutil, datetime, importlib, importlib.util, traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.basename(ROOT)
MODE = 'quick'
REUSE = False       # development only: --reuse takes the stdout of a step from its existing log instead of running it
ONLY = None         # development only: --only=a,b runs just these steps
for a in sys.argv[1:]:
    if a in ('--quick', '--full'): MODE = a[2:]
    elif a == '--reuse': REUSE = True
    elif a.startswith('--only='): ONLY = a[7:].split(',')
    elif a in ('-h', '--help'): print(__doc__); sys.exit(0)
    else: print('unknown argument', a); sys.exit(2)
FULL = MODE == 'full'
PY = sys.executable
EH = 'code/eh_init'; NL = 'code/nonlinear'
LOGDIR = os.path.join(ROOT, 'verification', 'logs')
os.makedirs(LOGDIR, exist_ok=True)

# ----------------------------------------------------------------------------------------------------------------- environment
def have(mod):
    try:
        if importlib.util.find_spec(mod) is None: return False
        importlib.import_module(mod); return True
    except Exception: return False
def ver(mod):
    try: return importlib.import_module(mod).__version__
    except Exception: return 'not installed'
HAVE = {m: have(m) for m in ('numpy', 'scipy', 'sympy', 'mpmath', 'matplotlib')}
HAVE['gcc'] = shutil.which('gcc') is not None
# numpy >= 2 is required by the scripts (np.trapezoid)
if HAVE['numpy']:
    import numpy as _np
    if int(_np.__version__.split('.')[0]) < 2: HAVE['numpy'] = False
if sys.version_info < (3, 10): print('Python >= 3.10 required'); sys.exit(2)

# ----------------------------------------------------------------------------------------------------------------- steps
# id, cwd, commands (stdout of all commands is concatenated), out (file in cwd that is refreshed with that stdout), needs, full (full mode only), env
STEPS = []
def S(id, cwd, cmds, out=None, needs=(), full=False, env=None, timeout=7200, produces=(), mkdir=None):
    """cmds: one argv list, or a list of entries (stdout concatenated).  An entry is an argv list (a first element ending in .py is run with this
    interpreter), a tuple (argv, dict of environment variables) (a value '@mu_f:<json>' is replaced by the key mu_f of that JSON file: the matching-factor
    scripts need it as MU_F / KERNEL_MU), or the string '@text:<line>' (the line is written to the output: headers of the composite logs)."""
    if cmds and isinstance(cmds[0], str) and not cmds[0].startswith('@'): cmds = [cmds]
    norm = []
    for c in cmds:
        if isinstance(c, str): norm.append((c, {}))
        elif isinstance(c, tuple): norm.append((list(c[0]), c[1]))
        else: norm.append((list(c), {}))
    STEPS.append(dict(id=id, cwd=cwd, cmds=norm, out=out, needs=tuple(needs), full=full, env=env or {}, timeout=timeout,
                      produces=tuple(produces) + ((out,) if out else ()), mkdir=mkdir))
def T(line): return '@text:' + line
G = lambda t: 'gen2_%s_A0_U1_w0.3_v300.json' % t
MUF = lambda j: {'MU_F': '@mu_f:' + j}

S('build_c_libs', '.', ['sh', 'code/build.sh'], needs=['gcc'])
# ---- exact / symbolic / high-precision parts (sympy, mpmath: no scipy)
S('sympy_checks', EH, ['sympy_checks.py'], out='results_sympy_checks.txt', needs=['sympy'])
S('static_hole', EH, ['static_hole.py'], out='results_static_hole.txt', needs=['mpmath'])
S('check_field_equations', EH, ['check_field_equations.py'], out='results_check_field_equations.txt')
# ---- Section 2: nonlinear validation (static interior, Raychaudhuri residual); run_checks (6 min) in full mode
S('nl_validation', NL, ['run_validation.py'], needs=['scipy'], produces=['validation_nonlinear.json'])
S('nl_checks', NL, ['run_checks.py'], needs=['scipy'], full=True, produces=['checks_nonlinear.json'])
S('paper_numbers_nl', NL, ['paper_numbers_nl.py'], out='results_paper_numbers_nl.txt')
# ---- Section 3: event-horizon data (all from the shipped JSON data sets)
S('table_eh', EH, ['table_eh.py'], out='results_table_eh.txt')
S('report_stream', EH, ['report_stream.py'], out='results_stream_5grid.txt')
S('paper_numbers', EH, ['paper_numbers.py'], out='results_paper_numbers.txt')
S('static_y_noise', EH, ['static_y_noise.py'], out='results_static_y_noise.txt', needs=['scipy'])
S('phidecay', EH, ['phidecay.py', 'gen_B0_k1.5_A0.02_U0.7_w0.2_v110.json', 'gen_B0_k1.5_A0.02_U1_w0.3_v110.json', 'gen_B0.03_k1.5_A0_U1_w0.3_v110.json',
                  'gen_B0.03_k1.5_A0_U1_w0.3_v110_T0.3.json', 'gen_B0.03_k1.5_A0_U1_w0.3_v110_T10.json', 'gen_B0.03_k1.5_A0_U1_w0.3_v110_P10_2.json'], out='results_phidecay.txt')
# regeneration test of a data set: the two coarsest grids of gen_B0.03_k1.5_A0_U1_w0.3_v110.json are recomputed (gen.py, written to verification/tmp) and
# compared with the shipped file; the finest grid and the v = 450 run are regenerated in full mode
_g = '../../../code/eh_init/'          # the generators are run in a scratch directory (verification/tmp/...), so that the shipped data sets are not overwritten
S('regen_gen_coarse', 'verification/tmp/regen', [[_g + 'gen.py', '0.03', '1.5', '0', '1', '0.3', '110', '0.05', '0.025']], needs=['scipy', 'gcc'], mkdir=True)
S('regen_compare_coarse', EH, ['regen_compare.py', '../../verification/tmp/regen/gen_B0.03_k1.5_A0_U1_w0.3_v110.json', 'gen_B0.03_k1.5_A0_U1_w0.3_v110.json'], needs=['scipy'])
S('regen_gen_finest', 'verification/tmp/regen_finest', [[_g + 'gen.py', '0.03', '1.5', '0', '1', '0.3', '110', '0.003125']], needs=['scipy', 'gcc'], full=True, mkdir=True)
S('regen_compare_finest', EH, ['regen_compare.py', '../../verification/tmp/regen_finest/gen_B0.03_k1.5_A0_U1_w0.3_v110.json', 'gen_B0.03_k1.5_A0_U1_w0.3_v110.json'], needs=['scipy'], full=True)
S('regen_gen3_v450_finest', 'verification/tmp/regen_v450', [[_g + 'gen3.py', '0.003', '1.5', '0', '1', '0.3', '450', '0.00625']], needs=['scipy', 'gcc'], full=True, mkdir=True)
S('regen_compare_v450', EH, ['regen_compare.py', '../../verification/tmp/regen_v450/gen3_B0.003_k1.5_v450.json', 'gen3_B0.003_k1.5_v450.json'], needs=['scipy'], full=True)
# ---- Section 4: interior kernel
S('trace_residues_mN5', EH, ['trace_residues.py', '5'], out='results_trace_residues_mN5.txt', needs=['scipy'], full=True)
S('trace_residues_mN1.4', EH, ['trace_residues.py', '1.4'], out='results_trace_residues_mN1.4.txt', needs=['scipy'], full=True)
S('kernel_ft2', EH, ['kernel_ft2.py'], out='results_kernel_ft.txt', needs=['scipy'], full=True)
S('kernel_analytic', EH, ['kernel_analytic.py'], out='results_kernel_analytic.txt', needs=['scipy'], produces=['K_analytic_tau.npy'])
S('kernel_sensitivity', EH, ['kernel_sensitivity.py'], out='results_kernel_sensitivity.txt', needs=['scipy'])
S('longrun', EH, ['longrun.py', 'gen_B0.003_k0.5_A0_U1_w0.3_v300.json', 'gen_B0.003_k1.5_A0_U1_w0.3_v300.json'], out='results_longrun_v300.txt')
S('crossover_analytic', EH, ['crossover_analytic.py'], out='results_crossover_analytic.txt', needs=['scipy'])
S('flux_nl', EH, ['flux_nl.py'], out='results_flux_nl.txt', needs=['scipy'])
S('kernel_test', EH, ['kernel_test.py'], out='results_kernel_test.txt', needs=['scipy'])
S('kernel_mN', EH, [['kernel_mN.py', m, 'gen_B0.003_k1.5_A0_U1_w0.3_v150_mN%s_P40_2.json' % m] for m in ('1.4', '1.6', '2', '3')], out='results_kernel_mN.txt', needs=['scipy'])
S('kernel_pulse_mN5', EH, [T('== pulse at v_s=30, m_N=5, B=0.003'), ['kernel_mN.py', '5', 'gen_B0.003_k1.5_A0_U1_w0.3_v150_P30_2.json', '30'],
                           T('== pulse at v_s=60, m_N=5, B=0.003'), ['kernel_mN.py', '5', 'gen_B0.003_k1.5_A0_U1_w0.3_v150_P60_2.json', '60']],
  out='results_kernel_pulse_mN5_B0003.txt', needs=['scipy'])
S('kernel_B0003', EH, ['kernel_mN.py', '5', 'gen_B0.0003_k1.5_A0_U1_w0.3_v150_P60_2.json', '60'], out='results_kernel_B0003.txt', needs=['scipy'])
S('kernel_general_mN1.4', EH, ['kernel_general.py', '1.4', 'gen_B0.003_k1.5_A0_U1_w0.3_v250_mN1.4.json'], out='results_mN1.4_tail250.txt', needs=['scipy'])
S('e12_ratio', EH, ['e12_ratio.py'], out='results_e12_ratio.txt', needs=['scipy'])
S('e11_ratio', EH, ['e11_ratio.py'], out='results_e11_ratio.txt', needs=['scipy'])
S('kernel_mu', EH, [(['kernel_mu.py', 'gen3_%s_v300.json' % t], MUF('gen3_%s_v300.json' % t)) for t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5', 'B0.03_k2', 'B0.03_k3', 'B0.003_k2', 'B0.003_k3')],
  out='results_kernel_mu.txt', needs=['scipy'])
_es = ('gen_B0.003_k1.5_A0_U1_w0.3_v110.json', 'gen_B0.03_k1.5_A0_U1_w0.3_v110.json', 'gen_B0.05_k1.5_A0_U1_w0.3_v110.json', 'gen_B0.03_k0.5_A0_U1_w0.3_v110.json', 'gen_B0.05_k0.5_A0_U1_w0.3_v110.json')
S('e11_scaling', EH, [(['e11_scaling.py', j], MUF(j)) for j in _es], out='results_e11_scaling.txt', needs=['scipy'])
S('e11_pulse_all', EH, ['e11_pulse_all.py'], out='results_e11_pulse.txt', needs=['scipy'])
S('shell_kernel', EH, ['shell_kernel.py'], out='results_shell_kernel.txt', needs=['scipy'])
# ---- Section 5: ray integration, constraint-projected mass
for _t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5'):
    S('ray_mass_' + _t, EH, ['ray_mass.py', G(_t)], out='results_ray_mass_%s.txt' % _t, needs=['scipy'])
S('ray_stability', EH, [['ray_stability.py', G(t)] for t in ('B0.03_k1.5', 'B0.003_k1.5', 'B0.03_k0.5', 'B0.003_k0.5')], out='results_ray_stability.txt', needs=['scipy'])
for _t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5'):
    S('ray_long_' + _t, EH, ['ray_long.py', G(_t)], out='results_ray_long_%s.txt' % _t, needs=['scipy'])
S('ray_ratio_all_v', EH, ['ray_ratio_all_v.py'], out='results_ray_ratio_all_v.txt', needs=['scipy'])   # NEW (provenance audit): ratio error/level-spread at every integer v
for _t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.03_k2', 'B0.03_k3'):
    S('ray_long_gen3_' + _t, EH, ['ray_long.py', 'gen3_%s_v300.json' % _t], out='results_ray_long_gen3_%s.txt' % _t, needs=['scipy'])
S('ray_validate', EH, [['ray_validate.py', 'gen2_B0.03_k1.5_A0_U1_w0.3_v110.json'], ['ray_validate.py', 'gen2_B0.03_k0.5_A0_U1_w0.3_v110.json']], out='results_ray_validate.txt', needs=['scipy'])
S('e13_table', EH, ['e13_table.py'], out='results_e13_table.txt', needs=['scipy'], produces=['frag11/rows.tex'])
S('e13_errconst', EH, [['e13_errconst.py', 'gen3_%s_v300.json' % t, n] for t in ('B0.03_k1.5', 'B0.003_k1.5', 'B0.03_k0.5') for n in ('2', '0')], out='results_e13_errconst.txt', needs=['scipy'])
S('e13_v0', EH, ['e13_v0.py'], out='results_e13_v0.txt', needs=['scipy'])
_e13 = ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5', 'B0.03_k2', 'B0.03_k3', 'B0.003_k2', 'B0.003_k3')
for _t in _e13:
    S('e13_all_' + _t, EH, [['e13_all.py', 'gen3_%s_v300.json' % _t, n] for n in ('2', '0')], out='results_e13_%s.txt' % _t, needs=['scipy'], full=True)
for _t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5'):
    S('ray_extend_' + _t, EH, ['ray_extend.py', G(_t)], out='results_ray_extend_%s.txt' % _t, needs=['scipy'], full=True, produces=['ray_extend_%s.npz' % _t])
for _t in _e13:
    _j = 'gen3_%s_v300.json' % _t
    # a gen2 run of the same (B, k) writes ray_extend_B*_k*.npz (read by ray_fig.py): the gen3 run must not overwrite it -> NPZ_SUFFIX=_gen3
    _gen2_exists = _t in ('B0.03_k1.5', 'B0.03_k0.5', 'B0.003_k1.5', 'B0.003_k0.5')
    S('ray_extend_def_' + _t, EH, [(['ray_extend.py', _j], {'NPZ_SUFFIX': '_gen3'})] if _gen2_exists else ['ray_extend.py', _j], out='results_ray_extend_ext_def_%s.txt' % _t, needs=['scipy'], full=True)
    S('ray_extend_mu_' + _t, EH, [(['ray_extend.py', _j], {'KERNEL_MU': '@mu_f:' + _j})], out='results_ray_extend_ext_mu_%s.txt' % _t, needs=['scipy'], full=True)
S('ray_rate_only', EH, ['ray_rate_only.py'], out='results_ray_rate_only.txt', needs=['scipy'], full=True)
S('ray_fig', EH, ['ray_fig.py'], needs=['scipy', 'matplotlib'], produces=['fig_ray_mass.png'])
S('e13_fig', EH, ['e13_fig.py'], needs=['scipy', 'matplotlib'], full=True, produces=['fig_e13.png'])
# ---- older logs of the event-horizon runs (composite logs: headers are written by this script); full mode
S('hist_eh_init', EH, [T('== static validation (A=B=0), (s,v) grid, errors vs exact static solution, 2nd-order =='), ['t_static4.py'], T(''),
                       T('== B=0.03 k=1.5 sigma_v vs kappa-(mu_f) =='), ['conv1.py', '0.03', '1.5', '100', '0.05', '0.025'], T(''),
                       T('== B=0.04 k=1.5 =='), ['conv1.py', '0.04', '1.5', '100', '0.05', '0.025'], T(''),
                       T('== B=0.03 k=0.5 =='), ['conv1.py', '0.03', '0.5', '100', '0.05', '0.025'], T(''),
                       T('== local mass check mu_loc, kappa-(mu_loc) vs sigma_v =='), ['mucheck.py', '0.03', '1.5', '100', '0.025'], ['mucheck.py', '0.03', '0.5', '100', '0.025'], T(''),
                       T('== B=0.05 collapse location (r->0 at large U) =='), ['nanloc.py', '0.05', '0.05', '100']], out='results_eh_init.txt', needs=['scipy'], full=True)
S('hist_tailonly_collapse', EH, [T('== tail-only B=0.05 k=1.5 =='), ['conv1.py', '0.05', '1.5', '100', '0.05', '0.025'], T('== tail-only B=0.03 k=0.5 =='), ['conv1.py', '0.03', '0.5', '100', '0.05', '0.025'], T(''),
                                 T('== first NaN column (r<0) vs B =='), T('B=0.03'), ['nanloc.py', '0.03', '0.05', '100'], T('B=0.04'), ['nanloc.py', '0.04', '0.05', '100'], T('B=0.05'), ['nanloc.py', '0.05', '0.05', '100']],
  out='results_tailonly_collapse.txt', needs=['scipy'], full=True)
S('hist_aniso', EH, [T('# aniso.py output (B=0, v1=100, mu = M - M_N(r) of the numerical static solution; truncation-error mass)'), ['aniso.py']], out='results_aniso_noise.txt', needs=['scipy'], full=True)
S('hist_checks_extra', EH, [['t_uniform.py'], T(''), ['noise.py'], T(''), ['phiexp_extrap.py'], T(''), T('== B=0.03 k=1.5 tail-only, three grids =='), ['conv1.py', '0.03', '1.5', '100', '0.05', '0.025'], ['conv3.py']],
  out='results_checks_extra.txt', needs=['scipy'], full=True)
S('hist_muid', EH, [T('== exact consequence mu_v = -8 pi r^2 (r_u/W) phi_v^2 (seeded data, k=1.5): ratio -> 1 as h^2 where M is accurate =='), ['muid.py']], out='results_muid_regen.txt', needs=['scipy'], full=True)
# results_seeded_identity_constraint.txt is the author's original log (muid.py block + constraint-residual / seed5 blocks that no script here regenerates): it is shipped
# unchanged; muid.py regenerates only its first block, into results_muid_regen.txt (checked against the original block by hist_muid_regen_*).
# ---- numbers parsed from the logs above (run after them)
S('paper_numbers_kernel', EH, ['paper_numbers_kernel.py'], out='results_paper_numbers_kernel.txt', needs=['scipy'])
S('paper_numbers_ray', EH, ['paper_numbers_ray.py'], out='results_paper_numbers_ray.txt')
S('paper_numbers_hist', EH, ['paper_numbers_hist.py'], out='results_paper_numbers_hist.txt')

# ----------------------------------------------------------------------------------------------------------------- run
def cpu_children():
    try:
        import resource
        r = resource.getrusage(resource.RUSAGE_CHILDREN); return r.ru_utime + r.ru_stime
    except Exception: return 0.0

def keep_log(log, text):
    # a skipped step does not overwrite the log of an earlier run (e.g. the shipped log of a --full run)
    if not os.path.exists(log): open(log, 'w').write(text)

def run_step(st):
    log = os.path.join(LOGDIR, st['id'] + '.log')
    res = dict(id=st['id'], status='', secs=0.0, cpu=0.0, rc=None, log=os.path.relpath(log, ROOT), changed=None)
    miss = [n for n in st['needs'] if not HAVE.get(n, False)]
    if miss:
        res['status'] = 'SKIPPED (missing: %s)' % ', '.join(miss)
        keep_log(log, 'SKIPPED: %s not available\n' % ', '.join(miss)); return res
    if st['full'] and not FULL:
        res['status'] = 'SKIPPED (full mode only)'; keep_log(log, 'SKIPPED: full mode only\n'); return res
    cwd = os.path.join(ROOT, st['cwd'])
    if st['mkdir']: os.makedirs(cwd, exist_ok=True)
    if (REUSE or (ONLY and st['id'] not in ONLY)) and os.path.exists(log):
        txt = open(log).read()
        if '# ---- stdout\n' in txt:
            a = txt.index('# ---- stdout\n') + 14; b = txt.rindex('\n# ---- stderr')
            m = re.search(r'# return code (\S+), ([\d.]+) s(?:, ([\d.]+) s cpu)?', txt)
            res.update(status='OK' if m and m.group(1) == '0' else 'FAILED (reused)', secs=float(m.group(2)) if m else 0.0, cpu=float(m.group(3) or 0) if m else 0.0, rc=0, stdout=txt[a:b] + '\n'); return res
    base_env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', MPLBACKEND='Agg', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                    MKL_NUM_THREADS='1')
    base_env.update(st['env'])
    t0 = time.time(); c0 = cpu_children(); so_all = []; se_all = []; head = []; rc = 0
    for argv, xenv in st['cmds']:
        if isinstance(argv, str):                      # '@text:<line>'
            so_all.append(argv[6:] + '\n'); continue
        env = dict(base_env)
        for k, v in xenv.items():
            if isinstance(v, str) and v.startswith('@mu_f:'): v = repr(json.load(open(os.path.join(cwd, v[6:])))['mu_f'])
            env[k] = v
        cmd = [PY] + argv if argv[0].endswith('.py') else argv
        head.append(' '.join('%s=%s' % kv for kv in xenv.items()) + (' ' if xenv else '') + ' '.join(cmd))
        try:
            p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=st['timeout'])
            r_, so, se = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            r_, so, se = -9, '', 'TIMEOUT after %d s' % st['timeout']
        so_all.append(so); se_all.append(se)
        if r_ != 0: rc = r_
    so = ''.join(so_all); se = ''.join(se_all)
    res['secs'] = time.time() - t0; res['cpu'] = cpu_children() - c0; res['rc'] = rc
    with open(log, 'w') as f:
        f.write('# step %s\n# cwd %s\n# commands\n%s\n# return code %s, %.1f s, %.1f s cpu\n# ---- stdout\n%s\n# ---- stderr\n%s\n' %
                (st['id'], st['cwd'], '\n'.join('#   ' + h for h in head), rc, res['secs'], res['cpu'], so, se))
    res['stdout'] = so
    if rc == 0:
        res['status'] = 'OK'
        if st['out']:
            dst = os.path.join(cwd, st['out'])
            old = open(dst).read() if os.path.exists(dst) else None
            res['changed'] = (old is not None and old != so)
            tmp = dst + '.tmp'; open(tmp, 'w').write(so); os.replace(tmp, dst)
    else:
        res['status'] = 'FAILED (rc=%s)' % rc
    return res

RESULTS = {}
def main():
    t00 = time.time()
    print('verify.py (%s mode) in %s' % (MODE, ROOT))
    for st in STEPS:
        r = run_step(st); RESULTS[st['id']] = r
        print('  step %-28s %-28s %7.1f s (cpu %.1f s)%s' % (st['id'], r['status'], r['secs'], r['cpu'], '  [log differs from the shipped one]' if r.get('changed') else '')); sys.stdout.flush()
    # ------------------------------------------------------------------------------------------------------------- checks
    sys.path.insert(0, os.path.join(ROOT, 'verification'))
    import expected
    rows = expected.evaluate(ROOT, STEPS, RESULTS, FULL)
    npass = sum(1 for r in rows if r['status'] in ('PASS', 'PASS*')); ncorr = sum(1 for r in rows if r['status'] == 'PASS*'); nfail = sum(1 for r in rows if r['status'] == 'FAIL')
    nskip = sum(1 for r in rows if r['status'] == 'SKIPPED'); nrun = npass + nfail
    stepfail = [i for i, r in RESULTS.items() if r['status'].startswith('FAILED')]
    write_report(rows, npass, nfail, nskip, stepfail, time.time() - t00, ncorr)
    for r in rows:
        if r['status'] == 'FAIL': print('  FAIL %-40s paper %s computed %s (%s)' % (r['id'], r['paper'], r['computed'], r['tol']))
    ok = nfail == 0 and not stepfail
    if ncorr: print('NOTE: %d of the passed checks are PASS* = the computed value agrees with the corrected value and the text of main.tex has to be corrected (REPORT.md, "Corrections applied to main.tex")' % ncorr)
    if nskip: print('NOTE: %d checks SKIPPED (missing tools, or data of the full mode only); they are not counted as passed' % nskip)
    print('RESULT %s: %s %d/%d checks (%s)' % (REPO, 'PASSED' if ok else 'FAILED', npass, nrun, MODE) + (' [%d SKIPPED]' % nskip if nskip else ''))
    sys.exit(0 if ok else 1)

def write_report(rows, npass, nfail, nskip, stepfail, secs, ncorr=0):
    import expected
    L = []
    L.append('# Verification report (%s)\n' % REPO)
    L.append('Mode: **%s**.  Date: %s.  Total wall time: %.0f s.\n' % (MODE, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), secs))
    nsteps_skip = sum(1 for r in RESULTS.values() if r['status'].startswith('SKIPPED'))
    L.append('Checks: **%d PASS (of which %d PASS* = corrections already applied in main.tex), %d FAIL, %d SKIPPED**; steps failed: %s.\n' % (npass, ncorr, nfail, nskip, ', '.join(stepfail) or 'none'))
    L.append('Steps: **%d run, %d SKIPPED** (%s). A check whose log is written by a SKIPPED step reads the log as shipped (the log of the last `--full` run, see `REPORT_full.md`); it is counted as passed, but the log was not regenerated in this run.\n' %
             (len(RESULTS) - nsteps_skip, nsteps_skip, 'full mode only, or missing tools'))
    L.append('## Environment\n')
    L.append('| item | value |\n|---|---|')
    L.append('| platform | %s |' % platform.platform())
    L.append('| python | %s (%s) |' % (platform.python_version(), PY))
    for m in ('numpy', 'scipy', 'sympy', 'mpmath', 'matplotlib'): L.append('| %s | %s |' % (m, ver(m) if HAVE[m] else 'not installed'))
    try: g = subprocess.run(['gcc', '--version'], capture_output=True, text=True).stdout.splitlines()[0]
    except Exception: g = 'not installed'
    L.append('| gcc | %s |' % g)
    L.append('| cpu count | %s |\n' % os.cpu_count())
    L.append('## Steps\n')
    L.append('| step | command | status | wall (s) | cpu (s) | output file refreshed | log |\n|---|---|---|---|---|---|---|')
    for st in STEPS:
        r = RESULTS[st['id']]
        cmds = ' ; '.join(c[0][6:] if isinstance(c[0], str) else ' '.join(c[0]) for c in st['cmds'] if not isinstance(c[0], str))
        L.append('| %s | `%s` (in `%s`) | %s | %.1f | %.1f | %s | `%s` |' % (st['id'], cmds, st['cwd'], r['status'], r['secs'], r['cpu'], ('`%s`%s' % (st['out'], ' (changed)' if r.get('changed') else '')) if st['out'] and r['status'] == 'OK' else '', r['log']))
    corr = [r for r in rows if r['status'] == 'PASS*']
    L.append('\n## Corrections applied to main.tex (PASS* rows)\n')
    if corr:
        L.append('For these rows the computed value reproduces the corrected value and not the one of the earlier version of main.tex; `expected.py` now holds the corrected value as the printed one, so a row is listed here only if the computed value still differs from it.\n')
        L.append('| id | location | quantity | main.tex now | computed | should read |\n|---|---|---|---|---|---|')
        fixes = {c['id']: c['fix'] for c in expected.CHECKS}
        for r in corr:
            L.append('| %s | %s | %s | %s | %s | %s |' % (r['id'], r['loc'], r['quantity'].replace('|', '/'), r['paper'].split(' (text')[0], r['computed'], fixes[r['id']]))
    else: L.append('none\n')
    tc = expected.textcoverage(ROOT)
    L.append('\n## Paper values against the text of main.tex\n')
    if tc is None: L.append('main.tex was not found next to verify.py; the typed paper values were not compared with the text.\n')
    else:
        L.append('%d of the %d typed paper values occur verbatim in main.tex (as typed, or written x\\times10^{n}). Not found (a bound or a rounded value may be written differently in the text; this list is informational, the numerical comparison is the table below): %s.\n' %
                 (tc[0], tc[1], ', '.join(tc[2]) or 'none'))
    L.append('\n## Checks\n')
    L.append('Tolerance "round" means: the computed value rounds to the printed digits of the paper value (half a unit in the last printed digit); '
             'other tolerances are stated with their reason.\n')
    L.append('| id | quantity | location in main.tex | paper | computed | tolerance | status |\n|---|---|---|---|---|---|---|')
    for r in rows:
        L.append('| %s | %s | %s | %s | %s | %s | %s |' % (r['id'], r['quantity'].replace('|', '/'), r['loc'], r['paper'], r['computed'], r['tol'].replace('|', '/'), r['status']))
    open(os.path.join(ROOT, 'verification', 'REPORT.md'), 'w').write('\n'.join(L) + '\n')

if __name__ == '__main__':
    main()
