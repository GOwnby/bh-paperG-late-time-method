# Code of Paper G

Python 3 + C. Everything needed to reproduce the numbers of the paper is in this repository (no sibling folders are needed).

## Dependencies

* Linux, gcc (tested: Ubuntu 22.04, gcc 11.4), Python >= 3.10 (tested 3.10.12).
* `pip install -r requirements.txt`: numpy >= 2.0 (tested 2.2.6; `np.trapezoid`), scipy (`solve_ivp` DOP853/LSODA, `brentq`, `CubicSpline`, `cumulative_trapezoid`, `least_squares`, `signal.fftconvolve`), matplotlib (tested 3.10.9).
* Windows: use WSL, or adapt `build.sh` (shared libraries are loaded with `ctypes` as `lib*.so` from the script directory).

## Build

```
sh code/build.sh
```

builds, with `gcc -O3 -shared -fPIC ... -lm` (no fast-math):

| library | source | loaded by |
|---|---|---|
| `eh_init/libdouble_null.so` | `eh_init/double_null.c` (stored-array evolution routine) | `dn2lib.py` |
| `eh_init/libstream.so` | `eh_init/stream.c` (two-row streaming copy, O(n_v) memory; bitwise identical output) | `dnU.py` (imported by `run_tail.py`, `gen.py`, `gen2.py`) |
| `eh_init/libstream2.so` | `eh_init/stream2.c` (streaming + row integral I(s)) | `gen3.py` |
| `nonlinear/libdouble_null.so` | `nonlinear/double_null.c` (identical file) | `nonlinear/dn2lib.py` |

The `.so` files are not shipped (they are ignored by `.gitignore`).

## Layout and conventions

* `ori_model.py`: the Ori thin-shell model, copied unchanged from the Paper E archive (doi:10.5281/zenodo.23455587). `eh_init/shell_kernel.py` and `nonlinear/run_rates.py`, `nonlinear/make_fig_nonlinear.py` import it from this directory.
* `eh_init/`: event-horizon-regular data, kernel, ray integration, constraint-projected mass (see `eh_init/README.md`). Run every script from `code/eh_init`; scripts read their JSON/NPY inputs from, and write their outputs to, the current directory
  (the figure scripts write `fig_e13.png`, `fig_ray_mass.png` there; copy them to the repository root to rebuild the PDF).
* `eh_init/MANIFEST.md`: the command that generated each `gen*_*.json` data set (several need minutes to tens of minutes on the finest grids). The JSON files are shipped, so the analysis scripts run without regenerating them.
* `nonlinear/`: the Section 2 validation runs (see `nonlinear/README.md`); run from `code/nonlinear`.
* Result files `results_*.txt` are the stdout of the script of the same stem (see the table in the top-level `README.md`); `e_*.log` are generator logs.

## Run times (one core, approximate)

Analysis scripts: 1 s to 30 s each (`e13_table.py`: 2-3 min for six runs; `e13_fig.py`: 30 s). `ray_rate_only.py` and `ray_extend.py` (integration to v = 3000): several minutes. `nonlinear/run_checks.py`: 6 min.
Data generation: see `eh_init/MANIFEST.md` (the finest-grid runs to v = 300 take 10-35 min). A fresh `gen3.py 0.03 1.5 0 1 0.3 110 0.05` (coarsest grid only) takes seconds and reproduces the shipped h = 0.05 data to 1e-10.

## Verification of this repository

`../verify.sh` (quick, default) recomputes every number quoted in `main.tex` from the shipped data and result logs and compares it with the paper; `../verify.sh --full` additionally re-runs every long script (data generation of the finest grid and of the v = 450 run, `ray_extend.py` to v = 3000, `ray_rate_only.py`, `nonlinear/run_checks.py`, `trace_residues.py`). Results and timings are in `../verification/REPORT.md`; the old-to-new differences of the regenerated logs are listed in the notes of the top-level `README.md`. The last full run (Python 3.13, numpy 2.5.3, scipy 1.18.1) passed 1021/1021 checks.
