# Late-Time Mass Inflation in Double-Null Evolutions: Event-Horizon-Regular Data, the Interior Linear Response and Exact Integration Along a Ray

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23455605.svg)](https://doi.org/10.5281/zenodo.23455605)

Gracen Ownby. Paper G of a series on regular black holes of Hayward type (companions: Paper A doi:10.5281/zenodo.23455575, Paper E doi:10.5281/zenodo.23455587, Paper F doi:10.5281/zenodo.23455595).
This repository (version 1.1.0, 2026-10-20) contains the manuscript, the compiled PDF, and all code, data and logs behind its numbers. Licence: code MIT, text and data CC-BY-4.0 (see `LICENSE.md`).

## Abstract

Mass inflation at an inner horizon is a late-time phenomenon: the mass grows like exp(kappa_- v), and a double-null evolution reaches only v of order 10^2 to 3x10^2, with a truncation error that itself grows with v.
The paper develops and tests a method for this regime in a system whose static interior and ray equations are exact (no published evolution is reproduced): the spherical Einstein-nonlinear-electrodynamics-massless-scalar system
with an additive closure M = mu + M_N(r), whose static interior is a Hayward-type regular black hole. (1) With data regular on the event horizon, the metric exponent at the Cauchy horizon follows the surface gravity of the accumulated mass,
kappa_-(mu_f), not the static one. (2) The ingoing flux at the Cauchy horizon is the linear response of the static interior to the horizon flux; its kernel follows from the interior wave equation, decays at kappa_+, and reproduces the measured flux to 4e-4 at B = 0.003.
(3) The field equations integrate exactly along a ray; this reproduces the Romberg-extrapolated PDE mass to 6e-5 (k = 3/2) and 2e-6 (k = 1/2) up to v = 108, and a constraint-projected PDE mass agrees with it in ln M to 1.4e-6 (B = 0.03) and 2.3e-6 (B = 0.003) up to v = 280, where M ~ e^160 to e^180.
(4) In a model driven by the kernel flux beyond v = 250, the ray integration reaches the Ori tail law in M at v of order 10^3.

## Directory map

| path | content |
|---|---|
| `main.tex`, `references.bib`, `main.bbl` | manuscript source, bibliography, bibliography as built |
| `paperG_late_time_method.pdf` | compiled manuscript (24 pages) |
| `fig_e13.png`, `fig_ray_mass.png` | the two figures included by `main.tex` |
| `code/README.md` | code overview, dependencies, build, run times |
| `code/build.sh`, `code/requirements.txt` | build script for the C libraries; Python dependencies |
| `code/ori_model.py` | Ori thin-shell model; byte-identical to the file of the Paper E archive (doi:10.5281/zenodo.23455587) |
| `PROVENANCE.md` | lineage of this repository, every file that differs from the author's archive (with the evidence), files that have no counterpart there, results that changed, what reproduces from the original code, known limits |
| `code/eh_init/` | event-horizon-regular data, kernel, ray integration, constraint-projected mass: scripts, C sources, data (`gen*_*.json`), logs (`results_*.txt`, `e_*.log`); `MANIFEST.md` lists the command that produced each JSON; own `README.md` |
| `code/nonlinear/` | the double-null evolution code and the validation runs of Section 2 (identical `double_null.c` to Paper E's); own `README.md` |
| `verify.sh`, `verify.py`, `requirements.txt` | self-verification (see "Verify"), Python requirements with minimum versions |
| `verification/` | `expected.py` (every number quoted in `main.tex` with its location, tolerance and the file or script it is computed from), `REPORT.md` (written by `verify.sh`), `logs/` (one log per step) |
| `LICENSE.md`, `CITATION.cff` | licence, citation metadata |

## Verify

```
sh verify.sh            # quick (default): about 7 CPU-minutes (24 min wall on a shared machine); recomputes every number of main.tex from the shipped data
sh verify.sh --full     # adds the heavy runs (finest-grid regeneration incl. the v = 450 run, kernel-driven extension to v = 3000, run_checks, trace_residues, ...): about 73 CPU-minutes (5 h wall on a shared 2-core machine); per-step timings in verification/REPORT.md
```

`verify.sh` needs Python >= 3.10, numpy >= 2, scipy >= 1.11, sympy, mpmath, matplotlib and gcc (`requirements.txt`), builds the C libraries itself, uses relative paths and no network (`PYTHON=python3.11 sh verify.sh` selects the interpreter).
It runs the generator scripts of the table below, refreshes their `results_*.txt` and figures, compares 1054 quantities with `main.tex` (the 1021 of the full run of 2026-10-21 and 33 added after the audit) (quantity, location, paper value, computed value, tolerance with its reason, PASS/FAIL) and writes `verification/REPORT.md` and `verification/logs/<step>.log`.
The last line is `RESULT bh-paperG-late-time-method: PASSED n/n checks (quick)`; the exit status is non-zero if a check or a step fails. Steps that need a missing package are reported as SKIPPED and their checks are not counted as passed. In quick mode the steps marked "full mode only" are reported as SKIPPED as well (`REPORT.md` states the number of skipped steps next to the number of skipped checks): the checks that use their logs read the logs as shipped, which were written by the last `--full` run (`verification/REPORT_full.md`), and are counted as passed. A `PASS*` row would be a statement of `main.tex` that the computation corrects (section "Corrections applied to main.tex" of `REPORT.md`); the corrections found in the audit of 2026-10-21 have been applied to `main.tex`, so none is expected. `verification/REPORT.md` also lists how many of the typed paper values occur verbatim in `main.tex`.
The files `results_*.txt` and `validation_nonlinear.json` are rewritten by every run (identical to the printed digits; the last digits of the JSON depend on the machine), the shipped data sets (`gen*_*.json`) are never overwritten (the regeneration test works in `verification/tmp/`).

## Build the PDF

```
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

(TeX Live with `natbib`, `hyperref`, `booktabs`; the figures are in this directory.) The shipped PDF is the output of exactly this sequence.

## Build the C libraries and run the code

Tested on Linux with gcc (Ubuntu 22.04, gcc 11.4), Python 3.10.12, numpy 2.2.6, matplotlib 3.10.9. On Windows use WSL, or adapt `code/build.sh` (the libraries are loaded with `ctypes` from the script directory as `lib*.so`).

```
pip install -r requirements.txt
sh code/build.sh              # libdouble_null.so, libstream.so, libstream2.so in code/eh_init; libdouble_null.so in code/nonlinear
cd code/eh_init               # all scripts are run from their own directory; outputs are written to the current directory
```

`requirements.txt` (also reachable as `code/requirements.txt`): numpy >= 2.0 (uses `np.trapezoid`), scipy >= 1.11, sympy, mpmath, matplotlib. No `-ffast-math` is used; the streaming kernels `stream.c`, `stream2.c` are bitwise identical to `double_null.c` on a test run.

## Result in the paper -> script -> output

Commands are run from `code/eh_init` unless stated. Run times are approximate, one core. Every row is run by `verify.sh` (the "long" rows and the finest-grid regenerations in `--full` mode) with real scipy, and its output is compared with the numbers of `main.tex`; the shipped `results_*.txt` are the outputs of the last such run (2026-10-21). The commands that generated the data sets are in `code/eh_init/MANIFEST.md`.

| result in the paper | script and command | output file | time |
|---|---|---|---|
| Table 1 (|sigma_v| at v = 95 against kappa_-(mu_f)) | `python3 table_eh.py` | `results_table_eh.txt` | 1 s |
| Table 2 and the phi_v exponents (rate against lambda - lambda'/lambda) | `python3 report_stream.py` | `results_stream_5grid.txt` | 1 s |
| Section 2 validation (static interior, orders, Raychaudhuri residual) | `cd ../nonlinear; python3 run_validation.py; python3 run_checks.py` | `validation_nonlinear.json`, `checks_nonlinear.json` | 15 s; 6 min |
| Section 2 field equations and Kretschmann decomposition | `python3 check_field_equations.py` | `results_check_field_equations.txt` | 1 s |
| Kernel residues and T(0) (Section 4) | `python3 trace_residues.py 5` (and `1.4`) | `results_trace_residues_mN5.txt`, `..._mN1.4.txt` | 1-2 min |
| Kernel against the tail-only flux, Section 4.3(b), Table 3 kernel columns | `python3 kernel_analytic.py` | `results_kernel_analytic.txt` | 15 s |
| Sensitivity of the kernel prediction to the smoothing and the tail-fit window | `python3 kernel_sensitivity.py` | `results_kernel_sensitivity.txt` | 3 s |
| Table 3 (long runs, local exponents, kernel columns) | `python3 longrun.py gen_B0.003_k0.5_A0_U1_w0.3_v300.json gen_B0.003_k1.5_A0_U1_w0.3_v300.json` | `results_longrun_v300.txt` | 1 s |
| Crossover v of the power law, flux-ratio table | `python3 crossover_analytic.py` | `results_crossover_analytic.txt` | 30 s |
| Linear against nonlinear flux at B = 0.03 | `python3 flux_nl.py` | `results_flux_nl.txt` | 1 s |
| Flux ratio to v = 420 (Section 4.3(e)) | `python3 e12_ratio.py` | `results_e12_ratio.txt` | 1 s |
| Matching factor of the final-hole kernel | `MU_F=<mu_f> python3 kernel_mu.py gen3_B0.03_k1.5_v300.json` (all six runs; `<mu_f>` from the JSON), `python3 e11_ratio.py` | `results_kernel_mu.txt`, `results_e11_ratio.txt` | 3 s; 1 s |
| Amplitude scaling of the remainder | `MU_F=<mu_f> python3 e11_scaling.py <json>` | `results_e11_scaling.txt` | 3 s |
| Compact-pulse remainder (Section 4.4(d)) | `python3 e11_pulse_all.py` | `results_e11_pulse.txt` | 35 s |
| Pulse kernels at m_N = 1.4 .. 5 | `python3 kernel_mN.py <mN> <json>`, `python3 kernel_general.py 1.4 gen_B0.003_k1.5_A0_U1_w0.3_v250_mN1.4.json` | `results_kernel_mN.txt`, `results_mN1.4_tail250.txt` | 10 s |
| Shell model with the filtered flux (Section 4.7) | `python3 shell_kernel.py` (needs `../ori_model.py`) | `results_shell_kernel.txt` | 20 s-2 min |
| Table 4 (ray ODE against PDE mass) | `python3 ray_mass.py gen2_B0.03_k1.5_A0_U1_w0.3_v300.json` (also `k0.5`, `B0.003`) | `results_ray_mass_B*_k*.txt` | 10 s each |
| Ratio of the ODE deviation to the Romberg level spread at every integer v = 84..290 (the statistics quoted next to Table 4); new script written for the audit, no counterpart in the archive | `python3 ray_ratio_all_v.py` | `results_ray_ratio_all_v.txt` | 6 s |
| Stability of the starting point, noise of y | `python3 ray_stability.py gen2_B0.03_k1.5_A0_U1_w0.3_v300.json`, `python3 static_y_noise.py` | `results_ray_stability.txt`, `results_static_y_noise.txt` | 10 s; 1 s |
| Table 5 (constraint-projected mass) | `python3 e13_table.py` (rows to stdout and `frag11/rows.tex`) | `results_e13_table.txt` | 2-3 min |
| Per-run detail of Table 5, error constants | `python3 e13_all.py gen3_B0.03_k1.5_v300.json 2` (and the other runs, rays 2 and 0), `python3 e13_errconst.py gen3_B0.03_k1.5_v300.json 2` | `results_e13_B*_k*.txt`, `results_e13_errconst.txt` | 25 s; 7 s |
| Rate-only extension (q_M(3000)) | `python3 ray_rate_only.py` | `results_ray_rate_only.txt` | about 5 min (long) |
| Kernel-driven extension to v = 3000 | `python3 ray_extend.py gen3_B0.03_k1.5_v300.json > results_ray_extend_ext_def_B0.03_k1.5.txt`; with `KERNEL_MU=<mu_f>` for `..._ext_mu_...` | `results_ray_extend_*.txt`, `ray_extend_*.npz` | several min each (long) |
| (the curves of the figure) `ray_extend.py gen2_B0.03_k*_A0_U1_w0.3_v300.json` writes `ray_extend_B0.03_k*.npz`, which `ray_fig.py` reads; the gen3 runs of the same (B, k) are run with `NPZ_SUFFIX=_gen3` and write `ray_extend_B*_k*_gen3.npz`, so that they do not overwrite the gen2 curves | | | |
| Figure 2 (`fig_ray_mass.png`) and Figure 1 (`fig_e13.png`) | `python3 ray_fig.py`, `python3 e13_fig.py` (write to the current directory; copy to the repository root to rebuild the PDF) | `fig_ray_mass.png`, `fig_e13.png` | 2 s; 30 s |
| Exact (sympy) derivations: field equations dn1-dn3, constraints, ray equations, mu_v identity, y_c integral, EF wave equation, Frobenius series, T(0), Reissner-Nordstrom = Ori's b_0, q_M -> 2k+2 (each with a negative control) | `python3 sympy_checks.py` | `results_sympy_checks.txt` | 30 s |
| Horizons, kappa_pm and T(0) of the static holes (m_N = 5 .. 1.4), of the holes of mass parameter mu_f, M_cross, the extremal limit (50 digits) | `python3 static_hole.py` | `results_static_hole.txt` | 2 s |
| Local decay rates of phi_v of the source tests (Section 4.1; 0.0589 at v = 40) | `python3 phidecay.py <six JSON files>` (see `verify.py`) | `results_phidecay.txt` | 1 s |
| Linear-response test: the pulse kernel (B = 0.003) convolved with the tail at B = 0.03 against the measured flux (Section 4.7, `flux_nl.py`) | `python3 kernel_test.py` | `results_kernel_test.txt` | 10 s |
| Pulse kernel at B = 3e-4 and the m_N = 5 pulses at v_s = 30, 60 | `python3 kernel_mN.py 5 <json> <v_s>` | `results_kernel_B0003.txt`, `results_kernel_pulse_mN5_B0003.txt` | 20 s |
| Exact ray integration beyond v = 110 with the extrapolated sigma_v, phi_v; level agreement of the two highest Romberg levels (Section 5) | `python3 ray_long.py <gen2 or gen3 json>` | `results_ray_long_*.txt` | 10 s each |
| Does the exact ray integration reproduce the five-grid extrapolated PDE mass (110-runs, amplitude included)? | `python3 ray_validate.py gen2_B0.03_k1.5_A0_U1_w0.3_v110.json` (and `k0.5`) | `results_ray_validate.txt` | 10 s |
| Starting-point dependence of the constraint-projected mass | `python3 e13_v0.py` | `results_e13_v0.txt` | 1 min |
| Regeneration of a data set (two coarsest grids of `gen_B0.03_k1.5_A0_U1_w0.3_v110.json`; the finest grid and the v = 450 run in `--full`) compared with the shipped JSON | `verify.sh` (`gen.py` in `verification/tmp/`, then `regen_compare.py`) | `verification/logs/regen_*.log` | 10 s (finest: minutes) |
| Numbers of the paper that are ratios, maxima or bounds over the logs above | `paper_numbers.py`, `paper_numbers_kernel.py`, `paper_numbers_ray.py`, `paper_numbers_hist.py`, `../nonlinear/paper_numbers_nl.py` (print `VALUE <name> <x>`) | `results_paper_numbers*.txt` | 1 s each |
| Data sets (all JSON) | commands in `code/eh_init/MANIFEST.md` | `gen_*.json`, `gen2_*.json`, `gen3_*.json` | minutes to 35 min each |

Notes on reproducing the shipped outputs (full run, 2026-10-21, Python 3.13, numpy 2.5.3, scipy 1.18.1; the earlier 2026-10-20 check used a numpy stand-in for scipy and is superseded): all 1021 checks of that time pass (1054 now, see `PROVENANCE.md`). Logs that differ from the previously shipped ones were rewritten; the differences are
(i) removed timing fields (`t=...`) and pasted concatenations that are now produced by `verify.sh` with headers, (ii) round-off or noise-level quantities: `e13_all.py` (1e-13 level), `results_kernel_mu.txt` (k = 2, B = 0.03: 1.00620 -> 1.00621 at v = 100, 1.00578 -> 1.00579 at v = 290), `static_y_noise.py` (Romberg value, 3 grids, v = 60: -6.5248 in the earlier log -> -6.5258 now; noise of order 1 to 1e18 at v >= 60), `report_stream.py` (wide-seed run, window [84,88]: lambda-lambda'/lambda 0.6112 in the earlier log -> 0.6087 now; `report_stream.py` run on the shipped data gives 0.6087), the first-NaN positions of the blow-up runs (e.g. U = 3.640, v = 29.7 -> U = 3.637, v = 33.95 for the tail-only B = 0.05 run), (iii) corrections: `results_e11_scaling.txt`, B = 0.05, k = 3/2: the earlier line used an invalid final-hole root (r_- = 0.0557, ratio - 1 = 1.5e3); with the correct root r_- = 1.0233 and ratio - 1 = 2.37e-2 at v = 100 (the original `transfer_mu.py` is shipped as `code/eh_init/transfer_mu_original.py`), (iv) `results_seeded_identity_constraint.txt` is the original log of the archive again (the regenerated version had lost its second half); `muid.py` writes its first block to `results_muid_regen.txt`, (v) the `ray_extend` curves of the gen2 runs are the original files again and the gen3 curves have new names (see above). The full list of differences from the archive, with the evidence, is in `PROVENANCE.md`.

## Citation

See `CITATION.cff`. Please cite doi:10.5281/zenodo.23455605 and, for the companions, the DOIs above.
