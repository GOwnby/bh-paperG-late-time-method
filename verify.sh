#!/bin/sh
# Self-verification of the repository: recomputes the numbers of main.tex from the shipped data and compares them with the manuscript.
#   sh verify.sh [--quick|--full]        (default: --quick; --full adds the heavy runs, see README.md)
# Needs Python >= 3.10 with numpy >= 2, scipy >= 1.11, sympy, mpmath, matplotlib, and gcc (requirements.txt).  No network.
# Writes verification/REPORT.md and verification/logs/*.log; the last line is "RESULT <repo>: PASSED n/n checks (<mode>)"; exit status 0 only if all passed.
cd "$(dirname "$0")" || exit 2
exec "${PYTHON:-python3}" verify.py "$@"
