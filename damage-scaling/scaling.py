#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 SeisSol Group
#
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-LicenseComments: Full text under /LICENSE and /LICENSES/
#
# SPDX-FileContributor: Author lists in /AUTHORS and /CITATION.cff

"""Checks that doubling the amplitude doubles the solution.

The stress of the damaged material is positively homogeneous of degree one in
the strain: every term is either linear in it or a function of the invariant
ratio, which does not change when the strain is scaled. The wave speed the
flux is scaled with follows the same ratio, and the timestep bound does not
depend on the state at all. Two runs that differ only in the amplitude of
their initial condition therefore have to agree after scaling, to roundoff --
not to a tolerance.

The one place where that fails on purpose is the floor under the second
invariant, which is tied to the working precision and not scaled with the
field. In double precision it sits at about 5e-32 and is far below anything a
run of this scenario reaches; in single precision it is 1.4e-14 and the cells
the wave is passing through zero in will differ.

Usage:

    scaling.py output-a1/tpv-receiver-00001.dat output-a2/tpv-receiver-00001.dat
"""

import argparse
import sys

import numpy as np

# The internal variables are not strains and do not scale.
UNSCALED = ("alpha", "breakage")


def read(path):
    names = None
    rows = []
    with open(path) as handle:
        for line in handle:
            if line.startswith("VARIABLES"):
                names = [
                    part.strip().strip('"') for part in line.split("=", 1)[1].split(",")
                ]
            elif line.startswith(("TITLE", "#")):
                continue
            elif line.strip():
                rows.append([float(part) for part in line.split()])
    if names is None:
        raise RuntimeError(f"{path} carries no VARIABLES line")
    return names, np.array(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference")
    parser.add_argument("scaled")
    parser.add_argument("--factor", type=float, default=2.0)
    parser.add_argument("--epsilon", type=float, default=1e-12)
    arguments = parser.parse_args()

    names, reference = read(arguments.reference)
    scaled_names, scaled = read(arguments.scaled)
    if names != scaled_names or reference.shape != scaled.shape:
        raise RuntimeError("the two receivers do not hold the same samples")

    failed = False
    for column, name in enumerate(names):
        if name == "Time":
            if np.any(reference[:, column] != scaled[:, column]):
                print("Time: the two runs did not sample at the same times")
                failed = True
            continue
        factor = 1.0 if name in UNSCALED else arguments.factor
        expected = factor * reference[:, column]
        scale = max(np.max(np.abs(expected)), np.max(np.abs(scaled[:, column])))
        if scale == 0.0:
            print(f"{name:<10} identically zero in both")
            continue
        error = np.max(np.abs(scaled[:, column] - expected)) / scale
        verdict = "ok" if error <= arguments.epsilon else "FAILED"
        failed = failed or error > arguments.epsilon
        print(
            f"{name:<10} factor {factor:>4.1f}  relative deviation {error:.3e}  {verdict}"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
