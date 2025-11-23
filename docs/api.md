# API overview

## Core primitives (`swarmlab.core`)

- `Agent`: holds an agent identifier, current state, and neighbor list.
- `Swarm`: orchestrates synchronous updates across many agents, exposing helpers like `step`, `run`, and `fully_connected`.
- `average_rule` / `majority_rule`: built-in update rules for continuous and binary consensus.

## Consensus simulator (`swarmlab.sim.consensus`)

- `ConsensusSimulator`: orchestrates multiple steps, returning a `ConsensusResult` containing history and convergence status.
- `run_consensus`: convenience function that builds a fully connected swarm for you.

## Utilities (`swarmlab.utils`)

- `set_seed`: deterministic seeding for Python, NumPy, and environment randomness.
- `configure_logging`: quickly provision a logger with sensible formatting.
- `load_config` / `save_json`: YAML/JSON helpers for reading experiment definitions and persisting results.

## Visualization (`swarmlab.viz.plots`)

- `plot_state_history`: line plot showing each agent's state across steps.
- `plot_distribution`: histogram of swarm states at a given point in time.

Refer to the docstrings in `src/` for detailed arguments and return types.
