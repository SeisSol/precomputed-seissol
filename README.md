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
Reference computed on June 27, 2023 with commit `2752c6d9`.

## TPV6
Reference computed on July 15 2022, with commit `153338af`.

## ASl vs ASI
On the master branch an output variable is wrongly named `ASI`. As a postprocessing step the variable name has been changed to `ASl`.
