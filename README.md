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

## TPVahsp
Reference computed on August 31, 2023, with commit `9b1b0ec9`.

This is not a SCEC benchmark, but SISMOWINE benchmark for anisotropic materials. We call it TPVahsp nonetheless, for consistency.

## TPVloh1-fused
Reference computed on September 26, 2023 with commit `be34d26c`.
This is not a SCEC benchmark, but SISMOWINE benchmark for elastic materials. We call it TPVloh1-fused nonetheless, for consistency.
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
A tpv5 mesh with four nucleations in different regions in the fault, triggering sequentially. Computed with `3bca92b35c35225f104a4093825717746f5d0982`, but submodules as of `3bca92b35c35225f104a4093825717746f5d0982`.
