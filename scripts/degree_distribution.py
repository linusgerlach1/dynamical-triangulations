"""Random edge flips on a fan triangulation; plot the vertex-degree distribution.

Run:  uv run python scripts/degree_distribution.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from dyntri.moves import (
    connected_components,
    euler_characteristic,
    example_adj,
    fan_triangulation,
    is_fpf_inv,
    random_flips,
    vertex_degrees,
)

FIGURES = Path(__file__).resolve().parents[1] / "figures"

if __name__ == "__main__":
    rng = np.random.default_rng(seed=42)

    print("example_adj valid:", is_fpf_inv(example_adj))
    adj = fan_triangulation(100)
    degrees = vertex_degrees(adj)
    print(f"fan: {len(adj) // 3} triangles, max degree {max(degrees)}")

    done = random_flips(adj, 10_000, rng)
    degrees = vertex_degrees(adj)
    print(f"after 10000 attempts: {done} flips carried out")
    print("valid gluing:", is_fpf_inv(adj))
    print("connected components:", connected_components(adj))
    print("Euler characteristic:", euler_characteristic(adj))
    print(f"vertices: {len(degrees)}, max degree {max(degrees)}")

    counts = np.bincount(degrees)
    plt.bar(range(len(counts)), counts)
    plt.xlabel("vertex degree")
    plt.ylabel("number of vertices")
    plt.title("Degree distribution after 10000 random flips")
    FIGURES.mkdir(exist_ok=True)
    plt.savefig(FIGURES / "degree_distribution.png", dpi=120)
    print(f"saved {FIGURES / 'degree_distribution.png'}")
