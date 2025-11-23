"""Utility helpers for deterministic behavior.

The project keeps random operations reproducible so that swarm runs
can be compared across machines.
"""
from __future__ import annotations

import os
import random
from typing import Optional

import numpy as np

DEFAULT_SEED = 42


def set_seed(seed: Optional[int] = None) -> int:
    """Seed Python, NumPy, and environment RNGs.

    Args:
        seed: Value to seed the RNGs with. If ``None`` a default constant
            is used to make behavior reproducible without extra work.

    Returns:
        The seed value that was applied. Returning the seed makes the
        function convenient to chain inside experiment setup code.
    """

    value = int(seed) if seed is not None else DEFAULT_SEED
    random.seed(value)
    np.random.seed(value)
    os.environ["PYTHONHASHSEED"] = str(value)
    return value
