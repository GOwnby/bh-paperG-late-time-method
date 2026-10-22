# Provenance of this repository (Paper G)

Written for review. It states what in this repository is the author's original material, what differs from it and why, what has no original, and what was re-run from the original code. Statements are backed by a run or a byte comparison; "evidence" names it. Nothing here is a new physical result.

## 0 Baselines used in this file

Three states are compared: (1) the author's tree `old_archive/1_sources/sources/<paper>`; (2) the first Zenodo release (the initial git commit of this repository); (3) the current repository. On 2026-10-21 (1) and (2) were compared byte for byte: they are identical except for the repository metadata (`.gitignore`, `.zenodo.json`, `CITATION.cff`), the compiled PDF and a `code/` directory. The rest of the old archive (`old_archive/2_docs_and_archive_1/archive/`: earlier manuscript versions, session logs, audit directories) was searched for code and data behind this paper's results; files found there that are not in the Zenodo release are listed below where they matter. Wherever this file says "original" or "v1.0.1" it means (1) = (2).

## 1 Lineage

* Paper G (late-time method) was split from Paper E (inner horizon, 39 pages, 2026-10-10). The code of both lived in the Paper E bundle (`code/eh_init`; Zenodo doi:10.5281/zenodo.23455587, v1.0.1). The earlier Paper G archive contained only `main.tex`, `main.bbl`, `references.bib`, the two figures and a README.
* This repository (v1.1.0, 2026-10-20) copies that code, adds generators and checks, regenerates logs, and has a self-verification (`verify.sh`). Of the 321 files under `code/`, 234 are byte-identical to the Paper E code, 41 differ, 46 have no counterpart.
* Compared on 2026-10-21 by an audit (Claude, for the author): the Paper E code `code/` against this repository file by file (`cmp`; logs by number-by-number comparison), the old and new `main.tex` word by word, 5 reproductions with the ORIGINAL scripts (section 5). `verification/REPORT_full.md` records the `--full` run of 2026-10-21 (18312 s); it was written before the corrections of section 4, so its PASS* rows are those corrections.
* Policy: original results and scripts are not replaced silently. Class a = cosmetic (paths, comments, timing, formatting); b = bug fix; c = additive output or a changed driver. Where an original is useful next to a fix it is shipped (`*_original.py`).

## 2 Files that differ from the original

| path | class | what changed | evidence |
|---|---|---|---|
| `code/ori_model.py` | a, restored | the repository had 2 added header lines claiming "copied unchanged"; the original bytes are restored, the README statement is now true | `cmp` with Paper E `code/ori_model.py`: identical |
| `eh_init/transfer_mu.py` | b | selects r_-, r_+ as the two LARGEST roots of the quartic (`idx[-2]`, `idx[-1]`) instead of the two smallest: for mu > 0.0278 the quartic has a third root r_s ~ 2 mu | B=0.05, k=3/2 (mu_f=0.0278): original gives r_-=0.0557, kappa_-=-8.895, T(0)=169.3; fixed gives r_-=1.023269, kappa_-=0.763567, T(0)=47.8247 (`out/G/spot_e11_scaling_*`); identical for all mu_f < 0.0278 (all other lines of `results_e11_scaling.txt` unchanged) |
| `eh_init/transfer_mu_original.py` | original | the archive file, shipped to reproduce the archive value | byte-identical to the archive |
| `eh_init/shell_kernel.py` | a | `sys.path` insert so that `import ori_model` finds `code/` | 2 lines; the archive relied on an unstated PYTHONPATH |
| `eh_init/aniso.py` | c | prints one extra summary line (ratios mu/(h_s^2+h_v^2)); table unchanged | log numbers identical (43 of 43); the summary line replaces a hand-typed one that read 1.72e-3, 1.51e-3 where the script gives 1.73e-3, 1.49e-3 |
| `eh_init/conv1.py`, `t_static4.py` | a | wall time printed to stderr instead of stdout (logs reproducible) | diff: 2 lines each |
| `eh_init/kernel_mN.py` | a | formatting of the tau list in one printed line | diff: 1 line |
| `eh_init/kernel_vs_long.py` | a | 3 comment lines "SUPERSEDED, not used" | not used for any number of the paper |
| `eh_init/e13_table.py` | c | usage text, optional case arguments, prints the rows, `VALUE e13_*` lines, `os.makedirs` | original and modified write identical `frag11/rows.tex` (8 s each), equal to the row of Table 5 (`out/G/spot_e13_table_*`) |
| `eh_init/ray_extend.py` | a | environment variable `NPZ_SUFFIX` appended to the `.npz` name (default: unchanged behavior) | rerun with and without it (section 5) |
| `eh_init/ray_extend_B0.03_k{0.5,1.5}.npz`, `ray_extend_B0.003_k{0.5,1.5}.npz` | restored | the `--full` run had overwritten the gen2 curves by those of the gen3 runs of the same (B,k); the originals are restored | gen2 `ray_extend.py` rerun reproduces the archive file with max rel. difference 0.0; `ray_fig.py` on the restored files reproduces `fig_ray_mass.png` (pixel-identical to the figure of the earlier archive, max difference 0.0), on the overwritten files it did not (108443 pixels differ) |
| `eh_init/ray_extend_B*_k*_gen3.npz` (4 files) | new names | the gen3 curves, formerly under the names above; `verify.py` now runs these steps with `NPZ_SUFFIX=_gen3` | gen3 rerun reproduces the shipped file (difference 0.0) and leaves the gen2 file untouched |
| `eh_init/ray_extend_B0.003_k{2,3}_mu.npz` | a | regenerated by the full run | max relative difference to the archive 3.7e-12 and 9.3e-11; kept |
| `eh_init/results_seeded_identity_constraint.txt` | restored | the regenerated version (24 lines) had lost the constraint-residual blocks and the `seed5` stdout of the archive log (55 lines) | the first block of the archive log is byte-identical to the output of `muid.py` (rerun); `muid.py` now writes `results_muid_regen.txt`, checked against the original block (`hist_muid_regen`) |
| 20 further `results_*.txt`, `checks_nonlinear.json`, `validation_nonlinear.json` | a / see 4 | regenerated by the `--full` run | `out/G/modified_logs_numdiff.txt`: 14 of the 21 logs (incl. the restored one) differ in no number (timing removed, formatting, pasted blocks, two completed tracebacks in `results_e11_pulse.txt`); the other 6 are in section 4 |
| `README.md`, `code/eh_init/README.md`, `code/README.md`, `nonlinear/README.md`, `verify.py`, `verification/expected.py` | a / c | documentation; verification code (see 6); two reversed old->new notes and the "0 SKIPPED" statement corrected | this file |

## 3 Files without an original

| path | what it generates | basis | quoted numbers that depend on it |
|---|---|---|---|
| `eh_init/static_hole.py` | `results_static_hole.txt`: horizons, kappa_pm, T(0) at 50 digits, holes of mass mu_f | closed-form quartic, mpmath | r_-, r_+, kappa_pm, T(0)=44.3045, T(0) of the final holes, r_-=1.023 (checked here against `transfer.py`, which prints the same values: `out/G/spot_transfer.txt`) |
| `eh_init/sympy_checks.py` | exact derivations of field equations, ray equations, mu_v identity, Frobenius solution, T(0) | sympy | Sec. 2 equations (not rerun by the audit: sympy absent) |
| `eh_init/table_eh.py` | Table 1 | the archive's `analyze.py` on the JSON data | percentages of Table 1; the audit's own five-grid computation reproduces all, the only change of the text is 0.80% -> 0.79% |
| `eh_init/kernel_sensitivity.py` | variants of the kernel (variance, fit window) | `kernel_analytic.py` machinery | the 1.2e-3 statement |
| `eh_init/e13_v0.py`, `e11_pulse_all.py`, `regen_compare.py` | start-point dependence; the whole `results_e11_pulse.txt`; regeneration test of data | archive scripts called in a loop | 1e-10 bound; pulse remainders (0.25 to 6 mu_f); data regeneration |
| `eh_init/paper_numbers*.py`, `nonlinear/paper_numbers_nl.py` | ratios, maxima, bounds parsed from the logs | the logs and JSON data | any number that is not a line of a log; they are not independent of the logs they parse |
| `eh_init/ray_ratio_all_v.py`, `results_ray_ratio_all_v.txt` | ratio of the ODE deviation to the Romberg level spread at every integer v (the same quantity as `ray_mass.py`, block [B]) | `analyze.extrap`, `raylib.integrate` of the archive | the statistics next to Table 4, abstract, Fig. 4 caption; 6 s |
| `eh_init/results_muid_regen.txt`, `build.sh`, `MANIFEST.md`, `requirements.txt` | regenerated block; build; commands of the data sets | -- | -- |
| 21 `results_*.txt` of archive scripts (`kernel_test`, `phidecay`, `ray_long_*`, `ray_validate`, ...) | logs the archive did not store | the unmodified archive scripts | `phidecay.py` (P10 pulse) rerun: 0.0589 |
| `eh_init/gen2_B0_k1.5_A0_U1_w0.3_v110.json`; 9 `ray_extend_*_mu.npz`, `ray_extend_B0.03_k{2,3}.npz` | data / curves of the full run | `gen2.py`, `ray_extend.py` of the archive | `static_y_noise.py` (Sec. 3); Sec. 5 extension beyond v=250 |

## 4 Results that changed relative to the original

* B=0.05, k=3/2 (Sec. 4.3(d)): the archive log had r_-=0.0557 and ratio-1 = 1.5e3 (wrong root, see 2). Corrected log: r_-=1.0233, ratio-1 = 2.37e-2 at v=100 (0.85 mu_f; 3.3 times the B=0.03 value against 2.78 for B^2). The text said "excluded ... we did not compute"; it now gives the computed number.
* Statements of the earlier Paper G text that the audit found false or unsupported, now corrected in `main.tex` (checks in `expected.py`): final mass parameter of the v_s=60 pulse 8.5e-4 -> 2.1e-3 (8.5e-4 is the v_s=10 run); constancy of the final-hole ratio 1e-5 -> 7e-5 (k=3/2) and 1.4e-4 (k=2,3); share of the excess accounted for 46% -> 47% (k=1/2); B^2 scaling "to three digits" -> within 3%; level spread of sigma_v quoted as 1.2e-8 -> 2e-13 (1.2e-8 is phi_v); 8e-9 -> 8.3e-9; 1e-3 -> 1.4e-3; 0.6% -> 0.5%; 1e-5 -> 2e-3; r_-=0.056 -> 1.023; decay rate 0.0594 -> 0.0589 (the old value is not reproducible: `phidecay.py` gives 0.0589); 0.80% -> 0.79%.
* "level spread understates the error by at least 8 at every v" (earlier: "two to three orders of magnitude"): true at the 10 rows of Table 4 (smallest about 8), not at every v. Over all integer v=84..290 the ratio has median 154 (k=3/2) and 136 (k=1/2), minimum 0.23 (v=272) and 0.77 (v=223), each within 2 of a sign change of M_ODE-M_PDE; at B=0.003 the median is 4.3 and 8.3. The text now says this (`results_ray_ratio_all_v.txt`).
* "no parameter fitted" (kernel): the pole-tail coefficients are fitted to the ODE kernel itself and the numerical choices change the prediction by up to 1.2e-3, more than the 4e-4 agreement of the baseline; the abstract and Secs. 4.3(b), 5 now say so (`results_kernel_sensitivity.txt`).
* sigma_v level spread: 2e-13 at the printed v; at worst over every integer 60<=v<=290: 5.1e-13 (k=3/2), 1.1e-12 (k=1/2), 2.5e-12 (B=0.003). "which therefore does not exclude them" is replaced by: the agreement of two levels is not an error bound; attribution of the residual to delta sigma_v is a hypothesis.
* Regenerated logs (timing removed, round-off): `static_y_noise` Romberg value -6.5248 -> -6.5258, `report_stream` 0.6112 -> 0.6087 (the script on the shipped data gives 0.6087), `kernel_mu` 1.00620 -> 1.00621, first-NaN positions of blow-up runs U=3.640 -> 3.637 (the paper quotes U_c to 2 digits: 3.6). `results_e11_pulse.txt`: the archive log ended two runs in `IndexError` tracebacks; the regenerated log is complete.

## 5 What reproduces from the ORIGINAL code (runs of 2026-10-21, one core, no `verify.py`)

| original script | time | result |
|---|---|---|
| `e11_ratio.py`, `e12_ratio.py` | 2.7 s, 1.9 s | logs identical to the shipped ones |
| `kernel_analytic.py` | 29 s | identical (4e-4 agreement at B=0.003) |
| `ray_mass.py` B=0.03, k=3/2 | 6.8 s | byte-identical to `results_ray_mass_B0.03_k1.5.txt` (6e-5 of Table 4) |
| `e13_all.py` B0.03_k1.5, ray 2; `e13_table.py` | 15 s; 8 s | -3.34e-7 at v=280; same rows as the modified script, equal to Table 5 |
| `ray_extend.py` gen2 B0.03_k1.5 | 93 s | archive `.npz` reproduced exactly (difference 0.0), log identical |
| `muid.py` | 11 s | byte-identical to the first block of the archive log |
| `transfer.py` | killed at 180 s | header (r_-, r_+, kappa_-, T(0)) equals the abstract; not completed |
| `e11_scaling.py` B=0.05, k=3/2, original vs fixed `transfer_mu` | 10.5 s, 8.1 s | r_-=0.0557, ratio-1=1.5e3 (wrong) vs r_-=1.0233, ratio-1=2.37e-2 |
| `report_stream.py`; `phidecay.py` (P10) | 0.6 s; 1 s | 0.6087; 0.0589 |
| `ray_fig.py` on the restored `.npz` | 4 s | `fig_ray_mass.png` pixel-identical |
| five-grid computation of Table 1 | 2 s | all percentages reproduce (0.79% for 0.80%) |

`verify.py --quick` with the changes of this document (container without sympy and mpmath, 511 s): 970 checks PASS, 0 FAIL, 84 SKIPPED (the checks that read `sympy_checks` and `static_hole`; their shipped logs are unchanged); 0 PASS*.

Not rerun: `e13_all.py` for the other seven runs, the finest-grid regeneration of the data (10-35 min each), `ray_extend`/`ray_rate_only` for other cases, `transfer.py` to the end, `sympy_checks.py`, `static_hole.py` (no sympy/mpmath here). Their logs are those of the `--full` run.

## 6 Known limits

* Quick mode (`sh verify.sh`) skips 43 of 94 steps ("full mode only"); the checks that use their logs read the logs as shipped (written by `--full`) and count as passed. `REPORT.md` states both numbers.
* Tolerances: of the 1021 earlier checks 814 compare to the printed digits; 128 `abs`, 38 `eq` (integers), 32 `le`, 5 `ge`, 4 `rel`, each with its reason (`out/G/tolerances_non_round.csv`). The paper values in `expected.py` are typed by hand; `REPORT.md` lists which of them do not occur verbatim in `main.tex` (21 of 1054, bounds or rounded values).
* The Romberg level spread is not an error bound (shown in Sec. 5); the converged mass is established by the independent constraint-projected mass, to 1e-6 to 1e-7 in ln M, not by the extrapolation.
* The kernel is tested to 1.2e-3 (numerical choices), not to the 4e-4 of the baseline; the flux beyond v=250 at B=0.03 is a linear-response model; the closure is additive; nothing here addresses extendibility (all stated in the paper).
* The cause of the residual disagreement of the ray ODE with the projected mass (delta sigma_v of order 1e-9) is a hypothesis.
* Data sets (`gen*.json`) are shipped; quick mode regenerates only the two coarsest grids of one set (agreement 1e-10).
