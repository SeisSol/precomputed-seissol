# damage-tpv5

TPV5 on a damaged medium, in two stages.

Dynamic rupture and this material do not meet yet: `DamageMaterial` reports
`SupportsDR = false`, and a mesh with a rupture face is refused when the cell
local matrices are set up. The material says so rather than handing the
friction laws a traction it does not have -- the traction here is derived from
the state instead of being part of it, so joining the two means evaluating the
constitutive relation on the fault's quadrature points and letting the friction
laws read the result. Until that exists, both runs below abort at setup, and
that abort is itself worth keeping: it has to happen at setup, with a message
about the material, and not halfway into a run on values that look like
tractions.

## Stage one: the elastic limit

`parameters-elastic-limit.par` sets `alpha = 0`, `Cd = 0` and a zero initial
strain, which switches off every damage term and leaves a linear elastic
medium with the TPV5 moduli. It uses the mesh, the fault file and the receiver
positions of the `tpv5` case in this repository, so its output is read against
that reference directly.

This is the first question worth asking about damage and dynamic rupture, and
it needs no calibration of the model: does the rupture on a damaged material
reproduce the rupture on an elastic one when the damage is not there. Expect
agreement to the discretisation error rather than bit-for-bit -- the solver
integrates its step by a nodal rule in time and closes its faces with a
Rusanov flux, where the elastic reference uses the ADER expansion and a
Godunov flux, so the two differ at the order of the scheme even on the same
mesh and the same data.

## Stage two: the damaged run

`parameters.par` carries the background of the fault file in the material, as
a strain. This is the one place in the suite where a scenario can be wrong
without anything reporting it: the fault file states the background as a
stress because that is what a friction law compares against, the material
states it as a strain because the stress is not part of the state, and the two
describe the same medium. `initial_strain.py` inverts the constitutive
relation so they agree --

    initial_strain.py --stress "0, -120e6, 0, 70e6, 0, 0" --alpha 0.0

-- and `material.yaml` carries what it printed. Editing those six numbers by
hand is how this scenario breaks.

### What the inversion says about the calibration

The TPV5 background has an invariant ratio of `xi = -0.337960`. The onset sits
at `xi = -xi0`, so:

- at `xi0 = 0.8`, the value the model is usually first run with, the static
  background is already *above* the onset. Damage then grows everywhere from
  `t = 0` at the same rate, with or without a rupture, and an off-fault damage
  zone is not what the run would be showing.
- this scenario therefore uses `xi0 = 0.25`, which leaves the background below
  the onset by `0.088` and lets the rupture be the thing that lifts the medium
  across it near the fault and nowhere else.

The margin is thin, and deliberately so: at `alpha = 0.2` the same background
sits at `xi = -0.2999`, i.e. a pre-existing damage of that size is enough to
push the medium into growth on its own. That is why the run starts at
`alpha = 0` with a zero healing rate, and it is a property of the model worth
knowing before a scenario with a depth-dependent background is written.

`Cd = 3e-5` is calibrated to order of magnitude only -- enough for the mean
damage in the energy output to reach a few tenths over the two seconds of the
run. The fault output and `alpha` in the volume output are what the damage zone
is read from.

## Running it

    ./generating_the_mesh.sh
    seissol-damage-o6-f64 parameters-elastic-limit.par
    seissol-damage-o6-f64 parameters.par
