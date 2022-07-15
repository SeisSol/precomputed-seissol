This repository contains parameter files and reference solutions in order to run and evaluate SeisSol in an automated CI.

## TPV101
Reference computed on July 15, with commit `153338af`.

## TPV101-slip
Reference computed on July 15, with commit `153338af`.

## TPV104
Reference computed on July 15, with commit `153338af`.

## TPV105
Reference computed on July 15, with commit `153338af`.

## TPV16
Reference computed on July 15, with commit `153338af`.

Note: There seems to be something broken with the traction part of the faultreceiver output on the master branch as it outputs strange values. In particular the quantity `Ts0` at initial time does not have the same value as `T_s` in the header.

## TPVyoffe
Reference computed on July 15, with commit `153338af`.

This is not a SCEC benchmark, but rather a verification setup for the imposed slip friction law with Yoffe slip function.

## TPVgaussian
Reference computed on July 15, with commit `153338af`.

This is not a SCEC benchmark, but rather a verification setup for the imposed slip friction law with Gaussian slip function.

## TPV5
Reference computed on July 15, with commit `153338af`.

## TPV6
Reference computed on July 15, with commit `153338af`.

## ASl vs ASI
On the master branch an output variable is wrongly named `ASI`. As a postprocessing step the variable name has been changed to `ASl`.
