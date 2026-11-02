# dyntri

Monte Carlo simulations of causal dynamical triangulations (CDT) for lattice quantum gravity.

## Commands
- Run tests: `uv run pytest`
- Lint / format: `uv run ruff check .` and `uv run ruff format .`
- Type check: `uv run pyright`
- Add a dependency: `uv add <pkg>` (dev: `uv add --dev <pkg>`); never edit uv.lock by hand

## Layout
- `src/dyntri/`: package source (src layout)
- `tests/`: pytest tests

## Conventions
- Python 3.12+, full type hints, numpy for numerics
- Simulations must take an explicit seed / `numpy.random.Generator` so runs are reproducible
- Moves must preserve the triangulation's topology and causal (foliated) structure; add tests that check these invariants after each move type
