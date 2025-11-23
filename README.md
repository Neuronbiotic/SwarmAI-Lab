# SwarmAI-Lab

SwarmAI-Lab is a minimal, batteries-included playground for experimenting with swarm intelligence ideas in Python. It bundles tiny yet well-tested primitives for agents, synchronous updates, and consensus simulations, plus optional visualization helpers to inspect trajectories. The repository is intentionally simple so you can fork it for coursework, demos, or production prototypes.

## Highlights

- **Small core, readable code:** A few focused modules model agents, neighborhood updates, and consensus rules without heavy dependencies.
- **Deterministic experiments:** Helper utilities seed Python, NumPy, and environment RNGs to make runs reproducible.
- **Visualization ready:** Matplotlib-friendly plotting helpers visualize state traces or distributions.
- **Extensible simulations:** Drop in new update rules or simulators to explore coordination, formation control, or voting dynamics.
- **Container support:** A slim Dockerfile ships with the repo so you can build and run simulations consistently across machines.

## Project layout

- `src/swarmlab/core.py` — Agent and Swarm primitives plus built-in `average_rule` and `majority_rule` update functions.
- `src/swarmlab/sim/consensus.py` — A `ConsensusSimulator` that runs multiple synchronous steps and reports convergence.
- `src/swarmlab/utils/` — Logging, seeding, and configuration helpers for repeatable experiments.
- `src/swarmlab/viz/plots.py` — Optional matplotlib-based plotting for trajectories and distributions.
- `tests/` — Unit tests covering the core API and consensus behaviors.
- `requirements.txt` — Minimal runtime dependencies; optional extras for plotting or YAML configs.

## Installation

1. Use Python 3.10+.
2. Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/your-org/SwarmAI-Lab.git
   cd SwarmAI-Lab
   python -m venv .venv && source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   # Optional extras for plotting and YAML configs
   python -m pip install matplotlib pyyaml
   ```

3. Add the source tree to your `PYTHONPATH` so imports resolve when running from the repo root:

   ```bash
   export PYTHONPATH="$(pwd)/src"
   ```

## Quickstart (Python)

Run a simple consensus simulation and confirm convergence:

```python
from swarmlab.sim.consensus import run_consensus
from swarmlab.utils.seed import set_seed
from swarmlab.utils.logging import configure_logging

set_seed(7)
logger = configure_logging()

result = run_consensus(
    num_agents=5,
    initial_states=[0.0, 0.25, 0.5, 0.75, 1.0],
    rule="average",
    steps=8,
)

logger.info("Converged: %s", result.converged)
logger.info("Final states: %s", result.history[-1])
```

To visualize state trajectories (requires `matplotlib`):

```python
from swarmlab.viz.plots import plot_state_history
plot_state_history(result.history, title="Average consensus trajectory", save_path="artifacts/trajectory.png")
```

## Using SwarmAI-Lab from other languages

Because SwarmAI-Lab is pure Python, the easiest interop path is to treat it as a command you call from your host language. For example, a tiny Node.js script can invoke a Python one-liner and read JSON from stdout:

```ts
// run-consensus.ts
import { spawnSync } from "child_process";

const code = `import json;\n` +
  `from swarmlab.sim.consensus import run_consensus;\n` +
  `result = run_consensus(num_agents=3, initial_states=[0,1,1], rule=\"majority\", steps=2);\n` +
  `print(json.dumps(result.history[-1]))`;

const { stdout, stderr, status } = spawnSync("python", ["-c", code]);
if (status !== 0) throw new Error(stderr.toString());
console.log("Consensus result:", stdout.toString());
```

Any language that can spawn a subprocess (Rust, Go, Java, etc.) can follow the same pattern. For tighter integration, wrap your favorite update rules behind a minimal REST or gRPC shim inside Python, then call it from other runtimes.

## Docker support

A lightweight Dockerfile is included for reproducible runs on CI or remote machines.

1. Build the image:

   ```bash
   docker build -t swarmlab .
   ```

2. Launch an interactive shell with the repo mounted (so edits on your host are visible inside the container):

   ```bash
   docker run --rm -it -v "$(pwd)":/workspace -w /workspace swarmlab bash
   ```

3. Run a one-off simulation inside the container:

   ```bash
   docker run --rm swarmlab python - <<'PY'
from swarmlab.sim.consensus import run_consensus
result = run_consensus(num_agents=4, initial_states=[0, 0.25, 0.75, 1], rule="average", steps=6)
print("Converged:", result.converged)
print("Final states:", result.history[-1])
PY
   ```

The image sets `PYTHONPATH=/app/src` so imports work immediately. Install optional plotting extras at runtime with `docker run --rm swarmlab pip install matplotlib` if you want to generate figures inside the container.

## Running tests

Install developer dependencies (e.g., `pytest`) and execute the suite:

```bash
python -m pip install pytest
pytest
```

## Contributing

Issues and pull requests are welcome! If you add new simulators or visualization helpers, please accompany them with tests and a short example in the README or `docs/` directory so others can reproduce your setup.
