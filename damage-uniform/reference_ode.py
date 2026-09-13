#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 SeisSol Group
#
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-LicenseComments: Full text under /LICENSE and /LICENSES/
#
# SPDX-FileContributor: Author lists in /AUTHORS and /CITATION.cff

"""The exact answer for a cell whose strain does not change.

Under periodic boundaries and a state that starts uniform, the divergence of
the stress vanishes and the velocity stays zero, so the strain stays what the
material file put there for all time. What is left of the system is the two
source terms, and they are an ordinary differential equation in alpha and B
alone -- with a closed form as long as B stays zero, because then the drive is
constant and alpha is linear in time.

This reproduces the source terms of the kernel, including the guard that stops
the growth and the critical damage the breakage sigmoid is centred on, and
integrates them for the four cases the scenario runs. The numbers it prints
are what the receivers of a run have to show.
"""

import numpy as np

VOIGT = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 2.0])


def invariants(eps):
    i1 = eps[0] + eps[1] + eps[2]
    i2 = float(np.dot(VOIGT, eps * eps))
    xi = i1 / np.sqrt(i2) if i2 > 0.0 else 0.0
    return i1, i2, xi


def critical(material, xi):
    """The damage at which breakage sets in.

    The smaller root of the quadratic in alpha, capped against the ratio at
    which the effective shear modulus vanishes and against one -- the same
    three-way minimum the kernel forms.
    """
    mu0, lambda0, gamma, xi0 = (
        material["mu0"],
        material["lambda0"],
        material["gammaR"],
        material["xi0"],
    )
    a = (
        3.0 * gamma**2 * xi**2
        - 3.0 * gamma**2
        + 6.0 * gamma**2 * xi0 * xi
        + 4.0 * gamma**2 * xi0**2
    )
    b = (
        -(8.0 * mu0 + 6.0 * lambda0) * gamma * xi0
        - gamma * lambda0 * xi**3
        - 6.0 * gamma * mu0 * xi
    )
    c = 4.0 * mu0**2 + 6.0 * mu0 * lambda0
    candidates = []
    discriminant = b * b - 4.0 * a * c
    if discriminant > 0.0 and a != 0.0:
        root = (-b - np.sqrt(discriminant)) / (2.0 * a)
        candidates.append(root if root > 0.0 else 1.0)
    modulus = 2.0 * mu0 / (gamma * (xi + 2.0 * xi0)) if gamma != 0.0 else np.inf
    candidates.append(modulus if modulus > 0.0 else 1.0)
    return min(min(candidates), 1.0)


def sources(material, state, i2, xi):
    alpha, breakage = state
    drive = material["gammaR"] * (1.0 - breakage) * i2 * (xi + material["xi0"])
    growing = (xi + material["xi0"]) > 0.0 and alpha < 1.0 and breakage < 1.0
    rate = material["Cd"] if growing else material["healingrate"]
    sigmoid = 1.0 / (
        1.0 + np.exp((critical(material, xi) - alpha) / material["betaalpha"])
    )
    return np.array(
        [
            rate * drive,
            material["breakagerate"] * drive * sigmoid if growing else 0.0,
        ]
    )


def integrate(material, end, steps=200000):
    eps = np.array(
        [material[f"eps_{c}0"] for c in ("xx", "yy", "zz", "xy", "yz", "xz")]
    )
    _, i2, xi = invariants(eps)
    state = np.array([material["alpha0"], material["breakage0"]])
    step = end / steps
    for _ in range(steps):
        k1 = sources(material, state, i2, xi)
        k2 = sources(material, state + 0.5 * step * k1, i2, xi)
        k3 = sources(material, state + 0.5 * step * k2, i2, xi)
        k4 = sources(material, state + step * k3, i2, xi)
        state = state + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return state, i2, xi


ROCK = {
    "rho": 2700.0,
    "lambda0": 3.0e10,
    "mu0": 3.0e10,
    "xi0": 0.8,
    "breakagerate": 0.0,
    "healingrate": 0.0,
    "betaalpha": 1.0,
    "eps_xx0": 0.0,
    "eps_yy0": 0.0,
    "eps_zz0": 0.0,
    "eps_xy0": 0.0,
    "eps_yz0": 0.0,
    "eps_xz0": 0.0,
    "alpha0": 0.0,
    "breakage0": 0.0,
}

CASES = {
    # Uniaxial extension, xi = +1: above the onset, so alpha grows.
    "growth": dict(ROCK, gammaR=1.0e10, Cd=1.0e-3, eps_xx0=1.0e-4, end=2.0),
    # The same run carried past the point where the guard stops the growth.
    "saturation": dict(ROCK, gammaR=1.0e10, Cd=1.0e-3, eps_xx0=1.0e-4, end=6.0),
    # Uniaxial compression, xi = -1: below the onset, so alpha heals.
    "healing": dict(
        ROCK,
        gammaR=1.0e10,
        Cd=1.0e-3,
        healingrate=1.0e-2,
        eps_xx0=-1.0e-4,
        alpha0=0.5,
        end=2.0,
    ),
    # Pure shear, xi = 0 exactly: the second invariant carries the Voigt
    # weight of two, and a factor lost there halves the rate.
    "shear": dict(ROCK, gammaR=1.0e10, Cd=1.0e-3, eps_xy0=1.0e-4, end=2.0),
    # Pure shear with a damage modulus large enough to bring the critical
    # damage inside (0, 1), started just below it.
    "breakage": dict(
        ROCK,
        gammaR=6.0e10,
        Cd=1.0e-4,
        breakagerate=1.0e-4,
        betaalpha=0.02,
        eps_xy0=1.0e-4,
        alpha0=0.40,
        end=5.0,
    ),
}


def main():
    print(
        f"{'case':<12}{'xi':>8}{'I2':>12}{'drive':>10}{'a_cr':>8}"
        f"{'t':>7}{'alpha':>12}{'B':>12}{'alpha linear':>14}"
    )
    for name, material in CASES.items():
        end = material["end"]
        state, i2, xi = integrate(material, end)
        drive = material["gammaR"] * i2 * (xi + material["xi0"])
        rate = (
            material["Cd"] if (xi + material["xi0"]) > 0.0 else material["healingrate"]
        )
        linear = material["alpha0"] + rate * drive * end
        print(
            f"{name:<12}{xi:>8.3f}{i2:>12.3e}{drive:>10.1f}"
            f"{critical(material, xi):>8.4f}{end:>7.2f}"
            f"{state[0]:>12.6f}{state[1]:>12.6f}{linear:>14.6f}"
        )


if __name__ == "__main__":
    main()
