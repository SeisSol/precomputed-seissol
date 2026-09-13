#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 SeisSol Group
#
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-LicenseComments: Full text under /LICENSE and /LICENSES/
#
# SPDX-FileContributor: Author lists in /AUTHORS and /CITATION.cff

"""Writes a structured tetrahedral cube as a PUML mesh.

The scenarios that need an exactly uniform or exactly periodic state cannot
use a meshed geometry: a free surface reflects, an outflow boundary does not
absorb exactly, and either one turns a state that should stay constant into a
wave. The cube generator built into SeisSol would do, but it refuses to run
(`The cube generator is (currently) not supported.`), so the mesh is written
here instead.

Periodicity is topological: every vertex on a maximum-side plane is given the
topological identity of its partner on the minimum-side plane, which is what
the `identify-vertex` topology format reads. The two faces that are glued that
way are congruent -- the in-plane triangulation of a structured grid is the
same on both sides -- so the flux across the seam sees the same face from both
of its cells even where the cells themselves have different sizes.

Usage:

    mkcube.py out.puml.h5 --cells 8 8 8 --size 1000 1000 1000
    mkcube.py out.puml.h5 --cells 4 4 4 --bc 6 6 6 6 1 5
    mkcube.py out.puml.h5 --cells 16 4 4 --grade-x 0.6
"""

import argparse
import itertools

import h5py
import numpy as np

# The six tetrahedra of the Freudenthal decomposition, as corner indices of a
# hexahedron numbered by (dx, dy, dz) in binary with dx the lowest bit. Each
# one is the path from corner 0 to corner 7 through one permutation of the
# three unit steps, which is what makes the decomposition conforming: two
# neighbouring hexahedra split their shared quadrilateral along the same
# diagonal.
TETS = (
    (0, 1, 3, 7),
    (0, 1, 5, 7),
    (0, 2, 3, 7),
    (0, 2, 6, 7),
    (0, 4, 5, 7),
    (0, 4, 6, 7),
)

# The faces of a tetrahedron in the order PUML enumerates them: the four
# vertex triples, sorted. SeisSol's own order is a permutation of this one
# (`PumlFaceToSeisSol`), and the boundary array is indexed in PUML's.
FACES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))


def coordinates(count, length, grade):
    """Node positions along one axis.

    `grade` bends the spacing towards the middle of the axis without breaking
    the periodicity of the spacing: the derivative of the map agrees at both
    ends, so the seam between the last and the first cell is as smooth as any
    other cell boundary. The ratio between the widest and the narrowest cell
    is (1 + grade) / (1 - grade).
    """
    s = np.linspace(0.0, 1.0, count + 1)
    if grade != 0.0:
        s = s - (grade / (2.0 * np.pi)) * np.sin(2.0 * np.pi * s)
    return length * s


def build(cells, size, origin, grade):
    nx, ny, nz = cells
    xs = coordinates(nx, size[0], grade[0]) + origin[0]
    ys = coordinates(ny, size[1], grade[1]) + origin[1]
    zs = coordinates(nz, size[2], grade[2]) + origin[2]

    def vertex(i, j, k):
        return (i * (ny + 1) + j) * (nz + 1) + k

    geometry = np.empty(((nx + 1) * (ny + 1) * (nz + 1), 3), dtype=np.float64)
    for i, j, k in itertools.product(range(nx + 1), range(ny + 1), range(nz + 1)):
        geometry[vertex(i, j, k)] = (xs[i], ys[j], zs[k])

    connect = np.empty((nx * ny * nz * len(TETS), 4), dtype=np.int64)
    cell = 0
    for i, j, k in itertools.product(range(nx), range(ny), range(nz)):
        corners = [
            vertex(i + (c & 1), j + ((c >> 1) & 1), k + ((c >> 2) & 1))
            for c in range(8)
        ]
        for tet in TETS:
            vertices = [corners[c] for c in tet]
            edges = geometry[vertices[1:]] - geometry[vertices[0]]
            if np.linalg.det(edges) < 0.0:
                vertices[2], vertices[3] = vertices[3], vertices[2]
            connect[cell] = vertices
            cell += 1

    return geometry, connect


def identify(cells, bc):
    """Topological vertex identities.

    A vertex on a maximum-side plane of a periodic direction takes the
    identity of the vertex it is to be glued to; a vertex on an edge or a
    corner is folded in every periodic direction at once.
    """
    nx, ny, nz = cells
    counts = (nx, ny, nz)
    periodic = tuple(bc[2 * d] == 6 and bc[2 * d + 1] == 6 for d in range(3))
    for d, count in enumerate(counts):
        # Two cells per direction is not enough to glue: the topological mesh
        # then holds two distinct faces with the same vertices, and a cell
        # neighbours itself across the seam.
        if periodic[d] and count < 3:
            raise RuntimeError(
                f"a periodic direction needs at least three cells, got {count}"
            )
    ids = np.empty(((nx + 1) * (ny + 1) * (nz + 1),), dtype=np.int32)
    for i, j, k in itertools.product(range(nx + 1), range(ny + 1), range(nz + 1)):
        folded = [
            0 if periodic[d] and index == counts[d] else index
            for d, index in enumerate((i, j, k))
        ]
        ids[(i * (ny + 1) + j) * (nz + 1) + k] = (folded[0] * (ny + 1) + folded[1]) * (
            nz + 1
        ) + folded[2]
    return ids, any(periodic)


def boundaries(geometry, connect, size, origin, bc):
    """The boundary condition of every face, in PUML's face order.

    A face whose three vertices share a bounding plane lies in that plane, and
    a bounding plane of the domain holds nothing but boundary faces, so this
    is a decision and not a guess.
    """
    planes = [
        (0, origin[0]),
        (0, origin[0] + size[0]),
        (1, origin[1]),
        (1, origin[1] + size[1]),
        (2, origin[2]),
        (2, origin[2] + size[2]),
    ]
    tolerance = 1e-9 * max(size)
    boundary = np.zeros((connect.shape[0], 4), dtype=np.int32)
    for cell in range(connect.shape[0]):
        points = geometry[connect[cell]]
        for face, corners in enumerate(FACES):
            for plane, (axis, value) in enumerate(planes):
                if np.all(np.abs(points[list(corners), axis] - value) < tolerance):
                    boundary[cell, face] = bc[plane]
                    break
    return boundary


def verify(geometry, connect, ids, boundary):
    counts = {}
    for cell in range(connect.shape[0]):
        for face, corners in enumerate(FACES):
            key = tuple(sorted(int(ids[connect[cell, c]]) for c in corners))
            counts.setdefault(key, []).append((cell, face))
    for key, users in counts.items():
        interior = len(users) == 2
        tagged = all(boundary[cell, face] != 0 for cell, face in users)
        if not (interior or (len(users) == 1 and tagged)):
            raise RuntimeError(
                f"face {key} is used {len(users)} times, tagged {tagged}"
            )
    volumes = np.linalg.det(geometry[connect[:, 1:]] - geometry[connect[:, :1]])
    if np.any(volumes <= 0.0):
        raise RuntimeError("mesh contains degenerate or inverted cells")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output")
    parser.add_argument("--cells", type=int, nargs=3, default=(4, 4, 4))
    parser.add_argument("--size", type=float, nargs=3, default=(1000.0, 1000.0, 1000.0))
    parser.add_argument("--origin", type=float, nargs=3, default=(0.0, 0.0, 0.0))
    parser.add_argument(
        "--bc",
        type=int,
        nargs=6,
        default=(6, 6, 6, 6, 6, 6),
        help="boundary condition of xmin xmax ymin ymax zmin zmax; 6 is periodic",
    )
    parser.add_argument("--grade-x", type=float, default=0.0)
    parser.add_argument("--grade-y", type=float, default=0.0)
    parser.add_argument("--grade-z", type=float, default=0.0)
    parser.add_argument("--group", type=int, default=1)
    arguments = parser.parse_args()

    grade = (arguments.grade_x, arguments.grade_y, arguments.grade_z)
    geometry, connect = build(arguments.cells, arguments.size, arguments.origin, grade)
    ids, periodic = identify(arguments.cells, arguments.bc)
    boundary = boundaries(
        geometry, connect, arguments.size, arguments.origin, arguments.bc
    )
    verify(geometry, connect, ids, boundary)

    with h5py.File(arguments.output, "w") as out:
        out.create_dataset("connect", data=connect)
        out.create_dataset("geometry", data=geometry)
        out.create_dataset(
            "group", data=np.full((connect.shape[0],), arguments.group, dtype=np.int32)
        )
        out.create_dataset("boundary", data=boundary)
        out.attrs["boundary-format"] = np.bytes_("i32x4")
        if periodic:
            out.create_dataset("identify", data=ids)
            out.attrs["topology-format"] = np.bytes_("identify-vertex")
        else:
            out.attrs["topology-format"] = np.bytes_("geometric")

    print(
        f"{arguments.output}: {connect.shape[0]} cells, "
        f"{geometry.shape[0]} vertices, periodic: {periodic}"
    )


if __name__ == "__main__":
    main()
