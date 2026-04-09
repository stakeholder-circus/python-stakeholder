# Tooling

## Standard commands
- `ruff format --check src tests`
- `ruff check src tests`
- `python -m build`
- `pytest`
- `docker build -t python-stakeholder .`
- `docker run --rm python-stakeholder --list-values`

## Notes
- The repo uses an editable install with `src/` packaging.
- `ruff` is the formatter and linter gate.
