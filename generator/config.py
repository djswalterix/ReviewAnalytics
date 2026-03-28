"""
Generator configuration — all tunable hyperparameters in one place.
"""

from faker import Faker

# Reproducibility
SEED = 42

# Faker instance (Italian locale)
fake = Faker("it_IT")
Faker.seed(SEED)

NUM_SAMPLES = 500

DEPARTMENTS = ["Housekeeping", "Reception", "F&B"]

# Strategy weights for review generation (must sum to ~1.0)
STRATEGY_WEIGHTS = {
    "simple": 0.10,
    "detailed": 0.20,
    "negation": 0.15,
    "mixed": 0.15,
    "multi_aspect": 0.20,
    "ambiguous": 0.20,
}

# Probability of injecting a typo into a review
TYPO_PROBABILITY = 0.05

# Probability of adding cross-department noise
CROSS_DEPT_NOISE_PROBABILITY = 0.40
