"""Validate experiment configuration files against the project schema."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover - validation utility
    raise SystemExit("jsonschema is required: pip install jsonschema") from exc

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "experiments" / "schemas" / "config.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Path to the YAML or JSON config to validate")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    schema = json.loads(SCHEMA_PATH.read_text())

    from swarmlab.utils.io import load_config

    config = load_config(args.config)
    jsonschema.validate(instance=config, schema=schema)
    print(f"Config {args.config} is valid against {SCHEMA_PATH}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
