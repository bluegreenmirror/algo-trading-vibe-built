# Dev/Run Image
FROM python:3.13-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry in the image (no need on host)
ARG POETRY_VERSION=1.8.3
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"


# Environment: deterministic + unbuffered I/O
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

# Copy metadata first (better layer caching)
COPY pyproject.toml README.md .pre-commit-config.yaml .secrets.baseline ./
# If you commit a lockfile later, uncomment next line for reproducible builds:
# COPY poetry.lock ./

# Copy source (dev image includes tests; for a prod image, skip tests/)
COPY src ./src
COPY tests ./tests

# (not implemented) switch to non-root user for runtime security
# RUN addgroup --system app && adduser --system --ingroup app app
# RUN chown -R app:app /app
# USER app

# Install deps before copying the full source for better caching when code changes
# Install only dependencies (no project) to leverage caching
RUN poetry install --no-ansi --no-root

# Run with system Python; deps were installed into site-packages during build
ENTRYPOINT ["python", "-m", "src.app"]