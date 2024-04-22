# Reference for acceptance test of damaged-elastic rheology in SeisSol.

## Reference version
Compile SeisSol on commit aec344da4224aa7869d16225b92100f35d5158ea(earlier version) or on commit ba3b62bea8c4653ff6ba6d5554c2e7e390fb2228(corrected version after merging with an updated branch of master)

Build with `cmake .. -DGEMM_TOOLS_LIST=LIBXSMM -DASAGI=ON -DNETCDF=ON -DORDER=3 -DEQUATIONS="damaged-elastic" -DHOST_ARCH=skx -DCMAKE_BUILD_TYPE=Release -DPRECISION=double`

## Comparison

Run `./SeisSol_Release_dskx_3_damaged-elastic parametersLargeDam.par` and compare the simulation results and the reference solution with `python3 ~/SeisSol/postprocessing/validation/compare-receivers.py --prefix tpv5_C0p5F10VDmd0p43NBre6sCB100UniCd5em5Ga3p7e10 output_test/ reference/`.
