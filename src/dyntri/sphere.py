"""Triangulations of the 2-sphere.

A triangulation is a list of oriented triangles (a, b, c) of integer vertex
labels. Orientation is counter-clockwise seen from outside, so two triangles
sharing an edge traverse it in opposite directions.
"""

from __future__ import annotations

Triangle = tuple[int, int, int]


def fan_sphere(n: int) -> list[Triangle]:
    """Bipyramid triangulation of S^2: an n-cycle equator coned off by two poles.

    Vertices 0..n-1 lie on the equator, n is the north pole, n+1 the south pole.
    Has n + 2 vertices, 3n edges and 2n triangles.
    """
    if n < 3:
        raise ValueError("equator needs at least 3 vertices")
    north, south = n, n + 1
    triangles: list[Triangle] = []
    for i in range(n):
        j = (i + 1) % n
        triangles.append((i, j, north))
        # reversed, so the shared equator edge i-j is traversed in the
        # opposite direction -> consistent orientation
        triangles.append((j, i, south))
    return triangles


def euler_characteristic(triangles: list[Triangle]) -> int:
    """Check `triangles` form a closed oriented surface; return V - E + F.

    Raises ValueError if a triangle is degenerate, an edge is used twice in
    the same direction (inconsistent orientation or more than two triangles
    on an edge), or an edge has only one triangle (a boundary).
    """
    directed: set[tuple[int, int]] = set()
    for a, b, c in triangles:
        if len({a, b, c}) != 3:
            raise ValueError(f"degenerate triangle {(a, b, c)}")
        for edge in ((a, b), (b, c), (c, a)):
            if edge in directed:
                raise ValueError(f"edge {edge} used twice in the same direction")
            directed.add(edge)
    for a, b in directed:
        if (b, a) not in directed:
            raise ValueError(f"edge {(a, b)} lies on a boundary")
    vertices = {v for t in triangles for v in t}
    edges = len(directed) // 2
    return len(vertices) - edges + len(triangles)
