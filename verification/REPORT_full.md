# Verification report (bh-paperG-late-time-method)

Mode: **full**.  Date: 2026-10-21 08:35:59.  Total wall time: 18312 s.

Checks: **1021 PASS (of which 13 PASS* = manuscript text to be corrected), 0 FAIL, 0 SKIPPED**; steps failed: none.

## Environment

| item | value |
|---|---|
| platform | Linux-6.18.44-fc-v139-x86_64-with-glibc2.39 |
| python | 3.13.16 (/usr/bin/python3) |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| sympy | 1.14.0 |
| mpmath | 1.3.0 |
| matplotlib | 3.11.2 |
| gcc | gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| cpu count | 2 |

## Steps

| step | command | status | wall (s) | cpu (s) | output file refreshed | log |
|---|---|---|---|---|---|---|
| build_c_libs | `sh code/build.sh` (in `.`) | OK | 4.2 | 0.8 |  | `verification/logs/build_c_libs.log` |
| sympy_checks | `sympy_checks.py` (in `code/eh_init`) | OK | 37.8 | 7.8 | `results_sympy_checks.txt` | `verification/logs/sympy_checks.log` |
| static_hole | `static_hole.py` (in `code/eh_init`) | OK | 2.4 | 0.5 | `results_static_hole.txt` | `verification/logs/static_hole.log` |
| check_field_equations | `check_field_equations.py` (in `code/eh_init`) | OK | 1.7 | 0.4 | `results_check_field_equations.txt` | `verification/logs/check_field_equations.log` |
| nl_validation | `run_validation.py` (in `code/nonlinear`) | OK | 38.3 | 8.8 |  | `verification/logs/nl_validation.log` |
| nl_checks | `run_checks.py` (in `code/nonlinear`) | OK | 837.0 | 222.7 |  | `verification/logs/nl_checks.log` |
| paper_numbers_nl | `paper_numbers_nl.py` (in `code/nonlinear`) | OK | 0.1 | 0.0 | `results_paper_numbers_nl.txt` | `verification/logs/paper_numbers_nl.log` |
| table_eh | `table_eh.py` (in `code/eh_init`) | OK | 0.4 | 0.2 | `results_table_eh.txt` | `verification/logs/table_eh.log` |
| report_stream | `report_stream.py` (in `code/eh_init`) | OK | 0.6 | 0.2 | `results_stream_5grid.txt` | `verification/logs/report_stream.log` |
| paper_numbers | `paper_numbers.py` (in `code/eh_init`) | OK | 1.2 | 0.5 | `results_paper_numbers.txt` | `verification/logs/paper_numbers.log` |
| static_y_noise | `static_y_noise.py` (in `code/eh_init`) | OK | 0.5 | 0.2 | `results_static_y_noise.txt` | `verification/logs/static_y_noise.log` |
| phidecay | `phidecay.py gen_B0_k1.5_A0.02_U0.7_w0.2_v110.json gen_B0_k1.5_A0.02_U1_w0.3_v110.json gen_B0.03_k1.5_A0_U1_w0.3_v110.json gen_B0.03_k1.5_A0_U1_w0.3_v110_T0.3.json gen_B0.03_k1.5_A0_U1_w0.3_v110_T10.json gen_B0.03_k1.5_A0_U1_w0.3_v110_P10_2.json` (in `code/eh_init`) | OK | 0.6 | 0.2 | `results_phidecay.txt` | `verification/logs/phidecay.log` |
| regen_gen_coarse | `../../../code/eh_init/gen.py 0.03 1.5 0 1 0.3 110 0.05 0.025` (in `verification/tmp/regen`) | OK | 28.4 | 10.5 |  | `verification/logs/regen_gen_coarse.log` |
| regen_compare_coarse | `regen_compare.py ../../verification/tmp/regen/gen_B0.03_k1.5_A0_U1_w0.3_v110.json gen_B0.03_k1.5_A0_U1_w0.3_v110.json` (in `code/eh_init`) | OK | 0.5 | 0.2 |  | `verification/logs/regen_compare_coarse.log` |
| regen_gen_finest | `../../../code/eh_init/gen.py 0.03 1.5 0 1 0.3 110 0.003125` (in `verification/tmp/regen_finest`) | OK | 661.4 | 241.8 |  | `verification/logs/regen_gen_finest.log` |
| regen_compare_finest | `regen_compare.py ../../verification/tmp/regen_finest/gen_B0.03_k1.5_A0_U1_w0.3_v110.json gen_B0.03_k1.5_A0_U1_w0.3_v110.json` (in `code/eh_init`) | OK | 0.7 | 0.2 |  | `verification/logs/regen_compare_finest.log` |
| regen_gen3_v450_finest | `../../../code/eh_init/gen3.py 0.003 1.5 0 1 0.3 450 0.00625` (in `verification/tmp/regen_v450`) | OK | 4581.6 | 1307.1 |  | `verification/logs/regen_gen3_v450_finest.log` |
| regen_compare_v450 | `regen_compare.py ../../verification/tmp/regen_v450/gen3_B0.003_k1.5_v450.json gen3_B0.003_k1.5_v450.json` (in `code/eh_init`) | OK | 1.4 | 0.3 |  | `verification/logs/regen_compare_v450.log` |
| trace_residues_mN5 | `trace_residues.py 5` (in `code/eh_init`) | OK | 1066.3 | 235.7 | `results_trace_residues_mN5.txt` | `verification/logs/trace_residues_mN5.log` |
| trace_residues_mN1.4 | `trace_residues.py 1.4` (in `code/eh_init`) | OK | 532.2 | 131.6 | `results_trace_residues_mN1.4.txt` | `verification/logs/trace_residues_mN1.4.log` |
| kernel_ft2 | `kernel_ft2.py` (in `code/eh_init`) | OK | 16.0 | 3.9 | `results_kernel_ft.txt` | `verification/logs/kernel_ft2.log` |
| kernel_analytic | `kernel_analytic.py` (in `code/eh_init`) | OK | 80.8 | 19.5 | `results_kernel_analytic.txt` | `verification/logs/kernel_analytic.log` |
| kernel_sensitivity | `kernel_sensitivity.py` (in `code/eh_init`) | OK | 18.6 | 4.6 | `results_kernel_sensitivity.txt` | `verification/logs/kernel_sensitivity.log` |
| longrun | `longrun.py gen_B0.003_k0.5_A0_U1_w0.3_v300.json gen_B0.003_k1.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 0.8 | 0.2 | `results_longrun_v300.txt` | `verification/logs/longrun.log` |
| crossover_analytic | `crossover_analytic.py` (in `code/eh_init`) | OK | 282.6 | 68.6 | `results_crossover_analytic.txt` | `verification/logs/crossover_analytic.log` |
| flux_nl | `flux_nl.py` (in `code/eh_init`) | OK | 2.3 | 0.6 | `results_flux_nl.txt` | `verification/logs/flux_nl.log` |
| kernel_test | `kernel_test.py` (in `code/eh_init`) | OK | 1.2 | 0.3 | `results_kernel_test.txt` | `verification/logs/kernel_test.log` |
| kernel_mN | `kernel_mN.py 1.4 gen_B0.003_k1.5_A0_U1_w0.3_v150_mN1.4_P40_2.json ; kernel_mN.py 1.6 gen_B0.003_k1.5_A0_U1_w0.3_v150_mN1.6_P40_2.json ; kernel_mN.py 2 gen_B0.003_k1.5_A0_U1_w0.3_v150_mN2_P40_2.json ; kernel_mN.py 3 gen_B0.003_k1.5_A0_U1_w0.3_v150_mN3_P40_2.json` (in `code/eh_init`) | OK | 91.1 | 22.0 | `results_kernel_mN.txt` | `verification/logs/kernel_mN.log` |
| kernel_pulse_mN5 | `kernel_mN.py 5 gen_B0.003_k1.5_A0_U1_w0.3_v150_P30_2.json 30 ; kernel_mN.py 5 gen_B0.003_k1.5_A0_U1_w0.3_v150_P60_2.json 60` (in `code/eh_init`) | OK | 33.8 | 8.0 | `results_kernel_pulse_mN5_B0003.txt` (changed) | `verification/logs/kernel_pulse_mN5.log` |
| kernel_B0003 | `kernel_mN.py 5 gen_B0.0003_k1.5_A0_U1_w0.3_v150_P60_2.json 60` (in `code/eh_init`) | OK | 15.6 | 3.8 | `results_kernel_B0003.txt` (changed) | `verification/logs/kernel_B0003.log` |
| kernel_general_mN1.4 | `kernel_general.py 1.4 gen_B0.003_k1.5_A0_U1_w0.3_v250_mN1.4.json` (in `code/eh_init`) | OK | 28.1 | 6.8 | `results_mN1.4_tail250.txt` | `verification/logs/kernel_general_mN1.4.log` |
| e12_ratio | `e12_ratio.py` (in `code/eh_init`) | OK | 4.1 | 1.0 | `results_e12_ratio.txt` | `verification/logs/e12_ratio.log` |
| e11_ratio | `e11_ratio.py` (in `code/eh_init`) | OK | 6.7 | 1.7 | `results_e11_ratio.txt` | `verification/logs/e11_ratio.log` |
| kernel_mu | `kernel_mu.py gen3_B0.03_k1.5_v300.json ; kernel_mu.py gen3_B0.03_k0.5_v300.json ; kernel_mu.py gen3_B0.003_k1.5_v300.json ; kernel_mu.py gen3_B0.003_k0.5_v300.json ; kernel_mu.py gen3_B0.03_k2_v300.json ; kernel_mu.py gen3_B0.03_k3_v300.json ; kernel_mu.py gen3_B0.003_k2_v300.json ; kernel_mu.py gen3_B0.003_k3_v300.json` (in `code/eh_init`) | OK | 129.2 | 31.3 | `results_kernel_mu.txt` | `verification/logs/kernel_mu.log` |
| e11_scaling | `e11_scaling.py gen_B0.003_k1.5_A0_U1_w0.3_v110.json ; e11_scaling.py gen_B0.03_k1.5_A0_U1_w0.3_v110.json ; e11_scaling.py gen_B0.05_k1.5_A0_U1_w0.3_v110.json ; e11_scaling.py gen_B0.03_k0.5_A0_U1_w0.3_v110.json ; e11_scaling.py gen_B0.05_k0.5_A0_U1_w0.3_v110.json` (in `code/eh_init`) | OK | 79.8 | 19.4 | `results_e11_scaling.txt` | `verification/logs/e11_scaling.log` |
| e11_pulse_all | `e11_pulse_all.py` (in `code/eh_init`) | OK | 265.9 | 65.0 | `results_e11_pulse.txt` (changed) | `verification/logs/e11_pulse_all.log` |
| shell_kernel | `shell_kernel.py` (in `code/eh_init`) | OK | 50.2 | 12.1 | `results_shell_kernel.txt` | `verification/logs/shell_kernel.log` |
| ray_mass_B0.03_k1.5 | `ray_mass.py gen2_B0.03_k1.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 20.0 | 4.8 | `results_ray_mass_B0.03_k1.5.txt` | `verification/logs/ray_mass_B0.03_k1.5.log` |
| ray_mass_B0.03_k0.5 | `ray_mass.py gen2_B0.03_k0.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 19.4 | 4.7 | `results_ray_mass_B0.03_k0.5.txt` | `verification/logs/ray_mass_B0.03_k0.5.log` |
| ray_mass_B0.003_k1.5 | `ray_mass.py gen2_B0.003_k1.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 17.1 | 4.1 | `results_ray_mass_B0.003_k1.5.txt` | `verification/logs/ray_mass_B0.003_k1.5.log` |
| ray_mass_B0.003_k0.5 | `ray_mass.py gen2_B0.003_k0.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 16.2 | 3.9 | `results_ray_mass_B0.003_k0.5.txt` | `verification/logs/ray_mass_B0.003_k0.5.log` |
| ray_stability | `ray_stability.py gen2_B0.03_k1.5_A0_U1_w0.3_v300.json ; ray_stability.py gen2_B0.003_k1.5_A0_U1_w0.3_v300.json ; ray_stability.py gen2_B0.03_k0.5_A0_U1_w0.3_v300.json ; ray_stability.py gen2_B0.003_k0.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 55.7 | 13.6 | `results_ray_stability.txt` | `verification/logs/ray_stability.log` |
| ray_long_B0.03_k1.5 | `ray_long.py gen2_B0.03_k1.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 10.7 | 2.6 | `results_ray_long_B0.03_k1.5.txt` | `verification/logs/ray_long_B0.03_k1.5.log` |
| ray_long_B0.03_k0.5 | `ray_long.py gen2_B0.03_k0.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 8.8 | 2.1 | `results_ray_long_B0.03_k0.5.txt` | `verification/logs/ray_long_B0.03_k0.5.log` |
| ray_long_B0.003_k1.5 | `ray_long.py gen2_B0.003_k1.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 9.5 | 2.2 | `results_ray_long_B0.003_k1.5.txt` | `verification/logs/ray_long_B0.003_k1.5.log` |
| ray_long_B0.003_k0.5 | `ray_long.py gen2_B0.003_k0.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 8.8 | 2.1 | `results_ray_long_B0.003_k0.5.txt` | `verification/logs/ray_long_B0.003_k0.5.log` |
| ray_long_gen3_B0.03_k1.5 | `ray_long.py gen3_B0.03_k1.5_v300.json` (in `code/eh_init`) | OK | 10.2 | 2.4 | `results_ray_long_gen3_B0.03_k1.5.txt` | `verification/logs/ray_long_gen3_B0.03_k1.5.log` |
| ray_long_gen3_B0.03_k0.5 | `ray_long.py gen3_B0.03_k0.5_v300.json` (in `code/eh_init`) | OK | 8.8 | 2.1 | `results_ray_long_gen3_B0.03_k0.5.txt` | `verification/logs/ray_long_gen3_B0.03_k0.5.log` |
| ray_long_gen3_B0.03_k2 | `ray_long.py gen3_B0.03_k2_v300.json` (in `code/eh_init`) | OK | 11.0 | 2.6 | `results_ray_long_gen3_B0.03_k2.txt` | `verification/logs/ray_long_gen3_B0.03_k2.log` |
| ray_long_gen3_B0.03_k3 | `ray_long.py gen3_B0.03_k3_v300.json` (in `code/eh_init`) | OK | 11.7 | 2.7 | `results_ray_long_gen3_B0.03_k3.txt` | `verification/logs/ray_long_gen3_B0.03_k3.log` |
| ray_validate | `ray_validate.py gen2_B0.03_k1.5_A0_U1_w0.3_v110.json ; ray_validate.py gen2_B0.03_k0.5_A0_U1_w0.3_v110.json` (in `code/eh_init`) | OK | 13.8 | 3.2 | `results_ray_validate.txt` | `verification/logs/ray_validate.log` |
| e13_table | `e13_table.py` (in `code/eh_init`) | OK | 137.0 | 32.4 | `results_e13_table.txt` | `verification/logs/e13_table.log` |
| e13_errconst | `e13_errconst.py gen3_B0.03_k1.5_v300.json 2 ; e13_errconst.py gen3_B0.03_k1.5_v300.json 0 ; e13_errconst.py gen3_B0.003_k1.5_v300.json 2 ; e13_errconst.py gen3_B0.003_k1.5_v300.json 0 ; e13_errconst.py gen3_B0.03_k0.5_v300.json 2 ; e13_errconst.py gen3_B0.03_k0.5_v300.json 0` (in `code/eh_init`) | OK | 58.7 | 13.8 | `results_e13_errconst.txt` | `verification/logs/e13_errconst.log` |
| e13_v0 | `e13_v0.py` (in `code/eh_init`) | OK | 26.0 | 6.1 | `results_e13_v0.txt` | `verification/logs/e13_v0.log` |
| e13_all_B0.03_k1.5 | `e13_all.py gen3_B0.03_k1.5_v300.json 2 ; e13_all.py gen3_B0.03_k1.5_v300.json 0` (in `code/eh_init`) | OK | 50.5 | 11.9 | `results_e13_B0.03_k1.5.txt` (changed) | `verification/logs/e13_all_B0.03_k1.5.log` |
| e13_all_B0.03_k0.5 | `e13_all.py gen3_B0.03_k0.5_v300.json 2 ; e13_all.py gen3_B0.03_k0.5_v300.json 0` (in `code/eh_init`) | OK | 45.3 | 10.9 | `results_e13_B0.03_k0.5.txt` (changed) | `verification/logs/e13_all_B0.03_k0.5.log` |
| e13_all_B0.003_k1.5 | `e13_all.py gen3_B0.003_k1.5_v300.json 2 ; e13_all.py gen3_B0.003_k1.5_v300.json 0` (in `code/eh_init`) | OK | 50.8 | 12.1 | `results_e13_B0.003_k1.5.txt` (changed) | `verification/logs/e13_all_B0.003_k1.5.log` |
| e13_all_B0.003_k0.5 | `e13_all.py gen3_B0.003_k0.5_v300.json 2 ; e13_all.py gen3_B0.003_k0.5_v300.json 0` (in `code/eh_init`) | OK | 48.1 | 11.4 | `results_e13_B0.003_k0.5.txt` (changed) | `verification/logs/e13_all_B0.003_k0.5.log` |
| e13_all_B0.03_k2 | `e13_all.py gen3_B0.03_k2_v300.json 2 ; e13_all.py gen3_B0.03_k2_v300.json 0` (in `code/eh_init`) | OK | 50.8 | 12.0 | `results_e13_B0.03_k2.txt` (changed) | `verification/logs/e13_all_B0.03_k2.log` |
| e13_all_B0.03_k3 | `e13_all.py gen3_B0.03_k3_v300.json 2 ; e13_all.py gen3_B0.03_k3_v300.json 0` (in `code/eh_init`) | OK | 51.6 | 12.2 | `results_e13_B0.03_k3.txt` (changed) | `verification/logs/e13_all_B0.03_k3.log` |
| e13_all_B0.003_k2 | `e13_all.py gen3_B0.003_k2_v300.json 2 ; e13_all.py gen3_B0.003_k2_v300.json 0` (in `code/eh_init`) | OK | 50.8 | 12.0 | `results_e13_B0.003_k2.txt` (changed) | `verification/logs/e13_all_B0.003_k2.log` |
| e13_all_B0.003_k3 | `e13_all.py gen3_B0.003_k3_v300.json 2 ; e13_all.py gen3_B0.003_k3_v300.json 0` (in `code/eh_init`) | OK | 52.0 | 12.3 | `results_e13_B0.003_k3.txt` (changed) | `verification/logs/e13_all_B0.003_k3.log` |
| ray_extend_B0.03_k1.5 | `ray_extend.py gen2_B0.03_k1.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 296.1 | 69.9 | `results_ray_extend_B0.03_k1.5.txt` | `verification/logs/ray_extend_B0.03_k1.5.log` |
| ray_extend_B0.03_k0.5 | `ray_extend.py gen2_B0.03_k0.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 289.6 | 69.0 | `results_ray_extend_B0.03_k0.5.txt` | `verification/logs/ray_extend_B0.03_k0.5.log` |
| ray_extend_B0.003_k1.5 | `ray_extend.py gen2_B0.003_k1.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 290.7 | 69.0 | `results_ray_extend_B0.003_k1.5.txt` | `verification/logs/ray_extend_B0.003_k1.5.log` |
| ray_extend_B0.003_k0.5 | `ray_extend.py gen2_B0.003_k0.5_A0_U1_w0.3_v300.json` (in `code/eh_init`) | OK | 263.6 | 66.4 | `results_ray_extend_B0.003_k0.5.txt` | `verification/logs/ray_extend_B0.003_k0.5.log` |
| ray_extend_def_B0.03_k1.5 | `ray_extend.py gen3_B0.03_k1.5_v300.json` (in `code/eh_init`) | OK | 356.5 | 70.6 | `results_ray_extend_ext_def_B0.03_k1.5.txt` | `verification/logs/ray_extend_def_B0.03_k1.5.log` |
| ray_extend_mu_B0.03_k1.5 | `ray_extend.py gen3_B0.03_k1.5_v300.json` (in `code/eh_init`) | OK | 268.7 | 51.6 | `results_ray_extend_ext_mu_B0.03_k1.5.txt` | `verification/logs/ray_extend_mu_B0.03_k1.5.log` |
| ray_extend_def_B0.03_k0.5 | `ray_extend.py gen3_B0.03_k0.5_v300.json` (in `code/eh_init`) | OK | 376.0 | 68.2 | `results_ray_extend_ext_def_B0.03_k0.5.txt` | `verification/logs/ray_extend_def_B0.03_k0.5.log` |
| ray_extend_mu_B0.03_k0.5 | `ray_extend.py gen3_B0.03_k0.5_v300.json` (in `code/eh_init`) | OK | 305.2 | 53.6 | `results_ray_extend_ext_mu_B0.03_k0.5.txt` | `verification/logs/ray_extend_mu_B0.03_k0.5.log` |
| ray_extend_def_B0.003_k1.5 | `ray_extend.py gen3_B0.003_k1.5_v300.json` (in `code/eh_init`) | OK | 409.2 | 71.0 | `results_ray_extend_ext_def_B0.003_k1.5.txt` | `verification/logs/ray_extend_def_B0.003_k1.5.log` |
| ray_extend_mu_B0.003_k1.5 | `ray_extend.py gen3_B0.003_k1.5_v300.json` (in `code/eh_init`) | OK | 321.1 | 55.6 | `results_ray_extend_ext_mu_B0.003_k1.5.txt` | `verification/logs/ray_extend_mu_B0.003_k1.5.log` |
| ray_extend_def_B0.003_k0.5 | `ray_extend.py gen3_B0.003_k0.5_v300.json` (in `code/eh_init`) | OK | 406.9 | 70.3 | `results_ray_extend_ext_def_B0.003_k0.5.txt` | `verification/logs/ray_extend_def_B0.003_k0.5.log` |
| ray_extend_mu_B0.003_k0.5 | `ray_extend.py gen3_B0.003_k0.5_v300.json` (in `code/eh_init`) | OK | 306.6 | 53.4 | `results_ray_extend_ext_mu_B0.003_k0.5.txt` | `verification/logs/ray_extend_mu_B0.003_k0.5.log` |
| ray_extend_def_B0.03_k2 | `ray_extend.py gen3_B0.03_k2_v300.json` (in `code/eh_init`) | OK | 427.4 | 74.4 | `results_ray_extend_ext_def_B0.03_k2.txt` | `verification/logs/ray_extend_def_B0.03_k2.log` |
| ray_extend_mu_B0.03_k2 | `ray_extend.py gen3_B0.03_k2_v300.json` (in `code/eh_init`) | OK | 336.4 | 57.9 | `results_ray_extend_ext_mu_B0.03_k2.txt` (changed) | `verification/logs/ray_extend_mu_B0.03_k2.log` |
| ray_extend_def_B0.03_k3 | `ray_extend.py gen3_B0.03_k3_v300.json` (in `code/eh_init`) | OK | 435.7 | 75.3 | `results_ray_extend_ext_def_B0.03_k3.txt` | `verification/logs/ray_extend_def_B0.03_k3.log` |
| ray_extend_mu_B0.03_k3 | `ray_extend.py gen3_B0.03_k3_v300.json` (in `code/eh_init`) | OK | 331.2 | 57.5 | `results_ray_extend_ext_mu_B0.03_k3.txt` | `verification/logs/ray_extend_mu_B0.03_k3.log` |
| ray_extend_def_B0.003_k2 | `ray_extend.py gen3_B0.003_k2_v300.json` (in `code/eh_init`) | OK | 423.2 | 76.4 | `results_ray_extend_ext_def_B0.003_k2.txt` | `verification/logs/ray_extend_def_B0.003_k2.log` |
| ray_extend_mu_B0.003_k2 | `ray_extend.py gen3_B0.003_k2_v300.json` (in `code/eh_init`) | OK | 307.0 | 58.4 | `results_ray_extend_ext_mu_B0.003_k2.txt` | `verification/logs/ray_extend_mu_B0.003_k2.log` |
| ray_extend_def_B0.003_k3 | `ray_extend.py gen3_B0.003_k3_v300.json` (in `code/eh_init`) | OK | 370.8 | 70.6 | `results_ray_extend_ext_def_B0.003_k3.txt` | `verification/logs/ray_extend_def_B0.003_k3.log` |
| ray_extend_mu_B0.003_k3 | `ray_extend.py gen3_B0.003_k3_v300.json` (in `code/eh_init`) | OK | 306.8 | 60.9 | `results_ray_extend_ext_mu_B0.003_k3.txt` | `verification/logs/ray_extend_mu_B0.003_k3.log` |
| ray_rate_only | `ray_rate_only.py` (in `code/eh_init`) | OK | 709.5 | 182.4 | `results_ray_rate_only.txt` | `verification/logs/ray_rate_only.log` |
| ray_fig | `ray_fig.py` (in `code/eh_init`) | OK | 12.6 | 2.9 |  | `verification/logs/ray_fig.log` |
| e13_fig | `e13_fig.py` (in `code/eh_init`) | OK | 54.4 | 12.7 |  | `verification/logs/e13_fig.log` |
| hist_eh_init | `t_static4.py ; conv1.py 0.03 1.5 100 0.05 0.025 ; conv1.py 0.04 1.5 100 0.05 0.025 ; conv1.py 0.03 0.5 100 0.05 0.025 ; mucheck.py 0.03 1.5 100 0.025 ; mucheck.py 0.03 0.5 100 0.025 ; nanloc.py 0.05 0.05 100` (in `code/eh_init`) | OK | 403.3 | 95.1 | `results_eh_init.txt` (changed) | `verification/logs/hist_eh_init.log` |
| hist_tailonly_collapse | `conv1.py 0.05 1.5 100 0.05 0.025 ; conv1.py 0.03 0.5 100 0.05 0.025 ; nanloc.py 0.03 0.05 100 ; nanloc.py 0.04 0.05 100 ; nanloc.py 0.05 0.05 100` (in `code/eh_init`) | OK | 207.9 | 50.3 | `results_tailonly_collapse.txt` (changed) | `verification/logs/hist_tailonly_collapse.log` |
| hist_aniso | `aniso.py` (in `code/eh_init`) | OK | 56.9 | 12.8 | `results_aniso_noise.txt` (changed) | `verification/logs/hist_aniso.log` |
| hist_checks_extra | `t_uniform.py ; noise.py ; phiexp_extrap.py ; conv1.py 0.03 1.5 100 0.05 0.025 ; conv3.py` (in `code/eh_init`) | OK | 247.1 | 66.7 | `results_checks_extra.txt` (changed) | `verification/logs/hist_checks_extra.log` |
| hist_muid | `muid.py` (in `code/eh_init`) | OK | 35.4 | 9.3 | `results_seeded_identity_constraint.txt` (changed) | `verification/logs/hist_muid.log` |
| paper_numbers_kernel | `paper_numbers_kernel.py` (in `code/eh_init`) | OK | 3.9 | 0.9 | `results_paper_numbers_kernel.txt` | `verification/logs/paper_numbers_kernel.log` |
| paper_numbers_ray | `paper_numbers_ray.py` (in `code/eh_init`) | OK | 2.2 | 0.5 | `results_paper_numbers_ray.txt` | `verification/logs/paper_numbers_ray.log` |
| paper_numbers_hist | `paper_numbers_hist.py` (in `code/eh_init`) | OK | 0.3 | 0.1 | `results_paper_numbers_hist.txt` | `verification/logs/paper_numbers_hist.log` |

## Manuscript corrections (PASS* rows)

The computed value reproduces the corrected value and not the one printed in main.tex; the text should be changed as follows.

| id | location | quantity | main.tex now | computed | should read |
|---|---|---|---|---|---|
| rminus_B005_k15 | Sec. 4.3(d) (end) | inner horizon r_- of the final hole at B=0.05, k=3/2 (mu_f=0.0278); 0.0557 is the extra small root r_s ~ 2 mu_f, not the Cauchy horizon | 0.056 | 1.02327 | 1.023 |
| kc_mu_f_pulse | Sec. 4.3(c) | final mass parameter of the v_s=60, B=0.003 pulse run (paper: 8.5e-4, which is the v_s=10 run) | 8.5e-4 | 0.0020947 | 2.1e-3 |
| kd_final_k15_const | Sec. 4.3(d) | same: constant over 150<=v<=290 to (paper: 1e-5; the spread is 7e-5 from v=150, 1e-5 from v=200) | 1e-5 | 7e-05 | 7e-5 |
| kd_account_k05 | Sec. 4.3(d) | displacement of the horizons accounts for (percent), k=1/2 | 46 | 46.6 | 47 |
| kd_final_const_k2k3 | Sec. 4.3(d) | final-hole ratio constant over 150<=v<=290 for k=2, 3 (paper: 1e-5; spreads are 1.5e-4 and 4e-5) | 1e-5 | 0.00014 | 1.4e-4 |
| kd_pulse_B2_vs60 | Sec. 4.3(d) | eps/B^2 of the v_s=60 pulse at B=3e-4 against B=3e-3 (paper: B^2 scaling "to three digits"; they differ by 3 percent) | 0.1 | 2.80172 | 2.8 |
| ray_A_underestimate_k15 | Sec. 5 and Fig. 4 caption | M_PDE error divided by the level spread over the rows of Table 4 (smallest over k=3/2 and 1/2; paper: "10^2-10^3 at every v") | 100 | 8 | 8 |
| e13_sV_levels_quote | Result paragraph | level spread of sigma_v quoted as "1.2e-8" (that number is the relative level spread of phi_v; sigma_v: 2e-13) | 1.2e-8 | 2e-13 | 2e-13 |
| e13_levels_I_280 | Sec. 5 | same up to v=280 | 8e-09 | 8.3e-09 | 8.3e-9 |
| ext_k05_rate_change | Sec. 5 (extension) | k=1/2: the three treatments change the rate by at most (finite differences of the printed treatment columns, v>=1000) | 1e-3 | 0.0014 | 1.4e-3 |
| pt_drift_k2 | Sec. 5 (physical tails) | drift of the static-kernel matching factor between v=250 and 290, k=2 (percent) | 0.6 | 0.516303 | 0.5 |
| abs_underestimate | Abstract; Sec. 5 | level spread of M_PDE understates its error by (smallest factor over Table 4 rows; text: "two to three orders of magnitude") | 100 | 8 | 8 |
| gap_kernel_choice_B0003 | Sec. 4.3(d) | same at B=0.003: largest change over the four tails (text: <=1e-5; the logs print ln M to 3 decimals, k=3: 1893.123 against 1893.121) | 1e-05 | 0.002 | 2e-3 |

## Checks

Tolerance "round" means: the computed value rounds to the printed digits of the paper value (half a unit in the last printed digit); other tolerances are stated with their reason.

| id | quantity | location in main.tex | paper | computed | tolerance | status |
|---|---|---|---|---|---|---|
| static_rm | r_- of the static hole m_N=5, a_N=10 (50-digit mpmath) | Abstract; Sec. 2 | 1.057475 | 1.05747 | round (half unit of last printed digit) | PASS |
| static_rp | r_+ of the static hole m_N=5, a_N=10 (50-digit mpmath) | Abstract; Sec. 2 | 9.897927 | 9.89793 | round (half unit of last printed digit) | PASS |
| static_km | kappa_- of the static hole m_N=5, a_N=10 (50-digit mpmath) | Abstract; Sec. 2 | 0.795649 | 0.795649 | round (half unit of last printed digit) | PASS |
| static_kp | kappa_+ of the static hole m_N=5, a_N=10 (50-digit mpmath) | Abstract; Sec. 2 | 0.048969 | 0.0489687 | round (half unit of last printed digit) | PASS |
| static_ratio_rp_rm | r_+/r_- (high-frequency gain of the kernel) | Sec. 4.2 | 9.36 | 9.35997 | round (half unit of last printed digit) | PASS |
| T0_mN5 | T(0) = (1 + r_+^2/r_-^2)/2, m_N=5 | Eq. (T0) | 44.30 | 44.3045 | round (half unit of last printed digit) | PASS |
| T0_mN3 | T(0) = (1 + r_+^2/r_-^2)/2, m_N=3 | Eq. (T0) | 14.32 | 14.3248 | round (half unit of last printed digit) | PASS |
| T0_mN2 | T(0) = (1 + r_+^2/r_-^2)/2, m_N=2 | Eq. (T0) | 5.33 | 5.32598 | round (half unit of last printed digit) | PASS |
| T0_mN1.6 | T(0) = (1 + r_+^2/r_-^2)/2, m_N=1.6 | Eq. (T0) | 2.81 | 2.81244 | round (half unit of last printed digit) | PASS |
| T0_mN1.4 | T(0) = (1 + r_+^2/r_-^2)/2, m_N=1.4 | Eq. (T0) | 1.733 | 1.73253 | round (half unit of last printed digit) | PASS |
| kp_mN3 | kappa_+ of the hole m_N=3 | Sec. 4.3(c) | 0.07827 | 0.0782687 | round (half unit of last printed digit) | PASS |
| kp_mN2 | kappa_+ of the hole m_N=2 | Sec. 4.3(c) | 0.10541 | 0.105406 | round (half unit of last printed digit) | PASS |
| kp_mN1.6 | kappa_+ of the hole m_N=1.6 | Sec. 4.3(c) | 0.1101 | 0.110128 | round (half unit of last printed digit) | PASS |
| kp_mN1.4 | kappa_+ of the hole m_N=1.4 | Sec. 4.3(c) | 0.0901 | 0.0900626 | round (half unit of last printed digit) | PASS |
| km_mN1.4 | kappa_- at m_N=1.4 | Sec. 4.5 | 0.164 | 0.163981 | round (half unit of last printed digit) | PASS |
| km_minus_2kp_mN1.4 | kappa_- - 2 kappa_+ at m_N=1.4 | Sec. 4.5 | -0.016 | -0.0161438 | round (half unit of last printed digit) | PASS |
| M_cross | mass at which kappa_- = 2 kappa_+ | Sec. 4.5 | 1.435 | 1.4353 | round (half unit of last printed digit) | PASS |
| eps_cross | eps = M/M* - 1 at that mass | Sec. 4.5 | 0.105 | 0.104893 | round (half unit of last printed digit) | PASS |
| kappa_over_sqrt_eps | kappa_pm / sqrt(eps) as eps -> 0 | Sec. 4.5 | 0.471 | 0.471405 | round (half unit of last printed digit) | PASS |
| mu_f_hole_rm | r_- of the hole of mass parameter mu_f = 9.96e-3 | Sec. 4.3(d) | 1.04549 | 1.04549 | round (half unit of last printed digit) | PASS |
| mu_f_hole_rp | r_+ of the same hole | Sec. 4.3(d) | 9.91846 | 9.91846 | round (half unit of last printed digit) | PASS |
| mu_f_hole_T0 | T(0) of the same hole | Sec. 4.3(d) | 45.500 | 45.5003 | round (half unit of last printed digit) | PASS |
| mu_f_hole_T0_percent | T(0) of the hole of mass mu_f larger than the static one by (percent) | Sec. 4.3(d) | 2.7 | 2.69917 | round (half unit of last printed digit) | PASS |
| rminus_B005_k15 | inner horizon r_- of the final hole at B=0.05, k=3/2 (mu_f=0.0278); 0.0557 is the extra small root r_s ~ 2 mu_f, not the Cauchy horizon | Sec. 4.3(d) (end) | 0.056 (text should read 1.023) | 1.02327 | round (half unit of last printed digit) | PASS* |
| shift_percent_B0.03 | predicted shift of kappa_- from the static value at B=0.03 (percent) | Sec. 3 | 1.4 | 1.361 | round (half unit of last printed digit) | PASS |
| shift_percent_B0.04 | predicted shift of kappa_- from the static value at B=0.04 (percent) | Sec. 3 | 2.5 | 2.488 | round (half unit of last printed digit) | PASS |
| shift_percent_B0.05 | predicted shift of kappa_- from the static value at B=0.05 (percent) | Sec. 3 | 4.0 | 4.032 | round (half unit of last printed digit) | PASS |
| static_minus_final_km_k15 | kappa_-^static - kappa_-(mu_f), B=0.003, k=3/2 | Sec. 4.4 (long runs) | 1.0e-4 | 0.0001046 | round (half unit of last printed digit) | PASS |
| static_minus_final_km_k05 | kappa_-^static - kappa_-(mu_f), B=0.003, k=1/2 | Sec. 4.4 (long runs) | 6.2e-5 | 6.225e-05 | round (half unit of last printed digit) | PASS |
| cfe_residual | max /G_ab - 8 pi T_ab/ with dn1, dn2 and the constraints imposed (E_thth) | Sec. 2 | 3e-6 | 2.63e-06 | round (half unit of last printed digit) | PASS |
| cfe_perturb_min | component departure when its second derivative is changed by 0.1 (smallest) | Sec. 2 | 0.07 | 0.0667 | round (half unit of last printed digit) | PASS |
| cfe_perturb_max | component departure (largest, E_thth for ds_uv) | Sec. 2 | 1.6 | 1.63 | round (half unit of last printed digit) | PASS |
| cfe_box_phi | box phi = 0 against dn3 | Sec. 2 | 1e-15 | 6.63e-16 | round (half unit of last printed digit) | PASS |
| sym_S1_uu_constraint | uu Einstein constraint of ds^2 = -W du dv + r^2 dOmega^2 with the NED+scalar stress tensor (exact, sympy) | Eq. (constraints) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_vv_constraint | vv Einstein constraint (exact, sympy) | Eq. (constraints) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_dn1 | Eq. (dn1) = theta-theta/uv Einstein equation (exact, sympy) | Eq. (dn1) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_dn2 | Eq. (dn2) (exact, sympy) | Eq. (dn2) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_dn3 | Eq. (dn3) = box phi = 0 (exact, sympy) | Eq. (dn3) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_remaining_components | all remaining Einstein components vanish identically (exact, sympy) | Sec. 2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_misner_sharp | Misner-Sharp mass M = (r/2)(1 + 4 r_u r_v/W) (exact, sympy) | Sec. 2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_negative_control_dn2 | negative control: wrong coefficient in dn2 is detected (exact, sympy) | Sec. 2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_negative_control_dn1 | negative control: wrong coefficient in dn1 is detected (exact, sympy) | Sec. 2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_negative_control_constraint | negative control: wrong constraint is detected (exact, sympy) | Sec. 2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S1_scalar_T_uv_vanishes | scalar T_uv = 0 (massless, so Eq. dn2 has no phi^2 term) (exact, sympy) | Sec. 2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S2_rho_prime | rho' = sigma_v rho + 4 pi r phi_v^2 (exact, sympy) | Eq. (ray) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S2_lny_prime | (ln y)' = rho/r - sigma_v + S/y (exact, sympy) | Eq. (ray) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S2_M_of_y_rho | M = (r/2)(1 + 4 y rho) (exact, sympy) | Eq. (ray) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S2_rayrate | d ln(M - r/2)/dv = 4 pi r phi_v^2/rho + S/y (exact, sympy) | Eq. (rayrate) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S3_mu_v | mu_v = -8 pi r^2 (r_u/W) phi_v^2 (exact, sympy) | Eq. (muv) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S4_u_constraint_integral | d_u(r_u/W) = -4 pi r phi_u^2/W, hence y_c = 1/2 + integral (exact, sympy) | Eq. (yc) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S5_wave_equation_EF | ingoing-EF wave equation (r^2 f F')' - 2 i w r (r F)' = 0 (exact, sympy) | Sec. 4.2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S5_frobenius_a | regular solution F = 1 + a (r_+ - r) + ..., a = -i w/[r_+(kappa_+ - i w)] (exact, sympy) | Sec. 4.2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S5_recursion_denominators | recursion denominators n(kappa_+ n - i w): poles at w = -i n kappa_+ (exact, sympy) | Sec. 4.2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S5_static_equation | static equation (r^2 f g')' + 2 r = 0 for phi = j0 (v + g(r)) (exact, sympy) | Sec. 4.2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S5_static_solution | regular solution r^2 f g' = r_+^2 - r^2 (exact, sympy) | Sec. 4.2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S5_T0_gain | T(0) = (1 + r_+^2/r_-^2)/2 from the static solution (exact, sympy) | Eq. (T0) | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S5_outgoing_ray | phi_v = j0 [1 + (f/2) g'] = j0 (1 + r_+^2/r^2)/2 on the outgoing ray (exact, sympy) | Sec. 4.2 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S6_RN_kappas | Reissner-Nordstrom: kappa_pm = (r_+ - r_-)/(2 r_pm^2) (exact, sympy) | Sec. 4.6 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S6_RN_T0_equals_ori_b0 | RN: T(0) = (kappa_+ + kappa_-)/(2 kappa_+) = Ori b_0 (exact, sympy) | Sec. 4.6 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S7_filter_a1 | exponential filtering of a power-law flux: first correction a_1 = p/kappa (exact, sympy) | Sec. 5 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| sym_S7_q_limit_equals_p | lim (kappa - d ln M/dv) v = p = 2k+2 for a flux phi_v^2 ~ v^-(2k+2) (exact, sympy) | Sec. 5 | 1 | 1 | eq (exact symbolic statement: the script prints PASS or FAIL) | PASS |
| T1_k1.5_B0.03_0 | Table 1 (k, B) = (3/2, 0.03): mu_f | Table 1 | 9.956e-3 | 0.0099555 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.03_1 | Table 1 (k, B) = (3/2, 0.03): kappa_-(mu_f) | Table 1 | 0.784821 | 0.784821 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.03_2 | Table 1 (k, B) = (3/2, 0.03): /sigma_v/ h=0.05 | Table 1 | 0.78597 | 0.78597 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.03_3 | Table 1 (k, B) = (3/2, 0.03): /sigma_v/ h=0.0125 | Table 1 | 0.78507 | 0.78507 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.03_4 | Table 1 (k, B) = (3/2, 0.03): /sigma_v/ h=0.003125 | Table 1 | 0.78502 | 0.78502 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.03_5 | Table 1 (k, B) = (3/2, 0.03): /sigma_v/ extrap. U=0.3 | Table 1 | 0.78501 | 0.78501 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.03_6 | Table 1 (k, B) = (3/2, 0.03): /sigma_v/ extrap. U=1 | Table 1 | 0.78561 | 0.78561 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.05_0 | Table 1 (k, B) = (3/2, 0.05): mu_f | Table 1 | 2.7757e-2 | 0.027757 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.05_1 | Table 1 (k, B) = (3/2, 0.05): kappa_-(mu_f) | Table 1 | 0.763567 | 0.763567 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.05_2 | Table 1 (k, B) = (3/2, 0.05): /sigma_v/ h=0.05 | Table 1 | 0.76518 | 0.76518 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.05_3 | Table 1 (k, B) = (3/2, 0.05): /sigma_v/ h=0.0125 | Table 1 | 0.76422 | 0.76422 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.05_4 | Table 1 (k, B) = (3/2, 0.05): /sigma_v/ h=0.003125 | Table 1 | 0.76416 | 0.76416 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.05_5 | Table 1 (k, B) = (3/2, 0.05): /sigma_v/ extrap. U=0.3 | Table 1 | 0.76416 | 0.76416 | round (half unit of last printed digit) | PASS |
| T1_k1.5_B0.05_6 | Table 1 (k, B) = (3/2, 0.05): /sigma_v/ extrap. U=1 | Table 1 | 0.76604 | 0.76604 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.03_0 | Table 1 (k, B) = (1/2, 0.03): mu_f | Table 1 | 5.913e-3 | 0.0059132 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.03_1 | Table 1 (k, B) = (1/2, 0.03): kappa_-(mu_f) | Table 1 | 0.789303 | 0.789303 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.03_2 | Table 1 (k, B) = (1/2, 0.03): /sigma_v/ h=0.05 | Table 1 | 0.79231 | 0.79231 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.03_3 | Table 1 (k, B) = (1/2, 0.03): /sigma_v/ h=0.0125 | Table 1 | 0.79147 | 0.79147 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.03_4 | Table 1 (k, B) = (1/2, 0.03): /sigma_v/ h=0.003125 | Table 1 | 0.79142 | 0.79142 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.03_5 | Table 1 (k, B) = (1/2, 0.03): /sigma_v/ extrap. U=0.3 | Table 1 | 0.79142 | 0.79142 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.03_6 | Table 1 (k, B) = (1/2, 0.03): /sigma_v/ extrap. U=1 | Table 1 | 0.79557 | 0.79557 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.05_0 | Table 1 (k, B) = (1/2, 0.05): mu_f | Table 1 | 1.6461e-2 | 0.016461 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.05_1 | Table 1 (k, B) = (1/2, 0.05): kappa_-(mu_f) | Table 1 | 0.777349 | 0.777349 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.05_2 | Table 1 (k, B) = (1/2, 0.05): /sigma_v/ h=0.05 | Table 1 | 0.78443 | 0.78443 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.05_3 | Table 1 (k, B) = (1/2, 0.05): /sigma_v/ h=0.0125 | Table 1 | 0.78364 | 0.78364 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.05_4 | Table 1 (k, B) = (1/2, 0.05): /sigma_v/ h=0.003125 | Table 1 | 0.78359 | 0.78359 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.05_5 | Table 1 (k, B) = (1/2, 0.05): /sigma_v/ extrap. U=0.3 | Table 1 | 0.78358 | 0.78358 | round (half unit of last printed digit) | PASS |
| T1_k0.5_B0.05_6 | Table 1 (k, B) = (1/2, 0.05): /sigma_v/ extrap. U=1 | Table 1 | 0.79669 | 0.79669 | round (half unit of last printed digit) | PASS |
| T1_pct_U0.3_B0.03_k1.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=0.3 (percent), B=0.03 k=1.5 | Sec. 3 | 0.024 | 0.0244 | round (half unit of last printed digit) | PASS |
| T1_pct_U1_B0.03_k1.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=1 (percent), B=0.03 k=1.5 | Sec. 3 | 0.10 | 0.1004 | round (half unit of last printed digit) | PASS |
| T1_pct_single_B0.03_k1.5 | single-grid h=0.05 /sigma_v/ above kappa_-(mu_f) on U=0.3 (percent), B=0.03 k=1.5 | Sec. 3 | 0.15 | 0.1462 | round (half unit of last printed digit) | PASS |
| T1_pct_U0.3_B0.05_k1.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=0.3 (percent), B=0.05 k=1.5 | Sec. 3 | 0.077 | 0.0771 | round (half unit of last printed digit) | PASS |
| T1_pct_U1_B0.05_k1.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=1 (percent), B=0.05 k=1.5 | Sec. 3 | 0.32 | 0.3237 | round (half unit of last printed digit) | PASS |
| T1_pct_single_B0.05_k1.5 | single-grid h=0.05 /sigma_v/ above kappa_-(mu_f) on U=0.3 (percent), B=0.05 k=1.5 | Sec. 3 | 0.21 | 0.2119 | round (half unit of last printed digit) | PASS |
| T1_pct_U0.3_B0.03_k0.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=0.3 (percent), B=0.03 k=0.5 | Sec. 3 | 0.27 | 0.2676 | round (half unit of last printed digit) | PASS |
| T1_pct_U1_B0.03_k0.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=1 (percent), B=0.03 k=0.5 | Sec. 3 | 0.79 | 0.7946 | round (half unit of last printed digit) | PASS |
| T1_pct_U0.3_B0.05_k0.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=0.3 (percent), B=0.05 k=0.5 | Sec. 3 | 0.80 | 0.8021 | round (half unit of last printed digit) | PASS |
| T1_pct_U1_B0.05_k0.5 | extrapolated /sigma_v/ above kappa_-(mu_f) on U=1 (percent), B=0.05 k=0.5 | Sec. 3 | 2.5 | 2.4884 | round (half unit of last printed digit) | PASS |
| T1_B005_k05_U1_exceeds_static | k=1/2, B=0.05: extrapolated /sigma_v/ on U=1 (0.79669) exceeds the static value 0.795649 | Sec. 3 | 0.795649 | 0.79669 | ge (inequality quoted in the text: computed value must be >= static kappa_-) | PASS |
| T1_succ_ratio0_B0.03_k1.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 1, B0.03_k1.5 | Sec. 3 | 3.98 | 3.981 | abs:0.05 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio1_B0.03_k1.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 2, B0.03_k1.5 | Sec. 3 | 4.0 | 3.995 | abs:0.1 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio2_B0.03_k1.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 3, B0.03_k1.5 | Sec. 3 | 4.0 | 3.999 | abs:0.1 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio0_B0.03_k0.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 1, B0.03_k0.5 | Sec. 3 | 3.98 | 3.983 | abs:0.05 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio1_B0.03_k0.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 2, B0.03_k0.5 | Sec. 3 | 4.0 | 3.996 | abs:0.1 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio2_B0.03_k0.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 3, B0.03_k0.5 | Sec. 3 | 4.0 | 3.999 | abs:0.1 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio0_B0.05_k1.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 1, B0.05_k1.5 | Sec. 3 | 3.98 | 3.982 | abs:0.05 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio1_B0.05_k1.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 2, B0.05_k1.5 | Sec. 3 | 4.0 | 3.995 | abs:0.1 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| T1_succ_ratio2_B0.05_k1.5 | ratio of successive differences of the single-grid /sigma_v/ (v=95, U=0.3), number 3, B0.05_k1.5 | Sec. 3 | 4.0 | 3.999 | abs:0.1 (paper quotes the second-order ratio 4.0 to two digits; sequences are 3.98 -> 4.0 -> 4.0) | PASS |
| rawM_v100_grid0 | single-grid M at v=100, B=0.03, k=3/2, U=1, grid 0 of 5 (units 1e17) | Sec. 3 (raw mass) | -9.1 | -9.058 | round (half unit of last printed digit) | PASS |
| rawM_v100_grid1 | single-grid M at v=100, B=0.03, k=3/2, U=1, grid 1 of 5 (units 1e17) | Sec. 3 (raw mass) | -2.6 | -2.64 | round (half unit of last printed digit) | PASS |
| rawM_v100_grid2 | single-grid M at v=100, B=0.03, k=3/2, U=1, grid 2 of 5 (units 1e17) | Sec. 3 (raw mass) | -0.67 | -0.6651 | round (half unit of last printed digit) | PASS |
| rawM_v100_grid3 | single-grid M at v=100, B=0.03, k=3/2, U=1, grid 3 of 5 (units 1e17) | Sec. 3 (raw mass) | -0.15 | -0.1487 | round (half unit of last printed digit) | PASS |
| rawM_v100_grid4 | single-grid M at v=100, B=0.03, k=3/2, U=1, grid 4 of 5 (units 1e17) | Sec. 3 (raw mass) | -0.018 | -0.01815 | round (half unit of last printed digit) | PASS |
| rawM_v100_extrap | five-grid extrapolated M at v=100 (units 1e15) | Sec. 3 (raw mass) | 2.5 | 2.549 | round (half unit of last printed digit) | PASS |
| rawM_finest_off_v60 | finest-grid M off from the extrapolant at v=60 (percent) | Sec. 3 | 2 | 2.2 | round (half unit of last printed digit) | PASS |
| rawM_next_off_v60 | second-finest grid M off from the extrapolant at v=60 (percent) | Sec. 3 | 9 | 8.7 | round (half unit of last printed digit) | PASS |
| rawM_finest_off_v80 | finest-grid M off from the extrapolant at v=80 (percent) | Sec. 3 | 18 | 17.7 | abs:0.5 (paper rounds 17.7 to 18) | PASS |
| rawM_next_off_v80 | second-finest grid M off from the extrapolant at v=80 (percent) | Sec. 3 | 71 | 70.7 | round (half unit of last printed digit) | PASS |
| rawM_finest_off_v100 | finest-grid M off from the extrapolant at v=100 (percent) | Sec. 3 | 171 | 171.2 | round (half unit of last printed digit) | PASS |
| rawM_next_off_v100 | second-finest grid M off from the extrapolant at v=100 (percent) | Sec. 3 | 683 | 683.3 | round (half unit of last printed digit) | PASS |
| rawM_err_v100_grid0 | error of single-grid M against the extrapolant at v=100, grid 0 (units 1e17) | Sec. 3 | 9.1 | 9.08 | round (half unit of last printed digit) | PASS |
| rawM_err_v100_grid1 | error of single-grid M against the extrapolant at v=100, grid 1 (units 1e17) | Sec. 3 | 2.7 | 2.67 | round (half unit of last printed digit) | PASS |
| rawM_err_v100_grid2 | error of single-grid M against the extrapolant at v=100, grid 2 (units 1e17) | Sec. 3 | 0.69 | 0.691 | round (half unit of last printed digit) | PASS |
| rawM_err_v100_grid3 | error of single-grid M against the extrapolant at v=100, grid 3 (units 1e17) | Sec. 3 | 0.17 | 0.174 | round (half unit of last printed digit) | PASS |
| rawM_err_v100_grid4 | error of single-grid M against the extrapolant at v=100, grid 4 (units 1e17) | Sec. 3 | 0.044 | 0.0436 | round (half unit of last printed digit) | PASS |
| rawM_err_factor0 | successive factor of the errors of single-grid M at v=100, number 1 | Sec. 3 | 3.4 | 3.41 | round (half unit of last printed digit) | PASS |
| rawM_err_factor1 | successive factor of the errors of single-grid M at v=100, number 2 | Sec. 3 | 3.9 | 3.86 | round (half unit of last printed digit) | PASS |
| rawM_err_factor2 | successive factor of the errors of single-grid M at v=100, number 3 | Sec. 3 | 4.0 | 3.97 | round (half unit of last printed digit) | PASS |
| rawM_err_factor3 | successive factor of the errors of single-grid M at v=100, number 4 | Sec. 3 | 4.0 | 3.99 | round (half unit of last printed digit) | PASS |
| rawM_rate_extrap | rate of the extrapolated M over [84,88], k=3/2 | Sec. 3 | 0.691 | 0.6911 | round (half unit of last printed digit) | PASS |
| rawM_rate_finest | rate of the finest-grid M over [84,88] | Sec. 3 | 0.632 | 0.6323 | round (half unit of last printed digit) | PASS |
| rawM_rate_undefined | grids on which the rate over [84,88] is undefined (M<0) | Sec. 3 | 4 | 4 | eq (integer count) | PASS |
| rawM_rate_low_percent | finest-grid rate low by (percent) | Sec. 3 | 8.5 | 8.5 | round (half unit of last printed digit) | PASS |
| rawM_k05_finest_v100 | k=1/2: finest-grid M at v=100 (units 1e17) | Sec. 3 | 2.4 | 2.36 | round (half unit of last printed digit) | PASS |
| rawM_k05_extrap_v100 | k=1/2: extrapolated M at v=100 (units 1e17) | Sec. 3 | 2.5 | 2.548 | abs:0.06 (computed 2.55 lies at the rounding boundary between 2.5 and 2.6) | PASS |
| rawM_k05_v60_min | k=1/2: smallest single-grid M at v=60 | Sec. 3 | -6e3 | -6210 | round (half unit of last printed digit) | PASS |
| rawM_k05_v60_max | k=1/2: largest single-grid M at v=60 | Sec. 3 | 3.2e4 | 31800 | round (half unit of last printed digit) | PASS |
| rawM_B005_k15_finest_off | B=0.05, k=3/2: finest-grid M off at v=100 (percent) | Sec. 3 | 53 | 52.7 | round (half unit of last printed digit) | PASS |
| rawM_B005_k05_finest_off | B=0.05, k=1/2: finest-grid M off at v=100 (percent) | Sec. 3 | 2 | 2.5 | round (half unit of last printed digit) | PASS |
| rawM_levels_main | two highest Romberg levels of M agree (relative), v>=60, main series | Sec. 3 | 1.4e-6 | 1.36e-06 | round (half unit of last printed digit) | PASS |
| rawM_levels_wide | same including the wide-seed run | Sec. 3 | 1.1e-4 | 0.00011 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_60_rate | Table 2 tail k=1/2, window [60,64]: rate | Table 2 | 0.7338 | 0.7338 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_60_lam | Table 2 tail k=1/2, window [60,64]: lambda | Table 2 | 0.7347 | 0.7347 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_60_lam2 | Table 2 tail k=1/2, window [60,64]: lambda-lambda'/lambda | Table 2 | 0.7340 | 0.734 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_60_sV | Table 2 tail k=1/2, window [60,64]: /sigma_v/ | Table 2 | 0.8008 | 0.8008 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_84_rate | Table 2 tail k=1/2, window [84,88]: rate | Table 2 | 0.7457 | 0.7457 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_84_lam | Table 2 tail k=1/2, window [84,88]: lambda | Table 2 | 0.7463 | 0.7463 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_84_lam2 | Table 2 tail k=1/2, window [84,88]: lambda-lambda'/lambda | Table 2 | 0.7457 | 0.7457 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_84_sV | Table 2 tail k=1/2, window [84,88]: /sigma_v/ | Table 2 | 0.7967 | 0.7967 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_104_rate | Table 2 tail k=1/2, window [104,108]: rate | Table 2 | 0.7543 | 0.7543 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_104_lam | Table 2 tail k=1/2, window [104,108]: lambda | Table 2 | 0.7548 | 0.7548 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_104_lam2 | Table 2 tail k=1/2, window [104,108]: lambda-lambda'/lambda | Table 2 | 0.7544 | 0.7544 | round (half unit of last printed digit) | PASS |
| T2_tailk=12_104_sV | Table 2 tail k=1/2, window [104,108]: /sigma_v/ | Table 2 | 0.7945 | 0.7945 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_60_rate | Table 2 tail k=3/2, window [60,64]: rate | Table 2 | 0.6868 | 0.6868 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_60_lam | Table 2 tail k=3/2, window [60,64]: lambda | Table 2 | 0.6872 | 0.6872 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_60_lam2 | Table 2 tail k=3/2, window [60,64]: lambda-lambda'/lambda | Table 2 | 0.6869 | 0.6869 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_60_sV | Table 2 tail k=3/2, window [60,64]: /sigma_v/ | Table 2 | 0.7880 | 0.788 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_84_rate | Table 2 tail k=3/2, window [84,88]: rate | Table 2 | 0.6911 | 0.6911 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_84_lam | Table 2 tail k=3/2, window [84,88]: lambda | Table 2 | 0.6913 | 0.6913 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_84_lam2 | Table 2 tail k=3/2, window [84,88]: lambda-lambda'/lambda | Table 2 | 0.6911 | 0.6911 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_84_sV | Table 2 tail k=3/2, window [84,88]: /sigma_v/ | Table 2 | 0.7860 | 0.786 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_104_rate | Table 2 tail k=3/2, window [104,108]: rate | Table 2 | 0.6947 | 0.6947 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_104_lam | Table 2 tail k=3/2, window [104,108]: lambda | Table 2 | 0.6950 | 0.695 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_104_lam2 | Table 2 tail k=3/2, window [104,108]: lambda-lambda'/lambda | Table 2 | 0.6947 | 0.6947 | round (half unit of last printed digit) | PASS |
| T2_tailk=32_104_sV | Table 2 tail k=3/2, window [104,108]: /sigma_v/ | Table 2 | 0.7853 | 0.7853 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_60_rate | Table 2 seed k=1/2, window [60,64]: rate | Table 2 | 0.7086 | 0.7086 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_60_lam | Table 2 seed k=1/2, window [60,64]: lambda | Table 2 | 0.7077 | 0.7077 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_60_lam2 | Table 2 seed k=1/2, window [60,64]: lambda-lambda'/lambda | Table 2 | 0.7079 | 0.7079 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_60_sV | Table 2 seed k=1/2, window [60,64]: /sigma_v/ | Table 2 | 0.7635 | 0.7635 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_84_rate | Table 2 seed k=1/2, window [84,88]: rate | Table 2 | 0.7272 | 0.7272 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_84_lam | Table 2 seed k=1/2, window [84,88]: lambda | Table 2 | 0.7285 | 0.7285 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_84_lam2 | Table 2 seed k=1/2, window [84,88]: lambda-lambda'/lambda | Table 2 | 0.7273 | 0.7273 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_84_sV | Table 2 seed k=1/2, window [84,88]: /sigma_v/ | Table 2 | 0.7780 | 0.778 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_104_rate | Table 2 seed k=1/2, window [104,108]: rate | Table 2 | 0.7425 | 0.7425 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_104_lam | Table 2 seed k=1/2, window [104,108]: lambda | Table 2 | 0.7433 | 0.7433 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_104_lam2 | Table 2 seed k=1/2, window [104,108]: lambda-lambda'/lambda | Table 2 | 0.7426 | 0.7426 | round (half unit of last printed digit) | PASS |
| T2_seedk=12_104_sV | Table 2 seed k=1/2, window [104,108]: /sigma_v/ | Table 2 | 0.7826 | 0.7826 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_60_rate | Table 2 seed k=3/2, window [60,64]: rate | Table 2 | 0.6948 | 0.6948 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_60_lam | Table 2 seed k=3/2, window [60,64]: lambda | Table 2 | 0.6890 | 0.689 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_60_lam2 | Table 2 seed k=3/2, window [60,64]: lambda-lambda'/lambda | Table 2 | 0.6930 | 0.693 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_60_sV | Table 2 seed k=3/2, window [60,64]: /sigma_v/ | Table 2 | 0.7704 | 0.7704 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_84_rate | Table 2 seed k=3/2, window [84,88]: rate | Table 2 | 0.6861 | 0.6861 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_84_lam | Table 2 seed k=3/2, window [84,88]: lambda | Table 2 | 0.6866 | 0.6866 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_84_lam2 | Table 2 seed k=3/2, window [84,88]: lambda-lambda'/lambda | Table 2 | 0.6861 | 0.6861 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_84_sV | Table 2 seed k=3/2, window [84,88]: /sigma_v/ | Table 2 | 0.7803 | 0.7803 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_104_rate | Table 2 seed k=3/2, window [104,108]: rate | Table 2 | 0.6926 | 0.6926 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_104_lam | Table 2 seed k=3/2, window [104,108]: lambda | Table 2 | 0.6930 | 0.693 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_104_lam2 | Table 2 seed k=3/2, window [104,108]: lambda-lambda'/lambda | Table 2 | 0.6926 | 0.6926 | round (half unit of last printed digit) | PASS |
| T2_seedk=32_104_sV | Table 2 seed k=3/2, window [104,108]: /sigma_v/ | Table 2 | 0.7831 | 0.7831 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_60_rate | Table 2 seed k=5/2, window [60,64]: rate | Table 2 | 0.6958 | 0.6958 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_60_lam | Table 2 seed k=5/2, window [60,64]: lambda | Table 2 | 0.6889 | 0.6889 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_60_lam2 | Table 2 seed k=5/2, window [60,64]: lambda-lambda'/lambda | Table 2 | 0.6938 | 0.6938 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_60_sV | Table 2 seed k=5/2, window [60,64]: /sigma_v/ | Table 2 | 0.7701 | 0.7701 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_84_rate | Table 2 seed k=5/2, window [84,88]: rate | Table 2 | 0.6808 | 0.6808 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_84_lam | Table 2 seed k=5/2, window [84,88]: lambda | Table 2 | 0.6811 | 0.6811 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_84_lam2 | Table 2 seed k=5/2, window [84,88]: lambda-lambda'/lambda | Table 2 | 0.6808 | 0.6808 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_84_sV | Table 2 seed k=5/2, window [84,88]: /sigma_v/ | Table 2 | 0.7794 | 0.7794 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_104_rate | Table 2 seed k=5/2, window [104,108]: rate | Table 2 | 0.6838 | 0.6838 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_104_lam | Table 2 seed k=5/2, window [104,108]: lambda | Table 2 | 0.6840 | 0.684 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_104_lam2 | Table 2 seed k=5/2, window [104,108]: lambda-lambda'/lambda | Table 2 | 0.6838 | 0.6838 | round (half unit of last printed digit) | PASS |
| T2_seedk=52_104_sV | Table 2 seed k=5/2, window [104,108]: /sigma_v/ | Table 2 | 0.7819 | 0.7819 | round (half unit of last printed digit) | PASS |
| T2_km_k=12 | Table 2 caption: kappa_-(mu_f) for k=1/2 | Table 2 | 0.78930 | 0.7893 | round (half unit of last printed digit) | PASS |
| T2_km_k=32 | Table 2 caption: kappa_-(mu_f) for k=3/2 | Table 2 | 0.78482 | 0.78482 | round (half unit of last printed digit) | PASS |
| T2_km_k=52 | Table 2 caption: kappa_-(mu_f) for k=5/2 | Table 2 | 0.78342 | 0.78342 | round (half unit of last printed digit) | PASS |
| seed_node_k=12 | node of the seeded phi_v on U=1 (k=1/2) | Sec. 3 (Table 2 text) | 44.5 | 44.25 | abs:0.5 (the paper quotes the node range "v ~ 44.5-47.5" (interpolated zeros 44.25, 46.82, 47.37; k=3/2 only has to lie inside the range)) | PASS |
| seed_node_k=32 | node of the seeded phi_v on U=1 (k=3/2) | Sec. 3 (Table 2 text) | 46 | 46.82 | abs:1.5 (the paper quotes the node range "v ~ 44.5-47.5" (interpolated zeros 44.25, 46.82, 47.37; k=3/2 only has to lie inside the range)) | PASS |
| seed_node_k=52 | node of the seeded phi_v on U=1 (k=5/2) | Sec. 3 (Table 2 text) | 47.5 | 47.37 | abs:0.5 (the paper quotes the node range "v ~ 44.5-47.5" (interpolated zeros 44.25, 46.82, 47.37; k=3/2 only has to lie inside the range)) | PASS |
| rel_main_U1_from72 | max /rate - (lambda - lambda'/lambda)/, five series, rays U=1 and 1.2, windows from [72,76] | Sec. 3 | 0.0002 | 0.000108 | le (bound quoted in the text) | PASS |
| rel_main_U06_from72 | same on U=0.6 from [72,76] | Sec. 3 | 0.0002 | 0.00019 | le (bound quoted in the text) | PASS |
| rel_seeded_60_min | seeded runs, U=1, [60,64]: smallest difference (+0.7e-3) | Sec. 3 | 0.7e-3 | 0.000701 | round (half unit of last printed digit) | PASS |
| rel_seeded_60_max | seeded runs, U=1, [60,64]: largest difference (+2.1e-3) | Sec. 3 | 2.1e-3 | 0.00207 | round (half unit of last printed digit) | PASS |
| rel_tail_60 | tail alone, U=1, [60,64]: difference | Sec. 3 | 0.0002 | 0.000161 | le (bound quoted in the text) | PASS |
| rel_M_small_min | difference on U=0.3, 0.6 while M<~10: smallest | Sec. 3 | 0.01 | 0.014 | abs:0.005 (paper quotes the range "0.01-0.7" to one digit) | PASS |
| rel_M_small_max | difference on U=0.3, 0.6 while M<~10: largest | Sec. 3 | 0.7 | 0.747 | abs:0.05 (paper quotes the range "0.01-0.7" to one digit (0.747)) | PASS |
| rel_example | tail only, k=3/2, U=0.3, [84,88]: difference (M=9) | Sec. 3 | -1.4e-2 | -0.014 | round (half unit of last printed digit) | PASS |
| rel_example_M | M at v=84 for that example | Sec. 3 | 9 | 8.99 | abs:0.5 (paper: "M=9") | PASS |
| rel_M_large | difference once M >~ 4e2 (all five series, all rays, windows from [72,76]) | Sec. 3 | 0.0004 | 0.00032 | le (bound quoted in the text) | PASS |
| rel_B005_60 | B=0.05 tail only: difference at [60,64] (k=1/2, bound 5e-4) | Sec. 3 | 0.0005 | 0.000469 | le (bound quoted in the text) | PASS |
| rel_B005_72_k05 | B=0.05, k=1/2: difference from [72,76] (bound 2e-4) | Sec. 3 | 2e-4 | 0.000202 | round (half unit of last printed digit) | PASS |
| rel_B005_72_k15 | B=0.05, k=3/2: difference from [72,76] (bound 2e-4) | Sec. 3 | 0.0002 | 2.36e-05 | le (bound quoted in the text) | PASS |
| rel_B005_60_k15 | B=0.05, k=3/2: difference at [60,64] (bound 5e-4) | Sec. 3 | 0.0005 | 0.000123 | le (bound quoted in the text) | PASS |
| rate_B005_k05_min | B=0.05, k=1/2: smallest rate over the windows | Sec. 3 | 0.746 | 0.7459 | round (half unit of last printed digit) | PASS |
| rate_B005_k05_max | B=0.05, k=1/2: largest rate | Sec. 3 | 0.753 | 0.7532 | round (half unit of last printed digit) | PASS |
| rate_B005_k15_min | B=0.05, k=3/2: smallest rate | Sec. 3 | 0.672 | 0.6724 | round (half unit of last printed digit) | PASS |
| rate_B005_k15_max | B=0.05, k=3/2: largest rate | Sec. 3 | 0.675 | 0.6746 | round (half unit of last printed digit) | PASS |
| B005_km_k05 | kappa_-(mu_f) at B=0.05, k=1/2 | Sec. 3 | 0.77735 | 0.777349 | abs:6e-6 (T1 prints six digits (0.777349); paper rounds to five) | PASS |
| B005_km_k15 | kappa_-(mu_f) at B=0.05, k=3/2 | Sec. 3 | 0.76357 | 0.763567 | abs:6e-6 (T1 prints six digits (0.763567); paper rounds to five) | PASS |
| lam_corr_seed_k05_72 | without the lambda'/lambda correction: rate - lambda, seeded k=1/2, [72,76] | Sec. 3 | 1.5e-3 | 0.00154 | round (half unit of last printed digit) | PASS |
| lam_corr_seed_k15_60 | without the correction: rate - lambda, seeded k=3/2, [60,64] | Sec. 3 | 5.8e-3 | 0.00577 | round (half unit of last printed digit) | PASS |
| lam_corr_seed_k25_60 | without the correction: rate - lambda, seeded k=5/2, [60,64] | Sec. 3 | 7.0e-3 | 0.00697 | round (half unit of last printed digit) | PASS |
| seed01_72 | seed (0.01,1,0.3): difference for v>=72 (bound 5e-5) | Sec. 3 | 5e-05 | 3.22e-05 | le (bound quoted in the text) | PASS |
| seed01_60 | seed (0.01,1,0.3): difference at [60,64] | Sec. 3 | 8e-4 | 0.000829 | round (half unit of last printed digit) | PASS |
| seed07_72 | seed (0.02,0.7,0.2): difference at [72,76] | Sec. 3 | 5e-4 | 0.00051 | round (half unit of last printed digit) | PASS |
| seed07_84 | seed (0.02,0.7,0.2): difference after [72,76] (bound 5e-5) | Sec. 3 | 5e-05 | 3.15e-05 | le (bound quoted in the text) | PASS |
| seed07_60 | seed (0.02,0.7,0.2): difference at [60,64] | Sec. 3 | -5.6e-3 | -0.00561 | round (half unit of last printed digit) | PASS |
| seed07_node1 | seed (0.02,0.7,0.2): first node of phi_v | Sec. 3 | 34 | 34 | round (half unit of last printed digit) | PASS |
| seed07_node2 | seed (0.02,0.7,0.2): second node of phi_v | Sec. 3 | 54 | 54 | round (half unit of last printed digit) | PASS |
| seed05_node | wide seed (0.02,1,0.5): phi_v changes sign at v | Sec. 3 | 92 | 92 | abs:1 (grid spacing 1 in vq; paper says "v~92") | PASS |
| seed05_rate_72 | wide seed: rate of M over [72,76] | Sec. 3 | 0.52 | 0.52 | round (half unit of last printed digit) | PASS |
| seed05_lam2_72 | wide seed: lambda - lambda'/lambda over [72,76] | Sec. 3 | 0.52 | 0.52 | round (half unit of last printed digit) | PASS |
| seed05_diff_72 | wide seed: difference over [72,76] | Sec. 3 | -1.8e-3 | -0.00184 | round (half unit of last printed digit) | PASS |
| seed05_rate_84 | wide seed: rate of M over [84,88] | Sec. 3 | 0.38 | 0.38 | round (half unit of last printed digit) | PASS |
| seed05_lam2_84 | wide seed: lambda - lambda'/lambda over [84,88] | Sec. 3 | 0.61 | 0.61 | round (half unit of last printed digit) | PASS |
| seed05_diff_84 | wide seed: difference over [84,88] | Sec. 3 | -0.23 | -0.22958 | round (half unit of last printed digit) | PASS |
| seed05_rate_96 | wide seed: rate of M over [96,100] | Sec. 3 | 1.07 | 1.07 | round (half unit of last printed digit) | PASS |
| seed05_lam2_96 | wide seed: lambda - lambda'/lambda over [96,100] | Sec. 3 | 1.09 | 1.09 | round (half unit of last printed digit) | PASS |
| seed05_diff_96 | wide seed: difference over [96,100] | Sec. 3 | -0.018 | -0.01753 | abs:6e-4 (computed -0.0175 lies at the rounding boundary of -0.018) | PASS |
| seed05_rate_104 | wide seed: rate of M over [104,108] | Sec. 3 | 0.82 | 0.82 | round (half unit of last printed digit) | PASS |
| seed05_lam2_104 | wide seed: lambda - lambda'/lambda over [104,108] | Sec. 3 | 0.82 | 0.82 | round (half unit of last printed digit) | PASS |
| seed05_diff_104 | wide seed: difference over [104,108] | Sec. 3 | 2.0e-3 | 0.00198 | round (half unit of last printed digit) | PASS |
| seed03_M_U06_v60 | A=0.03 seed at U_0=0.6: extrapolated M on U=0.6 at v=60 (units 1e9) | Sec. 3 | 3.7 | 3.68 | round (half unit of last printed digit) | PASS |
| seed03_grids | A=0.03 seed: number of grids | Sec. 3 | 4 | 4 | eq (integer count) | PASS |
| seed03_both_signs | A=0.03 seed: the four grids give both signs of M at v=80 (flag) | Sec. 3 | 1 | 1 | eq (flag) | PASS |
| seed03_rneg | A=0.03 seed: sigma_v non-finite on U=1 on every grid from v=45 (r<0 between v=40 and 60) | Sec. 3 | 1 | 1 | eq (flag) | PASS |
| seed03_first_nan | A=0.03 seed: first non-finite v on U=1 (between 40 and 60) | Sec. 3 | 40 | 45 | ge (paper: "between v=40 and 60") | PASS |
| seed03_first_nan_le | A=0.03 seed: first non-finite v on U=1 (between 40 and 60) | Sec. 3 | 60 | 45 | le (paper: "between v=40 and 60") | PASS |
| flux_ratio_tail_k12_v60 | tail only k=1/2: /phi_v/ over the tail transported from H+ with r_+/r_- = 9.36, v=60 | Sec. 3 (flux) | 9.8 | 9.8 | round (half unit of last printed digit) | PASS |
| flux_exp_tail_k12_v60 | tail only k=1/2: local exponent -d ln/phi_v//d ln v, v=60 | Sec. 3 (flux) | 2.0 | 2.02 | round (half unit of last printed digit) | PASS |
| flux_ratio_tail_k12_v80 | tail only k=1/2: /phi_v/ over the tail transported from H+ with r_+/r_- = 9.36, v=80 | Sec. 3 (flux) | 8.2 | 8.2 | round (half unit of last printed digit) | PASS |
| flux_exp_tail_k12_v80 | tail only k=1/2: local exponent -d ln/phi_v//d ln v, v=80 | Sec. 3 (flux) | 2.2 | 2.16 | round (half unit of last printed digit) | PASS |
| flux_ratio_tail_k12_v100 | tail only k=1/2: /phi_v/ over the tail transported from H+ with r_+/r_- = 9.36, v=100 | Sec. 3 (flux) | 7.1 | 7.1 | round (half unit of last printed digit) | PASS |
| flux_exp_tail_k12_v100 | tail only k=1/2: local exponent -d ln/phi_v//d ln v, v=100 | Sec. 3 (flux) | 2.1 | 2.13 | round (half unit of last printed digit) | PASS |
| flux_ratio_tail_k32_v60 | tail only k=3/2: /phi_v/ over the tail transported from H+ with r_+/r_- = 9.36, v=60 | Sec. 3 (flux) | 91 | 91.2 | round (half unit of last printed digit) | PASS |
| flux_exp_tail_k32_v60 | tail only k=3/2: local exponent -d ln/phi_v//d ln v, v=60 | Sec. 3 (flux) | 3.0 | 3.04 | round (half unit of last printed digit) | PASS |
| flux_ratio_tail_k32_v80 | tail only k=3/2: /phi_v/ over the tail transported from H+ with r_+/r_- = 9.36, v=80 | Sec. 3 (flux) | 69 | 69.3 | round (half unit of last printed digit) | PASS |
| flux_exp_tail_k32_v80 | tail only k=3/2: local exponent -d ln/phi_v//d ln v, v=80 | Sec. 3 (flux) | 3.8 | 3.84 | round (half unit of last printed digit) | PASS |
| flux_ratio_tail_k32_v100 | tail only k=3/2: /phi_v/ over the tail transported from H+ with r_+/r_- = 9.36, v=100 | Sec. 3 (flux) | 47 | 47 | round (half unit of last printed digit) | PASS |
| flux_exp_tail_k32_v100 | tail only k=3/2: local exponent -d ln/phi_v//d ln v, v=100 | Sec. 3 (flux) | 4.6 | 4.58 | round (half unit of last printed digit) | PASS |
| flux_ratio_min | smallest ratio to the transported tail (tail only and seeded k=1/2, 3/2) | Sec. 3 (flux) | 7 | 7.1 | round (half unit of last printed digit) | PASS |
| flux_ratio_max | largest ratio to the transported tail (tail only and seeded k=1/2, 3/2) | Sec. 3 (flux) | 110 | 106.7 | abs:5 (quoted to two significant figures (106.7 -> 110)) | PASS |
| flux_ratio_k25 | seeded k=5/2: ratio to the transported tail (~3e3) | Sec. 3 (flux) | 3e3 | 3013 | round (half unit of last printed digit) | PASS |
| flux_spread_k05 | spread of phi_v over the rays U=0.3-1.2 at v=100, k=1/2 (percent) | Sec. 3 (flux) | 2.5 | 2.5 | round (half unit of last printed digit) | PASS |
| flux_spread_k15 | spread of phi_v over the rays at v=100, k=3/2 (percent) | Sec. 3 (flux) | 1 | 1.1 | abs:0.5 (paper quotes 1 (computed 1.1)) | PASS |
| flux_vs_T0_k05 | phi_v over T(0) j at v=100, k=1/2 | Sec. 3 (flux) | 1.4 | 1.43 | abs:0.05 (two-digit rounding of 1.43) | PASS |
| flux_vs_T0_k15 | phi_v over T(0) j at v=100, k=3/2 | Sec. 3 (flux) | 9.5 | 9.54 | abs:0.05 (two-digit rounding of 9.54) | PASS |
| flux_exp_k15_B0003_v140 | local exponent of phi_v at v=140, k=3/2, B=0.003 | Sec. 3 (flux) | 5.5 | 5.54 | abs:0.05 (two digits of 5.54) | PASS |
| late_sV_k1.5_v62 | /sigma_v/ on U=1, tail only k=3/2, v~62 | Sec. 3 (late times) | 0.7880 | 0.788 | round (half unit of last printed digit) | PASS |
| late_sV_k1.5_v74 | /sigma_v/ on U=1, tail only k=3/2, v~74 | Sec. 3 (late times) | 0.7868 | 0.7868 | round (half unit of last printed digit) | PASS |
| late_sV_k1.5_v86 | /sigma_v/ on U=1, tail only k=3/2, v~86 | Sec. 3 (late times) | 0.7860 | 0.786 | round (half unit of last printed digit) | PASS |
| late_sV_k1.5_v98 | /sigma_v/ on U=1, tail only k=3/2, v~98 | Sec. 3 (late times) | 0.7855 | 0.7855 | round (half unit of last printed digit) | PASS |
| late_sV_k1.5_v106 | /sigma_v/ on U=1, tail only k=3/2, v~106 | Sec. 3 (late times) | 0.7853 | 0.7853 | round (half unit of last printed digit) | PASS |
| late_sV_pct_k1.5 | /sigma_v/ above kappa_-(mu_f) at v=106, k=3/2 (percent) | Sec. 3 (late times) | 0.06 | 0.062 | abs:0.005 (paper rounds 0.062 to 0.06) | PASS |
| late_exp60_k1.5 | local exponent of the excess /sigma_v/ - kappa_- at v=60 (U=1), k=3/2 | Sec. 3 (late times) | 2.1 | 2.104 | round (half unit of last printed digit) | PASS |
| late_exp100_k1.5 | local exponent of the excess at v=100, k=3/2 | Sec. 3 (late times) | 4.4 | 4.406 | round (half unit of last printed digit) | PASS |
| late_sV_k0.5_v62 | /sigma_v/ on U=1, tail only k=1/2, v~62 | Sec. 3 (late times) | 0.8008 | 0.8008 | round (half unit of last printed digit) | PASS |
| late_sV_k0.5_v74 | /sigma_v/ on U=1, tail only k=1/2, v~74 | Sec. 3 (late times) | 0.7986 | 0.7986 | round (half unit of last printed digit) | PASS |
| late_sV_k0.5_v86 | /sigma_v/ on U=1, tail only k=1/2, v~86 | Sec. 3 (late times) | 0.7967 | 0.7967 | round (half unit of last printed digit) | PASS |
| late_sV_k0.5_v98 | /sigma_v/ on U=1, tail only k=1/2, v~98 | Sec. 3 (late times) | 0.7953 | 0.7953 | round (half unit of last printed digit) | PASS |
| late_sV_k0.5_v106 | /sigma_v/ on U=1, tail only k=1/2, v~106 | Sec. 3 (late times) | 0.7945 | 0.7945 | round (half unit of last printed digit) | PASS |
| late_sV_pct_k0.5 | /sigma_v/ above kappa_-(mu_f) at v=106, k=1/2 (percent) | Sec. 3 (late times) | 0.66 | 0.659 | round (half unit of last printed digit) | PASS |
| late_exp60_k0.5 | local exponent of the excess /sigma_v/ - kappa_- at v=60 (U=1), k=1/2 | Sec. 3 (late times) | 0.9 | 0.854 | abs:0.06 (computed 0.85 lies on the rounding boundary of 0.9) | PASS |
| late_exp100_k0.5 | local exponent of the excess at v=100, k=1/2 | Sec. 3 (late times) | 1.7 | 1.701 | round (half unit of last printed digit) | PASS |
| late_U03_min | k=1/2, U=0.3: excess /sigma_v/ - kappa_- over v=70-100, smallest (1e-3) | Sec. 3 (late times) | 2.0 | 2.01 | round (half unit of last printed digit) | PASS |
| late_U03_max | same, largest (1e-3) | Sec. 3 (late times) | 2.3 | 2.26 | abs:0.05 (computed 2.26 (paper: 2.0-2.3)) | PASS |
| late_U03_fall | k=1/2, U=0.3: the excess falls by about 10 percent after v=80 | Sec. 3 (late times) | 10 | 11 | abs:1.5 (paper says "about 10%") | PASS |
| late_seeded_k15 | seeded k=3/2: /sigma_v/ at v=106 | Sec. 3 (late times) | 0.7831 | 0.7831 | round (half unit of last printed digit) | PASS |
| late_B005_k15_pct | B=0.05 k=3/2: excess at v~106 (percent) | Sec. 3 (late times) | 0.20 | 0.2 | round (half unit of last printed digit) | PASS |
| late_B005_k15_sV | B=0.05 k=3/2: /sigma_v/ at v~106 | Sec. 3 (late times) | 0.7651 | 0.7651 | round (half unit of last printed digit) | PASS |
| late_B005_k15_sV62 | B=0.05 k=3/2: /sigma_v/ at v~62 | Sec. 3 (late times) | 0.7735 | 0.7735 | round (half unit of last printed digit) | PASS |
| late_B005_k05_pct | B=0.05 k=1/2: excess at v~106 (percent) | Sec. 3 (late times) | 2.1 | 2.06 | round (half unit of last printed digit) | PASS |
| late_B005_k05_sV | B=0.05 k=1/2: /sigma_v/ at v~106 | Sec. 3 (late times) | 0.7934 | 0.7934 | round (half unit of last printed digit) | PASS |
| src_a_seed_min | seed alone (B=0): smallest /phi_v/(v=100) on the four rays | Sec. 4.1(a) | 4e-7 | 3.8e-07 | round (half unit of last printed digit) | PASS |
| src_a_seed_max | seed alone: largest /phi_v/(v=100) | Sec. 4.1(a) | 1e-6 | 1.03e-06 | round (half unit of last printed digit) | PASS |
| src_a_tail | tail alone: /phi_v/(v=100), B=0.03, k=3/2, U=1 | Sec. 4.1(a) | 1.9e-4 | 0.000193 | round (half unit of last printed digit) | PASS |
| src_a_rate50 | seed alone: local decay rate at v=50 (U=1, A=0.02, U0=1, w=0.3) | Sec. 4.1(a) | 0.27 | 0.2717 | round (half unit of last printed digit) | PASS |
| src_a_rate100 | seed alone: local decay rate at v=100 | Sec. 4.1(a) | 0.076 | 0.0758 | round (half unit of last printed digit) | PASS |
| src_b_phi_V0_0.3 | /phi_v/(v=100) for phi_H = B(1+v/V0)^-k, V0=0.3 | Sec. 4.1(b) | 1.6e-4 | 0.000161 | round (half unit of last printed digit) | PASS |
| src_b_rate_V0_0.3 | local rate -d ln/phi_v//dv at v=100, V0=0.3 | Sec. 4.1(b) | 0.0486 | 0.0486 | round (half unit of last printed digit) | PASS |
| src_b_phi_V0_1 | /phi_v/(v=100) for phi_H = B(1+v/V0)^-k, V0=1 | Sec. 4.1(b) | 1.9e-4 | 0.000193 | round (half unit of last printed digit) | PASS |
| src_b_rate_V0_1 | local rate -d ln/phi_v//dv at v=100, V0=1 | Sec. 4.1(b) | 0.0459 | 0.0459 | round (half unit of last printed digit) | PASS |
| src_b_phi_V0_10 | /phi_v/(v=100) for phi_H = B(1+v/V0)^-k, V0=10 | Sec. 4.1(b) | 9.2e-4 | 0.000922 | round (half unit of last printed digit) | PASS |
| src_b_rate_V0_10 | local rate -d ln/phi_v//dv at v=100, V0=10 | Sec. 4.1(b) | 0.0295 | 0.0295 | round (half unit of last printed digit) | PASS |
| src_c_rate_v40 | pulse of horizon flux: local rate at v=40 on U=1 | Sec. 4.1(c) | 0.0589 | 0.0589 | round (half unit of last printed digit) | PASS |
| src_c_rate_v50 | pulse of horizon flux: local rate at v=50 on U=1 | Sec. 4.1(c) | 0.0565 | 0.0565 | round (half unit of last printed digit) | PASS |
| src_c_rate_v60 | pulse of horizon flux: local rate at v=60 on U=1 | Sec. 4.1(c) | 0.0534 | 0.0534 | round (half unit of last printed digit) | PASS |
| src_c_rate_v70 | pulse of horizon flux: local rate at v=70 on U=1 | Sec. 4.1(c) | 0.0514 | 0.0514 | round (half unit of last printed digit) | PASS |
| src_c_rate_v80 | pulse of horizon flux: local rate at v=80 on U=1 | Sec. 4.1(c) | 0.0502 | 0.0502 | round (half unit of last printed digit) | PASS |
| src_c_rate_v90 | pulse of horizon flux: local rate at v=90 on U=1 | Sec. 4.1(c) | 0.0494 | 0.0494 | round (half unit of last printed digit) | PASS |
| src_c_rate_v100 | pulse of horizon flux: local rate at v=100 on U=1 | Sec. 4.1(c) | 0.0489 | 0.0489 | round (half unit of last printed digit) | PASS |
| src_c_peak_U1 | pulse flux peaks at v on U=1 | Sec. 4.1(c) | 34 | 34 | eq (integer grid point of the extrapolated flux) | PASS |
| src_c_peak_min | pulse flux peak, earliest over the rays (U=1.2) | Sec. 4.1(c) | 30 | 30 | eq (integer grid point) | PASS |
| src_c_peak_max | pulse flux peak, latest over the rays (U=0.3) | Sec. 4.1(c) | 59 | 59 | eq (integer grid point) | PASS |
| src_c_rate_spread | rates on the four rays agree at v=100 to (percent) | Sec. 4.1(c) | 0.2 | 0.21 | round (half unit of last printed digit) | PASS |
| src_c_kappa_plus | kappa_+ of the static hole | Sec. 4.1(c) | 0.04897 | 0.0489687 | round (half unit of last printed digit) | PASS |
| src_c_mu_f | mu_f of the B=0.03 pulse run | Sec. 4.1(c) | 0.088 | 0.0879 | round (half unit of last printed digit) | PASS |
| res_R1 | residue R_1 at omega = -i kappa_+ (central difference), m_N=5 | Sec. 4.2 | 0.6442 | 0.64423 | round (half unit of last printed digit) | PASS |
| res_R1_diff | R_1 central difference, 5 digits | Sec. 4.2 | 0.64423 | 0.64423 | round (half unit of last printed digit) | PASS |
| res_R1_c03 | R_1 by contour integral, radius 0.3 kappa_+ | Sec. 4.2 | 0.64422 | 0.64422 | round (half unit of last printed digit) | PASS |
| res_R1_c05 | R_1 by contour integral, radius 0.5 kappa_+ | Sec. 4.2 | 0.64423 | 0.64423 | round (half unit of last printed digit) | PASS |
| res_K_tau100 | K(tau) exp(kappa_+ tau) at tau ~ 100 | Sec. 4.2 | 0.65 | 0.65 | round (half unit of last printed digit) | PASS |
| res_T0_numeric | numerical A(omega = 1e-3), m_N=5 | Sec. 4.2 | 44.298 | 44.2979 | round (half unit of last printed digit) | PASS |
| res_T0_corr | O(omega^2) difference A(1e-3) - T(0) | Sec. 4.2 | 0.0066 | 0.0066 | round (half unit of last printed digit) | PASS |
| T_inf | T(omega -> infinity) = r_+/r_- (omega-extrapolated from the ODE transfer function) | Sec. 4.2 | 9.36 | 9.36 | round (half unit of last printed digit) | PASS |
| Kreg0 | K_reg(0+) from omega Im T at omega = 5.9 | Sec. 4.2 | 3.2 | 3.203 | abs:0.05 (paper: "approximately 3.2"; omega Im T = 3.203 at the largest omega of the table and still decreasing slowly) | PASS |
| res14_R1 | R_1 at m_N=1.4 (residue) | Sec. 4.5 | 0.0368 | 0.03677 | round (half unit of last printed digit) | PASS |
| res14_R1_fit | R_1 at m_N=1.4 from the three-term fit to the kernel | Sec. 4.5 | 0.0364 | 0.03641 | round (half unit of last printed digit) | PASS |
| res14_T0 | T(0) at m_N=1.4 | Sec. 4.5 | 1.73 | 1.73253 | round (half unit of last printed digit) | PASS |
| res14_memory | memory time 1/kappa_+ at m_N=1.4 | Sec. 4.5 | 11 | 11.1034 | round (half unit of last printed digit) | PASS |
| Kpulse_tau60_vs3 | impulse response K(tau=60) from the pulse at v_s=3, U=1, B=0.003 (1e-2) | Sec. 4.3(a) | 3.567 | 3.567 | round (half unit of last printed digit) | PASS |
| Kpulse_tau60_vs10 | impulse response K(tau=60) from the pulse at v_s=10, U=1, B=0.003 (1e-2) | Sec. 4.3(a) | 3.624 | 3.624 | round (half unit of last printed digit) | PASS |
| Kpulse_tau60_vs30 | impulse response K(tau=60) from the pulse at v_s=30, U=1, B=0.003 (1e-2) | Sec. 4.3(a) | 3.670 | 3.67 | round (half unit of last printed digit) | PASS |
| Kpulse_tau60_vs60 | impulse response K(tau=60) from the pulse at v_s=60, U=1, B=0.003 (1e-2) | Sec. 4.3(a) | 3.684 | 3.684 | round (half unit of last printed digit) | PASS |
| Kpulse_30_60 | kernels from v_s=30 and 60 agree for tau>=30 to (percent) | Sec. 4.3(a) | 0.4 | 0.37 | round (half unit of last printed digit) | PASS |
| Kpulse_ray_60_a | v_s=10, K(tau=60) on U=0.3 (1e-2) | Sec. 4.3(a) | 3.624 | 3.624 | round (half unit of last printed digit) | PASS |
| Kpulse_ray_60_b | v_s=10, K(tau=60) on U=1 (1e-2) | Sec. 4.3(a) | 3.624 | 3.624 | round (half unit of last printed digit) | PASS |
| Kpulse_ray_95_a | v_s=10, K(tau=95) on U=0.3 (1e-3) | Sec. 4.3(a) | 6.24 | 6.24 | round (half unit of last printed digit) | PASS |
| Kpulse_ray_95_b | v_s=10, K(tau=95) on U=1 (1e-3) | Sec. 4.3(a) | 6.24 | 6.24 | round (half unit of last printed digit) | PASS |
| Kpulse_delay_a | v_s=10, K(tau=30) on U=0.3 (1e-4) | Sec. 4.3(a) | 7.1 | 7.1 | round (half unit of last printed digit) | PASS |
| Kpulse_delay_b | v_s=10, K(tau=30) on U=1 | Sec. 4.3(a) | 0.19 | 0.19 | round (half unit of last printed digit) | PASS |
| Kinf_rate_tau30 | local decay rate of K_infinity at tau=30 | Sec. 4.3(a) | 0.0638 | 0.0638 | round (half unit of last printed digit) | PASS |
| Kinf_rate_tau40 | local decay rate of K_infinity at tau=40 | Sec. 4.3(a) | 0.0571 | 0.0571 | round (half unit of last printed digit) | PASS |
| Kinf_rate_tau50 | local decay rate of K_infinity at tau=50 | Sec. 4.3(a) | 0.0537 | 0.0537 | round (half unit of last printed digit) | PASS |
| Kinf_rate_tau60 | local decay rate of K_infinity at tau=60 | Sec. 4.3(a) | 0.0517 | 0.0517 | round (half unit of last printed digit) | PASS |
| Kinf_rate_tau70 | local decay rate of K_infinity at tau=70 | Sec. 4.3(a) | 0.0506 | 0.0506 | round (half unit of last printed digit) | PASS |
| Kinf_rate_tau80 | local decay rate of K_infinity at tau=80 | Sec. 4.3(a) | 0.0500 | 0.05 | round (half unit of last printed digit) | PASS |
| Kinf_rate_tau85 | local decay rate of K_infinity at tau=85 | Sec. 4.3(a) | 0.0497 | 0.0497 | round (half unit of last printed digit) | PASS |
| Kpulse_tau0 | response to the Gaussian pulse at tau=0 | Sec. 4.3(a) | 4.3 | 4.33 | round (half unit of last printed digit) | PASS |
| Kpulse_taum2 | smoothed response at tau=-2 | Sec. 4.3(a) | 1.2 | 1.24 | round (half unit of last printed digit) | PASS |
| kb_a | pole-tail coefficient a fitted to the ODE kernel on 60<=tau<=120 | Sec. 4.3(b) | 1.063 | 1.063 | round (half unit of last printed digit) | PASS |
| kb_b | pole-tail coefficient b | Sec. 4.3(b) | 0.056 | 0.056 | round (half unit of last printed digit) | PASS |
| kb_ratio_k05_v60 | measured/predicted phi_v, k=1/2, v=60 (B=0.003, U=1, four grids) | Sec. 4.3(b) | 1.0000 | 1 | round (half unit of last printed digit) | PASS |
| kb_ratio_k05_v100 | measured/predicted phi_v, k=1/2, v=100 (B=0.003, U=1, four grids) | Sec. 4.3(b) | 1.0002 | 1.0002 | round (half unit of last printed digit) | PASS |
| kb_ratio_k05_v290 | measured/predicted phi_v, k=1/2, v=290 (B=0.003, U=1, four grids) | Sec. 4.3(b) | 1.0003 | 1.0003 | round (half unit of last printed digit) | PASS |
| kb_ratio_k15_v60 | measured/predicted phi_v, k=3/2, v=60 (B=0.003, U=1, four grids) | Sec. 4.3(b) | 0.9996 | 0.9996 | round (half unit of last printed digit) | PASS |
| kb_ratio_k15_v100 | measured/predicted phi_v, k=3/2, v=100 (B=0.003, U=1, four grids) | Sec. 4.3(b) | 0.9998 | 0.9998 | round (half unit of last printed digit) | PASS |
| kb_ratio_k15_v290 | measured/predicted phi_v, k=3/2, v=290 (B=0.003, U=1, four grids) | Sec. 4.3(b) | 1.0003 | 1.0003 | round (half unit of last printed digit) | PASS |
| kb_every_v | prediction within this of the measured flux at every v of Table 3 | Sec. 4.3(b) | 4e-4 | 0.0004 | round (half unit of last printed digit) | PASS |
| kb_exponent | local exponents agree to | Sec. 4.3(b) | 0.01 | 0 | le (bound quoted in the text) | PASS |
| kb_sens | change of the prediction by the smoothing variance and the fit window (v=60,100,290), at most | Sec. 4.3(b) and Sec. 6, limit 7a | 1.2e-3 | 0.0012 | round (half unit of last printed digit) | PASS |
| kb_sens_drop | change of the prediction when the higher pole terms of the tail are dropped (Sec. 4.2: <=1e-3) | Sec. 4.2 | 0.001 | 0 | le (bound quoted in the text) | PASS |
| kc_rate80_mN3 | local decay rate of the pulse kernel at tau=80, m_N=3 | Sec. 4.3(c) | 0.0784 | 0.0784 | round (half unit of last printed digit) | PASS |
| kc_rate100_mN3 | local decay rate of the pulse kernel at tau=100, m_N=3 | Sec. 4.3(c) | 0.0783 | 0.0783 | round (half unit of last printed digit) | PASS |
| kc_kp_mN3 | kappa_+ of m_N=3 | Sec. 4.3(c) | 0.07827 | 0.0782687 | round (half unit of last printed digit) | PASS |
| kc_rate80_mN2 | local decay rate of the pulse kernel at tau=80, m_N=2 | Sec. 4.3(c) | 0.1054 | 0.1054 | round (half unit of last printed digit) | PASS |
| kc_rate100_mN2 | local decay rate of the pulse kernel at tau=100, m_N=2 | Sec. 4.3(c) | 0.1054 | 0.1054 | round (half unit of last printed digit) | PASS |
| kc_kp_mN2 | kappa_+ of m_N=2 | Sec. 4.3(c) | 0.10541 | 0.105406 | round (half unit of last printed digit) | PASS |
| kc_rate80_mN1.6 | local decay rate of the pulse kernel at tau=80, m_N=1.6 | Sec. 4.3(c) | 0.1102 | 0.1102 | round (half unit of last printed digit) | PASS |
| kc_rate100_mN1.6 | local decay rate of the pulse kernel at tau=100, m_N=1.6 | Sec. 4.3(c) | 0.1102 | 0.1102 | round (half unit of last printed digit) | PASS |
| kc_kp_mN1.6 | kappa_+ of m_N=1.6 | Sec. 4.3(c) | 0.1101 | 0.110128 | round (half unit of last printed digit) | PASS |
| kc_rate80_mN1.4 | local decay rate of the pulse kernel at tau=80, m_N=1.4 | Sec. 4.3(c) | 0.0895 | 0.0895 | round (half unit of last printed digit) | PASS |
| kc_rate100_mN1.4 | local decay rate of the pulse kernel at tau=100, m_N=1.4 | Sec. 4.3(c) | 0.0900 | 0.09 | round (half unit of last printed digit) | PASS |
| kc_kp_mN1.4 | kappa_+ of m_N=1.4 | Sec. 4.3(c) | 0.0901 | 0.0900626 | round (half unit of last printed digit) | PASS |
| kc_intK_mN3 | integral of the pulse kernel (trapezoid, tail added), m_N=3 | Sec. 4.3(c) | 14.37 | 14.368 | round (half unit of last printed digit) | PASS |
| kc_intK_mN2 | integral of the pulse kernel (trapezoid, tail added), m_N=2 | Sec. 4.3(c) | 5.33 | 5.332 | round (half unit of last printed digit) | PASS |
| kc_intK_mN1.6 | integral of the pulse kernel (trapezoid, tail added), m_N=1.6 | Sec. 4.3(c) | 2.81 | 2.814 | round (half unit of last printed digit) | PASS |
| kc_intK_mN1.4 | integral of the pulse kernel (trapezoid, tail added), m_N=1.4 | Sec. 4.3(c) | 1.733 | 1.733 | round (half unit of last printed digit) | PASS |
| kc_dev | kernel of Sec. 4.2 reproduces each pulse kernel over -2<=tau<=100 to (percent) | Sec. 4.3(c) | 0.5 | 0.52 | abs:0.05 (paper rounds 0.52% to 0.5%) | PASS |
| kc_mN5_v30_min | m_N=5, v_s=30 pulse kernel above the ODE kernel for tau>=5: smallest (percent) | Sec. 4.3(c) | 1.0 | 1 | round (half unit of last printed digit) | PASS |
| kc_mN5_v30_max | same: largest (percent) | Sec. 4.3(c) | 1.9 | 1.88 | round (half unit of last printed digit) | PASS |
| kc_mN5_v60_min | v_s=60: smallest (percent) | Sec. 4.3(c) | 1.9 | 1.93 | round (half unit of last printed digit) | PASS |
| kc_mN5_v60_max | v_s=60: largest (percent) | Sec. 4.3(c) | 2.4 | 2.36 | round (half unit of last printed digit) | PASS |
| kc_B0003_lo | v_s=60 pulse at B=0.0003: ratio PDE/ODE, smallest, quoted as 1.0002 +- 0.0002 | Sec. 4.3(c) | 1.0 | 1 | ge (range 1.0000-1.0004 implied by 1.0002 +- 0.0002) | PASS |
| kc_B0003_hi | same, largest | Sec. 4.3(c) | 1.0004 | 1.0002 | le (range 1.0000-1.0004 implied by 1.0002 +- 0.0002) | PASS |
| kc_mu_f_pulse | final mass parameter of the v_s=60, B=0.003 pulse run (paper: 8.5e-4, which is the v_s=10 run) | Sec. 4.3(c) | 8.5e-4 (text should read 2.1e-3) | 0.0020947 | round (half unit of last printed digit) | PASS* |
| ke_ratio_v60 | PDE/kernel flux ratio (Romberg top level) at v=60, B=0.003, k=3/2 | Sec. 4.3(e) | 0.99964 | 0.999644 | round (half unit of last printed digit) | PASS |
| ke_ratio_v100 | PDE/kernel flux ratio (Romberg top level) at v=100, B=0.003, k=3/2 | Sec. 4.3(e) | 0.99979 | 0.999789 | round (half unit of last printed digit) | PASS |
| ke_ratio_v150 | PDE/kernel flux ratio (Romberg top level) at v=150, B=0.003, k=3/2 | Sec. 4.3(e) | 1.00032 | 1.00032 | round (half unit of last printed digit) | PASS |
| ke_ratio_v200 | PDE/kernel flux ratio (Romberg top level) at v=200, B=0.003, k=3/2 | Sec. 4.3(e) | 1.00032 | 1.00032 | round (half unit of last printed digit) | PASS |
| ke_ratio_v250 | PDE/kernel flux ratio (Romberg top level) at v=250, B=0.003, k=3/2 | Sec. 4.3(e) | 1.00030 | 1.0003 | round (half unit of last printed digit) | PASS |
| ke_ratio_v300 | PDE/kernel flux ratio (Romberg top level) at v=300, B=0.003, k=3/2 | Sec. 4.3(e) | 1.00030 | 1.0003 | round (half unit of last printed digit) | PASS |
| ke_ratio_v350 | PDE/kernel flux ratio (Romberg top level) at v=350, B=0.003, k=3/2 | Sec. 4.3(e) | 1.00031 | 1.00031 | round (half unit of last printed digit) | PASS |
| ke_ratio_v420 | PDE/kernel flux ratio (Romberg top level) at v=420, B=0.003, k=3/2 | Sec. 4.3(e) | 1.00030 | 1.0003 | round (half unit of last printed digit) | PASS |
| ke_ratio_v440 | PDE/kernel flux ratio (Romberg top level) at v=440, B=0.003, k=3/2 | Sec. 4.3(e) | 1.00029 | 1.00029 | round (half unit of last printed digit) | PASS |
| ke_const | ratio constant over 150<=v<=420 to | Sec. 4.3(e) | 2e-05 | 1.8e-05 | le (bound quoted in the text (spread of the six printed ratios)) | PASS |
| ke_flux_150 | flux itself at v=150 (kernel_phi_v column, 1e-6) | Sec. 4.3(e) | 2.3 | 2.2675 | abs:0.05 (paper: "2.3e-6" from 2.2675e-6) | PASS |
| ke_flux_420 | flux at v=420 (1e-8) | Sec. 4.3(e) | 5.8 | 5.8369 | round (half unit of last printed digit) | PASS |
| ke_factor40 | flux falls by a factor ~40 between v=150 and 420 | Sec. 4.3(e) | 40 | 38.8477 | abs:1.5 (quoted to one significant figure: 2.3e-6 / 5.8e-8 = 39.7, computed ratio 38.8) | PASS |
| ke_finest_150 | finest-grid ratio at v=150 | Sec. 4.3(e) | 0.986 | 0.986121 | round (half unit of last printed digit) | PASS |
| ke_finest_400 | finest-grid ratio at v=400 | Sec. 4.3(e) | 0.47 | 0.472142 | round (half unit of last printed digit) | PASS |
| ke_level2_250 | second Romberg level departs from the first by (v=250) | Sec. 4.3(e) | 5e-4 | 0.000529 | round (half unit of last printed digit) | PASS |
| ke_level2_400 | second Romberg level departs from the first by (v=400) | Sec. 4.3(e) | 6e-3 | 0.005744 | round (half unit of last printed digit) | PASS |
| kd_static_B0.03_k1.5_v250 | PDE/kernel(static hole) flux ratio, B=0.03 k=3/2, v=250 | Sec. 4.3(d) | 1.0354 | 1.03543 | round (half unit of last printed digit) | PASS |
| kd_static_B0.03_k1.5_v290 | PDE/kernel(static hole) flux ratio, B=0.03 k=3/2, v=290 | Sec. 4.3(d) | 1.0346 | 1.0346 | round (half unit of last printed digit) | PASS |
| kd_static_B0.03_k0.5_v250 | PDE/kernel(static hole) flux ratio, B=0.03 k=1/2, v=250 | Sec. 4.3(d) | 1.0351 | 1.03511 | round (half unit of last printed digit) | PASS |
| kd_static_B0.03_k0.5_v290 | PDE/kernel(static hole) flux ratio, B=0.03 k=1/2, v=290 | Sec. 4.3(d) | 1.0349 | 1.03492 | round (half unit of last printed digit) | PASS |
| kd_static_B0.003_k1.5 | PDE/kernel(static hole) ratio at v=250, B0.003_k1.5 | Sec. 4.3(d) | 1.0003 | 1.0003 | round (half unit of last printed digit) | PASS |
| kd_static_B0.003_k0.5 | PDE/kernel(static hole) ratio at v=250, B0.003_k0.5 | Sec. 4.3(d) | 1.0003 | 1.00032 | round (half unit of last printed digit) | PASS |
| kd_final_k15 | PDE/kernel(final hole), B=0.03 k=3/2, v=250 | Sec. 4.3(d) | 1.0067 | 1.0067 | round (half unit of last printed digit) | PASS |
| kd_final_k15_const | same: constant over 150<=v<=290 to (paper: 1e-5; the spread is 7e-5 from v=150, 1e-5 from v=200) | Sec. 4.3(d) | 1e-5 (text should read 7e-5) | 7e-05 | round (half unit of last printed digit) | PASS* |
| kd_final_k05_290 | PDE/kernel(final hole), B=0.03 k=1/2, v=290 | Sec. 4.3(d) | 1.0186 | 1.01861 | round (half unit of last printed digit) | PASS |
| kd_final_k05_100 | same at v=100 | Sec. 4.3(d) | 1.0211 | 1.02112 | round (half unit of last printed digit) | PASS |
| kd_final_B0003_k15 | PDE/kernel(final hole) at B=0.003, k=3/2, v=250 | Sec. 4.3(d) | 1.0000 | 1 | round (half unit of last printed digit) | PASS |
| kd_final_B0003_k05 | same, k=1/2 | Sec. 4.3(d) | 1.0002 | 1.00016 | round (half unit of last printed digit) | PASS |
| kd_account_k15 | displacement of the horizons accounts for (percent of the excess), k=3/2 | Sec. 4.3(d) | 81 | 81.1 | round (half unit of last printed digit) | PASS |
| kd_account_k05 | displacement of the horizons accounts for (percent), k=1/2 | Sec. 4.3(d) | 46 (text should read 47) | 46.6 | round (half unit of last printed digit) | PASS* |
| kd_static_k2_250 | PDE/kernel(static hole), k=2, B=0.03, v=250 | Sec. 4.3(d) | 1.0440 | 1.04396 | round (half unit of last printed digit) | PASS |
| kd_static_k2_290 | same at v=290 | Sec. 4.3(d) | 1.0386 | 1.03857 | round (half unit of last printed digit) | PASS |
| kd_final_k2_290 | PDE/kernel(final hole), k=2, B=0.03, v=290 | Sec. 4.3(d) | 1.0058 | 1.00579 | round (half unit of last printed digit) | PASS |
| kd_final_k2_250 | PDE/kernel(final hole), k=2, B=0.03, v=250 (Sec. 5: matching factor r_b) | Sec. 5 | 1.0058 | 1.00581 | round (half unit of last printed digit) | PASS |
| kd_static_k3_250 | PDE/kernel(static hole), k=3, B=0.03, v=250 | Sec. 4.3(d) | 1.0639 | 1.06391 | round (half unit of last printed digit) | PASS |
| kd_static_k3_290 | same at v=290 | Sec. 4.3(d) | 1.0672 | 1.06724 | round (half unit of last printed digit) | PASS |
| kd_final_k3_290 | PDE/kernel(final hole), k=3, B=0.03, v=290 | Sec. 4.3(d) | 1.0056 | 1.00557 | round (half unit of last printed digit) | PASS |
| kd_final_k3_250 | PDE/kernel(final hole), k=3, B=0.03, v=250 (Sec. 5: matching factor r_b) | Sec. 5 | 1.0055 | 1.00554 | round (half unit of last printed digit) | PASS |
| kd_final_const_k2k3 | final-hole ratio constant over 150<=v<=290 for k=2, 3 (paper: 1e-5; spreads are 1.5e-4 and 4e-5) | Sec. 4.3(d) | 1e-5 (text should read 1.4e-4) | 0.00014 | round (half unit of last printed digit) | PASS* |
| kd_rem_low | remainder of the tails k>=3/2 in units of mu_f: smallest (k=3) | Sec. 4.3(d) | 0.48 | 0.48 | round (half unit of last printed digit) | PASS |
| kd_rem_high | remainder in units of mu_f: largest (k=3/2) | Sec. 4.3(d) | 0.67 | 0.673 | round (half unit of last printed digit) | PASS |
| kd_rem_k05 | remainder in units of mu_f for k=1/2 | Sec. 4.3(d) | 3 | 3.169 | abs:0.2 (paper: "3 mu_f" (computed 3.17); the later text says 3-4 mu_f) | PASS |
| kd_scal_B003 | k=1/2, B=0.03: remainder at v=100 | Sec. 4.3(d) | 2.12e-2 | 0.02117 | round (half unit of last printed digit) | PASS |
| kd_scal_B005 | k=1/2, B=0.05: remainder at v=100 | Sec. 4.3(d) | 6.67e-2 | 0.06673 | round (half unit of last printed digit) | PASS |
| kd_scal_mu03 | k=1/2, B=0.03: remainder in units of mu_f | Sec. 4.3(d) | 3.6 | 3.58016 | round (half unit of last printed digit) | PASS |
| kd_scal_mu05 | k=1/2, B=0.05: remainder in units of mu_f | Sec. 4.3(d) | 4.1 | 4.0539 | round (half unit of last printed digit) | PASS |
| kd_scal_ratio | ratio of the remainders B=0.05 / B=0.03 | Sec. 4.3(d) | 3.15 | 3.1521 | round (half unit of last printed digit) | PASS |
| kd_scal_B4 | excess of the remainder ratio over B^2 scaling, eps(0.05)/eps(0.03) / (0.05/0.03)^2 - 1 (percent) | Sec. 4.3(d) | 13 | 13.4757 | abs:1 (the text calls this a "B^4 term of ~13%"; the quantity is 13.5%) | PASS |
| kd_scal_k15_B003 | k=3/2, B=0.03: remainder at v=100 | Sec. 4.3(d) | 7.1e-3 | 0.007147 | round (half unit of last printed digit) | PASS |
| kd_scal_k15_B0003 | k=3/2, B=0.003: remainder at v=100 | Sec. 4.3(d) | -5.5e-4 | -0.0005451 | round (half unit of last printed digit) | PASS |
| kd_scal_k15_B0003_v290 | k=3/2, B=0.003: ratio - 1 at v=290 | Sec. 4.3(d) | 3e-5 | 3e-05 | round (half unit of last printed digit) | PASS |
| kd_scal_k05_B0003 | k=1/2, B=0.003: remainder at v>=250 | Sec. 4.3(d) | 1.6e-4 | 0.00016 | round (half unit of last printed digit) | PASS |
| kd_scal_k05_B0003_mu | same in units of mu_f | Sec. 4.3(d) | 2.7 | 2.71 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_vs60_B0.0003 | pulse v_s=60, B=0.0003: PDE response at tau=60 exceeds the final-hole kernel by | Sec. 4.3(d) | 1.2e-4 | 0.000122 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_vs60_B0.003 | pulse v_s=60, B=0.003: PDE response at tau=60 exceeds the final-hole kernel by | Sec. 4.3(d) | 1.25e-2 | 0.0125 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_vs30_B0.0003 | pulse v_s=30, B=0.0003: PDE response at tau=60 exceeds the final-hole kernel by | Sec. 4.3(d) | 9.9e-5 | 9.87e-05 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_vs30_B0.003 | pulse v_s=30, B=0.003: PDE response at tau=60 exceeds the final-hole kernel by | Sec. 4.3(d) | 1.0e-2 | 0.0101 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_range_lo | eps/mu_f for v_s=30, 60: smallest | Sec. 4.3(d) | 5.8 | 5.81 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_range_hi | eps/mu_f for v_s=30, 60: largest | Sec. 4.3(d) | 6.0 | 5.98 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_vs10_B0003 | pulse v_s=10, B=3e-4: excess over the final-hole kernel | Sec. 4.3(d) | 2.2e-6 | 2.15e-06 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_vs10_B003 | pulse v_s=10, B=3e-3: excess over the final-hole kernel | Sec. 4.3(d) | 2.2e-4 | 0.000215 | round (half unit of last printed digit) | PASS |
| kd_pulse_eps_vs10_mu | pulse v_s=10: eps/mu_f | Sec. 4.3(d) | 0.25 | 0.25 | round (half unit of last printed digit) | PASS |
| kd_pulse_v1 | pulse v_s=10, B=3e-3: same excess at v1=110 and 150 | Sec. 4.3(d) | 2.2e-4 | 0.000215 | round (half unit of last printed digit) | PASS |
| kd_pulse_B2_vs60 | eps/B^2 of the v_s=60 pulse at B=3e-4 against B=3e-3 (paper: B^2 scaling "to three digits"; they differ by 3 percent) | Sec. 4.3(d) | 0.1 (text should read 2.8) | 2.80172 | round (half unit of last printed digit) | PASS* |
| kd_pulse_removes_35 | replacing the static-hole kernel by the final-hole kernel removes (percent of the deviation), v_s=30, B=3e-3 | Sec. 4.3(d) | 35 | 35.2564 | round (half unit of last printed digit) | PASS |
| kd_pulse_static_coeff | static-hole kernel deviation of the v_s=30,60 pulses in units of mu_f (paper: 9.3 -> 6.0) | Sec. 4.3(d) | 9.3 | 9.20546 | abs:0.2 (computed mean of the two pulses 9.17; the log prints 9.14 and 9.20) | PASS |
| kd_pulse_removes_93 | same for v_s=10 (percent) | Sec. 4.3(d) | 93 | 92.637 | round (half unit of last printed digit) | PASS |
| kd_pulse_vs3 | pulse at v_s=3 (B=3e-3 only): excess over the final-hole kernel | Sec. 4.3(d) | -1.4e-2 | -0.014 | round (half unit of last printed digit) | PASS |
| kd_const_factor | matching factor constant in v between 250 and 290 to (bound 1e-3), all four B=0.03 tails | Sec. 4.3(d) | 0.001 | 0.00015 | le (bound quoted in the text) | PASS |
| xo_vc_k0.5 | crossover v at which phi_v is within 10% of T(0) j(v), k=1/2 | Sec. 4.4 | 200 | 200 | round (half unit of last printed digit) | PASS |
| xo_ratio100_k0.5 | phi_v/(T(0) j) at v=100, k=1/2 | Sec. 4.4 | 1.4 | 1.43 | rel:0.04 (the log prints three significant digits (1.43, 9.54, 60.94, 3899); the text rounds to two) | PASS |
| xo_vc_k1.5 | crossover v at which phi_v is within 10% of T(0) j(v), k=3/2 | Sec. 4.4 | 310 | 310 | round (half unit of last printed digit) | PASS |
| xo_ratio100_k1.5 | phi_v/(T(0) j) at v=100, k=3/2 | Sec. 4.4 | 9.5 | 9.54 | rel:0.04 (the log prints three significant digits (1.43, 9.54, 60.94, 3899); the text rounds to two) | PASS |
| xo_vc_k2.0 | crossover v at which phi_v is within 10% of T(0) j(v), k=2 | Sec. 4.4 | 370 | 370 | round (half unit of last printed digit) | PASS |
| xo_ratio100_k2.0 | phi_v/(T(0) j) at v=100, k=2 | Sec. 4.4 | 61 | 60.94 | rel:0.04 (the log prints three significant digits (1.43, 9.54, 60.94, 3899); the text rounds to two) | PASS |
| xo_vc_k3.0 | crossover v at which phi_v is within 10% of T(0) j(v), k=3 | Sec. 4.4 | 500 | 500 | round (half unit of last printed digit) | PASS |
| xo_ratio100_k3.0 | phi_v/(T(0) j) at v=100, k=3 | Sec. 4.4 | 3.9e3 | 3899 | rel:0.04 (the log prints three significant digits (1.43, 9.54, 60.94, 3899); the text rounds to two) | PASS |
| xo_exp150_k15 | local exponent at v=150, k=3/2 | Sec. 4.4 | 5.55 | 5.55 | round (half unit of last printed digit) | PASS |
| xo_exp300_k3 | local exponent at v=300, k=3 | Sec. 4.4 | 14.1 | 14.1 | abs:0.05 (two-digit rounding of 14.06) | PASS |
| xo_exp3000_k1.5 | local exponent at v=3000, k=1.5 (-> k+1) | Sec. 4.4 | 2.51 | 2.51 | round (half unit of last printed digit) | PASS |
| xo_exp3000_k2.0 | local exponent at v=3000, k=2.0 (-> k+1) | Sec. 4.4 | 3.01 | 3.01 | round (half unit of last printed digit) | PASS |
| xo_exp3000_k3.0 | local exponent at v=3000, k=3.0 (-> k+1) | Sec. 4.4 | 4.01 | 4.01 | round (half unit of last printed digit) | PASS |
| xo_kv_k0.5 | kappa_- v at the crossover, k=1/2 | Sec. 4.4 | 160 | 159.13 | abs:6 (the text rounds kappa_- v to the nearest 10 (159, 247, 294, 398)) | PASS |
| xo_kv_k1.5 | kappa_- v at the crossover, k=3/2 | Sec. 4.4 | 250 | 246.651 | abs:6 (the text rounds kappa_- v to the nearest 10 (159, 247, 294, 398)) | PASS |
| xo_kv_k2.0 | kappa_- v at the crossover, k=2 | Sec. 4.4 | 290 | 294.39 | abs:6 (the text rounds kappa_- v to the nearest 10 (159, 247, 294, 398)) | PASS |
| xo_kv_k3.0 | kappa_- v at the crossover, k=3 | Sec. 4.4 | 400 | 397.825 | abs:6 (the text rounds kappa_- v to the nearest 10 (159, 247, 294, 398)) | PASS |
| ori_rate_pred | Ori rate kappa_-(mu_f) - 2 kappa_+ for k=3/2, B=0.03 | Sec. 4.4 | 0.6869 | 0.686884 | round (half unit of last printed digit) | PASS |
| ori_rate_meas_60 | measured rate of M at [60,64], k=3/2, tail only (B=0.03) | Sec. 4.4 | 0.6868 | 0.6868 | round (half unit of last printed digit) | PASS |
| ori_rate_meas_84 | same at [84,88] | Sec. 4.4 | 0.6911 | 0.6911 | round (half unit of last printed digit) | PASS |
| ori_rate_meas_104 | same at [104,108] | Sec. 4.4 | 0.6947 | 0.6947 | round (half unit of last printed digit) | PASS |
| ori_excess_sV | excess of /sigma_v/ over kappa_-(mu_f) at [60,64] (k=3/2, B=0.03) | Sec. 4.4 | 3.2e-3 | 0.003179 | abs:5e-5 (the table value /sigma_v/ = 0.7880 is printed to 4 digits) | PASS |
| ori_dlnphi | d ln/phi_v//dv at [60,64], k=3/2 tail only (from lambda and /sigma_v/) | Sec. 4.4 | -0.0504 | -0.0504 | abs:5e-5 (lambda and /sigma_v/ are printed to 4 digits) | PASS |
| ori_dlnphi_minus_kp | departure of d ln/phi_v//dv from -kappa_+ | Sec. 4.4 | -1.4e-3 | -0.00143126 | abs:1e-4 (built from 4-digit table entries) | PASS |
| ori_dlnphi_contrib | its contribution to lambda (twice the departure) | Sec. 4.4 | -2.9e-3 | -0.00286252 | abs:2e-4 (built from 4-digit table entries) | PASS |
| T3_k0.5_v100_rate | -d ln/phi_v//dv, Table 3 (k=0.5, v=100) | Table 3 | 0.02127 | 0.02127 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v100_beta | beta (measured), Table 3 (k=0.5, v=100) | Table 3 | 2.15 | 2.147 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v100_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=0.5, v=100) | Table 3 | 2.15 | 2.15 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v100_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=0.5, v=100) | Table 3 | 5.5e-5 | 5.5e-05 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v100_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=0.5, v=100) | Table 3 | -1.3e-2 | -0.013 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v180_rate | -d ln/phi_v//dv, Table 3 (k=0.5, v=180) | Table 3 | 0.00941 | 0.00941 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v180_beta | beta (measured), Table 3 (k=0.5, v=180) | Table 3 | 1.70 | 1.703 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v180_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=0.5, v=180) | Table 3 | 1.70 | 1.7 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v180_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=0.5, v=180) | Table 3 | 2.1e-5 | 2.1e-05 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v180_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=0.5, v=180) | Table 3 | -2.2e-3 | -0.0022 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v290_rate | -d ln/phi_v//dv, Table 3 (k=0.5, v=290) | Table 3 | 0.00538 | 0.00538 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v290_beta | beta (measured), Table 3 (k=0.5, v=290) | Table 3 | 1.57 | 1.567 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v290_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=0.5, v=290) | Table 3 | 1.57 | 1.57 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v290_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=0.5, v=290) | Table 3 | 1.1e-5 | 1.1e-05 | round (half unit of last printed digit) | PASS |
| T3_k0.5_v290_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=0.5, v=290) | Table 3 | -4.5e-4 | -0.00045 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v100_rate | -d ln/phi_v//dv, Table 3 (k=1.5, v=100) | Table 3 | 0.04588 | 0.04588 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v100_beta | beta (measured), Table 3 (k=1.5, v=100) | Table 3 | 4.63 | 4.631 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v100_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=1.5, v=100) | Table 3 | 4.63 | 4.63 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v100_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=1.5, v=100) | Table 3 | 5.9e-6 | 5.9e-06 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v100_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=1.5, v=100) | Table 3 | -4.2e-2 | -0.042 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v140_rate | -d ln/phi_v//dv, Table 3 (k=1.5, v=140) | Table 3 | 0.03930 | 0.0393 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v140_beta | beta (measured), Table 3 (k=1.5, v=140) | Table 3 | 5.54 | 5.54 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v140_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=1.5, v=140) | Table 3 | 5.54 | 5.54 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v140_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=1.5, v=140) | Table 3 | 1.1e-6 | 1.1e-06 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v140_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=1.5, v=140) | Table 3 | -4.3e-2 | -0.043 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v180_rate | -d ln/phi_v//dv, Table 3 (k=1.5, v=180) | Table 3 | 0.02755 | 0.02755 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v180_beta | beta (measured), Table 3 (k=1.5, v=180) | Table 3 | 4.99 | 4.985 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v180_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=1.5, v=180) | Table 3 | 4.99 | 4.99 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v180_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=1.5, v=180) | Table 3 | 2.9e-7 | 2.9e-07 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v180_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=1.5, v=180) | Table 3 | -2.7e-2 | -0.027 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v220_rate | -d ln/phi_v//dv, Table 3 (k=1.5, v=220) | Table 3 | 0.01675 | 0.01675 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v220_beta | beta (measured), Table 3 (k=1.5, v=220) | Table 3 | 3.70 | 3.702 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v220_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=1.5, v=220) | Table 3 | 3.70 | 3.7 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v220_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=1.5, v=220) | Table 3 | 1.2e-7 | 1.2e-07 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v220_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=1.5, v=220) | Table 3 | -1.1e-2 | -0.011 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v260_rate | -d ln/phi_v//dv, Table 3 (k=1.5, v=260) | Table 3 | 0.01133 | 0.01133 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v260_beta | beta (measured), Table 3 (k=1.5, v=260) | Table 3 | 2.96 | 2.958 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v260_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=1.5, v=260) | Table 3 | 2.96 | 2.96 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v260_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=1.5, v=260) | Table 3 | 7.0e-8 | 7e-08 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v260_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=1.5, v=260) | Table 3 | -3.5e-3 | -0.0035 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v290_rate | -d ln/phi_v//dv, Table 3 (k=1.5, v=290) | Table 3 | 0.00940 | 0.0094 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v290_beta | beta (measured), Table 3 (k=1.5, v=290) | Table 3 | 2.74 | 2.737 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v290_beta_kernel | beta (kernel from the interior ODE), Table 3 (k=1.5, v=290) | Table 3 | 2.74 | 2.74 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v290_sV | /sigma_v/ - kappa_-(mu_f), Table 3 (k=1.5, v=290) | Table 3 | 5.1e-8 | 5.1e-08 | round (half unit of last printed digit) | PASS |
| T3_k1.5_v290_lam | lambda - [kappa_- - 2(k+1)/(v+1)], Table 3 (k=1.5, v=290) | Table 3 | -1.6e-3 | -0.0016 | round (half unit of last printed digit) | PASS |
| T3_km_k05 | Table 3 caption: kappa_-(mu_f), k=1/2 | Table 3 | 0.795587 | 0.795587 | round (half unit of last printed digit) | PASS |
| T3_km_k15 | Table 3 caption: kappa_-(mu_f), k=3/2 | Table 3 | 0.795545 | 0.795545 | round (half unit of last printed digit) | PASS |
| T3_km_static | Table 3 caption: static kappa_- | Table 3 | 0.795649 | 0.795649 | round (half unit of last printed digit) | PASS |
| lr_mu_f_k05 | long run k=1/2: mu_f (units 1e-5) | Sec. 4.4 (long runs) | 5.9 | 5.9132 | round (half unit of last printed digit) | PASS |
| lr_mu_f_k15 | long run k=3/2: mu_f (units 1e-5) | Sec. 4.4 (long runs) | 9.9 | 9.935 | round (half unit of last printed digit) | PASS |
| lr_levels_gap | two highest Romberg levels of phi_v agree at v=290, k=3/2 | Sec. 4.4 (long runs) | 2.4e-3 | 0.00239 | round (half unit of last printed digit) | PASS |
| lr_beta_above_k15 | beta at v=290 above k+1 (percent), k=3/2 | Sec. 4.4 (long runs) | 10 | 9.48 | abs:1 (the text quotes 2.74/2.5 - 1 = 9.6 percent as 10) | PASS |
| lr_beta_above_k05 | beta at v=290 above k+1 (percent), k=1/2 | Sec. 4.4 (long runs) | 5 | 4.46667 | abs:0.6 (1.567/1.5 - 1 = 4.5 percent, quoted as 5) | PASS |
| lr_sV_k05_v60 | /sigma_v/ - kappa_-(mu_f) at v=60, k=1/2 | Sec. 4.4 (long runs) | 1.1e-4 | 0.00011 | round (half unit of last printed digit) | PASS |
| lr_sV_k05_v290 | same at v=290 | Sec. 4.4 (long runs) | 1.1e-5 | 1.1e-05 | round (half unit of last printed digit) | PASS |
| lr_sV_k15_v60 | same at v=60, k=3/2 | Sec. 4.4 (long runs) | 3.2e-5 | 3.2e-05 | round (half unit of last printed digit) | PASS |
| lr_sV_k15_v290 | same at v=290 | Sec. 4.4 (long runs) | 5.1e-8 | 5.1e-08 | round (half unit of last printed digit) | PASS |
| lr_sV_k15_v290_lower | same, next-lower Romberg level | Sec. 4.4 (long runs) | 5.2e-8 | 5.2e-08 | round (half unit of last printed digit) | PASS |
| lr_omit_k05_v100 | omitted -lambda'/lambda, k=1/2, v=100 | Sec. 4.4 (long runs) | -6.8e-4 | -0.000678 | round (half unit of last printed digit) | PASS |
| lr_omit_k05_v140 | omitted -lambda'/lambda, k=1/2, v=140 | Sec. 4.4 (long runs) | -3.6e-4 | -0.000363 | round (half unit of last printed digit) | PASS |
| lr_omit_k05_v290 | omitted -lambda'/lambda, k=1/2, v=290 | Sec. 4.4 (long runs) | -5e-5 | -5.04e-05 | abs:5e-6 (one significant figure of 5.04e-5) | PASS |
| lr_omit_k15_v100 | omitted -lambda'/lambda, k=3/2, v=100 | Sec. 4.4 (long runs) | -3.2e-4 | -0.000317 | round (half unit of last printed digit) | PASS |
| lr_omit_k15_v140 | omitted -lambda'/lambda, k=3/2, v=140 | Sec. 4.4 (long runs) | -6.5e-4 | -0.000653 | round (half unit of last printed digit) | PASS |
| lr_omit_k15_v180 | omitted -lambda'/lambda, k=3/2, v=180 | Sec. 4.4 (long runs) | -8.7e-4 | -0.000866 | round (half unit of last printed digit) | PASS |
| lr_omit_k15_v290 | omitted -lambda'/lambda, k=3/2, v=290 | Sec. 4.4 (long runs) | -1.2e-4 | -0.000124 | round (half unit of last printed digit) | PASS |
| lr_omit_frac_lo | omitted term as a share of the deficit at v=290, k=3/2 (percent) | Sec. 4.4 (long runs) | 8 | 7.6 | abs:0.5 (quoted as "8-11%"; computed 7.6) | PASS |
| lr_omit_frac_hi | same, k=1/2 | Sec. 4.4 (long runs) | 11 | 11.2 | round (half unit of last printed digit) | PASS |
| lr_twobeta | effective exponent of M at the flux level, 2 beta at v=290, k=3/2 | Sec. 4.4 (long runs) | 5.5 | 5.474 | abs:0.05 (2 x 2.737 = 5.47) | PASS |
| c14_ratio_v40 | kernel prediction of the measured flux at v=40, m_N=1.4 (percent) | Sec. 4.5 | 0.7 | 0.68 | abs:0.06 (the log prints the ratio to 4 digits (0.9932, 0.9974, 1.0013, 1.0011)) | PASS |
| c14_ratio_v60 | kernel prediction of the measured flux at v=60, m_N=1.4 (percent) | Sec. 4.5 | 0.3 | 0.26 | abs:0.06 (the log prints the ratio to 4 digits (0.9932, 0.9974, 1.0013, 1.0011)) | PASS |
| c14_ratio_v80 | kernel prediction of the measured flux at v=80, m_N=1.4 (percent) | Sec. 4.5 | 0.13 | 0.13 | abs:0.06 (the log prints the ratio to 4 digits (0.9932, 0.9974, 1.0013, 1.0011)) | PASS |
| c14_ratio_v100 | kernel prediction of the measured flux at v=100, m_N=1.4 (percent) | Sec. 4.5 | 0.1 | 0.11 | abs:0.06 (the log prints the ratio to 4 digits (0.9932, 0.9974, 1.0013, 1.0011)) | PASS |
| c14_ratio_v120 | kernel prediction of the measured flux for v>=120, m_N=1.4: largest deviation | Sec. 4.5 | 0.0004 | 0.0004 | le (bound quoted in the text (4e-4 or better)) | PASS |
| c14_lam_v40 | flux-level rate lambda at v=40, m_N=1.4 | Sec. 4.5 | 0.016 | 0.0161 | round (half unit of last printed digit) | PASS |
| c14_beta_v40 | beta at v=40, m_N=1.4 | Sec. 4.5 | 3.0 | 3.02 | round (half unit of last printed digit) | PASS |
| c14_lam_v100 | flux-level rate lambda at v=100, m_N=1.4 | Sec. 4.5 | 0.09 | 0.0915 | abs:0.002 (the log prints 0.0915; the text rounds to 0.09) | PASS |
| c14_beta_v100 | beta at v=100, m_N=1.4 | Sec. 4.5 | 3.7 | 3.66 | abs:0.05 (3.66 rounded to 3.7) | PASS |
| c14_lam_v240 | flux-level rate lambda at v=240, m_N=1.4 | Sec. 4.5 | 0.143 | 0.143 | round (half unit of last printed digit) | PASS |
| c14_beta_v240 | beta at v=240, m_N=1.4 | Sec. 4.5 | 2.53 | 2.53 | round (half unit of last printed digit) | PASS |
| c14_lam_neg | analytic lambda is negative only for v up to (zero crossing, linear interpolation between the printed v=10 and 15) | Sec. 4.5 | 14 | 14.5789 | abs:1 (the text says v<~14; the printed windows give 14.6) | PASS |
| c14_R1_mN5 | R_1 at m_N=5 (fit; compare 44.3) | Sec. 4.5 | 0.644 | 0.64423 | abs:0.0005 (rounded to 3 digits) | PASS |
| c14_Tstatic_mN5 | T(0) at m_N=5 | Sec. 4.5 | 44.3 | 44.3045 | round (half unit of last printed digit) | PASS |
| T4s_k32_PDE_v60 | shell table, k=3/2, PDE, window at v=60 | Sec. 4.7 table | 0.6868 | 0.6868 | round (half unit of last printed digit) | PASS |
| T4s_k32_PDE_v72 | shell table, k=3/2, PDE, window at v=72 | Sec. 4.7 table | 0.6892 | 0.6892 | round (half unit of last printed digit) | PASS |
| T4s_k32_PDE_v84 | shell table, k=3/2, PDE, window at v=84 | Sec. 4.7 table | 0.6911 | 0.6911 | round (half unit of last printed digit) | PASS |
| T4s_k32_PDE_v96 | shell table, k=3/2, PDE, window at v=96 | Sec. 4.7 table | 0.6931 | 0.6931 | round (half unit of last printed digit) | PASS |
| T4s_k32_PDE_v104 | shell table, k=3/2, PDE, window at v=104 | Sec. 4.7 table | 0.6947 | 0.6947 | round (half unit of last printed digit) | PASS |
| T4s_k32_shell_v60 | shell table, k=3/2, shell, filtered flux, window at v=60 | Sec. 4.7 table | 0.6832 | 0.6832 | round (half unit of last printed digit) | PASS |
| T4s_k32_shell_v72 | shell table, k=3/2, shell, filtered flux, window at v=72 | Sec. 4.7 table | 0.6867 | 0.6867 | round (half unit of last printed digit) | PASS |
| T4s_k32_shell_v84 | shell table, k=3/2, shell, filtered flux, window at v=84 | Sec. 4.7 table | 0.6891 | 0.6891 | round (half unit of last printed digit) | PASS |
| T4s_k32_shell_v96 | shell table, k=3/2, shell, filtered flux, window at v=96 | Sec. 4.7 table | 0.6914 | 0.6914 | round (half unit of last printed digit) | PASS |
| T4s_k32_shell_v104 | shell table, k=3/2, shell, filtered flux, window at v=104 | Sec. 4.7 table | 0.6930 | 0.693 | round (half unit of last printed digit) | PASS |
| T4s_k32_shellx_v60 | shell table, k=3/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=60 | Sec. 4.7 table | 0.6864 | 0.6864 | round (half unit of last printed digit) | PASS |
| T4s_k32_shellx_v72 | shell table, k=3/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=72 | Sec. 4.7 table | 0.6886 | 0.6886 | round (half unit of last printed digit) | PASS |
| T4s_k32_shellx_v84 | shell table, k=3/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=84 | Sec. 4.7 table | 0.6903 | 0.6903 | round (half unit of last printed digit) | PASS |
| T4s_k32_shellx_v96 | shell table, k=3/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=96 | Sec. 4.7 table | 0.6921 | 0.6921 | round (half unit of last printed digit) | PASS |
| T4s_k32_shellx_v104 | shell table, k=3/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=104 | Sec. 4.7 table | 0.6935 | 0.6935 | round (half unit of last printed digit) | PASS |
| T4s_k32_power_v60 | shell table, k=3/2, power law kappa_- - (2k+2)/(v+1), window at v=60 | Sec. 4.7 table | 0.7055 | 0.7055 | round (half unit of last printed digit) | PASS |
| T4s_k32_power_v72 | shell table, k=3/2, power law kappa_- - (2k+2)/(v+1), window at v=72 | Sec. 4.7 table | 0.7182 | 0.7182 | round (half unit of last printed digit) | PASS |
| T4s_k32_power_v84 | shell table, k=3/2, power law kappa_- - (2k+2)/(v+1), window at v=84 | Sec. 4.7 table | 0.7273 | 0.7273 | round (half unit of last printed digit) | PASS |
| T4s_k32_power_v96 | shell table, k=3/2, power law kappa_- - (2k+2)/(v+1), window at v=96 | Sec. 4.7 table | 0.7343 | 0.7343 | round (half unit of last printed digit) | PASS |
| T4s_k32_power_v104 | shell table, k=3/2, power law kappa_- - (2k+2)/(v+1), window at v=104 | Sec. 4.7 table | 0.7381 | 0.7381 | round (half unit of last printed digit) | PASS |
| T4s_k12_PDE_v60 | shell table, k=1/2, PDE, window at v=60 | Sec. 4.7 table | 0.7338 | 0.7338 | round (half unit of last printed digit) | PASS |
| T4s_k12_PDE_v72 | shell table, k=1/2, PDE, window at v=72 | Sec. 4.7 table | 0.7400 | 0.74 | round (half unit of last printed digit) | PASS |
| T4s_k12_PDE_v84 | shell table, k=1/2, PDE, window at v=84 | Sec. 4.7 table | 0.7457 | 0.7457 | round (half unit of last printed digit) | PASS |
| T4s_k12_PDE_v96 | shell table, k=1/2, PDE, window at v=96 | Sec. 4.7 table | 0.7510 | 0.751 | round (half unit of last printed digit) | PASS |
| T4s_k12_PDE_v104 | shell table, k=1/2, PDE, window at v=104 | Sec. 4.7 table | 0.7543 | 0.7543 | round (half unit of last printed digit) | PASS |
| T4s_k12_shell_v60 | shell table, k=1/2, shell, filtered flux, window at v=60 | Sec. 4.7 table | 0.7213 | 0.7213 | round (half unit of last printed digit) | PASS |
| T4s_k12_shell_v72 | shell table, k=1/2, shell, filtered flux, window at v=72 | Sec. 4.7 table | 0.7298 | 0.7298 | round (half unit of last printed digit) | PASS |
| T4s_k12_shell_v84 | shell table, k=1/2, shell, filtered flux, window at v=84 | Sec. 4.7 table | 0.7375 | 0.7375 | round (half unit of last printed digit) | PASS |
| T4s_k12_shell_v96 | shell table, k=1/2, shell, filtered flux, window at v=96 | Sec. 4.7 table | 0.7444 | 0.7444 | round (half unit of last printed digit) | PASS |
| T4s_k12_shell_v104 | shell table, k=1/2, shell, filtered flux, window at v=104 | Sec. 4.7 table | 0.7486 | 0.7486 | round (half unit of last printed digit) | PASS |
| T4s_k12_shellx_v60 | shell table, k=1/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=60 | Sec. 4.7 table | 0.7328 | 0.7328 | round (half unit of last printed digit) | PASS |
| T4s_k12_shellx_v72 | shell table, k=1/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=72 | Sec. 4.7 table | 0.7391 | 0.7391 | round (half unit of last printed digit) | PASS |
| T4s_k12_shellx_v84 | shell table, k=1/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=84 | Sec. 4.7 table | 0.7449 | 0.7449 | round (half unit of last printed digit) | PASS |
| T4s_k12_shellx_v96 | shell table, k=1/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=96 | Sec. 4.7 table | 0.7504 | 0.7504 | round (half unit of last printed digit) | PASS |
| T4s_k12_shellx_v104 | shell table, k=1/2, shell + (/sigma_v/ - kappa_-(mu_f)), window at v=104 | Sec. 4.7 table | 0.7538 | 0.7538 | round (half unit of last printed digit) | PASS |
| T4s_k12_power_v60 | shell table, k=1/2, power law kappa_- - (2k+2)/(v+1), window at v=60 | Sec. 4.7 table | 0.7417 | 0.7417 | round (half unit of last printed digit) | PASS |
| T4s_k12_power_v72 | shell table, k=1/2, power law kappa_- - (2k+2)/(v+1), window at v=72 | Sec. 4.7 table | 0.7493 | 0.7493 | round (half unit of last printed digit) | PASS |
| T4s_k12_power_v84 | shell table, k=1/2, power law kappa_- - (2k+2)/(v+1), window at v=84 | Sec. 4.7 table | 0.7548 | 0.7548 | round (half unit of last printed digit) | PASS |
| T4s_k12_power_v96 | shell table, k=1/2, power law kappa_- - (2k+2)/(v+1), window at v=96 | Sec. 4.7 table | 0.7590 | 0.759 | round (half unit of last printed digit) | PASS |
| T4s_k12_power_v104 | shell table, k=1/2, power law kappa_- - (2k+2)/(v+1), window at v=104 | Sec. 4.7 table | 0.7613 | 0.7613 | round (half unit of last printed digit) | PASS |
| T4s_excess_k32_v60 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=3/2, window at v=60 | Sec. 4.7 | 3.2e-3 | 0.0032 | round (half unit of last printed digit) | PASS |
| T4s_excess_k32_v72 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=3/2, window at v=72 | Sec. 4.7 | 2.0e-3 | 0.002 | round (half unit of last printed digit) | PASS |
| T4s_excess_k32_v84 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=3/2, window at v=84 | Sec. 4.7 | 1.2e-3 | 0.0012 | round (half unit of last printed digit) | PASS |
| T4s_excess_k32_v96 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=3/2, window at v=96 | Sec. 4.7 | 0.7e-3 | 0.0007 | round (half unit of last printed digit) | PASS |
| T4s_excess_k32_v104 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=3/2, window at v=104 | Sec. 4.7 | 0.5e-3 | 0.0005 | round (half unit of last printed digit) | PASS |
| T4s_excess_k12_v60 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=1/2, window at v=60 | Sec. 4.7 | 11.5e-3 | 0.0115 | round (half unit of last printed digit) | PASS |
| T4s_excess_k12_v72 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=1/2, window at v=72 | Sec. 4.7 | 9.3e-3 | 0.0093 | round (half unit of last printed digit) | PASS |
| T4s_excess_k12_v84 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=1/2, window at v=84 | Sec. 4.7 | 7.4e-3 | 0.0074 | round (half unit of last printed digit) | PASS |
| T4s_excess_k12_v96 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=1/2, window at v=96 | Sec. 4.7 | 6.0e-3 | 0.006 | round (half unit of last printed digit) | PASS |
| T4s_excess_k12_v104 | /sigma_v/ - kappa_-(mu_f) of the PDE, k=1/2, window at v=104 | Sec. 4.7 | 5.2e-3 | 0.0052 | round (half unit of last printed digit) | PASS |
| T4s_agree_32 | shell + excess against the PDE rate, largest difference over the five windows, k=3/2 | Sec. 4.7 | 0.0012 | 0.0012 | le (bound quoted in the text (1.2e-3 or better)) | PASS |
| T4s_agree_12 | shell + excess against the PDE rate, largest difference over the five windows, k=1/2 | Sec. 4.7 | 0.0012 | 0.001 | le (bound quoted in the text (1.2e-3 or better)) | PASS |
| T4s_agree_pct | same, as a fraction of the rate (percent, at most) | Sec. 4.7 | 0.17 | 0.172736 | round (half unit of last printed digit) | PASS |
| T4s_power_k32_lo | power-law input against the PDE, k=3/2: smallest misfit | Sec. 4.7 | 1.9e-2 | 0.0187 | round (half unit of last printed digit) | PASS |
| T4s_power_k32_hi | same: largest misfit | Sec. 4.7 | 4.3e-2 | 0.0434 | round (half unit of last printed digit) | PASS |
| T4s_power_k12_lo | power-law input against the PDE, k=1/2: smallest misfit | Sec. 4.7 | 0.7e-2 | 0.007 | abs:5e-4 (one significant figure (0.0070)) | PASS |
| T4s_power_k12_hi | same: largest misfit | Sec. 4.7 | 0.9e-2 | 0.0093 | abs:5e-4 (one significant figure (0.0093)) | PASS |
| T4s_ex_shell_v60 | k=1/2 without the measured excess: /shell - PDE/ at v=60 | Sec. 4.7 | 1.25e-2 | 0.0125 | abs:6e-4 (rate columns are printed to 4 digits; 0.0125 and 0.0102) | PASS |
| T4s_ex_power_v60 | k=1/2: /power law - PDE/ at v=60 | Sec. 4.7 | 0.8e-2 | 0.0079 | abs:6e-4 (one significant figure) | PASS |
| T4s_ex_shell_v72 | k=1/2 without the measured excess: /shell - PDE/ at v=72 | Sec. 4.7 | 1.0e-2 | 0.0102 | abs:6e-4 (rate columns are printed to 4 digits; 0.0125 and 0.0102) | PASS |
| T4s_ex_power_v72 | k=1/2: /power law - PDE/ at v=72 | Sec. 4.7 | 0.9e-2 | 0.0093 | abs:6e-4 (one significant figure) | PASS |
| T4s_k12_better_84 | k=1/2 without the excess the filtered shell beats the power law from v=84 (/shell-PDE/ < /power-PDE/), all of 84, 96, 104 | Sec. 4.7 | 1 | 1 | eq (boolean statement) | PASS |
| fnl_ratio | measured phi_v at B=0.03 over the linear one: range of the printed ratios (1.033-1.042) | Sec. 4.7 | 1.04 | 1.0419 | abs:0.005 (ratios 1.0329 to 1.0419 quoted as 1.04) | PASS |
| fnl_exponent | same exponents to | Sec. 4.7 | 0.06 | 0.06 | round (half unit of last printed digit) | PASS |
| fnl_expo_effect | a change of 0.06 in the local exponent changes 2 beta/(v+1) by (at v = 100) | Sec. 4.7 | 1.2e-3 | 0.00118812 | round (half unit of last printed digit) | PASS |
| ray_A_k15 | max /M_ODE/M_PDE - 1/ over v0 < v <= 108, tail k=3/2, B=0.03, v0 = 48, 60, 72, 84 | Sec. 5 | 6.1e-5 | 6.1e-05 | round (half unit of last printed digit) | PASS |
| ray_A_k05 | same, k=1/2 | Sec. 5 | 2.1e-6 | 2.1e-06 | round (half unit of last printed digit) | PASS |
| ray_A_v0_indep | the maximum is the same for the four starting points (spread of the four maxima) | Sec. 5 | 0 | 0 | eq (the printed maxima are identical to two digits) | PASS |
| ray_A_growth_lo_k1.5 | M_PDE at v0=48, k=3/2 | Sec. 5 | 1.2 | 1.233 | round (half unit of last printed digit) | PASS |
| ray_A_growth_hi_k1.5 | M_PDE at v=108, k=3/2 | Sec. 5 | 6.6e17 | 6.584e+17 | round (half unit of last printed digit) | PASS |
| ray_A_growth_lo_k0.5 | M_PDE at v0=48, k=1/2 | Sec. 5 | 5.6 | 5.621 | abs:0.05 (5.62 rounds to 5.6) | PASS |
| ray_A_growth_hi_k0.5 | M_PDE at v=108, k=1/2 | Sec. 5 | 1.1e20 | 1.057e+20 | round (half unit of last printed digit) | PASS |
| ray_A_levels_s_v100 | sigma_v: two highest Romberg levels agree at v=100 (k=3/2, relative) | Sec. 5 | 2e-13 | 1.5e-13 | round (half unit of last printed digit) | PASS |
| ray_A_levels_phi_v100 | phi_v: same | Sec. 5 | 3e-11 | 3e-11 | round (half unit of last printed digit) | PASS |
| ray_A_levels_M | level spread of M_PDE (v <= 108) | Sec. 5 | 1e-7 | 1.1e-07 | abs:2e-8 (quoted to one significant figure: the printed spreads are 3.3e-8, 7.4e-8, 1.1e-7) | PASS |
| ray_A_underestimate_k15 | M_PDE error divided by the level spread over the rows of Table 4 (smallest over k=3/2 and 1/2; paper: "10^2-10^3 at every v") | Sec. 5 and Fig. 4 caption | 100 (text should read 8) | 8 | ge (the text says the error exceeds the spread by 10^2-10^3 at every v) | PASS* |
| ray_A_underestimate_max | same, largest ratio over the rows | Sec. 5 | 1000 | 554 | le (upper end 10^3 of the quoted range (computed 554)) | PASS |
| T4_k1.5_v108_M | Table 4 (k=1.5) M_PDE at v=108 | Table 4 | 6.58e17 | 6.5837e+17 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v108_levels | Table 4 (k=1.5) Romberg levels at v=108 | Table 4 | 1.1e-7 | 1.1e-07 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v108_dev | Table 4 (k=1.5) M_ODE/M_PDE - 1 at v=108 | Table 4 | +1.9e-5 | 1.9e-05 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v108_rate | Table 4 (k=1.5) rate_ODE at v=108 | Table 4 | 0.69513 | 0.695132 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v108_qM | Table 4 (k=1.5) q_M at v=108 | Table 4 | 9.78 | 9.7761 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v140_M | Table 4 (k=1.5) M_PDE at v=140 | Table 4 | 3.50e27 | 3.4967e+27 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v140_levels | Table 4 (k=1.5) Romberg levels at v=140 | Table 4 | 4.1e-7 | 4.1e-07 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v140_dev | Table 4 (k=1.5) M_ODE/M_PDE - 1 at v=140 | Table 4 | +1.0e-4 | 0.0001 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v140_rate | Table 4 (k=1.5) rate_ODE at v=140 | Table 4 | 0.70565 | 0.705652 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v140_qM | Table 4 (k=1.5) q_M at v=140 | Table 4 | 11.16 | 11.1628 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v180_M | Table 4 (k=1.5) M_PDE at v=180 | Table 4 | 9.81e39 | 9.8102e+39 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v180_levels | Table 4 (k=1.5) Romberg levels at v=180 | Table 4 | 2.3e-5 | 2.3e-05 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v180_dev | Table 4 (k=1.5) M_ODE/M_PDE - 1 at v=180 | Table 4 | -2.6e-3 | -0.0026 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v180_rate | Table 4 (k=1.5) rate_ODE at v=180 | Table 4 | 0.72870 | 0.728704 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v180_qM | Table 4 (k=1.5) q_M at v=180 | Table 4 | 10.16 | 10.1572 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v240_M | Table 4 (k=1.5) M_PDE at v=240 | Table 4 | 2.47e59 | 2.474e+59 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v240_levels | Table 4 (k=1.5) Romberg levels at v=240 | Table 4 | 8.0e-5 | 8e-05 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v240_dev | Table 4 (k=1.5) M_ODE/M_PDE - 1 at v=240 | Table 4 | +2.9e-2 | 0.029 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v290_M | Table 4 (k=1.5) M_PDE at v=290 | Table 4 | 9.8e75 | 9.7844e+75 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v290_levels | Table 4 (k=1.5) Romberg levels at v=290 | Table 4 | 2.3e-3 | 0.0023 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v290_dev | Table 4 (k=1.5) M_ODE/M_PDE - 1 at v=290 | Table 4 | -6.6e-2 | -0.066 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v290_rate | Table 4 (k=1.5) rate_ODE at v=290 | Table 4 | 0.76587 | 0.76587 | round (half unit of last printed digit) | PASS |
| T4_k1.5_v290_qM | Table 4 (k=1.5) q_M at v=290 | Table 4 | 5.51 | 5.5146 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v108_M | Table 4 (k=0.5) M_PDE at v=108 | Table 4 | 1.06e20 | 1.0571e+20 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v108_levels | Table 4 (k=0.5) Romberg levels at v=108 | Table 4 | 4.2e-9 | 4.2e-09 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v108_dev | Table 4 (k=0.5) M_ODE/M_PDE - 1 at v=108 | Table 4 | -1.2e-6 | -1.2e-06 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v108_rate | Table 4 (k=0.5) rate_ODE at v=108 | Table 4 | 0.75508 | 0.755081 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v108_qM | Table 4 (k=0.5) q_M at v=108 | Table 4 | 3.73 | 3.7294 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v140_M | Table 4 (k=0.5) M_PDE at v=140 | Table 4 | 3.93e30 | 3.9299e+30 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v140_levels | Table 4 (k=0.5) Romberg levels at v=140 | Table 4 | 8.5e-9 | 8.5e-09 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v140_dev | Table 4 (k=0.5) M_ODE/M_PDE - 1 at v=140 | Table 4 | +7e-8 | 6.8e-08 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v140_rate | Table 4 (k=0.5) rate_ODE at v=140 | Table 4 | 0.76533 | 0.765327 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v140_qM | Table 4 (k=0.5) q_M at v=140 | Table 4 | 3.38 | 3.3795 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v180_M | Table 4 (k=0.5) M_PDE at v=180 | Table 4 | 9.10e43 | 9.0986e+43 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v180_levels | Table 4 (k=0.5) Romberg levels at v=180 | Table 4 | 1.3e-8 | 1.3e-08 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v180_dev | Table 4 (k=0.5) M_ODE/M_PDE - 1 at v=180 | Table 4 | +7.2e-6 | 7.2e-06 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v180_rate | Table 4 (k=0.5) rate_ODE at v=180 | Table 4 | 0.77250 | 0.772496 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v180_qM | Table 4 (k=0.5) q_M at v=180 | Table 4 | 3.04 | 3.0407 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v240_M | Table 4 (k=0.5) M_PDE at v=240 | Table 4 | 1.45e64 | 1.4504e+64 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v240_levels | Table 4 (k=0.5) Romberg levels at v=240 | Table 4 | 1.1e-7 | 1.1e-07 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v240_dev | Table 4 (k=0.5) M_ODE/M_PDE - 1 at v=240 | Table 4 | -1.2e-5 | -1.2e-05 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v290_M | Table 4 (k=0.5) M_PDE at v=290 | Table 4 | 1.17e81 | 1.1702e+81 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v290_levels | Table 4 (k=0.5) Romberg levels at v=290 | Table 4 | 4.4e-7 | 4.4e-07 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v290_dev | Table 4 (k=0.5) M_ODE/M_PDE - 1 at v=290 | Table 4 | -6.6e-6 | -6.6e-06 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v290_rate | Table 4 (k=0.5) rate_ODE at v=290 | Table 4 | 0.77959 | 0.779585 | round (half unit of last printed digit) | PASS |
| T4_k0.5_v290_qM | Table 4 (k=0.5) q_M at v=290 | Table 4 | 2.83 | 2.8259 | round (half unit of last printed digit) | PASS |
| ray_b_k05_agree | k=1/2, B=0.03: ODE and PDE mass agree up to v=290 to | Sec. 5 | 1.2e-5 | 1.2e-05 | round (half unit of last printed digit) | PASS |
| ray_b_k05_lnM | ln M at v=290, k=1/2, B=0.03 | Sec. 5 | 186.7 | 186.667 | round (half unit of last printed digit) | PASS |
| ray_b_k15_dev_v84 | k=3/2, B=0.03: /M_ODE/M_PDE - 1/ at v=84 | Sec. 5 | 9e-6 | 9.2e-06 | round (half unit of last printed digit) | PASS |
| ray_b_k15_spread_v84 | k=3/2, B=0.03: spread of the two highest Romberg levels at v=84 | Sec. 5 | 3e-8 | 3.3e-08 | round (half unit of last printed digit) | PASS |
| ray_b_k15_dev_v180 | k=3/2, B=0.03: /M_ODE/M_PDE - 1/ at v=180 | Sec. 5 | 2.6e-3 | 0.0026 | round (half unit of last printed digit) | PASS |
| ray_b_k15_spread_v180 | k=3/2, B=0.03: spread of the two highest Romberg levels at v=180 | Sec. 5 | 2e-5 | 2.3e-05 | round (half unit of last printed digit) | PASS |
| ray_b_k15_dev_v290 | k=3/2, B=0.03: /M_ODE/M_PDE - 1/ at v=290 | Sec. 5 | 7e-2 | 0.066 | round (half unit of last printed digit) | PASS |
| ray_b_k15_spread_v290 | k=3/2, B=0.03: spread of the two highest Romberg levels at v=290 | Sec. 5 | 2e-3 | 0.0023 | round (half unit of last printed digit) | PASS |
| ray_stab_finest4 | ln M_ODE changes by at most (four finest grids), k=3/2, B=0.03, 84<=v<=290 | Sec. 5 | 2e-8 | 2e-08 | round (half unit of last printed digit) | PASS |
| ray_stab_coarsest4 | same, four coarsest grids | Sec. 5 | 5e-6 | 5e-06 | round (half unit of last printed digit) | PASS |
| ray_stab_finest3 | same, three finest grids | Sec. 5 | 1.2e-6 | 1.2e-06 | round (half unit of last printed digit) | PASS |
| ray_stab_pde_v140 | extrapolated PDE ln M changes by (v=140), k=3/2 | Sec. 5 | 1e-4 | 0.00012 | abs:5e-5 (one significant figure (1.2e-4)) | PASS |
| ray_stab_pde_v290_lo | extrapolated PDE ln M changes at v=290 from one subset to another: smallest | Sec. 5 | 0.07 | 0.07 | round (half unit of last printed digit) | PASS |
| ray_stab_pde_v290_hi | same: largest | Sec. 5 | 0.6 | 0.56 | abs:0.05 (one significant figure (0.56)) | PASS |
| ray_stab_k05_ode | k=1/2: ODE ln M changes by at most (both amplitudes) | Sec. 5 | 1.4e-7 | 1.4e-07 | round (half unit of last printed digit) | PASS |
| ray_stab_k05_pde003 | k=1/2, B=0.03: PDE mass changes by up to | Sec. 5 | 1e-4 | 0.00012 | abs:5e-5 (one significant figure (1.2e-4)) | PASS |
| ray_stab_k05_pde0003 | k=1/2, B=0.003: PDE mass changes by up to | Sec. 5 | 0.2 | 0.22 | abs:0.05 (one significant figure (0.22)) | PASS |
| ray_stab_converged | ray-integrated mass converged in the grid in ln M over the whole range (all runs and subsets), at most | Sec. 5 | 1e-05 | 5.6e-06 | le (bound quoted in the text) | PASS |
| ray_levels_sV | sigma_v: two highest Romberg levels agree to (relative, v<=290, k=3/2 B=0.03) | Sec. 5 | 2e-13 | 2e-13 | round (half unit of last printed digit) | PASS |
| ray_levels_phiv | phi_v: same | Sec. 5 | 1.2e-8 | 1.2e-08 | round (half unit of last printed digit) | PASS |
| ray_rate_exact | ODE rate against 4 pi r phi_v^2/rho, k=3/2, B=0.03, v>=84 | Sec. 5 | 5e-6 | 5e-06 | round (half unit of last printed digit) | PASS |
| ray_rate_lamlam_k15 | ODE rate against lambda - lambda'/lambda, k=3/2 | Sec. 5 | 2e-5 | 1.9e-05 | round (half unit of last printed digit) | PASS |
| ray_rate_lamlam_k05 | same, k=1/2 | Sec. 5 | 4e-5 | 4.2e-05 | round (half unit of last printed digit) | PASS |
| ec_hratio | ratio of the errors of the two finest grids, every v listed | Sec. 5 | 4.00 | 4 | round (half unit of last printed digit) | PASS |
| ec_Crho_k15_v40 | C_rho at v=40, k=3/2, B=0.03 | Sec. 5 | -1.8e2 | -179.9 | round (half unit of last printed digit) | PASS |
| ec_Crho_k05_v40 | C_rho at v=40, k=1/2, B=0.03 | Sec. 5 | -87 | -86.88 | round (half unit of last printed digit) | PASS |
| ec_Crho_k15_v60 | C_rho at v=60, k=3/2, B=0.03 | Sec. 5 | -2.0e3 | -1955 | round (half unit of last printed digit) | PASS |
| ec_Crho_k05_v60 | C_rho at v=60, k=1/2, B=0.03 | Sec. 5 | -4.4e2 | -444.3 | round (half unit of last printed digit) | PASS |
| ec_Crho_k15_v100 | C_rho at v=100, k=3/2, B=0.03 | Sec. 5 | -9.2e4 | -92430 | round (half unit of last printed digit) | PASS |
| ec_Crho_k05_v100 | C_rho at v=100, k=1/2, B=0.03 | Sec. 5 | -4.0e3 | -4014 | round (half unit of last printed digit) | PASS |
| ec_dlnC_k15 | C_rho grows like exp(x v) at v ~ 100, k=3/2: x | Sec. 5 | 0.09 | 0.093 | round (half unit of last printed digit) | PASS |
| ec_dlnC_k05 | same, k=1/2 | Sec. 5 | 0.05 | 0.046 | round (half unit of last printed digit) | PASS |
| ec_Cy_k15_lo | C_y range over v=40..100, k=3/2: smallest (abs) | Sec. 5 | 70 | 70.2 | round (half unit of last printed digit) | PASS |
| ec_Cy_k15_hi | same: largest | Sec. 5 | 77 | 76.5 | abs:0.6 (76.5 rounded to 77) | PASS |
| ec_Cy_k05_lo | C_y range, k=1/2: smallest | Sec. 5 | 37 | 37.2 | round (half unit of last printed digit) | PASS |
| ec_Cy_k05_hi | same: largest | Sec. 5 | 40 | 40.5 | abs:0.6 (40.5 rounded to 40) | PASS |
| ec_rho_err_v40 | relative error of the evolved rho at h=0.003125, v=40 (percent), k=3/2 | Sec. 5 | 0.2 | 0.18 | abs:0.03 (0.18 rounded to 0.2) | PASS |
| ec_rho_err_v60 | relative error of the evolved rho at h=0.003125, v=60 (percent), k=3/2 | Sec. 5 | 1.9 | 1.9 | round (half unit of last printed digit) | PASS |
| ec_rho_err_v100 | relative error of the evolved rho at h=0.003125, v=100 (percent), k=3/2 | Sec. 5 | 90 | 90 | round (half unit of last printed digit) | PASS |
| ec_y_err | relative error of y at h=0.003125 (percent) | Sec. 5 | 0.07 | 0.073 | round (half unit of last printed digit) | PASS |
| ec_Cy_B0003 | C_y at B=0.003, v=60 | Sec. 5 | -8.3e3 | -8307 | round (half unit of last printed digit) | PASS |
| ec_Cy_B2 | C_y(B=0.003)/C_y(B=0.03) against B^-2 (percent deviation, "up to 10%") | Sec. 5 | 10 | 10.4 | abs:0.5 (10.4 percent) | PASS |
| ec_Crho_B0003 | C_rho at B=0.003, v=60 | Sec. 5 | -2.1e5 | -210300 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_v84 | Table 5 B0.03_k0.5: ln M_cc - ln M_ODE at v=84 | Table 5 | -1.3e-9 | -1.3199e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_v140 | Table 5 B0.03_k0.5: ln M_cc - ln M_ODE at v=140 | Table 5 | -1.0e-9 | -1.0313e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_v200 | Table 5 B0.03_k0.5: ln M_cc - ln M_ODE at v=200 | Table 5 | +6.3e-9 | 6.265e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_v280 | Table 5 B0.03_k0.5: ln M_cc - ln M_ODE at v=280 | Table 5 | +2.2e-9 | 2.1869e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_max | Table 5 B0.03_k0.5: max /Delta ln M/ over 84<=v<=280 | Table 5 and Result paragraph | 1.4e-8 | 1.3558e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_spread | Table 5 B0.03_k0.5: spread of ln M_cc, four finest grids | Table 5 and Result paragraph | 3.6e-10 | 3.6476e-10 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_lnK | Table 5 B0.03_k0.5: ln K bound at v=280 | Table 5 | 360 | 360.3 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k0.5_lnM280 | Table 5 caption: ln M_ODE(v=280), B0.03_k0.5 | Table 5 caption | 179 | 178.86 | abs:0.5 (rounded to integers (the value 160.5 is printed to 0.1)) | PASS |
| T5_B0.03_k0.5_U03 | Table 5 caption: max /Delta ln M/ on U=0.3, B0.03_k0.5 | Table 5 caption | 2.5e-6 | 2.4891e-06 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_v84 | Table 5 B0.03_k1.5: ln M_cc - ln M_ODE at v=84 | Table 5 | +1.9e-10 | 1.8609e-10 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_v140 | Table 5 B0.03_k1.5: ln M_cc - ln M_ODE at v=140 | Table 5 | -3.6e-9 | -3.6088e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_v200 | Table 5 B0.03_k1.5: ln M_cc - ln M_ODE at v=200 | Table 5 | -9.2e-9 | -9.2443e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_v280 | Table 5 B0.03_k1.5: ln M_cc - ln M_ODE at v=280 | Table 5 | -3.3e-7 | -3.3445e-07 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_max | Table 5 B0.03_k1.5: max /Delta ln M/ over 84<=v<=280 | Table 5 and Result paragraph | 3.3e-7 | 3.3445e-07 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_spread | Table 5 B0.03_k1.5: spread of ln M_cc, four finest grids | Table 5 and Result paragraph | 1.2e-8 | 1.2373e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_lnK | Table 5 B0.03_k1.5: ln K bound at v=280 | Table 5 | 337 | 337 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k1.5_lnM280 | Table 5 caption: ln M_ODE(v=280), B0.03_k1.5 | Table 5 caption | 167 | 167.24 | abs:0.5 (rounded to integers (the value 160.5 is printed to 0.1)) | PASS |
| T5_B0.03_k1.5_U03 | Table 5 caption: max /Delta ln M/ on U=0.3, B0.03_k1.5 | Table 5 caption | 1.1e-5 | 1.05e-05 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_v84 | Table 5 B0.03_k2: ln M_cc - ln M_ODE at v=84 | Table 5 | -5.8e-9 | -5.7726e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_v140 | Table 5 B0.03_k2: ln M_cc - ln M_ODE at v=140 | Table 5 | -9.7e-9 | -9.7427e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_v200 | Table 5 B0.03_k2: ln M_cc - ln M_ODE at v=200 | Table 5 | -1.4e-8 | -1.4315e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_v280 | Table 5 B0.03_k2: ln M_cc - ln M_ODE at v=280 | Table 5 | -1.1e-6 | -1.0516e-06 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_max | Table 5 B0.03_k2: max /Delta ln M/ over 84<=v<=280 | Table 5 and Result paragraph | 1.1e-6 | 1.0516e-06 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_spread | Table 5 B0.03_k2: spread of ln M_cc, four finest grids | Table 5 and Result paragraph | 1.1e-7 | 1.0615e-07 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_lnK | Table 5 B0.03_k2: ln K bound at v=280 | Table 5 | 327 | 326.8 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k2_lnM280 | Table 5 caption: ln M_ODE(v=280), B0.03_k2 | Table 5 caption | 162 | 162.15 | abs:0.5 (rounded to integers (the value 160.5 is printed to 0.1)) | PASS |
| T5_B0.03_k2_U03 | Table 5 caption: max /Delta ln M/ on U=0.3, B0.03_k2 | Table 5 caption | 1.3e-5 | 1.3092e-05 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_v84 | Table 5 B0.03_k3: ln M_cc - ln M_ODE at v=84 | Table 5 | +7.7e-10 | 7.7156e-10 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_v140 | Table 5 B0.03_k3: ln M_cc - ln M_ODE at v=140 | Table 5 | -3.0e-9 | -3.0453e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_v200 | Table 5 B0.03_k3: ln M_cc - ln M_ODE at v=200 | Table 5 | +1.3e-8 | 1.3084e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_v280 | Table 5 B0.03_k3: ln M_cc - ln M_ODE at v=280 | Table 5 | -1.4e-6 | -1.3882e-06 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_max | Table 5 B0.03_k3: max /Delta ln M/ over 84<=v<=280 | Table 5 and Result paragraph | 1.4e-6 | 1.3882e-06 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_spread | Table 5 B0.03_k3: spread of ln M_cc, four finest grids | Table 5 and Result paragraph | 7.8e-7 | 7.8124e-07 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_lnK | Table 5 B0.03_k3: ln K bound at v=280 | Table 5 | 319 | 318.7 | round (half unit of last printed digit) | PASS |
| T5_B0.03_k3_lnM280 | Table 5 caption: ln M_ODE(v=280), B0.03_k3 | Table 5 caption | 158 | 158.05 | abs:0.5 (rounded to integers (the value 160.5 is printed to 0.1)) | PASS |
| T5_B0.03_k3_U03 | Table 5 caption: max /Delta ln M/ on U=0.3, B0.03_k3 | Table 5 caption | 1.4e-5 | 1.4499e-05 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_v84 | Table 5 B0.003_k0.5: ln M_cc - ln M_ODE at v=84 | Table 5 | +3.7e-8 | 3.7119e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_v140 | Table 5 B0.003_k0.5: ln M_cc - ln M_ODE at v=140 | Table 5 | +3.1e-8 | 3.1124e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_v200 | Table 5 B0.003_k0.5: ln M_cc - ln M_ODE at v=200 | Table 5 | +2.6e-8 | 2.6454e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_v280 | Table 5 B0.003_k0.5: ln M_cc - ln M_ODE at v=280 | Table 5 | +1.6e-8 | 1.6361e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_max | Table 5 B0.003_k0.5: max /Delta ln M/ over 84<=v<=280 | Table 5 and Result paragraph | 3.7e-8 | 3.7119e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_spread | Table 5 B0.003_k0.5: spread of ln M_cc, four finest grids | Table 5 and Result paragraph | 1.3e-10 | 1.2632e-10 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_lnK | Table 5 B0.003_k0.5: ln K bound at v=280 | Table 5 | 343 | 342.7 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k0.5_lnM280 | Table 5 caption: ln M_ODE(v=280), B0.003_k0.5 | Table 5 caption | 170 | 170.14 | abs:0.5 (rounded to integers (the value 160.5 is printed to 0.1)) | PASS |
| T5_B0.003_k0.5_U03 | Table 5 caption: max /Delta ln M/ on U=0.3, B0.003_k0.5 | Table 5 caption | 2.0e-4 | 0.00020213 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_v84 | Table 5 B0.003_k1.5: ln M_cc - ln M_ODE at v=84 | Table 5 | -9.8e-8 | -9.7886e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_v140 | Table 5 B0.003_k1.5: ln M_cc - ln M_ODE at v=140 | Table 5 | -9.9e-8 | -9.8737e-08 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_v200 | Table 5 B0.003_k1.5: ln M_cc - ln M_ODE at v=200 | Table 5 | -4.5e-7 | -4.4671e-07 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_v280 | Table 5 B0.003_k1.5: ln M_cc - ln M_ODE at v=280 | Table 5 | -2.3e-6 | -2.3447e-06 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_max | Table 5 B0.003_k1.5: max /Delta ln M/ over 84<=v<=280 | Table 5 and Result paragraph | 2.3e-6 | 2.3447e-06 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_spread | Table 5 B0.003_k1.5: spread of ln M_cc, four finest grids | Table 5 and Result paragraph | 4.5e-9 | 4.4564e-09 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_lnK | Table 5 B0.003_k1.5: ln K bound at v=280 | Table 5 | 323 | 323.5 | round (half unit of last printed digit) | PASS |
| T5_B0.003_k1.5_lnM280 | Table 5 caption: ln M_ODE(v=280), B0.003_k1.5 | Table 5 caption | 161 | 160.53 | abs:0.5 (rounded to integers (the value 160.5 is printed to 0.1)) | PASS |
| T5_B0.003_k1.5_U03 | Table 5 caption: max /Delta ln M/ on U=0.3, B0.003_k1.5 | Table 5 caption | 7.6e-4 | 0.00075976 | round (half unit of last printed digit) | PASS |
| T5_lnM_B003k15_v84 | Table 5 caption: ln M_ODE(v=84), k=3/2, B=0.03 | Table 5 caption | 24 | 24.39 | abs:0.5 (rounded to integers) | PASS |
| T5_lnM_B003k15_v140 | Table 5 caption: ln M_ODE(v=140), k=3/2, B=0.03 | Table 5 caption | 63 | 63.41 | abs:0.5 (rounded to integers) | PASS |
| T5_lnM_B003k15_v200 | Table 5 caption: ln M_ODE(v=200), k=3/2, B=0.03 | Table 5 caption | 107 | 106.77 | abs:0.5 (rounded to integers) | PASS |
| e13_growth_lo | growth of M over the six runs: smallest ln M_ODE(280) -> decimal exponent | Result paragraph | 69 | 68.6402 | abs:0.5 (e^158 = 10^68.6) | PASS |
| e13_growth_hi | same, largest | Result paragraph | 78 | 77.6779 | abs:0.5 (e^179 = 10^77.7) | PASS |
| e13_le160 | B=0.003, k=3/2: /Delta ln M/ <= 1e-7 for v <= 160 | Result paragraph | 1e-07 | 9.9e-08 | le (bound quoted in the text) | PASS |
| e13_dsigma_003 | implied extrapolation error of sigma_v for B=0.03 (max /Delta ln M//220, k=3/2) | Result paragraph | 1.5e-9 | 1.52023e-09 | round (half unit of last printed digit) | PASS |
| e13_dsigma_0003 | same for B=0.003 (k=3/2) | Result paragraph | 1e-8 | 1.06577e-08 | abs:1e-9 (one significant figure (1.07e-8)) | PASS |
| e13_sV_levels_quote | level spread of sigma_v quoted as "1.2e-8" (that number is the relative level spread of phi_v; sigma_v: 2e-13) | Result paragraph | 1.2e-8 (text should read 2e-13) | 2e-13 | round (half unit of last printed digit) | PASS* |
| e13_levels_I_200 | Romberg levels of the profile integral agree to (v<=200, relative, all runs) | Sec. 5 | 2e-09 | 2e-09 | le (bound quoted in the text) | PASS |
| e13_levels_I_280 | same up to v=280 | Sec. 5 | 8e-09 (text should read 8.3e-9) | 8.3e-09 | le (bound quoted in the text (computed 8.3e-9)) | PASS* |
| e13_v0_change | starting at v0 = 48..84 changes ln M_cc by (v=100, 200, 280; B=0.03, k=3/2) | Sec. 5 | 1e-10 | 9.03e-11 | le (bound quoted in the text) | PASS |
| e13_U03_B0003 | on U=0.3 the ODE calibrated on the evolved y is off by (B=0.003, k=3/2) | Result paragraph | 7.6e-4 | 0.00075976 | round (half unit of last printed digit) | PASS |
| e13_U03_B003 | same at B=0.03 | Result paragraph | 1.1e-5 | 1.05e-05 | round (half unit of last printed digit) | PASS |
| e13_pde_wrong | evolved PDE mass wrong at v=290 (B=0.03, k=3/2) | Result paragraph | 7e-2 | 0.066 | abs:0.005 (one significant figure (6.6e-2)) | PASS |
| e13_M_v0_B0003 | M(v0=60) at B=0.003, k=3/2 (marginal) | Caveats | 0.85 | 0.8519 | round (half unit of last printed digit) | PASS |
| qM_k15_v140 | q_M at v=140, k=3/2 | Sec. 5 (tail exponent) | 11.2 | 11.1628 | round (half unit of last printed digit) | PASS |
| qM_k15_v260 | q_M at v=260, k=3/2 | Sec. 5 (tail exponent) | 5.99 | 5.9857 | round (half unit of last printed digit) | PASS |
| qM_k15_v290 | q_M at v=290, k=3/2 | Sec. 5 (tail exponent) | 5.51 | 5.5146 | round (half unit of last printed digit) | PASS |
| qM_k05_v84 | q_M at v=84, k=1/2 | Sec. 5 (tail exponent) | 3.79 | 3.7877 | round (half unit of last printed digit) | PASS |
| qM_k05_v290 | q_M at v=290, k=1/2 | Sec. 5 (tail exponent) | 2.83 | 2.8259 | round (half unit of last printed digit) | PASS |
| qM_k05_excess | /sigma_v/ - kappa_-(mu_f) at v=290, k=1/2 | Sec. 5 (tail exponent) | 1.1e-3 | 0.0011 | round (half unit of last printed digit) | PASS |
| qM_k05_contrib | -(/sigma_v/ - kappa_-)(v+1) at v=290, k=1/2 | Sec. 5 (tail exponent) | -0.32 | -0.3201 | round (half unit of last printed digit) | PASS |
| ext_eb_k05 | excess /sigma_v/ - kappa_- at v_b = 250, k=1/2, B=0.03 | Sec. 5 (extension) | 1.4e-3 | 0.0014 | round (half unit of last printed digit) | PASS |
| ext_eb_k15 | same, k=3/2 | Sec. 5 (extension) | 8.3e-6 | 8.3e-06 | round (half unit of last printed digit) | PASS |
| ext_q_k05 | fitted power q of the excess, k=1/2 | Sec. 5 (extension) | 1.48 | 1.48 | round (half unit of last printed digit) | PASS |
| ext_q_k15 | same, k=3/2 | Sec. 5 (extension) | 4.42 | 4.42 | round (half unit of last printed digit) | PASS |
| ext_rb | calibration factor r_b = PDE/kernel flux at v_b = 250 (static-hole kernel), k=3/2, B=0.03 | Sec. 5 (extension) | 1.035 | 1.03545 | abs:0.0005 (1.0354 rounded to 1.035) | PASS |
| ext_rb_final_k1.5 | r_b with the kernel of the final hole, k=1.5, B=0.03 | Sec. 5 (extension) | 1.0067 | 1.0067 | round (half unit of last printed digit) | PASS |
| ext_rb_final_k0.5 | r_b with the kernel of the final hole, k=0.5, B=0.03 | Sec. 5 (extension) | 1.0188 | 1.01876 | round (half unit of last printed digit) | PASS |
| ext_rb_final_k2 | r_b with the kernel of the final hole, k=2, B=0.03 | Sec. 5 (extension) | 1.0058 | 1.00581 | round (half unit of last printed digit) | PASS |
| ext_rb_final_k3 | r_b with the kernel of the final hole, k=3, B=0.03 | Sec. 5 (extension) | 1.0055 | 1.00554 | round (half unit of last printed digit) | PASS |
| ext_final_effect | the final-hole kernel changes ln M(v=2500) by at most (all four tails, B=0.03) | Sec. 5 (extension) | 0.05 | 0.051 | abs:0.002 (computed 0.051) | PASS |
| ext_cmp_k15 | kernel-driven against PDE-driven ln M at v=290, k=3/2, B=0.03 (174.908 against 174.906) | Sec. 5 (extension) | 1.5e-3 | 0.002 | abs:6e-4 (both ln M are printed to 3 decimals) | PASS |
| ext_cmp_k05 | same, k=1/2 | Sec. 5 (extension) | 2e-4 | 0 | abs:5e-4 (both ln M are printed to 3 decimals (difference below the printing)) | PASS |
| ext_tab_lnM_k1.5_v290 | extension table ln M, k=1.5, v=290 | Sec. 5 (extension table) | 174.91 | 174.908 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k1.5_v290 | extension table q_M, k=1.5, v=290 | Sec. 5 (extension table) | 5.51 | 5.5085 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k1.5_v400 | extension table ln M, k=1.5, v=400 | Sec. 5 (extension table) | 259.55 | 259.545 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k1.5_v400 | extension table q_M, k=1.5, v=400 | Sec. 5 (extension table) | 5.175 | 5.1751 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k1.5_v1000 | extension table ln M, k=1.5, v=1000 | Sec. 5 (extension table) | 725.77 | 725.769 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k1.5_v1000 | extension table q_M, k=1.5, v=1000 | Sec. 5 (extension table) | 5.058 | 5.0577 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k1.5_v2000 | extension table ln M, k=1.5, v=2000 | Sec. 5 (extension table) | 1507.10 | 1507.1 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k1.5_v2000 | extension table q_M, k=1.5, v=2000 | Sec. 5 (extension table) | 5.028 | 5.0275 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k1.5_v2500 | extension table ln M, k=1.5, v=2500 | Sec. 5 (extension table) | 1898.39 | 1898.39 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k1.5_v2500 | extension table q_M, k=1.5, v=2500 | Sec. 5 (extension table) | 5.022 | 5.0217 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k0.5_v290 | extension table ln M, k=0.5, v=290 | Sec. 5 (extension table) | 186.67 | 186.667 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k0.5_v290 | extension table q_M, k=0.5, v=290 | Sec. 5 (extension table) | 2.83 | 2.8259 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k0.5_v400 | extension table ln M, k=0.5, v=400 | Sec. 5 (extension table) | 272.59 | 272.585 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k0.5_v400 | extension table q_M, k=0.5, v=400 | Sec. 5 (extension table) | 2.82 | 2.8194 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k0.5_v1000 | extension table ln M, k=0.5, v=1000 | Sec. 5 (extension table) | 743.57 | 743.568 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k0.5_v1000 | extension table q_M, k=0.5, v=1000 | Sec. 5 (extension table) | 2.86 | 2.8562 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k0.5_v2000 | extension table ln M, k=0.5, v=2000 | Sec. 5 (extension table) | 1530.87 | 1530.87 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k0.5_v2000 | extension table q_M, k=0.5, v=2000 | Sec. 5 (extension table) | 2.89 | 2.8888 | round (half unit of last printed digit) | PASS |
| ext_tab_lnM_k0.5_v2500 | extension table ln M, k=0.5, v=2500 | Sec. 5 (extension table) | 1924.88 | 1924.88 | round (half unit of last printed digit) | PASS |
| ext_tab_q_k0.5_v2500 | extension table q_M, k=0.5, v=2500 | Sec. 5 (extension table) | 2.90 | 2.8982 | round (half unit of last printed digit) | PASS |
| ext_C_2500 | ln M - kappa_- v + 5 ln(v+1) at v=2500, k=3/2 | Sec. 5 (extension) | -24.541 | -24.5413 | round (half unit of last printed digit) | PASS |
| ext_C_change | its change between v=2000 and 2500 | Sec. 5 (extension) | 5e-3 | 0.0054 | round (half unit of last printed digit) | PASS |
| ext_treat_k15 | the three treatments of the excess differ by at most (ln M, v=2500, k=3/2) | Sec. 5 (extension) | 0.02 | 0.018 | abs:0.005 (0.018 rounded to 0.02) | PASS |
| ext_k05_zero | k=1/2: treatment e=0 against the power-law treatment, ln M at v=2500 | Sec. 5 (extension) | -0.48 | -0.48 | round (half unit of last printed digit) | PASS |
| ext_k05_const | k=1/2: treatment e=e(v_b) held, ln M at v=2500 | Sec. 5 (extension) | +2.6 | 2.6 | round (half unit of last printed digit) | PASS |
| ext_k05_q2500 | k=1/2: q_M at v=2500 (still rising) | Sec. 5 (extension) | 2.90 | 2.8982 | round (half unit of last printed digit) | PASS |
| ext_k05_rate_change | k=1/2: the three treatments change the rate by at most (finite differences of the printed treatment columns, v>=1000) | Sec. 5 (extension) | 1e-3 (text should read 1.4e-3) | 0.0014 | le (bound quoted in the text; estimated from d(Delta ln M)/dv between printed rows (1.4e-3)) | PASS* |
| ro_q3000_k0.5 | rate-only q_M at v=3000, k=1/2 | Sec. 5 (extension) | 3.012 | 3.0117 | round (half unit of last printed digit) | PASS |
| ro_cross_k0.5 | rate-only 10% crossover of the flux, k=1/2 | Sec. 5 (extension) | 197 | 197 | round (half unit of last printed digit) | PASS |
| ro_q3000_k1.5 | rate-only q_M at v=3000, k=3/2 | Sec. 5 (extension) | 5.019 | 5.0191 | round (half unit of last printed digit) | PASS |
| ro_cross_k1.5 | rate-only 10% crossover of the flux, k=3/2 | Sec. 5 (extension) | 309 | 309 | round (half unit of last printed digit) | PASS |
| ro_q3000_k2.0 | rate-only q_M at v=3000, k=2 | Sec. 5 (extension) | 6.023 | 6.0228 | round (half unit of last printed digit) | PASS |
| ro_cross_k2.0 | rate-only 10% crossover of the flux, k=2 | Sec. 5 (extension) | 368 | 368 | round (half unit of last printed digit) | PASS |
| ro_q3000_k3.0 | rate-only q_M at v=3000, k=3 | Sec. 5 (extension) | 8.030 | 8.0303 | round (half unit of last printed digit) | PASS |
| ro_cross_k3.0 | rate-only 10% crossover of the flux, k=3 | Sec. 5 (extension) | 495 | 495 | round (half unit of last printed digit) | PASS |
| b3_k05_A | B=0.003, k=1/2: ray integration against M_PDE for v<=108 | Sec. 5 (B=0.003) | 4.8e-4 | 0.00048 | round (half unit of last printed digit) | PASS |
| b3_k05_v240 | same at v=240 | Sec. 5 (B=0.003) | 8.5e-4 | 0.00085 | round (half unit of last printed digit) | PASS |
| b3_k15_v100 | B=0.003, k=3/2: difference at v=100 | Sec. 5 (B=0.003) | 1.0e-2 | 0.0097 | round (half unit of last printed digit) | PASS |
| b3_k15_levels | two highest Romberg levels at v=100 | Sec. 5 (B=0.003) | 5e-6 | 4.7e-06 | round (half unit of last printed digit) | PASS |
| b3_k15_v180 | difference at v=180 | Sec. 5 (B=0.003) | -0.19 | -0.19 | abs:0.005 (two digits (-1.9e-1)) | PASS |
| b3_k15_negative | M_PDE < 0 at v=200 (B=0.003, k=3/2) | Sec. 5 (B=0.003) | 1 | 1 | eq (boolean statement) | PASS |
| b3_v100_k05 | B=0.003: difference from the ray integration at v=100, k=1/2 | Sec. 5 (B=0.003) | 5e-5 | 5.2e-05 | abs:5e-5 (the log prints 3.0e-7 for B=0.03 and 4.5e-5 for B=0.003 (one significant figure in the text)) | PASS |
| b3_v100_k15 | same for k=3/2 | Sec. 5 (B=0.003) | 1e-2 | 0.0097 | abs:5e-4 (one significant figure (9.7e-3)) | PASS |
| b3_v100_B003_k05 | B=0.03: difference at v=100, k=1/2 | Sec. 5 (B=0.003) | 3e-7 | 3e-07 | round (half unit of last printed digit) | PASS |
| b3_v100_B003_k15 | B=0.03: difference at v=100, k=3/2 | Sec. 5 (B=0.003) | 7e-6 | 7.2e-06 | round (half unit of last printed digit) | PASS |
| b3_M108_k05 | M(v=108) at B=0.03 over B=0.003, k=1/2 | Sec. 5 (B=0.003) | 1.2e4 | 12200 | round (half unit of last printed digit) | PASS |
| b3_M108_k15 | same, k=3/2 | Sec. 5 (B=0.003) | 5e3 | 5180 | abs:2e2 (one significant figure (5.2e3)) | PASS |
| b3_rate_exact | ODE rate against 4 pi r phi_v^2/rho at B=0.003, k=3/2, v=290 | Sec. 5 (B=0.003) | 5e-6 | 1e-06 | le (bound quoted in the text) | PASS |
| b3_rate_lamlam | ODE rate against lambda - lambda'/lambda at v=140, B=0.003, k=3/2 | Sec. 5 (B=0.003) | 2e-5 | 1.8e-05 | abs:3e-6 (one significant figure (1.8e-5)) | PASS |
| b3_q290_k05 | B=0.003, k=1/2: q_M at v=290 | Sec. 5 (B=0.003) | 3.145 | 3.1454 | round (half unit of last printed digit) | PASS |
| b3_q2500_k05 | same at v=2500 | Sec. 5 (B=0.003) | 3.012 | 3.0117 | round (half unit of last printed digit) | PASS |
| b3_q290_k15 | B=0.003, k=3/2: q_M at v=290 | Sec. 5 (B=0.003) | 5.509 | 5.5092 | round (half unit of last printed digit) | PASS |
| b3_q2500_k15 | same at v=2500 | Sec. 5 (B=0.003) | 5.022 | 5.0216 | round (half unit of last printed digit) | PASS |
| b3_Cchange_k05 | change of ln M - kappa_- v + (2k+2) ln(v+1) between v=2000 and 2500, k=1/2 | Sec. 5 (B=0.003) | 3e-3 | 0.003 | round (half unit of last printed digit) | PASS |
| b3_Cchange_k15 | same, k=3/2 | Sec. 5 (B=0.003) | 6e-3 | 0.0055 | abs:1e-3 (5.5e-3 rounded to 6e-3) | PASS |
| b3_treat | the three treatments change ln M by at most (v=2500, B=0.003, k=1/2) | Sec. 5 (B=0.003) | 0.025 | 0.025 | round (half unit of last printed digit) | PASS |
| b3_lnM_2500 | ln M at v=2500, B=0.003, k=1/2 (out of "1930") | Sec. 5 (B=0.003) | 1930 | 1929.69 | abs:1 (three significant figures) | PASS |
| b3_eb_k05 | B=0.003: excess at v_b, k=1/2 (v=290 value quoted: 1.1e-5) | Sec. 5 (B=0.003) | 1.1e-5 | 1.1e-05 | round (half unit of last printed digit) | PASS |
| pt_muf_k2 | mu_f of the k=2 tail, B=0.03 | Sec. 5 (physical tails) | 1.070e-2 | 0.0107027 | round (half unit of last printed digit) | PASS |
| pt_km_k2 | kappa_-(mu_f) of the k=2 tail, B=0.03 | Sec. 5 (physical tails) | 0.783979 | 0.783979 | round (half unit of last printed digit) | PASS |
| pt_muf_k3 | mu_f of the k=3 tail, B=0.03 | Sec. 5 (physical tails) | 1.154e-2 | 0.0115426 | round (half unit of last printed digit) | PASS |
| pt_km_k3 | kappa_-(mu_f) of the k=3 tail, B=0.03 | Sec. 5 (physical tails) | 0.783028 | 0.783028 | round (half unit of last printed digit) | PASS |
| pt3_muf_k2 | mu_f of the k=2 tail, B=0.003 | Sec. 5 (physical tails at B=0.003) | 1.068e-4 | 0.000106788 | round (half unit of last printed digit) | PASS |
| pt3_km_k2 | kappa_-(mu_f) of the k=2 tail, B=0.003 | Sec. 5 (physical tails at B=0.003) | 0.795537 | 0.795537 | round (half unit of last printed digit) | PASS |
| pt3_muf_k3 | mu_f of the k=3 tail, B=0.003 | Sec. 5 (physical tails at B=0.003) | 1.151e-4 | 0.000115144 | round (half unit of last printed digit) | PASS |
| pt3_km_k3 | kappa_-(mu_f) of the k=3 tail, B=0.003 | Sec. 5 (physical tails at B=0.003) | 0.795528 | 0.795528 | round (half unit of last printed digit) | PASS |
| pt_e13_k2 | projected mass against the ray integration, k=2, B=0.03 | Sec. 5 (physical tails) | 1.1e-6 | 1.0516e-06 | round (half unit of last printed digit) | PASS |
| pt_e13_k3 | projected mass against the ray integration, k=3, B=0.03 | Sec. 5 (physical tails) | 1.4e-6 | 1.3882e-06 | round (half unit of last printed digit) | PASS |
| pt_eb_k2 | excess of /sigma_v/ at v_b, k=2, B=0.03 | Sec. 5 (physical tails) | 9.6e-7 | 9.6e-07 | round (half unit of last printed digit) | PASS |
| pt_treat_k2 | three treatments differ by at most (ln M, v=2500), k=2, B=0.03 | Sec. 5 (physical tails) | 2.1e-3 | 0.0021 | round (half unit of last printed digit) | PASS |
| pt_eb_k3 | excess of /sigma_v/ at v_b, k=3, B=0.03 | Sec. 5 (physical tails) | 3.1e-7 | 3.1e-07 | round (half unit of last printed digit) | PASS |
| pt_treat_k3 | three treatments differ by at most (ln M, v=2500), k=3, B=0.03 | Sec. 5 (physical tails) | 6.9e-4 | 0.00069 | round (half unit of last printed digit) | PASS |
| pt_rb_static_k2 | matching factor of the static-hole kernel at v_b, k=2, B=0.03 | Sec. 5 (physical tails) | 1.0440 | 1.04396 | round (half unit of last printed digit) | PASS |
| pt_rb_static_k3 | matching factor of the static-hole kernel at v_b, k=3, B=0.03 | Sec. 5 (physical tails) | 1.0639 | 1.06391 | round (half unit of last printed digit) | PASS |
| pt_drift_k2 | drift of the static-kernel matching factor between v=250 and 290, k=2 (percent) | Sec. 5 (physical tails) | 0.6 (text should read 0.5) | 0.516303 | round (half unit of last printed digit) | PASS* |
| pt_drift_k3 | same, k=3 (percent) | Sec. 5 (physical tails) | 0.3 | 0.312996 | round (half unit of last printed digit) | PASS |
| pt_final_k2 | matching factor of the final-hole kernel at v_b, k=2 (constant) | Sec. 5 (physical tails) | 1.0058 | 1.00581 | round (half unit of last printed digit) | PASS |
| pt_final_k3 | same, k=3 | Sec. 5 (physical tails) | 1.0055 | 1.00554 | round (half unit of last printed digit) | PASS |
| pt_static_cmp_k2 | kernel-driven (static kernel) minus PDE-driven ln M at v=290, k=2, B=0.03 | Sec. 5 (physical tails) | 1.0e-2 | 0.0105 | abs:6e-4 (the log values are printed to 4 decimals (+0.0105, -0.0056, +0.0017, +0.0006)) | PASS |
| pt_static_cmp_k3 | kernel-driven (static kernel) minus PDE-driven ln M at v=290, k=3, B=0.03 | Sec. 5 (physical tails) | -5.6e-3 | -0.0056 | abs:6e-4 (the log values are printed to 4 decimals (+0.0105, -0.0056, +0.0017, +0.0006)) | PASS |
| pt_static_cmp_k1.5 | kernel-driven (static kernel) minus PDE-driven ln M at v=290, k=1.5, B=0.03 | Sec. 5 (physical tails) | 1.7e-3 | 0.0017 | abs:6e-4 (the log values are printed to 4 decimals (+0.0105, -0.0056, +0.0017, +0.0006)) | PASS |
| pt_static_cmp_k0.5 | kernel-driven (static kernel) minus PDE-driven ln M at v=290, k=0.5, B=0.03 | Sec. 5 (physical tails) | 5.8e-4 | 0.0006 | abs:6e-4 (the log values are printed to 4 decimals (+0.0105, -0.0056, +0.0017, +0.0006)) | PASS |
| pt_final_cmp | with the final-hole kernel all four agree at v=290 to | Sec. 5 (physical tails) | 0.001 | 0.0006 | le (bound quoted in the text) | PASS |
| pt_q2500_k2 | q_M at v=2500, k=2, B=0.03 (static-hole kernel) | Sec. 5 (physical tails) | 6.026 | 6.0262 | round (half unit of last printed digit) | PASS |
| pt_C2500_k2 | ln M - kappa_- v + (2k+2) ln(v+1) at v=2500, k=2 | Sec. 5 (physical tails) | -24.112 | -24.1121 | round (half unit of last printed digit) | PASS |
| pt_Cchange_k2 | its change since v=2000, k=2 | Sec. 5 (physical tails) | 7e-3 | 0.0067 | abs:6e-4 (one significant figure (6.7e-3, 9.0e-3)) | PASS |
| pt_q2500_k3 | q_M at v=2500, k=3, B=0.03 (static-hole kernel) | Sec. 5 (physical tails) | 8.035 | 8.0353 | round (half unit of last printed digit) | PASS |
| pt_C2500_k3 | ln M - kappa_- v + (2k+2) ln(v+1) at v=2500, k=3 | Sec. 5 (physical tails) | -23.332 | -23.3324 | round (half unit of last printed digit) | PASS |
| pt_Cchange_k3 | its change since v=2000, k=3 | Sec. 5 (physical tails) | 9e-3 | 0.009 | abs:6e-4 (one significant figure (6.7e-3, 9.0e-3)) | PASS |
| pt_rate290_k2 | rate at v=290, k=2 | Sec. 5 (physical tails) | 0.7540 | 0.753964 | round (half unit of last printed digit) | PASS |
| pt_q290_k2 | q_M at v=290, k=2 | Sec. 5 (physical tails) | 8.73 | 8.7345 | round (half unit of last printed digit) | PASS |
| pt_q400_k2 | q_M at v=400, k=2 | Sec. 5 (physical tails) | 6.27 | 6.2651 | round (half unit of last printed digit) | PASS |
| pt_rate290_k3 | rate at v=290, k=3 | Sec. 5 (physical tails) | 0.6882 | 0.688156 | round (half unit of last printed digit) | PASS |
| pt_q290_k3 | q_M at v=290, k=3 | Sec. 5 (physical tails) | 27.6 | 27.6076 | round (half unit of last printed digit) | PASS |
| pt_q400_k3 | q_M at v=400, k=3 | Sec. 5 (physical tails) | 16.8 | 16.7928 | round (half unit of last printed digit) | PASS |
| pt3_e13_k2 | projected mass against the ray integration at v=280, k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 2.3e-6 | 2.26e-06 | round (half unit of last printed digit) | PASS |
| pt3_e13_U03_k2 | same on U=0.3 | Sec. 5 (physical tails at B=0.003) | 8.7e-4 | 0.000872 | round (half unit of last printed digit) | PASS |
| pt3_e13_le200_k2 | same for 84<=v<=200 | Sec. 5 (physical tails at B=0.003) | 1e-06 | 9.9e-07 | le (bound quoted in the text) | PASS |
| pt3_lnM_k2 | growth of M, ln M_ODE(280), k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 156 | 156 | round (half unit of last printed digit) | PASS |
| pt3_e13_k3 | projected mass against the ray integration at v=280, k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 5.4e-7 | 5.4e-07 | round (half unit of last printed digit) | PASS |
| pt3_e13_U03_k3 | same on U=0.3 | Sec. 5 (physical tails at B=0.003) | 9.6e-4 | 0.000956 | round (half unit of last printed digit) | PASS |
| pt3_e13_le200_k3 | same for 84<=v<=200 | Sec. 5 (physical tails at B=0.003) | 1e-06 | 6.9e-07 | le (bound quoted in the text) | PASS |
| pt3_lnM_k3 | growth of M, ln M_ODE(280), k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 152 | 152 | round (half unit of last printed digit) | PASS |
| pt3_flux_k2 | flux over the final-hole kernel at v=280, k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 0.99993 | 0.99993 | round (half unit of last printed digit) | PASS |
| pt3_flux_k3 | flux over the final-hole kernel at v=280, k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 0.99947 | 0.99947 | round (half unit of last printed digit) | PASS |
| pt3_rb_k2 | matching factor of the final-hole kernel at v_b, k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 0.99982 | 0.99982 | round (half unit of last printed digit) | PASS |
| pt3_rb_k3 | matching factor of the final-hole kernel at v_b, k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 0.99947 | 0.99947 | round (half unit of last printed digit) | PASS |
| pt3_eb_k2 | excess of /sigma_v/ at v_b, k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 9e-9 | 9.2e-09 | round (half unit of last printed digit) | PASS |
| pt3_treat_k2 | three treatments differ by at most (ln M, v=2500), k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 2e-5 | 2e-05 | round (half unit of last printed digit) | PASS |
| pt3_eb_k3 | excess of /sigma_v/ at v_b, k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 3e-9 | 3e-09 | round (half unit of last printed digit) | PASS |
| pt3_treat_k3 | three treatments differ by at most (ln M, v=2500), k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 7e-6 | 6.7e-06 | round (half unit of last printed digit) | PASS |
| pt3_q2500_k2 | q_M at v=2500, k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 6.0261 | 6.0261 | round (half unit of last printed digit) | PASS |
| pt3_C2500_k2 | ln M - kappa_- v + (2k+2) ln(v+1) at v=2500, k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | -33.834 | -33.8339 | round (half unit of last printed digit) | PASS |
| pt3_Cchange_k2 | its change since v=2000, k=2, B=0.003 | Sec. 5 (physical tails at B=0.003) | 6.6e-3 | 0.0066 | abs:6e-4 (two digits of 6.5e-3, 8.8e-3) | PASS |
| pt3_q2500_k3 | q_M at v=2500, k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 8.0352 | 8.0352 | round (half unit of last printed digit) | PASS |
| pt3_C2500_k3 | ln M - kappa_- v + (2k+2) ln(v+1) at v=2500, k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | -33.104 | -33.1036 | round (half unit of last printed digit) | PASS |
| pt3_Cchange_k3 | its change since v=2000, k=3, B=0.003 | Sec. 5 (physical tails at B=0.003) | 8.9e-3 | 0.0089 | abs:6e-4 (two digits of 6.5e-3, 8.8e-3) | PASS |
| sy_single_v40 | static interior, single-grid y on the coarsest grid at v=40 | Sec. 5 (caveats) | -0.8 | -0.7939 | round (half unit of last printed digit) | PASS |
| sy_single_v50 | static interior, single-grid y on the coarsest grid at v=50 | Sec. 5 (caveats) | -3.7e3 | -3706 | round (half unit of last printed digit) | PASS |
| sy_single_v60 | static interior, single-grid y on the coarsest grid at v=60 | Sec. 5 (caveats) | -1.1e7 | -1.062e+07 | abs:5e5 (two digits of -1.06e7) | PASS |
| sy_romberg60 | three-grid Romberg value of y at v=60 is wrong by | Sec. 5 (caveats) | 7 | 7.0258 | abs:0.5 (/-6.52 - 0.5/ = 7.0) | PASS |
| val_static_h0.08 | static interior: error of the evolution at h=0.08 | Sec. 2 (validation) | 1.1e-3 | 0.001106 | round (half unit of last printed digit) | PASS |
| val_static_h0.04 | static interior: error of the evolution at h=0.04 | Sec. 2 (validation) | 2.8e-4 | 0.000277 | round (half unit of last printed digit) | PASS |
| val_static_h0.02 | static interior: error of the evolution at h=0.02 | Sec. 2 (validation) | 6.9e-5 | 6.929e-05 | round (half unit of last printed digit) | PASS |
| val_static_h0.01 | static interior: error of the evolution at h=0.01 | Sec. 2 (validation) | 1.7e-5 | 1.732e-05 | round (half unit of last printed digit) | PASS |
| val_static_order_lo | static interior: measured order, smallest | Sec. 2 (validation) | 1.998 | 1.9975 | round (half unit of last printed digit) | PASS |
| val_static_order_hi | static interior: measured order, largest | Sec. 2 (validation) | 2.000 | 1.9998 | round (half unit of last printed digit) | PASS |
| val_cu1_h0.08 | relative Raychaudhuri residual in u, v<=20, h=0.08 | Sec. 2 (validation) | 2.2e-3 | 0.002159 | round (half unit of last printed digit) | PASS |
| val_cu2_h0.08 | same, 20<v<=60 | Sec. 2 (validation) | 5.3e-3 | 0.005315 | round (half unit of last printed digit) | PASS |
| val_cv1_h0.08 | relative Raychaudhuri residual in v, v<=20, h=0.08 | Sec. 2 (validation) | 1.2e-3 | 0.001178 | round (half unit of last printed digit) | PASS |
| val_cv2_h0.08 | same, 20<v<=58 | Sec. 2 (validation) | 3.4e-4 | 0.0003376 | round (half unit of last printed digit) | PASS |
| val_cu1_h0.04 | relative Raychaudhuri residual in u, v<=20, h=0.04 | Sec. 2 (validation) | 5.4e-4 | 0.0005406 | round (half unit of last printed digit) | PASS |
| val_cu2_h0.04 | same, 20<v<=60 | Sec. 2 (validation) | 1.3e-3 | 0.001329 | round (half unit of last printed digit) | PASS |
| val_cv1_h0.04 | relative Raychaudhuri residual in v, v<=20, h=0.04 | Sec. 2 (validation) | 2.9e-4 | 0.0002942 | round (half unit of last printed digit) | PASS |
| val_cv2_h0.04 | same, 20<v<=58 | Sec. 2 (validation) | 8.4e-5 | 8.442e-05 | round (half unit of last printed digit) | PASS |
| val_cu1_h0.02 | relative Raychaudhuri residual in u, v<=20, h=0.02 | Sec. 2 (validation) | 1.4e-4 | 0.0001351 | round (half unit of last printed digit) | PASS |
| val_cu2_h0.02 | same, 20<v<=60 | Sec. 2 (validation) | 3.3e-4 | 0.0003324 | round (half unit of last printed digit) | PASS |
| val_cv1_h0.02 | relative Raychaudhuri residual in v, v<=20, h=0.02 | Sec. 2 (validation) | 7.3e-5 | 7.347e-05 | abs:1e-6 (7.35e-5 at the rounding boundary of 7.3e-5/7.4e-5) | PASS |
| val_cv2_h0.02 | same, 20<v<=58 | Sec. 2 (validation) | 2.1e-5 | 2.111e-05 | round (half unit of last printed digit) | PASS |
| val_cu_order | order of the u residual (quoted as 2.00) | Sec. 2 (validation) | 2.00 | 1.999 | abs:0.005 (measured 1.998 to 2.000) | PASS |
| hist_static_dsV_h0.2 | static run: sigma_v error at U=1, v=100 for h_s=h_v=0.2 | Sec. 3 | 2.0e-2 | 0.02 | round (half unit of last printed digit) | PASS |
| hist_static_dsV_h0.1 | static run: sigma_v error at U=1, v=100 for h_s=h_v=0.1 | Sec. 3 | 5.6e-3 | 0.0056 | round (half unit of last printed digit) | PASS |
| hist_static_dsV_h0.05 | static run: sigma_v error at U=1, v=100 for h_s=h_v=0.05 | Sec. 3 | 1.4e-3 | 0.0014 | round (half unit of last printed digit) | PASS |
| hist_B004_richardson | B=0.04, two grids: Richardson value of /sigma_v/ | Sec. 3 | 0.77622 | 0.77622 | round (half unit of last printed digit) | PASS |
| hist_B004_pred | B=0.04: kappa_-(mu_f) prediction | Sec. 3 | 0.775856 | 0.775856 | round (half unit of last printed digit) | PASS |
| hist_muloc_v40 | mu_loc at U=0.1, v=40 (B=0.03, k=3/2) | Sec. 3 | 9.959e-3 | 0.00995895 | round (half unit of last printed digit) | PASS |
| hist_muloc_muf | mu_f of that run | Sec. 3 | 9.956e-3 | 0.00995552 | round (half unit of last printed digit) | PASS |
| hist_muloc_rel_lo | mu_loc against mu_f on U=0.1, 40<=v<=65: smallest relative difference | Sec. 3 | 3e-4 | 0.00034 | abs:5e-5 (one significant figure (3.4e-4)) | PASS |
| hist_muloc_rel_hi | same: largest | Sec. 3 | 7e-4 | 0.00074 | abs:5e-5 (one significant figure (7.4e-4)) | PASS |
| hist_muloc_U03_lo | mu_loc against mu_f on U=0.3 (percent): smallest | Sec. 3 | 0.3 | 0.33 | abs:0.05 (one significant figure (0.33)) | PASS |
| hist_muloc_U03_hi | same: largest | Sec. 3 | 0.9 | 0.93 | abs:0.05 (one significant figure (0.93)) | PASS |
| hist_kappa_shift | change of kappa_- from the difference mu_loc - mu_f, at most | Sec. 3 | 1e-4 | 0.0001 | abs:2e-5 (one significant figure (1.0e-4)) | PASS |
| hist_Uc_B0.03 | U_c(B=0.03) from the first NaN column | Sec. 3 | 3.6 | 3.637 | round (half unit of last printed digit) | PASS |
| hist_Uc_B0.04 | U_c(B=0.04) from the first NaN column | Sec. 3 | 3.3 | 3.254 | round (half unit of last printed digit) | PASS |
| hist_Uc_B0.05 | U_c(B=0.05) from the first NaN column | Sec. 3 | 2.9 | 2.926 | round (half unit of last printed digit) | PASS |
| hist_aniso_lo | spurious mu/(h_s^2+h_v^2) at U=0.3, v=40, B=0: smallest of five combinations | Sec. 3 | 1.5e-3 | 0.00149 | round (half unit of last printed digit) | PASS |
| hist_aniso_hi | same: largest | Sec. 3 | 1.7e-3 | 0.00172 | round (half unit of last printed digit) | PASS |
| hist_aniso_a | anisotropic pair (0.1, 0.025) | Sec. 3 | 1.7e-3 | 0.00172 | round (half unit of last printed digit) | PASS |
| hist_aniso_b | anisotropic pair (0.025, 0.1) | Sec. 3 | 1.5e-3 | 0.00149 | round (half unit of last printed digit) | PASS |
| hist_muid_a1 | mu_v identity on seeded data: ratio of the two sides at v=5, U=0.5, h=0.05 | Sec. 3 | 1.0016 | 1.0016 | round (half unit of last printed digit) | PASS |
| hist_muid_a2 | same, h=0.025 | Sec. 3 | 1.0004 | 1.0004 | round (half unit of last printed digit) | PASS |
| hist_muid_b1 | ratio at v=30, U=1, h=0.05 | Sec. 3 | 0.994 | 0.994 | abs:5e-4 (paper prints 0.994 for 0.9940) | PASS |
| hist_muid_b2 | same, h=0.025 | Sec. 3 | 0.9985 | 0.9985 | round (half unit of last printed digit) | PASS |
| hist_uniform_nan_a | uniform U grid, h_U=0.04: first NaN at v | Sec. 3 | 56 | 55.8 | abs:0.5 (integer v of 55.8) | PASS |
| hist_uniform_nan_b | uniform U grid, h_U=0.02: first NaN at v | Sec. 3 | 70 | 70.2 | abs:0.5 (integer v of 70.2) | PASS |
| abs_ray_decades_k15 | growth of M over which the ray integration is tested, k=3/2 (decades, v0=48 to v=108) | Abstract; Sec. 5 | 17 | 17.7275 | abs:1 (the text counts whole decades ("seventeen to nineteen"): 17.7) | PASS |
| abs_ray_decades_k05 | same, k=1/2 (decades) | Abstract; Sec. 5 | 19 | 19.2743 | abs:1 (whole decades: 19.3) | PASS |
| abs_underestimate | level spread of M_PDE understates its error by (smallest factor over Table 4 rows; text: "two to three orders of magnitude") | Abstract; Sec. 5 | 100 (text should read 8) | 8 | ge (lower end of the quoted range) | PASS* |
| abs_flux_B0003 | abstract: B=0.003, k=3/2 flux agreement (ratio - 1, v=150..420) | Abstract; Sec. 6 | 3e-4 | 0.000319 | abs:1e-4 (one significant figure (3.0e-4 to 3.2e-4)) | PASS |
| abs_range_kv | kappa_- v at v = 110 (Sec. 6: "approximately 87") | Sec. 6 | 87 | 87.5214 | abs:1 (0.7956 x 110 = 87.5; kappa_-(mu_f) x 110 = 86.3) | PASS |
| abs_k15_excess_le | k=3/2: excess of /sigma_v/ over kappa_-(mu_f) at v_b = 250 is <= 1e-5 | Sec. 6 | 1e-05 | 8.3e-06 | le (bound quoted in the text) | PASS |
| gap_static_y_v80 | static interior, single-grid y on the coarsest grid at v=80 | Sec. 3 (construction) | -8.7e13 | -8.714e+13 | round (half unit of last printed digit) | PASS |
| gap_T0_static | T(0) of the static hole (Sec. 4.4(d) text) | Sec. 4.3(d) | 44.304 | 44.3045 | round (half unit of last printed digit) | PASS |
| gap_muf_k15 | mu_f at B=0.03, k=3/2 | Sec. 4.3(d) | 9.96e-3 | 0.00995553 | round (half unit of last printed digit) | PASS |
| gap_muf_B005_k15 | mu_f at B=0.05, k=3/2 | Sec. 4.3(d) | 0.0278 | 0.027757 | round (half unit of last printed digit) | PASS |
| gap_muf_k05 | mu_f at B=0.03, k=1/2 | Sec. 4.3(d) | 5.91e-3 | 0.00591315 | round (half unit of last printed digit) | PASS |
| gap_muf_B005_k05 | mu_f at B=0.05, k=1/2 | Sec. 4.3(d) | 1.65e-2 | 0.0164607 | round (half unit of last printed digit) | PASS |
| gap_B2 | (0.05/0.03)^2, the B^2 scaling of mu_f | Sec. 4.3(d) | 2.78 | 2.77778 | round (half unit of last printed digit) | PASS |
| gap_kernel_choice_k1.5 | ln M(v=2500) changes by (final-hole against static-hole kernel), B=0.03, k=1.5 | Sec. 4.3(d) | 3e-3 | 0.003 | abs:5e-4 (printed to 3 decimals) | PASS |
| gap_kernel_choice_k0.5 | ln M(v=2500) changes by (final-hole against static-hole kernel), B=0.03, k=0.5 | Sec. 4.3(d) | 0 | 0 | abs:5e-4 (printed to 3 decimals) | PASS |
| gap_kernel_choice_k2 | ln M(v=2500) changes by (final-hole against static-hole kernel), B=0.03, k=2 | Sec. 4.3(d) | 0.017 | 0.017 | round (half unit of last printed digit) | PASS |
| gap_kernel_choice_k3 | ln M(v=2500) changes by (final-hole against static-hole kernel), B=0.03, k=3 | Sec. 4.3(d) | 0.05 | 0.051 | abs:2e-3 (0.051 rounded to 0.05) | PASS |
| gap_kernel_choice_B0003 | same at B=0.003: largest change over the four tails (text: <=1e-5; the logs print ln M to 3 decimals, k=3: 1893.123 against 1893.121) | Sec. 4.3(d) | 1e-05 (text should read 2e-3) | 0.002 | le (bound quoted in the text) | PASS* |
| gap_qM_choice | q_M changes by at most (final-hole against static-hole kernel, B=0.03, all four tails, v>=1000) | Sec. 4.3(d) | 0.001 | 0.0005 | le (bound quoted in the text) | PASS |
| gap_rays_s0 | ray positions s_q of the profile integral: first | Sec. 5 | 246.70 | 246.7 | round (half unit of last printed digit) | PASS |
| gap_rays_s2 | ray positions s_q: last (U ~ 1) | Sec. 5 | 271.25 | 271.25 | round (half unit of last printed digit) | PASS |
| gap_rays_U0 | U at the first ray position | Sec. 5 | 0.3003 | 0.3003 | round (half unit of last printed digit) | PASS |
| gap_rays_U2 | U at the last ray position | Sec. 5 | 0.9993 | 0.9993 | round (half unit of last printed digit) | PASS |
| gap_seed03_M | wide seed A=0.03: extrapolated M on U=0.6 at v=60 (units 1e9) | Sec. 3 | 3.7 | 3.68 | round (half unit of last printed digit) | PASS |
| gap_2kp_mN14 | 2 kappa_+ at m_N=1.4 (exceeds kappa_-=0.164) | Sec. 4.2 | 0.18 | 0.180125 | round (half unit of last printed digit) | PASS |
| gap_beta_v60 | beta at v=60, k=3/2, B=0.003 | Sec. 4.4 (long runs) | 3.1 | 3.091 | round (half unit of last printed digit) | PASS |
| kd_scal_k15_B005 | k=3/2, B=0.05: remainder at v=100 (proposed addition: this run is valid; its inner horizon is r_-=1.0233) | Sec. 4.3(d) (proposed addition) | 2.37e-2 | 0.02366 | round (half unit of last printed digit) | PASS |
| kd_scal_k15_B005_mu | same in units of mu_f | Sec. 4.3(d) (proposed addition) | 0.85 | 0.852398 | round (half unit of last printed digit) | PASS |
| kd_scal_k15_B005_ratio | ratio of the remainders B=0.05 / B=0.03, k=3/2 (B^2 scaling: 2.78) | Sec. 4.3(d) (proposed addition) | 3.3 | 3.31048 | round (half unit of last printed digit) | PASS |
