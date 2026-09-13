#!/bin/bash
set -euo pipefail

# Graded in x, periodic in all three directions. The grading is what gives
# this scenario more than one time cluster: the widest cell is 3.7 times the
# narrowest, so at a rate of two the clustering has something to do. The
# grading is smooth across the periodic seam by construction.
python3 ../mkcube.py cube.puml.h5 \
    --cells 12 4 4 --size 2000 1000 1000 --grade-x 0.6
