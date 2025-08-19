# Getting Started with Algo Trading Bot

Welcome to the Algo Trading Bot project! This guide will help you set up your development environment, understand the project's structure, and make your first contribution.

## 1. Environment Setup

To ensure a consistent development experience, we use Docker and Poetry. Follow these steps to get your environment ready:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_ORG/YOUR_REPO.git
    cd algo-trading-vibe-built
    ```

2.  **Build the Docker image:**
    ```bash
    docker compose build
    ```

3.  **Create a local `.env` file:**
    ```bash
    cp .env.example .env
    ```
    Edit the `.env` file and fill in your Alpaca API credentials (you'll get these later, for now, leave them as placeholders if you don't have them).

4.  **Verify your environment:**
    ```bash
    make doctor
    ```
    This script checks for necessary dependencies and configurations.

## 2. Project Overview

This project is an algorithmic trading bot designed for paper trading via the Alpaca API. It features a strategy engine, policy engine, backtester, and structured logging.

*   **`src/`**: Contains the core source code.
*   **`tests/`**: Contains unit and integration tests.
*   **`docs/`**: Contains project documentation, including architecture, technical design, and sprint plans.
*   **`scripts/`**: Contains helper scripts for development tasks.
*   **`makefile`**: Provides convenient commands for building, testing, and running the project.

## 3. Key Decisions

For a deeper understanding of the architectural and technical decisions made in this project, please refer to the `DECISIONS.md` file.

## 4. Development Workflow

We follow a standardized development workflow to maintain code quality and consistency:

*   **Linting and Formatting**: Before committing, run `make lint` and `make fmt` to ensure your code adheres to our style guidelines.
*   **Testing**: Run `make test` to execute the test suite. All tests must pass before submitting a pull request.
*   **Commit Messages**: We use [Conventional Commits](https://www.conventionalcommits.org/) for clear and descriptive commit messages.
*   **Pull Requests**: Keep PRs small, focused, and incremental. Reference relevant sprint plans from `docs/sprint-plan/` in your PR description.

## 5. Interacting with AI Agents

If you are an AI agent working on this project, please refer to `GEMINI.md` for guidelines on how to best interact with the codebase and human developers.

## 6. Further Reading

*   **`README.md`**: High-level project overview.
*   **`DECISIONS.md`**: Detailed architectural and technical decisions.
*   **`GEMINI.md`**: Guidelines for AI agent interaction.
*   **`docs/`**: Comprehensive project documentation.
*   **`CONTRIBUTING.md`**: Guidelines for contributing to the project.
*   **`AGENTS.md`**: Information about the AI agents used in the project.
