"""
Hotel Review Dataset Generator
Generates synthetic Italian hotel reviews with controlled sentiment and department labels.
"""

import random

from .config import fake, STRATEGY_WEIGHTS
from .grammar import add_cross_dept_noise, maybe_inject_typo, generate_title
from .strategies import STRATEGY_BUILDERS


def build_review(target: int) -> dict:
    """Build a single review with controlled sentiment.

    Args:
        target: 1 for positive, 0 for negative

    Returns:
        dict with review data
    """
    strategies = list(STRATEGY_WEIGHTS.keys())
    weights = list(STRATEGY_WEIGHTS.values())
    strategy = random.choices(strategies, weights=weights, k=1)[0]

    body, dept = STRATEGY_BUILDERS[strategy](target)

    body = add_cross_dept_noise(body, dept)
    body = maybe_inject_typo(body)
    title = generate_title(target, dept)

    return {
        "id": fake.uuid4(),
        "title": title,
        "body": body,
        "department": dept,
        "sentiment": "positive" if target == 1 else "negative",
        "target": target,
        "strategy": strategy,
    }
