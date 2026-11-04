# Precomputed SeisSol (a.k.a. End-to-End Test Data)

This repository contains parameter files and reference solutions in order to run and evaluate SeisSol in an automated CI.

## Structure

* `cases.json` contains info on which cases exist, and where they are stored.

* `references.json` gives info on when a test case was recorded, with which SeisSol commit and
configurations, and, for a case with fault output, with which quadrature rule of the dynamic
rupture faces (`drQuadRule`, `stroud` or `dunavant`, as `DR_QUAD_RULE` of SeisSol): `verify.py`
does not compare a case with an executable of another rule.

* for each test case, there is a `tpv-data.json` (or `${PREFIX}-data.json`)
containing info about the output data available.

The verification and comparison scripts lie in the main SeisSol repository.
