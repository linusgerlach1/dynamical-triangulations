"""Triangulations of the 2-sphere as half-edge adjacency arrays, and edge flips.

A triangulation with n triangles is an int array `adj` of length 3n.
Half-edge j belongs to triangle j // 3; the three half-edges of a triangle
are 3t, 3t+1, 3t+2 in cyclic (counter-clockwise) order. adj[j] is the
half-edge in the neighbouring triangle that j is glued to, so `adj` must be
a fixed-point-free involution.
"""

from collections import deque

import numpy as np
import numpy.typing as npt

Adj = npt.NDArray[np.int32]

example_adj: Adj = np.array([9, 4, 6, 7, 1, 11, 2, 3, 10, 0, 8, 5], dtype=np.int32)


def fan_triangulation(n: int) -> Adj:
    """Fan triangulation of the sphere with n triangles (n must be even, >= 2)."""
    if n < 2 or n % 2:
        raise ValueError("n must be even and at least 2")
    return np.array(
        [
            [(i - 3) % (3 * n), i + 5, i + 4, (i + 6) % (3 * n), i + 2, i + 1]
            for i in range(0, 3 * n, 6)
        ],
        dtype=np.int32,
    ).flatten()


def is_fpf_inv(adj: Adj) -> bool:
    """True if adj is a fixed-point-free involution (a valid gluing)."""
    for x, a in enumerate(adj):
        if a < 0 or a >= len(adj) or x == a or adj[a] != x:
            return False
    return True


def triangle_neighbors(adj: Adj, i: int) -> list[int]:
    return [int(j) // 3 for j in adj[3 * i : 3 * i + 3]]


def connected_components(adj: Adj) -> int:
    """Number of connected components of the triangulation."""
    n = len(adj) // 3
    component = np.full(n, -1, dtype=np.int32)
    index = 0
    for i in range(n):
        if component[i] == -1:
            component[i] = index
            queue = deque([i])
            while queue:
                for nbr in triangle_neighbors(adj, queue.pop()):
                    if component[nbr] == -1:
                        component[nbr] = index
                        queue.appendleft(nbr)
            index += 1
    return index


def next_(j: int) -> int:
    """Next half-edge in the same triangle (counter-clockwise)."""
    return j - 2 if j % 3 == 2 else j + 1


def prev_(j: int) -> int:
    """Previous half-edge in the same triangle."""
    return j + 2 if j % 3 == 0 else j - 1


def vertex_degrees(adj: Adj) -> list[int]:
    """Degree of every vertex.

    Half-edges starting at the same vertex form an orbit of
    j -> next_(adj[j]); the orbit length is the vertex degree.
    """
    seen = np.zeros(len(adj), dtype=bool)
    degrees: list[int] = []
    for start in range(len(adj)):
        if seen[start]:
            continue
        degree = 0
        j = start
        while not seen[j]:
            seen[j] = True
            degree += 1
            j = next_(int(adj[j]))
        degrees.append(degree)
    return degrees


def euler_characteristic(adj: Adj) -> int:
    """V - E + F; equals 2 for a triangulation of the sphere."""
    vertices = len(vertex_degrees(adj))
    edges = len(adj) // 2
    faces = len(adj) // 3
    return vertices - edges + faces


def flip_edge(adj: Adj, i: int) -> bool:
    """Flip the edge of half-edge i in place; return False if it can't be flipped.

    The two triangles sharing the edge form a quadrilateral; the flip replaces
    the edge by the other diagonal. Edges whose two sides lie in the same
    triangle (a folded triangle) are not flipped.
    """
    k = int(adj[i])
    if k // 3 == i // 3:
        return False
    j = prev_(i)
    l = prev_(k)  # noqa: E741
    # outer half-edge next to l moves to i, the one next to j moves to k,
    # and j, l become the new diagonal
    n = int(adj[l])
    adj[i] = n
    adj[n] = i
    n = int(adj[j])
    adj[k] = n
    adj[n] = k
    adj[l] = j
    adj[j] = l
    return True


def random_flips(adj: Adj, num: int, rng: np.random.Generator) -> int:
    """Apply `num` attempted flips at uniformly random half-edges.

    Returns the number of flips that were actually carried out.
    """
    done = 0
    for _ in range(num):
        done += flip_edge(adj, int(rng.integers(len(adj))))
    return done
