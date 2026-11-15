"""1+1D causal dynamical triangulations.

Spacetime is a stack of T spatial slices (circles), periodic in time, so
the topology is a torus S^1 x S^1. Slice t has l_t vertices (and l_t edges).

The strip between slice t and slice t+1 is filled with triangles of two types:

- UP   triangles: base edge on slice t,   tip vertex on slice t+1   (a (2,1) triangle)
- DOWN triangles: base edge on slice t+1, tip vertex on slice t     (a (1,2) triangle)

Going around the strip in spatial order, a triangulation of the strip is just a
cyclic sequence of UP/DOWN labels, with exactly l_t UPs and l_{t+1} DOWNs.
So the whole triangulation is a list of T such sequences.
"""

from __future__ import annotations

from dataclasses import dataclass

UP = 1
DOWN = 0


@dataclass
class Triangulation:
    """A 1+1D CDT on a torus.

    strips[t] is the cyclic UP/DOWN sequence for the strip between
    slice t and slice (t + 1) % T.
    """

    strips: list[list[int]]

    @classmethod
    def uniform(cls, time_slices: int, slice_length: int) -> Triangulation:
        """Flat starting configuration: every slice has `slice_length` vertices."""
        if time_slices < 3:
            raise ValueError("need at least 3 time slices")
        if slice_length < 3:
            raise ValueError("need at least 3 vertices per slice")
        strip = [UP, DOWN] * slice_length
        return cls(strips=[list(strip) for _ in range(time_slices)])

    @property
    def time_slices(self) -> int:
        return len(self.strips)

    def slice_lengths(self) -> list[int]:
        """Number of vertices l_t on each spatial slice t."""
        return [strip.count(UP) for strip in self.strips]

    def num_triangles(self) -> int:
        """Total number of triangles N_2 (the discrete spacetime volume)."""
        return sum(len(strip) for strip in self.strips)

    def validate(self) -> None:
        """Raise ValueError if the triangulation is not a valid CDT.

        Neighbouring strips must agree on the length of the slice they share:
        the DOWNs in strip t and the UPs in strip t+1 both sit on slice t+1.
        """
        lengths = self.slice_lengths()
        for t, strip in enumerate(self.strips):
            next_length = lengths[(t + 1) % self.time_slices]
            if strip.count(DOWN) != next_length:
                raise ValueError(
                    f"strip {t} has {strip.count(DOWN)} DOWN triangles, "
                    f"but slice {t + 1} has {next_length} vertices"
                )
        for t, length in enumerate(lengths):
            if length < 3:
                raise ValueError(f"slice {t} has only {length} vertices (min 3)")
