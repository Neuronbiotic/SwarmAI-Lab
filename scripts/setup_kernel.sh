#!/usr/bin/env bash
set -euo pipefail

NAME=${1:-swarmlab}
python -m ipykernel install --user --name "$NAME" --display-name "Python (${NAME})"
echo "Registered Jupyter kernel '${NAME}'."
