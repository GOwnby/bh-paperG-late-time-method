# Nonlinear double-null test (Paper E, Section 6)

Einstein + NED monopole (Hayward profile, additive closure M = mu + M_N(r)) + massless scalar, spherical symmetry.
Equations, scheme, initial data and validation are in `main.tex`, Section 6; module docstring of `dn2lib.py` repeats them.

Run all scripts from this directory (they write cwd-relative files; `make_fig_nonlinear.py` writes `../../fig_nonlinear.png`).
Build (once):  `gcc -O3 -shared -fPIC -o libdouble_null.so double_null.c -lm`
Requires numpy, scipy, matplotlib.  Parameters: m_N = 5, a_N = 10 (ell^2 = a_N/2 m_N = 1).

| script | what it produces | wall time (1 core) |
|---|---|---|
| `run_validation.py` | static-interior error and Raychaudhuri residual vs h (orders) -> `validation_nonlinear.json` | ~1 min |
| `run_rates.py` | d ln|M|/dv on the Cauchy horizon: PDE (amplitudes, u, h) vs Ori shell model (closure `hn` in `../ori_model.py`) -> `rates_nonlinear.json` | ~2 min |
| `run_threshold.py h` | A_* by bisection and r_inf(A_*-A), h = 0.08, 0.04, 0.02 -> `threshold_h<h>.json` | 2-4 min each |
| `run_domain.py` | A_* vs outer edge u1; r_CH(u) profiles -> `domain_nonlinear.json` | ~8 min |
| `run_supercritical.py` | locus r = const above threshold -> `supercritical_nonlinear.json` | ~2 min |
| `run_universality.py` | Ori exponent q = 2k+2 for tails (1+v)^-k; critical exponent for other data families -> `universality_nonlinear.json` | ~10 min |
| `run_checks.py` | A_* independent of v1; saturation of r in v; rates near threshold (A_*-A down to 1e-10) and at the outer edge; sign change of M in u; Raychaudhuri residual in the v direction -> `checks_nonlinear.json` | ~6 min |
| `run_curvature.py` | Kretschmann scalar on the Cauchy horizon, static check, K = 2048 pi^2 (phi_u phi_v/W)^2, affine length, other tails/amplitudes -> `curvature_nonlinear.json` | ~2 min |
| `run_kappa_scan.py m_N [h]` | dependence on kappa_-: m_N = 5, 3, 2, 1.6, 1.4 (a_N = 2 m_N); threshold exponent and rate -> `kscan_mN<m_N>.json` | 2-8 min each |
| `make_fig_nonlinear.py` | `../../fig_nonlinear.png` | ~1 min |

Notes
* Collapse flag: r <= 1e-5 or non-finite anywhere on the grid (`run_domain.py` uses 1e-3, which shifts A_* by ~6e-10).
* r_inf := r(u = 40, v = 50). r_CH(u) saturates: r_CH(40) agrees with r_CH(50) to 4e-5 even at A_*-A = 1e-10 (at that distance r_CH(30) is still 12% larger than r_CH(40)).
* `sign_mech.py` (-> `sign_mech.log`): sign changes of M and r_u at v = 100 coincide (u = -1.88); mu_v = -8 pi r^2 (r_u/W) phi_v^2 => the growing mass has the sign of -r_u.
* `domain_mN1.4.py` (-> `domain_mN1.4.log`): A_* for m_N = 1.4 with kappa_- u1 = 20 and 40 (h = 0.1).
* Limits: additive closure only (the mass-tracking closure has no action); v <= 100; Kretschmann scalar computed but not the Weyl part separately, no geodesic deviation;
  above threshold only r >~ 0.05 is resolved.
* The second-order diamond scheme in `double_null.c` is the standard double-null idea (Gundlach-Price-Pullin 1994, bibliographic
  record only checked) with the first derivatives r_u, r_v, sigma_u, sigma_v, phi_u, phi_v as independent evolved variables.
* The event-horizon-regular set-up of Section 'Data regular on the event horizon' is in ../eh_init/ (own README).
* `sign_scan.py` (-> `sign_scan.log`): monotonicity of r_u/W in u (Raychaudhuri: d_v(r_u/W) = -4 pi r phi_u^2/W <= 0 along u) tested on 17 (A, B, h) combinations of the stored runs, NaN columns masked; hence r_u, and with it the sign of the inflating mass, changes sign at most once in u. The apparent irregular pattern at the smallest amplitude is a truncation violation of the monotonicity, not a second sign change. u* (the position of the change) is tabulated in the log; what fixes it from the data is not derived.
* `sign_ustar.py` (-> `sign_ustar.log`): u_*(v), the zero of r_u on the slices v = 10..100 for three (A, B) at h = 0.04. u_* stops moving for v >= 30 (-1.8790, -1.1565, -1.5430 to the printed digits). The check of the u-Raychaudhuri identity across the slice printed in the log is cancellation-limited at this resolution (relative mismatch O(1)) and is not used.
* `sign_separatrix.py` (-> `sign_separatrix.log`): the ray equation y' = a y + S is linear in y; y_sep(v0) = -int S/Phi dv is computed from the evolved ray fields, and the zero of y(v0,u) - y_sep(v0,u) lies at u_* for v0 = 30, 40, 50 (y_sep = 0.4990, 0.4715, 0.4998). Because y(v0,u) is extremely steep in u (|dy/du| > 1e4) this shows that the sign is decided by v ~ 30, not how u_* follows from A, B.
