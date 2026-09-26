#!/bin/bash
set -euo pipefail
prefix=aniso-oblique
gmsh -3 -algo hxt -optimize_netgen "${prefix}.geo" -o "${prefix}.msh"
pumgen -s msh2 "${prefix}.msh" "../meshes/${prefix}.puml.h5"
