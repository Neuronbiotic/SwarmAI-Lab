"""Consensus utilities built on top of the core primitives."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from swarmlab.core import Agent, Swarm, average_rule, majority_rule


@dataclass
class ConsensusResult:
    history: List[Dict[int, float]]
    converged: bool


class ConsensusSimulator:
    """Run consensus-style simulations with configurable rules."""

    def __init__(self, rule: str = "average"):
        if rule not in {"average", "majority"}:
            raise ValueError("rule must be either 'average' or 'majority'")
        self.rule = rule

    def _get_rule(self):
        return average_rule if self.rule == "average" else majority_rule

    def run(self, swarm: Swarm, steps: int = 10, tolerance: float = 1e-3) -> ConsensusResult:
        rule = self._get_rule()
        history = swarm.run(rule, steps)
        converged = self._has_converged(history[-1].values(), tolerance)
        return ConsensusResult(history=history, converged=converged)

    @staticmethod
    def _has_converged(states: Iterable[float], tolerance: float) -> bool:
        values = list(states)
        if not values:
            return True
        return max(values) - min(values) <= tolerance


def run_consensus(num_agents: int, initial_states: Iterable[float], rule: str = "average", steps: int = 10) -> ConsensusResult:
    """Convenience wrapper to spin up a swarm and execute a simulation."""
    agents: List[Agent] = []
    for idx, state in enumerate(initial_states):
        neighbors = [j for j in range(num_agents) if j != idx]
        agents.append(Agent(agent_id=idx, state=float(state), neighbors=neighbors))

    swarm = Swarm(agents)
    simulator = ConsensusSimulator(rule=rule)
    return simulator.run(swarm, steps=steps)
