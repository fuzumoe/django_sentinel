#!/bin/bash
# Script to type-check Python files using MyPy, tailored for CI and Git hooks
# Determine directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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
  echo "manual override, not executing mypy"
  # Skip type checking when IGNORE_COMMIT_HOOKS is set
  exit 0    
else
  echo "git hook mode"
  changed_files=$(git diff --name-only --diff-filter=ACM HEAD | grep '\.py$' | grep -v -E "$exclude_pattern")
fi

# In CI mode, display changed files and header
if [ "${!#}" = "CI" ]; then
  fmt="%s\n%s\n"
  printf "${fmt}" "changed files:" "${changed_files}"
  printf "\nType Errors: \n"
fi

# Activate virtual environment and run MyPy on changed files
if [ -n "$changed_files" ]; then
    source .venv/bin/activate
    # Use project-level mypy.ini configuration
    mypy --config-file="$SCRIPT_DIR/../mypy.ini" $changed_files
fi
