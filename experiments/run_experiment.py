"""CLI wrapper for running SwarmAI-Lab experiments from config files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List

from swarmlab.sim.consensus import ConsensusResult, run_consensus
from swarmlab.utils.io import load_config, save_json
from swarmlab.utils.logging import configure_logging
from swarmlab.utils.seed import set_seed

try:  # pragma: no cover - optional dependency
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "config.schema.json"
DEFAULT_OUTPUT_DIR = Path("artifacts/experiments")


def _validate_config(config: Dict) -> None:
    if jsonschema is None:
        return
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(instance=config, schema=schema)


def _merge(base: Dict, overrides: Dict | None) -> Dict:
    merged = base.copy()
    for key, value in (overrides or {}).items():
        merged[key] = value
    return merged


def _run_single(simulation: Dict, output_dir: Path, label: str, save_history: bool) -> Path:
    logger = configure_logging(name="swarmlab.experiments")
    set_seed(simulation.get("seed"))

    num_agents = simulation["num_agents"]
    initial_states: Iterable[float] = simulation["initial_states"]
    rule = simulation["rule"]
    steps = simulation["steps"]

    logger.info("Running experiment '%s' (%s rule, %s steps)", label, rule, steps)
    result: ConsensusResult = run_consensus(
        num_agents=num_agents, initial_states=initial_states, rule=rule, steps=steps
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{label}.json"
    payload = {
        "label": label,
        "num_agents": num_agents,
        "rule": rule,
        "steps": steps,
        "seed": simulation.get("seed"),
        "converged": result.converged,
        "final_state": result.history[-1],
    }
    if save_history:
        payload["history"] = result.history

    save_json(payload, output_path)
    logger.info("Saved results to %s", output_path)
    return output_path


def run_from_config(config_path: Path, output_dir: Path | None = None) -> List[Path]:
    config = load_config(config_path)
    _validate_config(config)

    metadata = config.get("metadata", {})
    simulation = config["simulation"]
    sweeps = config.get("sweeps") or []
    output_cfg = config.get("output", {})

    final_output_dir = Path(output_dir or output_cfg.get("directory") or DEFAULT_OUTPUT_DIR)
    save_history = bool(output_cfg.get("save_history", True))

    if len(simulation.get("initial_states", [])) != simulation.get("num_agents"):
        raise ValueError("initial_states length must match num_agents")

    if not sweeps:
        label = metadata.get("name", config_path.stem)
        return [_run_single(simulation, final_output_dir, label=label, save_history=save_history)]

    outputs: List[Path] = []
    base_label = metadata.get("name", config_path.stem)
    for sweep in sweeps:
        overrides = sweep.get("overrides", {})
        merged = _merge(simulation, overrides)
        label = sweep.get("name") or f"{base_label}-{len(outputs)}"
        outputs.append(_run_single(merged, final_output_dir, label=label, save_history=save_history))
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Path to a YAML or JSON experiment config")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Optional override for the output directory. Defaults to config output directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_from_config(args.config, output_dir=args.output_dir)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
