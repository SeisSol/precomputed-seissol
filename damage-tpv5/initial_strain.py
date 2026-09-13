#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 SeisSol Group
#
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-LicenseComments: Full text under /LICENSE and /LICENSES/
#
# SPDX-FileContributor: Author lists in /AUTHORS and /CITATION.cff

"""Turns a background stress into the initial strain of a damaged material.

A dynamic rupture scenario states its background as a stress, in the fault
file, because that is what a friction law compares against. A damaged material
states it as a strain, in the material file, because its stress is a function
of the state and not part of it. Both describe the same medium, so they have to
agree: the stress the constitutive relation forms from the initial strain has
to be the stress the fault file was written with. Prescribing the two
independently is the one way this scenario can be wrong without anything
reporting it.

The inversion is not the elastic one once the damage is nonzero, but it is
still small. By isotropy the deviator of the strain is parallel to the
deviator of the stress, so only two scalars are unknown: the first invariant
and the effective shear modulus. Those two satisfy

    m  = 2 mu0 - gammaR alpha (2 xi0 + xi)
    tr(sigma) = (3 lambda0 + m) I1 - 3 gammaR alpha sqrt(I2)

with the deviator fixed at e = sigma' / m, and they are solved here by Newton
on the pair.

Usage (values in Pa, Voigt order xx yy zz xy yz xz):

    initial_strain.py --stress "0, -120e6, 0, 70e6, 0, 0" --alpha 0.0
"""

import argparse

import numpy as np

VOIGT = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 2.0])
NAMES = ("xx", "yy", "zz", "xy", "yz", "xz")


def stress(eps, material):
    """The solid branch of the constitutive relation, for the check below."""
    i1 = eps[0] + eps[1] + eps[2]
    i2 = float(np.dot(VOIGT, eps * eps))
    root = np.sqrt(i2)
    xi = i1 / root if i2 > 0.0 else 0.0
    alpha, gamma = material["alpha"], material["gammaR"]
    shear = 2.0 * material["mu0"] - gamma * alpha * (2.0 * material["xi0"] + xi)
    out = shear * eps
    out[:3] += material["lambda0"] * i1 - gamma * alpha * root
    return out


def residual(unknowns, deviator, trace, material):
    i1, shear = unknowns
    norm = np.sqrt(float(np.dot(VOIGT, deviator * deviator))) / shear
    i2 = i1 * i1 / 3.0 + norm * norm
    root = np.sqrt(i2)
    xi = i1 / root if i2 > 0.0 else 0.0
    alpha, gamma = material["alpha"], material["gammaR"]
    return np.array(
        [
            shear
            - (2.0 * material["mu0"] - gamma * alpha * (2.0 * material["xi0"] + xi)),
            (3.0 * material["lambda0"] + shear) * i1
            - 3.0 * gamma * alpha * root
            - trace,
        ]
    )


def invert(sigma, material):
    trace = sigma[0] + sigma[1] + sigma[2]
    deviator = sigma.copy()
    deviator[:3] -= trace / 3.0

    unknowns = np.array(
        [
            trace / (3.0 * material["lambda0"] + 2.0 * material["mu0"]),
            2.0 * material["mu0"],
        ]
    )
    for _ in range(100):
        current = residual(unknowns, deviator, trace, material)
        if np.max(np.abs(current) / np.array([1.0, abs(trace) + 1.0])) < 1e-14:
            break
        jacobian = np.empty((2, 2))
        for column in range(2):
            step = 1e-7 * max(abs(unknowns[column]), 1.0)
            shifted = unknowns.copy()
            shifted[column] += step
            jacobian[:, column] = (
                residual(shifted, deviator, trace, material) - current
            ) / step
        unknowns = unknowns - np.linalg.solve(jacobian, current)
    else:
        raise RuntimeError("the inversion did not converge")

    i1, shear = unknowns
    eps = deviator / shear
    eps[:3] += i1 / 3.0
    return eps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    # One string rather than six numbers: a leading minus would otherwise be
    # read as an option.
    parser.add_argument("--stress", required=True)
    parser.add_argument("--alpha", type=float, default=0.0)
    parser.add_argument("--lambda0", type=float, default=3.2043759360e10)
    parser.add_argument("--mu0", type=float, default=3.2038120320e10)
    parser.add_argument("--gammaR", type=float, default=1.0e10)
    parser.add_argument("--xi0", type=float, default=0.3)
    arguments = parser.parse_args()

    material = {
        "alpha": arguments.alpha,
        "lambda0": arguments.lambda0,
        "mu0": arguments.mu0,
        "gammaR": arguments.gammaR,
        "xi0": arguments.xi0,
    }
    sigma = np.array(
        [float(part) for part in arguments.stress.replace(",", " ").split()]
    )
    if sigma.size != 6:
        raise RuntimeError("the stress needs six components, in Voigt order")
    eps = invert(sigma, material)

    i1 = eps[0] + eps[1] + eps[2]
    i2 = float(np.dot(VOIGT, eps * eps))
    xi = i1 / np.sqrt(i2)
    recovered = stress(eps, material)
    error = np.max(np.abs(recovered - sigma)) / np.max(np.abs(sigma))

    print(f"! invariant ratio of the background: xi = {xi:.6f}")
    print(f"! the onset sits at xi = -xi0 = {-arguments.xi0:.6f}, so the background is")
    print(
        f"! {'above' if xi + arguments.xi0 > 0 else 'below'} it and the damage {'grows' if xi + arguments.xi0 > 0 else 'does not grow'} without any rupture"
    )
    print(f"! stress recovered from this strain to a relative {error:.2e}")
    for name, value in zip(NAMES, eps):
        print(f"  eps_{name}0: {value:.12e}")


if __name__ == "__main__":
    main()
