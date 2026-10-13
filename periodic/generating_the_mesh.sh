#!/bin/bash
#set -euo pipefail

prefix=periodic
# Generate the mesh using gmsh; periodic.geo identifies opposite faces, which gmsh records in
# the msh 4 format
#for gmsh, see http://gmsh.info/#Download
gmsh -3 $prefix.geo

# Convert the mesh to the PUML format using pumgen, which writes the periodicity as the
# topological vertex identification ("identify")
# for pumgen, see https://github.com/SeisSol/PUMGen/wiki/How-to-compile-PUMGen
pumgen -s msh4 $prefix.msh ../meshes/$prefix.puml.h5
