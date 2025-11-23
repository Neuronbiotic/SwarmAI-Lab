"""Core primitives for running simple swarm simulations."""
from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Callable, Dict, Iterable, List

UpdateRule = Callable[[float, Iterable[float]], float]


@dataclass
class Agent:
    """Lightweight representation of an agent in the swarm."""

    agent_id: int
    state: float
    neighbors: List[int] = field(default_factory=list)

    def observe(self, swarm_states: Dict[int, float]) -> List[float]:
        """Return the states of this agent's neighbors."""
        return [swarm_states[n_id] for n_id in self.neighbors if n_id in swarm_states]

    def update(self, swarm_states: Dict[int, float], rule: UpdateRule) -> float:
        """Compute the next state using the provided update rule."""
        neighbor_states = self.observe(swarm_states)
        self.state = rule(self.state, neighbor_states)
        return self.state


class Swarm:
    """Container to coordinate a collection of agents."""

    def __init__(self, agents: Iterable[Agent]):
        self.agents: Dict[int, Agent] = {agent.agent_id: agent for agent in agents}

    def states(self) -> Dict[int, float]:
        return {agent_id: agent.state for agent_id, agent in self.agents.items()}

    def step(self, rule: UpdateRule) -> Dict[int, float]:
        """Apply one synchronous update step to all agents."""
        current_states = self.states()
        for agent in self.agents.values():
            agent.update(current_states, rule)
        return self.states()

    def run(self, rule: UpdateRule, steps: int) -> List[Dict[int, float]]:
        """Run multiple synchronous steps and collect state history."""
        history = [self.states()]
        for _ in range(steps):
            history.append(self.step(rule))
        return history

    @staticmethod
    def fully_connected(num_agents: int, initial_state: float = 0.0) -> "Swarm":
        """Create a fully connected swarm where each agent sees all others."""
        agents = []
        for idx in range(num_agents):
            neighbors = [j for j in range(num_agents) if j != idx]
            agents.append(Agent(agent_id=idx, state=initial_state, neighbors=neighbors))
        return Swarm(agents)


def average_rule(self_state: float, neighbor_states: Iterable[float]) -> float:
    """Update rule that moves the agent toward the neighborhood average."""
    values = list(neighbor_states)
    if not values:
        return self_state
    return float(mean([self_state, *values]))


def majority_rule(self_state: float, neighbor_states: Iterable[float]) -> float:
    """Binary majority voting rule for states in {0, 1}."""
    values = [int(round(v)) for v in neighbor_states]
    if not values:
        return int(round(self_state))
    ones = sum(values) + int(round(self_state))
    zeros = len(values) + 1 - ones
    return float(1 if ones >= zeros else 0)
