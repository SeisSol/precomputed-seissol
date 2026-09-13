#!/bin/bash
set -euo pipefail

python3 ../mkcube.py cube.puml.h5 --cells 6 6 6 --size 1000 1000 1000
