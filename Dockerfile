FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY README.md ./
COPY src ./src
COPY tests ./tests
RUN pip install --no-cache-dir build
RUN pip install --no-cache-dir -e .[dev,test]
RUN python -m build
RUN ruff format --check src tests
RUN ruff check src tests
RUN mypy src
RUN pytest
ENTRYPOINT ["python", "-m", "stakeholder"]
