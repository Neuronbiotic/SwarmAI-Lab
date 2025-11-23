"""Plotting helpers for inspecting swarm state trajectories."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List


def _require_matplotlib():  # pragma: no cover - visualization utility
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise ImportError("matplotlib is required for plotting utilities") from exc
    return plt


def plot_state_history(history: List[Dict[int, float]], title: str = "Swarm state trajectory", save_path: str | Path | None = None):
    """Plot the state of each agent across time steps."""
    if not history:
        raise ValueError("History cannot be empty")

    plt = _require_matplotlib()
    steps = range(len(history))
    agent_ids = sorted(history[0].keys())

    for agent_id in agent_ids:
        values = [states[agent_id] for states in history]
        plt.plot(steps, values, marker="o", label=f"agent {agent_id}")

    plt.xlabel("Step")
    plt.ylabel("State")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path)
    else:
        plt.show()

    plt.close()


def plot_distribution(states: Iterable[float], bins: int = 10, title: str = "State distribution", save_path: str | Path | None = None):
    """Plot a histogram of agent states."""
    values = list(states)
    if not values:
        raise ValueError("No states supplied for plotting")

    plt = _require_matplotlib()
    plt.hist(values, bins=bins, color="steelblue", alpha=0.8, edgecolor="black")
    plt.xlabel("State")
    plt.ylabel("Count")
    plt.title(title)
    plt.grid(True, alpha=0.3)

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path)
    else:
        plt.show()

    plt.close()
