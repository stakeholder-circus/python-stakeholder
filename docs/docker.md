# Docker

The repo uses a Python 3.12 slim image with editable install, build, lint, and tests executed in the image.

## Commands
- `docker build -t python-stakeholder .`
- `docker run --rm python-stakeholder --list-values`

## CI intent
- Build the package artifact with `python -m build`.
- Enforce `ruff` and `mypy` in the container build stage.
