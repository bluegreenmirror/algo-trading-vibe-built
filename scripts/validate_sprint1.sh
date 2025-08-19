#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Validating Sprint 1 Implementation"
echo "======================================"

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

# Check if dependencies are installed
if [[ ! -d ".venv" ]] && [[ ! -d "venv" ]]; then
    echo "⚠️  No virtual environment found. Installing dependencies..."
    if command -v poetry &> /dev/null; then
        poetry install
    else
        echo "❌ Poetry not found. Please install Poetry first:"
        echo "   pipx install poetry"
        exit 1
    fi
fi

# Check if .env exists
if [[ ! -f ".env" ]]; then
    echo "⚠️  No .env file found. Creating from template..."
    if [[ -f "env.example" ]]; then
        cp env.example .env
        echo "✅ Created .env from template"
        echo "⚠️  Please edit .env and add your Alpaca API keys"
    else
        echo "❌ env.example not found"
        exit 1
    fi
fi

# Check if all required modules exist
echo "📁 Checking module structure..."
required_modules=(
    "src/__init__.py"
    "src/data/__init__.py"
    "src/data/providers/__init__.py"
    "src/data/providers/alpaca.py"
    "src/strategy/__init__.py"
    "src/strategy/rules_engine.py"
    "src/risk/__init__.py"
    "src/risk/policy_engine.py"
    "src/broker/__init__.py"
    "src/exec/__init__.py"
    "src/exec/order_router.py"
    "src/trading_bot.py"
    "src/config.py"
)

missing_modules=()
for module in "${required_modules[@]}"; do
    if [[ -f "$module" ]]; then
        echo "✅ $module"
    else
        echo "❌ $module (missing)"
        missing_modules+=("$module")
    fi
done

if [[ ${#missing_modules[@]} -gt 0 ]]; then
    echo "❌ Missing modules: ${missing_modules[*]}"
    exit 1
fi

# Test the implementation
echo ""
echo "🧪 Running Sprint 1 tests..."
if command -v poetry &> /dev/null; then
    poetry run python test_sprint1.py
else
    python test_sprint1.py
fi

echo ""
echo "🎉 Sprint 1 validation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Alpaca API keys"
echo "2. Run: poetry run python -m src.trading_bot test"
echo "3. Run: poetry run python -m src.trading_bot run"
echo ""
echo "Or use Docker:"
echo "1. docker compose build"
echo "2. ./scripts/run.sh test"
echo "3. ./scripts/run.sh run"
