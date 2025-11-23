# Running experiments

The `experiments/` folder ships with reusable configuration files and a CLI runner for batch simulations.

## Validate a config

Use the helper script to confirm your config satisfies the JSON schema:

```bash
python scripts/validate_config.py experiments/configs/baseline.yaml
```

## Execute a single experiment

```bash
python experiments/run_experiment.py experiments/configs/baseline.yaml
```

By default, results are written to `artifacts/experiments` and include the full state history. Override the output directory:

```bash
python experiments/run_experiment.py experiments/configs/baseline.yaml --output-dir /tmp/runs
```

## Sweep over multiple settings

The grid-search config demonstrates comparing multiple rules and seeds:

```bash
python experiments/run_experiment.py experiments/configs/gridsearch.yaml
```

Each sweep entry produces its own JSON file with convergence details.
