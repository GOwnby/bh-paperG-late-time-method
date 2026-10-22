# Generating commands of the JSON data sets (Paper G)

All commands are run from this directory (`code/eh_init`) after `sh ../build.sh`.  Notation:

* `G5` = `0.05 0.025 0.0125 0.00625 0.003125`, `G4` = `0.05 0.025 0.0125 0.00625`, `G3` = `0.05 0.025 0.0125` (grid steps h_s = h_v).
* `gen.py B k A U0 w v1 h1 h2 ...` writes `gen_B<B>_k<k>_A<A>_U<U0>_w<w>_v<v1>[suffix].json` (M, sigma_v, phi_v on the rays U = 0.3, 0.6, 1.0, 1.2 for v = 20..v1-2).
  `A = 0` is tail-only data on H+; `A > 0` adds the seed (amplitude A, centre U0, width w).
* `gen2.py` takes the same arguments and also stores the eight evolved fields per ray (`gen2_*.json`); `gen3.py` stores the fields on the grid points of the coarsest grid
  and the row integral I(s) (`gen3_B<B>_k<k>_v<v1>.json`).
* Environment variables of `gen.py` / `gen2.py` (they add a suffix to the file name): `TAIL_PULSE=vs,ws` (Gaussian horizon-flux pulse of area -B instead of the power-law tail, suffix `_P<vs>_<ws>`),
  `TAIL_V0=V0` (tail (1+v/V0)^-k, suffix `_T<V0>`), `MN=m_N` (inner profile m_N, a_N = 2 m_N; suffix `_mN<m_N>`, absent for m_N = 5).
* Run times are for the finest grid on one core of an ordinary Linux machine and are approximate: G4 runs to v1 = 110: 1-2 min in total; v1 = 150: 2-3 min; v1 = 300: about 8 min
  for the finest grid of G4 and 10-35 min for G5 (35 min for the B = 0.003, k = 2, 3 runs of `gen3`); `gen3.py ... 450 G4`: 13 min for the finest grid.

## gen.py: tail-only data (A = 0)

| file | command |
|---|---|
| `gen_B0.03_k0.5_A0_U1_w0.3_v110.json` | `python3 gen.py 0.03 0.5 0 1 0.3 110 G5` |
| `gen_B0.03_k1.5_A0_U1_w0.3_v110.json` | `python3 gen.py 0.03 1.5 0 1 0.3 110 G5` |
| `gen_B0.05_k0.5_A0_U1_w0.3_v110.json` | `python3 gen.py 0.05 0.5 0 1 0.3 110 G5` |
| `gen_B0.05_k1.5_A0_U1_w0.3_v110.json` | `python3 gen.py 0.05 1.5 0 1 0.3 110 G5` |
| `gen_B0.003_k1.5_A0_U1_w0.3_v110.json`, `..._v150.json` | `python3 gen.py 0.003 1.5 0 1 0.3 110 G4` (and `150`) |
| `gen_B0.003_k0.5_A0_U1_w0.3_v300.json`, `gen_B0.003_k1.5_A0_U1_w0.3_v300.json` | `python3 gen.py 0.003 <k> 0 1 0.3 300 G4` |
| `gen_B0.003_k1.5_A0_U1_w0.3_v250_mN1.4.json` | `MN=1.4 python3 gen.py 0.003 1.5 0 1 0.3 250 G4` |
| `gen_B0.03_k1.5_A0_U1_w0.3_v110_T0.3.json`, `..._T10.json` | `TAIL_V0=0.3 python3 gen.py 0.03 1.5 0 1 0.3 110 G4` (and `TAIL_V0=10`) |

## gen.py: seeded data (A > 0)

| file | command |
|---|---|
| `gen_B0.03_k{0.5,1.5}_A0.02_U1_w0.3_v110.json`, `gen_B0.03_k2.5_A0.02_U1_w0.3_v110.json` | `python3 gen.py 0.03 <k> 0.02 1 0.3 110 G5` |
| `gen_B0.03_k1.5_A0.02_U0.7_w0.2_v110.json`, `gen_B0.03_k1.5_A0.02_U1_w0.5_v110.json` | `python3 gen.py 0.03 1.5 0.02 <U0> <w> 110 G5` |
| `gen_B0.03_k1.5_A0.01_U1_w0.3_v110.json`, `gen_B0.03_k1.5_A0.03_U0.6_w0.3_v110.json` | `python3 gen.py 0.03 1.5 <A> <U0> 0.3 110 G4` |
| `gen_B0.03_k0.5_A0.02_U1_w0.3_v70.json` | `python3 gen.py 0.03 0.5 0.02 1 0.3 70 G3` |
| `gen_B0_k1.5_A0.02_U0.7_w0.2_v110.json`, `gen_B0_k1.5_A0.02_U1_w0.3_v110.json` | `python3 gen.py 0 1.5 0.02 <U0> <w> 110 G4` |

## gen.py: compact horizon-flux pulses (kernel and matching-factor tests)

`TAIL_PULSE=<vs>,2 python3 gen.py <B> 1.5 0 1 0.3 <v1> G4`, file suffix `_P<vs>_2`:

| file | `<B>`, `<v1>`, `<vs>` |
|---|---|
| `gen_B0.003_k1.5_A0_U1_w0.3_v110_P3_2.json`, `..._P10_2.json` | 0.003, 110, 3 and 10 |
| `gen_B0.003_k1.5_A0_U1_w0.3_v150_P10_2.json`, `..._P30_2.json`, `..._P60_2.json` | 0.003, 150, 10, 30, 60 |
| `gen_B0.0003_k1.5_A0_U1_w0.3_v110_P10_2.json` | 0.0003, 110, 10 |
| `gen_B0.0003_k1.5_A0_U1_w0.3_v150_P30_2.json`, `..._P60_2.json` | 0.0003, 150, 30 and 60 |
| `gen_B0.03_k1.5_A0_U1_w0.3_v110_P10_2.json`, `..._P30_2.json` | 0.03, 110, 10 and 30 |
| `gen_B0.003_k1.5_A0_U1_w0.3_v150_mN<m>_P40_2.json`, m = 1.4, 1.6, 2, 3 | `MN=<m> TAIL_PULSE=40,2 python3 gen.py 0.003 1.5 0 1 0.3 150 G4` |

## gen2.py (all eight fields per ray; input of the exact ray integration)

| file | command |
|---|---|
| `gen2_B0.03_k{0.5,1.5}_A0_U1_w0.3_v300.json` | `python3 gen2.py 0.03 <k> 0 1 0.3 300 G5` |
| `gen2_B0.003_k{0.5,1.5}_A0_U1_w0.3_v300.json` | `python3 gen2.py 0.003 <k> 0 1 0.3 300 G5` |
| `gen2_B0.03_k{0.5,1.5}_A0_U1_w0.3_v110.json` | `python3 gen2.py 0.03 <k> 0 1 0.3 110 G5` |
| `gen2_B0.03_k1.5_A0_U1_w0.3_v80.json` | `python3 gen2.py 0.03 1.5 0 1 0.3 80 0.2 0.1 0.05` |
| `gen2_B0_k1.5_A0_U1_w0.3_v110.json` (static interior, input of `static_y_noise.py`) | `python3 gen2.py 0 1.5 0 1 0.3 110 G3` (23 s) |

## gen3.py (row integral; input of the constraint-projected mass)

| file | command |
|---|---|
| `gen3_B0.03_k{0.5,1.5,2,3}_v300.json` | `python3 gen3.py 0.03 <k> 0 1 0.3 300 G5` |
| `gen3_B0.003_k{0.5,1.5,2,3}_v300.json` | `python3 gen3.py 0.003 <k> 0 1 0.3 300 G5` |
| `gen3_B0.003_k1.5_v450.json` (flux to v = 420, `e12_ratio.py`) | `python3 gen3.py 0.003 1.5 0 1 0.3 450 G4` |
| `gen3_B0.03_k1.5_v110.json` | `python3 gen3.py 0.03 1.5 0 1 0.3 110 G4` |

(`gen3.py` places the ray positions on grid points of the coarsest grid; a fresh `gen3.py 0.03 1.5 0 1 0.3 110 0.05` reproduces the h = 0.05 data of the shipped file to 1e-10.)

## Scripts that need a number from the data by hand

`MU_F=<mu_f> python3 e11_pulse.py <json> <v_s>`, `MU_F=<mu_f> python3 kernel_mu.py <gen3 json>`, `MU_F=<mu_f> python3 e11_scaling.py <json>`: `<mu_f>` is the key `mu_f` of the JSON
(printed by the generator as `done mu_f=...`).  `e11_pulse_all.py` reads it from the JSON itself and regenerates `results_e11_pulse.txt`.
`ray_extend.py` takes `KERNEL_MU=<mu_f>` to use the kernel of the final hole.  The cache files `K_mu_<value>.npy` written by `kernel_lib_mu.py` are not shipped.

## Regeneration test (verify.sh)

`verify.sh` regenerates, in `verification/tmp/` (the shipped data are not overwritten), the two coarsest grids of `gen_B0.03_k1.5_A0_U1_w0.3_v110.json`
(`python3 gen.py 0.03 1.5 0 1 0.3 110 0.05 0.025`) and compares them with the shipped file: bitwise identical on the machines tested.  `verify.sh --full` also regenerates the finest grid
(`gen.py 0.03 1.5 0 1 0.3 110 0.003125`, `gen3.py 0.003 1.5 0 1 0.3 450 0.00625`) and compares those columns.  (`gen.py` and `gen3.py` write to the current directory.)
