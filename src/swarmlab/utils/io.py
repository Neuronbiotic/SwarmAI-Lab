"""Lightweight configuration I/O helpers."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

try:  # pragma: no cover - optional dependency
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


def load_config(path: str | Path) -> Dict[str, Any]:
    """Load a configuration file in YAML or JSON format."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")

    suffix = file_path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise ImportError("PyYAML is required to load YAML configurations")
        return yaml.safe_load(file_path.read_text()) or {}
    if suffix == ".json":
        return json.loads(file_path.read_text())

    raise ValueError(f"Unsupported config format: {suffix}")


def save_json(data: Dict[str, Any], path: str | Path) -> Path:
    """Serialize a dictionary to JSON with pretty formatting."""
    file_path = Path(path)
    file_path.write_text(json.dumps(data, indent=2, sort_keys=True))
    return file_path
