# damage-scaling

The same initial field at two amplitudes, on a periodic cube, with the damage
frozen.

The stress of the damaged material is positively homogeneous of degree one in
the strain: `lambda0 I1` and `2 mu0 eps` are linear, `gammaR alpha sqrt(I2)`
is linear in the size of the strain, and the invariant ratio `xi` does not
change when the strain is scaled at all. The wave speed the Rusanov
dissipation is scaled with follows `xi` and is therefore also scale-free, and
the timestep bound does not depend on the state. So doubling the amplitude has
to double the solution -- every quantity except the two internal variables,
which are not strains and stay put.

That makes this one of the two tests in the suite with an answer exact to
roundoff rather than to a tolerance. `scaling.py` compares two receiver files
and reports the relative deviation per quantity; the threshold is 1e-12 and
what a correct run produces is a few times 1e-16.

`Cd` is zero on purpose. With a growing damage the homogeneity breaks by
construction -- the drive is quadratic in the strain, so the damage at
amplitude `2A` is not the damage at `A` -- and the test would be measuring
that instead of the constitutive law. `alpha` is set to 0.3 by the initial
condition so that the law is exercised away from its elastic limit, and both
rates are zero so it stays there.

Two caveats. The initial field is not a solution of anything: the medium is
nonlinear, the wave deforms, and the analysis output at the end time (which
compares against the easi file, time-independent here) is noise and should be
ignored. And the floor under the second invariant is tied to the working
precision, not to the field, so it is the one part of the kernel that does not
scale: in double precision it sits near 5e-32, far below anything this run
reaches, but in single precision it is 1.4e-14 and the cells the wave passes
through zero in will differ. Run this one in double precision, or raise the
threshold to about 1e-6 for single.

## Running it

    ./generating_the_mesh.sh
    seissol-damage-o6-f64 parameters.par
    mv output output-a1
    seissol-damage-o6-f64 parameters-double.par
    mv output output-a2
    python3 scaling.py output-a1/tpv-receiver-00001.dat \
                       output-a2/tpv-receiver-00001.dat

Both parameter files write to `output/` -- that is what the comparison scripts
of this repository expect -- so the first run has to be moved aside before the
second one starts.
