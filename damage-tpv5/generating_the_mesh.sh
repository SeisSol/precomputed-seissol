#!/bin/bash
set -euo pipefail

# The same mesh the elastic TPV5 case uses -- the point of the elastic limit
# run is that nothing but the material differs.
cp ../tpv5/tpv5-20k.h5 .
