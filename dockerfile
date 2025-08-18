# Dev/Run Image
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry in the image (no need on host)
RUN pip install --no-cache-dir poetry==1.8.3

# Copy metadata first (better layer caching)
COPY pyproject.toml README.md .pre-commit-config.yaml .secrets.baseline ./
# Copy source last
COPY src ./src
COPY tests ./tests

# Install deps (no venv -> use system site-packages in container)
ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN poetry install --no-interaction --no-ansi

# Default command -> CLI help
# Run with system Python; deps were installed into site-packages during build
ENTRYPOINT ["python", "-m", "src.app"]