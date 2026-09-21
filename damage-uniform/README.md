# damage-uniform

Five runs on a periodic 3x3x3 cube in which nothing propagates.

The state starts uniform and the strain is carried entirely by the initial
strain of the material file, so the divergence of the stress vanishes, the
velocity stays zero, and the strain stays exactly what it was. What is left of
the system is the two source terms, which are then an ordinary differential
equation in `alpha` and `B` -- and for `B = 0` the drive does not change, so
`alpha` is *linear in time* and the answer is closed-form. This is the only
place where the damage evolution can be checked against an exact solution
rather than against another run.

The exact solution is written into each `ic-*.yaml` as a function of time, so
the analysis output at the end time reports the error in `alpha` directly and
no post-processing is needed. `reference_ode.py` reproduces the source terms,
integrates them, and prints what the receivers have to show:

| case                      | xi   | drive | expected                        |
|---------------------------|------|-------|---------------------------------|
| `parameters.par`          | +1   | 180   | `alpha(2 s) = 0.36`             |
| `parameters-saturation.par` | +1 | 180   | `alpha(6 s) = 1` + one step     |
| `parameters-healing.par`  | -1   | -20   | `alpha(2 s) = 0.10`             |
| `parameters-shear.par`    | 0    | 160   | `alpha(2 s) = 0.32`             |
| `parameters-breakage.par` | 0    | 960   | `alpha(5 s) = 0.431781`, `B = 0.010148` |

What each one is for:

- **Growth** and **shear** differ only in the strain that produces the same
  kind of loading. The shear case is the only one in which the Voigt weight of
  the second invariant appears on its own: `I2 = eps:eps` gives the shear
  entries a weight of two, and a factor lost there halves the rate exactly,
  to `alpha(2 s) = 0.16`.

- **Healing** is the other branch of the source. It also pins the sign
  convention of `xi0`, which is worth being explicit about: the implementation
  grows where `xi + xi0 > 0`, so the onset sits at `xi = -xi0` and not at
  `xi = +xi0`. With `xi0 = 0.8` a uniaxial extension (`xi = +1`) grows and a
  uniaxial compression (`xi = -1`) heals. A run in which the compression case
  grows and the extension case heals has the convention the other way round,
  and no other test in this suite would notice.

- **Saturation** runs the growth case past `t = 1 / (Cd * drive) = 5.56 s`.
  Nothing in the constitutive law bounds `alpha`; the `growing` guard does,
  and it reads the *mean* damage of the cell at the start of a nodal step. So
  the run overshoots one by one step of growth -- about `0.18 * dt` -- and then
  freezes. Anything more than that is the guard not being applied per step;
  anything less is it being applied before the step it belongs to.

- **Breakage** needs a critical damage inside `(0, 1)` to be reachable, which
  the mild `gammaR` of the other cases does not give: at `gammaR = 1e10` the
  three-way minimum for `alpha_cr` is capped at one and the sigmoid never
  opens. At `gammaR = 6e10` and `xi = 0` it sits at `0.4318`, and the run
  starts at `0.40`, just below. There is no closed form past that point, so
  this is the one case measured against `reference_ode.py` rather than against
  its own easi file -- the analysis output for it is meaningless and should be
  ignored.

  It is also the only case that says what the guard is for. The damage
  saturates at `alpha_cr` and not at one, so the run freezes at `0.4318` with
  the breakage still small. Read against a guard at one it looks as though the
  case had been cut short -- it is the other way round: with that guard the run
  drove `alpha` to `0.58` by two seconds, and past `0.464` the compressional
  family of this material has no real speed left. What a run of it showed was
  not a wrong number but a uniform state that would not stay uniform, at a rate
  that did not care what the timestep was. `reference_ode.py` carries the same
  guard, which is what keeps it an answer to this run.

The granular coefficients `a0` to `a3` are zero in all five. They enter the
stress and nothing else, and in a scenario where the stress has no divergence
they are unobservable; `damage-planarwave` pins them instead.

## An open question this exposes

The guard bounds the damage above and not below. Above, it saturates at the
critical damage, which is where the solid branch stops describing anything.
Below, nothing stops the healing branch: `alpha` reaches zero at `t = 2.5 s` in
the healing case and keeps going negative, and a negative damage *stiffens* the
material -- `2 mu0 - gammaR alpha (2 xi0 + xi)` grows -- so the state leaves the
model's range rather than returning to the undamaged one. The end time is 2 s to
stay inside it.

Raising it to 3.5 s is how the scenario asks the question, and the answer is
worth knowing before deciding: nothing goes wrong to look at. `alpha` follows
`0.5 - 0.2 t` to `-0.20` exactly, and the strain and the velocity stay at
roundoff throughout -- a stiffer medium is still a hyperbolic one, so the run
neither diverges nor reports anything. What it has left is the range the model
is defined on, quietly. Two consequences are worth writing down: the bound the
timestep is taken over covers `alpha` in `[0, 1]` and says nothing about a
negative one, and the effective moduli a negative damage produces are not moduli
the rheology was fitted for. Whether the guard should clamp at zero is a
decision about the model, not a bug in the implementation.

## Running it

    ./generating_the_mesh.sh
    python3 reference_ode.py
    seissol-damage-o6-f64 parameters.par
