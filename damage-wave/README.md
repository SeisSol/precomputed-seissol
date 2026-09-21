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
nothing else. A cell hands its neighbours a second expansion of its stress,
projected onto a Legendre basis in time, and a neighbour on a coarser cluster
reconstructs a subinterval of it from there rather than rebuilding it from its
own material. Whether that reconstruction holds to the order of the scheme is
what the two runs say.

It has been asked, and the answer is that the second expansion is not what
limits it. Read in the elastic limit -- `Cd = 0`, so the difference between the
two runs is a truncation error and not two nonlinear trajectories parting -- the
kinetic energy at a synchronisation point differs by `3.5e8` at `CFL = 0.5`,
`1.4e8` at a quarter and `6.7e7` at an eighth: first order in the timestep. The
linear elastic solver on the same mesh differs from itself by `3.1e8`, `1.4e8`
and `6.8e7`, which is the same number to within ten percent and the same order.
So the clustered scheme is what is first order here, for either material, and
this scenario says that carrying a second expansion costs nothing beyond it.

Comparing receivers instead of an energy is the wrong probe for this, and it is
worth saying why: at a fixed sample time the two runs evaluate different steps'
expansions, so the comparison picks up a reconstruction error that is not the
difference between the schemes. It reads as a ratio that will not settle.

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
