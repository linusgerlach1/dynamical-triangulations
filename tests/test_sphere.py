import pytest

from dyntri.sphere import Triangle, euler_characteristic, fan_sphere


@pytest.mark.parametrize("n", [3, 4, 5, 10, 100])
def test_fan_sphere_is_a_sphere(n: int) -> None:
    triangles = fan_sphere(n)
    assert euler_characteristic(triangles) == 2


@pytest.mark.parametrize("n", [3, 7])
def test_fan_sphere_counts(n: int) -> None:
    triangles = fan_sphere(n)
    vertices = {v for t in triangles for v in t}
    assert len(vertices) == n + 2
    assert len(triangles) == 2 * n


def test_fan_sphere_rejects_small_n() -> None:
    with pytest.raises(ValueError):
        fan_sphere(2)


def test_detects_boundary() -> None:
    # upper hemisphere only: a disk, not closed
    disk = fan_sphere(5)[::2]
    with pytest.raises(ValueError, match="boundary"):
        euler_characteristic(disk)


def test_detects_inconsistent_orientation() -> None:
    triangles = fan_sphere(5)
    a, b, c = triangles[0]
    triangles[0] = (b, a, c)  # flip one triangle
    with pytest.raises(ValueError, match="same direction"):
        euler_characteristic(triangles)


def test_detects_degenerate_triangle() -> None:
    bad: list[Triangle] = [(0, 0, 1)]
    with pytest.raises(ValueError, match="degenerate"):
        euler_characteristic(bad)


def test_torus_has_euler_characteristic_zero() -> None:
    # minimal 7-vertex (Moebius/Csaszar) torus triangulation
    triangles: list[Triangle] = []
    for i in range(7):
        triangles.append((i, (i + 1) % 7, (i + 3) % 7))
        triangles.append((i, (i + 3) % 7, (i + 2) % 7))
    assert euler_characteristic(triangles) == 0
