from swarmlab.core import Agent, Swarm, average_rule, majority_rule


def test_fully_connected_swarm_builds_neighbors():
    swarm = Swarm.fully_connected(num_agents=3, initial_state=0.5)
    assert set(swarm.agents.keys()) == {0, 1, 2}
    assert swarm.agents[0].neighbors == [1, 2]
    assert swarm.agents[1].neighbors == [0, 2]
    assert swarm.agents[2].neighbors == [0, 1]


def test_average_rule_moves_toward_neighbors():
    swarm = Swarm([
        Agent(0, 0.0, neighbors=[1]),
        Agent(1, 1.0, neighbors=[0]),
    ])

    history = swarm.run(average_rule, steps=3)
    # After several steps both agents should be close to 0.5
    final_states = history[-1]
    assert abs(final_states[0] - 0.5) < 0.05
    assert abs(final_states[1] - 0.5) < 0.05


def test_majority_rule_converges_to_mode():
    swarm = Swarm([
        Agent(0, 1.0, neighbors=[1, 2]),
        Agent(1, 1.0, neighbors=[0, 2]),
        Agent(2, 0.0, neighbors=[0, 1]),
    ])

    history = swarm.run(majority_rule, steps=2)
    final_states = history[-1]
    assert final_states[0] == final_states[1] == final_states[2] == 1.0
