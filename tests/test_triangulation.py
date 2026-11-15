import pytest

from dyntri.triangulation import DOWN, UP, Triangulation


def test_uniform_shape() -> None:
    tri = Triangulation.uniform(time_slices=4, slice_length=5)
    assert tri.time_slices == 4
    assert tri.slice_lengths() == [5, 5, 5, 5]
    # each strip between two slices of length l has 2l triangles
    assert tri.num_triangles() == 4 * 2 * 5
    tri.validate()


def test_uniform_rejects_tiny_lattice() -> None:
    with pytest.raises(ValueError):
        Triangulation.uniform(time_slices=2, slice_length=5)
    with pytest.raises(ValueError):
        Triangulation.uniform(time_slices=4, slice_length=2)


def test_validate_catches_mismatched_slices() -> None:
    tri = Triangulation.uniform(time_slices=3, slice_length=4)
    tri.strips[0].append(DOWN)  # strip 0 now claims slice 1 has 5 vertices
    with pytest.raises(ValueError):
        tri.validate()


def test_validate_accepts_varying_slice_lengths() -> None:
    # slices of length 3, 4, 3: strip t has l_t UPs and l_{t+1} DOWNs
    tri = Triangulation(
        strips=[
            [UP, DOWN, UP, DOWN, DOWN, UP, DOWN],  # 3 up, 4 down
            [UP, DOWN, UP, UP, DOWN, UP, DOWN],  # 4 up, 3 down
            [UP, DOWN, UP, DOWN, UP, DOWN],  # 3 up, 3 down
        ]
    )
    tri.validate()
    assert tri.slice_lengths() == [3, 4, 3]
