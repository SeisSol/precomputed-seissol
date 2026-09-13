#!/bin/bash
set -euo pipefail

# A uniform state needs no resolution, only periodicity: three cells per
# direction is the smallest mesh the topological identification allows.
python3 ../mkcube.py cube.puml.h5 --cells 3 3 3 --size 1000 1000 1000
