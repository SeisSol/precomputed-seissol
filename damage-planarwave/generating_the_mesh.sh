#!/bin/bash
set -euo pipefail

# Fully periodic cube, 1000 m on a side. Three cells per direction is the
# minimum the topological identification allows; the levels below are the
# ones convergence.sh walks.
python3 ../mkcube.py cube.puml.h5 --cells 6 6 6 --size 1000 1000 1000
