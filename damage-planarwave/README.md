# damage-planarwave

A P wave of the undamaged material, one wavelength across a fully periodic
cube of 1000 m, run for exactly one period.

At `alpha = 0` and `B = 0` every term the damage enters is zero and the system
is linear elastic in the strain variables, so this wave is an exact solution
and stays one: the run has an analytic answer to be measured against at any
resolution. `gammaR` is deliberately not zero -- it may only ever appear
multiplied by `alpha`, and a run in which it does not is a run in which that
is no longer true.

The exact solution lives in `ic.yaml` and is read twice: once as the initial
condition, and once by the analysis output at the end time, which prints the
L1, L2 and Linf errors per quantity. That is the reason the initial condition
is an easi file rather than `cICType = 'planarwave'` -- the built-in plane wave
needs a plane wave operator, which routes through a `MaterialSetup` the damaged
material does not specialise.

`convergence.sh` walks 3, 6, 12 and 24 cells per direction. The errors have to
fall at the order of the scheme. Note that the wave passes through zero strain
twice per wavelength, so the floor under the second invariant and the `xi = 0`
branch are traversed on every step even though the damage terms are switched
off; that is intentional, and it is why this case is worth running even though
it computes an elastic answer.

## The granular variant

`parameters-granular.par` runs the same wave against the same analytic
solution, but with `breakage = 1` from the start: the `(1 - B)` factor
switches the solid branch off entirely and the stress comes from the granular
branch alone. With `a1 = a3 = 0` that branch is

    sigma = 2 a0 eps + 2 a2 I1 1

which is Hooke's law with `2 mu = 2 a0` and `lambda = 2 a2`. The file therefore
sets `a0 = mu0 = 3e10` and `a2 = lambda0 / 2 = 1.5e10`, and the run has
to reproduce the solid-branch errors -- the same wave, carried by the other
half of the constitutive law. It pins `a0`, `a2` and the blend; `a1` and `a3`
have no elastic counterpart and cannot be pinned this way.

Two things about it are worth knowing. `growing` requires a mean breakage below
one, so `B` stays at one and nothing evolves. And this case is the only one that
reads the granular branch through anything but the stress: the operator the
predictor transports by and the two bounds a face scales its dissipation with are
blended the same way the stress is, so both branches have to be right for the
errors below to come out. They did once come out with `a0` set for a factor the
kernel does not have, which is worth knowing because nothing about a wrong
`a0` looks wrong -- the wave simply travels at the wrong speed and the error
stops converging. Setting `a0 = mu0` reproduces the solid errors to the digit;
`a0 = 2 mu0 / 3` gives `0.65` at every resolution.

The timestep bound covers both branches, so a granular branch stiffer than the
solid one shortens the step rather than being run past. Here the two carry the
same speed and the step is the solid one.

## Running it

    ./generating_the_mesh.sh
    seissol-damage-o6-f64 parameters.par
    ./convergence.sh seissol-damage-o6-f64

All faces are interior, so this case also runs on a GPU build, where a face
without a neighbor is refused at setup.
