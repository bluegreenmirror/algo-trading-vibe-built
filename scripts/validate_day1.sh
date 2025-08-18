# scripts/validate_day1.sh
#!/usr/bin/env bash
set -euo pipefail

RED=$'\e[31m'; GREEN=$'\e[32m'; YELLOW=$'\e[33m'; NC=$'\e[0m'
ok(){ echo "${GREEN}PASS${NC}  $*"; }
warn(){ echo "${YELLOW}WARN${NC}  $*"; }
fail(){ echo "${RED}FAIL${NC}  $*"; exit 1; }

# 1) Files & folders exist
REQUIRED_PATHS=(
  "pyproject.toml"
  ".gitignore"
  ".editorconfig"
  ".pre-commit-config.yaml"
  ".secrets.baseline"
  ".github/workflows/ci.yml"
  ".env.example"
  "scripts/bootstrap.sh"
  "src/app.py"
  "src/config.py"
  "tests/test_smoke.py"
)
for p in "${REQUIRED_PATHS[@]}"; do
  [[ -e "$p" ]] && ok "exists: $p" || fail "missing: $p"
done

# 2) .gitignore must ignore .env
grep -qx '\.env' .gitignore && ok ".env is ignored in .gitignore" || fail ".env not ignored in .gitignore"

# 3) Pre-commit hooks include black, ruff, detect-secrets
grep -q 'black' .pre-commit-config.yaml && ok "pre-commit: black hook present" || fail "pre-commit missing black"
grep -q 'ruff' .pre-commit-config.yaml && ok "pre-commit: ruff hook present" || fail "pre-commit missing ruff"
grep -q 'detect-secrets' .pre-commit-config.yaml && ok "pre-commit: detect-secrets hook present" || fail "pre-commit missing detect-secrets"

# 4) pyproject key deps & configs present
grep -q 'pydantic-settings' pyproject.toml && ok "pyproject: pydantic-settings present" || fail "pyproject missing pydantic-settings"
grep -q 'pytest' pyproject.toml && ok "pyproject: pytest present" || fail "pyproject missing pytest"
grep -q 'tool.ruff' pyproject.toml && ok "pyproject: ruff config present" || warn "pyproject ruff config not found"
grep -q 'tool.black' pyproject.toml && ok "pyproject: black config present" || warn "pyproject black config not found"
grep -q '\[tool\.pytest\.ini_options\]' pyproject.toml && ok "pyproject: pytest ini options" || warn "pyproject: pytest ini options not found"

# 5) bootstrap script shebang
head -n1 scripts/bootstrap.sh | grep -q '#!/usr/bin/env bash' && ok "bootstrap.sh has shebang" || warn "bootstrap.sh missing shebang"

# 6) EditorConfig Python indent 4
grep -q '^\[*.py\]' .editorconfig && grep -q '^indent_size = 4' .editorconfig \
  && ok "EditorConfig Python indent_size=4" || warn "EditorConfig Python indent may not be 4"

# 7) Basic commands
echo "== Installing deps with Poetry (dry run if already installed) =="
poetry --version >/dev/null 2>&1 || fail "Poetry not installed (install with: pipx install poetry)"
poetry install --no-interaction --no-ansi
ok "poetry install"

echo "== Installing pre-commit hooks =="
poetry run pre-commit install
ok "pre-commit installed"

echo "== Creating local .env if missing =="
[[ -f .env ]] || cp .env.example .env
ok ".env present (keep secrets empty for Day 1)"

echo "== Running linters =="
poetry run ruff check .
poetry run black --check .
ok "ruff + black"

echo "== Running tests =="
poetry run pytest -q
ok "pytest"

echo "== CLI smoke test =="
poetry run python -m src.app --help >/dev/null
poetry run python -m src.app hello | grep -q "Algo Bot MVP is alive." && ok "CLI hello" || fail "CLI hello failed"

echo
echo "${GREEN}All Day 1 checks passed.${NC}  ✅"