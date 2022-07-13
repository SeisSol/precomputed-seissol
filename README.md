This repository contains parameter files and reference solutions in order to run and evaluate SeisSol in an automated CI.

## TPV101
Reference computed on June 22, with commit `115018ad`.

## TPV101-slip
Reference computed on June 22, with commit `115018ad`.

## TPV104
Reference computed on June 22, with commit `115018ad`.

## TPV105
Reference computed on June 22, with commit `115018ad`.

## TPV16
Reference computed on July 1, with commit `4357f5e0`.

Note: There seems to be something broken with the traction part of the faultreceiver output on the master branch as it outputs strange values. In particular the quantity `Ts0` at initial time does not have the same value as `T_s` in the header.

## TPV33
Reference computed on July 13, with commit `40346cf3`.

Note: This is not the SCEC TPV33, but a test for SeisSol's friction law 33 (imposed slip rates with regularized yoffe STF).

## TPV34
Reference computed on July 13, with commit `40346cf3`.

Note: This is not the SCEC TPV34, but a test for SeisSol's friction law 34 (imposed slip rates with Gaussian STF).

## TPV5
Reference computed on June 22, with commit `115018ad`.

## TPV6
Reference computed on July 08, with commit `a5d9098c`.

## ASl vs ASI
On the master branch an output variable is wrongly named `ASI`. As a postprocessing step the variable name has been changed to `ASl`.
