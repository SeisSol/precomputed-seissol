# damage-wave

A Gaussian P pulse in a medium that the pulse itself damages, on a graded
periodic box of 2000 x 1000 x 1000 m.

This is the first case in the suite where the feedback the model is for
actually runs: the strain grows the damage, the damage softens the medium, and
the softer medium carries the rest of the pulse differently. There is no exact
answer, so what the case is read against is a second run of itself.

Under uniaxial strain the invariant ratio is `+1` where the pulse pulls and
`-1` where it pushes. With the onset at `xi = -xi0 = -0.8`, the extensional
half of the pulse grows damage and the compressional half does not, and the
healing rate is zero, so what the run leaves behind is a one-sided trail of
damage. That asymmetry is the observable, and it says something no uniform
case can: that the sign of the threshold survives being embedded in a wave.
`mean_damage` in the energy output is the scalar version of it.

## Global against local time stepping

`parameters.par` and `parameters-lts.par` differ in `ClusteredLTS` and in
nothing else. The documentation of the material lists local time stepping as
"mechanism complete, not verified", and this is the comparison that is missing:
a cell hands its neighbours a second expansion of its stress, projected onto a
Legendre basis in time, and a neighbour on a coarser cluster reconstructs a
subinterval of it from there rather than rebuilding it from its own material.
Whether that reconstruction holds to the order of the scheme is what the two
runs say when their receivers are compared.

The mesh is graded in x -- the widest cell is 3.7 times the narrowest -- which
is what gives the clustering something to do; a uniform cube has one cluster
and the local run would be the global one. The grading is smooth across the
periodic seam by construction, so the seam is not a mesh-density jump of its
own.

Expect agreement to the discretisation error, not to roundoff. Use
`postprocessing/validation/compare-receivers.py` with the epsilons a
converged pair of runs actually produces, and treat a widening difference
under refinement as the real signal.

## Running it

    ./generating_the_mesh.sh
    seissol-damage-o6-f64 parameters.par
    seissol-damage-o6-f64 parameters-lts.par

All faces are interior, so this case runs on a GPU build as well.
