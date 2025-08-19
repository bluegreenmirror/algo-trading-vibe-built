# Gemini Guidelines

This document provides best practices and standard guidelines for interacting with the Gemini AI assistant in this project. Adhering to these standards ensures consistency, efficiency, and alignment with the project's established development workflow.

## 1. Environment Setup

Before making any changes, ensure your environment is correctly configured. The project provides a streamlined setup process.

- **Initial Setup**: Run `make doctor` or `scripts/doctor.sh` to verify your environment. This script checks for necessary dependencies and configurations, ensuring that your local setup matches the project's requirements.
- **Containerized Development**: For a consistent and isolated development environment, use the provided Docker setup. Build the image with `docker compose build` and run commands via `scripts/run.sh`.

**Why this is needed**: A consistent environment prevents "it works on my machine" issues, which are common in collaborative projects. Using the provided scripts guarantees that all developers work with the same dependencies and configurations, reducing integration problems.

## 2. Development Workflow

Follow the established development workflow to maintain code quality and consistency.

- **Linting and Formatting**: Before committing any changes, run `make lint` and `make fmt`. This project uses Ruff for linting and Black for code formatting. These tools enforce a consistent code style, improving readability and maintainability.
- **Testing**: Run `make test` to execute the test suite. All tests must pass before submitting a pull request. This ensures that your changes do not break existing functionality.

**Why this is needed**: A standardized workflow automates quality checks, allowing developers to focus on writing code. Enforcing linting, formatting, and testing before committing reduces the number of errors and inconsistencies in the codebase.

## 3. Commit Messages

Adhere to the [Conventional Commits](https://www.conventionalcommits.org/) specification for all commit messages. This provides a clear and descriptive history of changes.

- **Format**: Use prefixes like `feat:`, `fix:`, `docs:`, `test:`, or `ci:` to indicate the type of change.
- **Style**: Write subject lines in the imperative mood (e.g., `feat: add user authentication`).

**Why this is needed**: Conventional Commits create a structured and easily navigable commit history. This makes it easier to understand the project's evolution, automate release notes, and identify the impact of specific changes.

## 4. Pull Requests

Keep pull requests (PRs) small, focused, and incremental. This simplifies the review process and reduces the risk of introducing bugs.

- **Scope**: Each PR should address a single, well-defined issue or feature.
- **Description**: Reference the relevant sprint plan from `docs/sprint-plan/` in the PR description. This provides context for the changes and helps track progress against project goals.

**Why this is needed**: Small, focused PRs are easier to review, test, and merge. Linking PRs to the sprint plan improves project management and transparency, ensuring that all work aligns with the team's objectives.

## 5. Secrets Management

Never commit secrets directly to the repository. This project uses `detect-secrets` to prevent accidental exposure of sensitive information.

- **Local Development**: Use a `.env` file for local development. Create it by copying `.env.example` and filling in the required values.
- **Pre-commit Hook**: The pre-commit configuration includes a hook that scans for secrets. Ensure that you run `pre-commit run --all-files` before committing to avoid accidentally leaking credentials.

**Why this is needed**: Leaking secrets can lead to severe security breaches. By using `.env` files and a pre-commit hook, we ensure that sensitive information is never stored in the version control system, protecting our infrastructure and data.

## 6. Testing

All new features and bug fixes must be accompanied by corresponding tests. This ensures the long-term stability and reliability of the codebase.

- **Coverage**: Add or update tests to cover all code changes.
- **Execution**: Run `pytest` or `make test` to execute the test suite.

**Why this is needed**: A comprehensive test suite acts as a safety net, allowing developers to refactor and add new features with confidence. It verifies that the code behaves as expected and prevents regressions.

## 7. Code Style

This project uses [Black](https://github.com/psf/black) for code formatting and [Ruff](https://github.com/astral-sh/ruff) for linting. These tools ensure a consistent and readable code style across the entire codebase.

- **Formatting**: Use `make fmt` to automatically format your code before committing.
- **Linting**: Use `make lint` to identify and fix potential issues.

**Why this is needed**: A consistent code style improves readability and maintainability. By automating this process, we reduce the cognitive load on developers and allow them to focus on the logic of their code.