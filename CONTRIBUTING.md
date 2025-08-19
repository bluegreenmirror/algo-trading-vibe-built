# Contributing

## Coding Style
- Use [Black](https://github.com/psf/black) for formatting. The repository configures Black with a 100 character line length and Python 3.11 support. Run `pre-commit run --files <file>` or `pre-commit run --all-files` to apply formatting.
- Lint with [Ruff](https://github.com/astral-sh/ruff); the pre-commit configuration auto-fixes simple issues.
- Secrets are scanned with `detect-secrets`; include `.secrets.baseline` when running pre-commit.

## Testing
- Add or update tests for all code changes.
- Run `pytest` (or `make test`) and ensure all tests pass before pushing commits.

## Commit Messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `fix:`, `docs:`, `test:`, `ci:`).
- Keep subject lines concise and written in the imperative mood.

## Pull Requests
- Keep PRs small and incremental.
- Reference the relevant sprint plan under `docs/sprint-plan/` in the PR description.
- Verify code formatting, linting, and tests before requesting review.
