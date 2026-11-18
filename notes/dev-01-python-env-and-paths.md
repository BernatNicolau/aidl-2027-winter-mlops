# Python environment and paths

## Environment

- The env is `.venv` at the repo root. Activate with `source .venv/bin/activate`;
  `deactivate` to leave. Check with `which python`.
- `uv pip install <pkg>` is a fast drop-in for `pip` and installs into the active env
  (or finds `.venv` from the repo root).
- Installing does **not** edit `requirements.txt`; add the lines yourself.
  Check the file against the imports in the code (a missing `pandas` and `torchvision`
  caused errors here).
- `ModuleNotFoundError` in the VS Code debugger: install into the right env and select
  the `.venv` interpreter (Command Palette: **Python: Select Interpreter**).

## Project-level env with `uv sync` (`pyproject.toml`)

- The root `pyproject.toml` lists the dependencies of **all** sessions plus a `dev` group
  (`ruff`, `poethepoet`). `uv sync` creates/updates `.venv` to match it exactly and writes
  `uv.lock` (exact versions, commit it for reproducibility). No `pip` needed.
- Add a dependency with `uv add <pkg>` (edits `pyproject.toml` + lock + env); dev-only
  tools with `uv add --dev <pkg>`. Run anything with `uv run <cmd>` (no activation).
- A new session's `requirements.txt` goes into the project with
  `uv add -r session-N/requirements.txt` (adds each line to `dependencies`, updates the
  lock and installs). `uv pip install -r` only installs and leaves `pyproject.toml`
  unchanged.
- Gotcha: `uv sync` makes `.venv` match `pyproject.toml` exactly, so anything installed
  only with `uv pip install` is removed. Do not mix the two; use `uv add`.
- Other commands: `uv remove <pkg>`, `uv add --dev <pkg>`; a pinned version
  (`torch==2.5.0`) is kept, and uv reports a conflict with an existing constraint.
- `[tool.uv] package = false`: the exercises are scripts, not an installable package.
- `uv run poe all` runs the tasks defined under `[tool.poe.tasks]` (`ruff check .` then
  `ruff format --check .`); `poe format` applies the formatting.
- `ruff check` also parses files: placeholder `def f(...)` from the course skeletons are
  reported as `invalid-syntax` until replaced with real parameters.

## Paths

- A relative path like `'data/x.csv'` resolves against the **current working directory**
  (where Python was launched), not the file's folder. Running `python session-2/main.py`
  from the repo root makes `data/...` point to the wrong place.
- Robust fix: `Path(__file__).parent / "data"`.
- The `/` join operator works only on `Path`, not on `str`. Accept `str | Path` in
  constructors and convert with `Path(x)`.
- Prefer passing paths in from the caller (e.g. via a config dict) instead of
  hardcoding them in modules.
