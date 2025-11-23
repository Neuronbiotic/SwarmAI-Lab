import math

from swarmlab.core import Swarm, Agent, average_rule
from swarmlab.sim.consensus import ConsensusSimulator, run_consensus


def test_consensus_simulator_detects_convergence():
    swarm = Swarm([
        Agent(0, 0.5, neighbors=[1, 2]),
        Agent(1, 0.5, neighbors=[0, 2]),
        Agent(2, 0.5, neighbors=[0, 1]),
    ])
    simulator = ConsensusSimulator(rule="average")
    result = simulator.run(swarm=swarm, steps=1)
    assert result.converged is True


def test_run_consensus_average_mode():
    result = run_consensus(num_agents=3, initial_states=[0.0, 0.5, 1.0], rule="average", steps=5)
    final_states = result.history[-1]
    assert math.isclose(final_states[0], final_states[1], rel_tol=1e-2, abs_tol=1e-2)
    assert math.isclose(final_states[1], final_states[2], rel_tol=1e-2, abs_tol=1e-2)


def test_run_consensus_majority_mode():
    result = run_consensus(num_agents=3, initial_states=[1, 1, 0], rule="majority", steps=2)
    final_states = result.history[-1]
    assert all(state == 1.0 for state in final_states.values())
