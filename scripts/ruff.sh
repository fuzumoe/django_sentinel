#!/bin/bash
# Script to lint Python files using Ruff, tailored for CI and Git hooks
# should be synchronous to ruff.toml in root folder
exclude=(
    ".venv/" \
    "venv/" \
    "pydj_auth/migrations/" \
    "__pycache__/" \
    "manage.py"
    )
exclude_pattern=$(printf "|^%s" "${exclude[@]}")
exclude_pattern=${exclude_pattern:1}  # Remove the leading '|'

# Determine mode: CI or Git hook based on last argument or environment
if [ "${!#}" = "CI" ]; then
  echo "CI mode"
  changed_files=$(git diff --name-only --diff-filter=ACM HEAD~1..HEAD | grep '\.py$' | grep -v -E "$exclude_pattern")
elif [ "${IGNORE_COMMIT_HOOKS}" = true ]; then
  echo "manual override, not executing ruff"
  # Skip linting when IGNORE_COMMIT_HOOKS is set
  # manual override, for example when merging from main and mypy and linter are not same version leading to different issues for example
  exit 0  
else
  echo "git hook mode"
  changed_files=$(git diff --name-only --diff-filter=ACM HEAD | grep '\.py$' | grep -v -E "$exclude_pattern")  
fi

# In CI mode, display changed files and header
if [ "${!#}" = "CI" ]; then
  fmt="%s\n%s\n"
  printf "${fmt}" "changed files:" "${changed_files}"
  printf "\nRuff: \n"
fi

# Activate virtual environment and run Ruff on changed files
if [ -n "$changed_files" ]; then
    source .venv/bin/activate
    ruff $1 $2 $changed_files 
fi