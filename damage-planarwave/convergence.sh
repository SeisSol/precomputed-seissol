#!/bin/bash
set -euo pipefail

# Refines the mesh and collects the error norms the analysis output prints at
# the end time. The exact solution is the easi file, so nothing else has to be
# prepared per level -- which is the reason this scenario uses an easi initial
# condition rather than cICType='planarwave': the plane wave initial condition
# needs a MaterialSetup specialisation the damaged material does not have.
executable=${1:?usage: convergence.sh <seissol-executable> [parameters.par]}
parameters=${2:-parameters.par}

for cells in 3 6 12 24; do
    python3 ../mkcube.py cube.puml.h5 --cells $cells $cells $cells --size 1000 1000 1000
    echo "=== ${cells} cells per direction"
    "$executable" "$parameters" | grep -A16 "Print analysis"
done
