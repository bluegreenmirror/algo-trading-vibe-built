
# AGENTS

# Agent Guidelines

## Sprint-oriented development
- Break work into small, demo-able increments.
- Associate commits with task or sprint identifiers.

## Containerization
- Use the existing `dockerfile` and `docker-compose.yml` for development and demos.
- Build and run containers with:
  ```bash
  docker build -f dockerfile -t algo-trading-vibe .
  docker compose up
  ```

## Best practices
- Reference `.pre-commit-config.yaml` for linting and formatting.
- Run `pre-commit run --files <file> [<file> ...]` to check staged files.
- Run tests or demo scripts before each commit.
- Propose improvements and note outstanding work for future sprints.
- Follow PEP 8 naming and formatting guidelines.
- Include module/function docstrings and descriptive comments.
- Structure functions and classes around the single-responsibility principle.
