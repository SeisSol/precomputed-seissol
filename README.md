This repository contains parameter files and reference solutions in order to run and evaluate SeisSol in an automated CI.

## TPV101
Reference computed on July 15 2022, with commit `153338af`.

## TPV101-slip
Reference computed on July 15 2022, with commit `153338af`.

## TPV104
Reference computed on July 15 2022, with commit `153338af`.

## TPV105
Reference computed on December 15 2022, with commit `64cc387e`.

## TPV13
With slight modification: Fault is smaller, but does not break up to the boundaries within 2s.
Reference computed on August 31, 2023, with commit `7fde4778`.

## TPV13-fused
With a coarse mesh with approximately 2.7k elements, and order 6: the simulation is just to verify that the fused simulations give consistent results and the physics may not make sense given the coarse mesh. We have energies and receivers to compare for now. These precomputed solutions consider elastic WP, LSW, and plasticity. Reference computed on July 24, 2025, with commit `2dbe03e5`

## TPV13-fused-plasticity
With a coarse mesh with approximately 2.7k elements, and order 6: the simulation is to verify that fused simulations with plasticity varying across simulations give consistent results, and the physics may not make sense given the coarse mesh. We have energies and receivers to compare for now. These precomputed solutions consider elastic WP, LSW, and plasticity. Reference computed on August 29, 2025, with commit `34c6c54a`

## TPV16
Reference computed on July 15 2022, with commit `153338af`.

Note: There seems to be something broken with the traction part of the faultreceiver output on the master branch as it outputs strange values. In particular the quantity `Ts0` at initial time does not have the same value as `T_s` in the header.

## TPV33
Reference computed on September 11 2023, with commit `1786163f`.

## AHSP
Reference computed on August 31, 2023, with commit `9b1b0ec9`.

This is not a SCEC benchmark, but SISMOWINE benchmark for anisotropic materials.

## LOH1-fused
Reference computed on September 26, 2023 with commit `be34d26c`.
This is not a SCEC benchmark, but SISMOWINE benchmark for elastic materials.
In particular this test is aimed at the fused simulation feature. It tests an ensemble of 8 simulations.

## TPVyoffe
Reference computed on July 15 2022, with commit `153338af`.

This is not a SCEC benchmark, but rather a verification setup for the imposed slip friction law with Yoffe slip function.

## TPVgaussian
Reference computed on July 15 2022, with commit `153338af`.

This is not a SCEC benchmark, but rather a verification setup for the imposed slip friction law with Gaussian slip function.

## TPV5
Reference computed on July 15 2022, with commit `153338af`.

## TPV5-nuc
This is a version of TPV5, which is nucleated with the nucleation stress method.
This feature does not work properly on the master branch.
We used a hotfix-branch to compute this reference.
Reference computed on July 20, with commit `1728b83a`.

## TPV5-visco
This is a viscoelastic version of TPV5.
Reference computed on August 31, 2023 with commit `9b1b0ec`.

## TPV5-poro
This is a poroelastic version of TPV5.
The rupture is nucleated by a fluid pressure pertubation at the initial time.
Reference computed on August 19, 2025 with commit `f0b153bfbf69c63e213651470ed8fd3fab412863`.

## TPV6
Reference computed on July 15 2022, with commit `153338af`.

## TTPV1
The reference was computed on July 22 2025, using commit `340af314176398c7e9313219ba851144418551b6`, and a dense memory layout.

## ASl vs ASI
On the master branch an output variable is wrongly named `ASI`. As a postprocessing step the variable name has been changed to `ASl`.

## LOH1-IC
LOH1, but with a Scholte wave running on it instead of point sources.
The reference was computed with `b5266c87a7b6bb7de3aeb9dc2fb6c9053452ece1` on 2025-09-04.

## TPV5-4NUC
A tpv5 mesh with four nucleations in different regions in the fault, triggering sequentially. Computed with `84a1862a570eedc7835da63f28788475c8afc0f9`, but the Yateto submodule as of `3bca92b35c35225f104a4093825717746f5d0982`.

## Damage

Five scenario directories for the continuum damage-breakage rheology, ordered
by how much of the implementation they involve. Each one is built around a
single question with an answer that does not come from another run of SeisSol
where that is possible at all:

| directory           | what it pins down                                              | measured against          |
|---------------------|----------------------------------------------------------------|---------------------------|
| `damage-planarwave` | the elastic limit, and the granular branch reproducing Hooke   | analytic, per resolution  |
| `damage-uniform`    | both source branches, the guards, the Voigt weight, `alpha_cr` | closed form, and an ODE   |
| `damage-scaling`    | the constitutive law being homogeneous of degree one           | itself, to roundoff       |
| `damage-wave`       | the feedback, and global against local time stepping           | its own global run        |
| `damage-tpv5`       | dynamic rupture, and the background stress-strain consistency  | the elastic `tpv5` case   |

The first three have exact answers because they avoid what makes the model
nonlinear in one of two ways: by keeping the damage at zero, or by keeping the
state uniform so that the flux drops out and only the sources are left. There
is no third way -- a plane wave in a medium with `gammaR * alpha > 0` is not a
solution, because the coupling term turns a pure shear strain into an
isotropic stress and drives a P motion out of it. Everything beyond those
three is a comparison between runs.

### Meshes

`mkcube.py` writes the structured periodic cubes the first four scenarios use.
The generator built into SeisSol would do, but it refuses to run ("The cube
generator is (currently) not supported"), and a meshed box is not an
alternative here: a free surface reflects and an outflow boundary does not
absorb exactly, either of which turns a state that should stay constant into a
wave. Periodicity is topological, through the `identify-vertex` format, and
needs at least three cells per periodic direction -- with two, the topological
mesh holds two distinct faces with the same vertices and a cell neighbours
itself across the seam. The script checks that and refuses.

The meshes are small on purpose: 162 cells for the uniform case, 1152 for the
graded one. They are the scale the CTest verification pipeline wants, and the
low resolution is a feature -- a drift shows up in a coarse run long before it
shows up in a converged one.

### What is not covered

- **Energy.** The stored energy of this rheology carries a square root of the
  second strain invariant and terms of third order in the state, and the
  moments the energy output is built on reach second order, so it is absent
  rather than approximated. Only the kinetic energy and the two means are
  checked, and those are exact.

- **`a1` and `a3`.** The granular branch is pinned only where it coincides
  with Hooke's law, which is `a0` and `a2`. The two odd coefficients have no
  elastic counterpart and no closed form to be read against; they would need a
  reference solution from outside SeisSol.

- **Plasticity.** Not supported by the material, and not meaningful with it:
  the rheology already carries the inelastic part.

- **Single precision.** All five run in single precision, but two of them
  change character: the floor under the second invariant is `eps^2` of the
  working precision, which is `1.4e-14` rather than `5e-32`, and the exactness
  claims of `damage-scaling` and of the zero crossings in `damage-planarwave`
  hold to about `1e-6` there instead of to roundoff.

### Adding them to the matrix

The `cases.json` entries are in place. The configuration name is `damage`, so
the executables are `seissol-damage-o6-f64` and
`seissol-damage-o6-f32`; the equation has to be added to the CI matrix with
`fault: false` everywhere except `damage-tpv5`, which stays out of the matrix
until the material supports dynamic rupture.

`damage-planarwave`, `damage-uniform`, `damage-scaling` and `damage-wave` have
no face without a neighbour and therefore also run on a GPU build, which
refuses one at setup.
