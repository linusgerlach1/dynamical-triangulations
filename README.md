# dynamical-triangulations

Non-equilibrium sampling of random geometries for gravitational path integrals.

Monte Carlo simulations of causal dynamical triangulations (CDT) for lattice quantum gravity.
The Python package is called `dyntri`.

## Development

```bash
uv sync                 # install deps
uv run pytest           # tests
uv run ruff check .     # lint
uv run ruff format .    # format
uv run pyright          # type check
uv run dyntri           # CLI entry point
```
