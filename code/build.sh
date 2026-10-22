#!/bin/sh
# Build the three C libraries of Paper G (Linux, gcc; no -ffast-math).  Run from anywhere:  sh code/build.sh
set -e
here=$(cd "$(dirname "$0")" && pwd)
cd "$here/eh_init"
gcc -O3 -shared -fPIC -o libdouble_null.so double_null.c -lm    # stored-array driver (used by dn2lib.py)
gcc -O3 -shared -fPIC -o libstream.so      stream.c      -lm    # two-row streaming driver (gen.py, gen2.py)
gcc -O3 -shared -fPIC -o libstream2.so     stream2.c     -lm    # streaming driver + row integral (gen3.py)
cd "$here/nonlinear"
gcc -O3 -shared -fPIC -o libdouble_null.so double_null.c -lm    # nonlinear/ (double_null.c is identical to the one in eh_init)
echo "built: eh_init/{libdouble_null,libstream,libstream2}.so nonlinear/libdouble_null.so"
