#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# Optional developer tools
python -m pip install pytest pre-commit pyyaml jsonschema mkdocs

echo "Environment bootstrapped. Activate your virtualenv and run 'pytest' to verify."
