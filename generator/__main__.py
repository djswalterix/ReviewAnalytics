"""
CLI entrypoint: python -m generator
"""

import random
import pandas as pd

from .config import SEED, NUM_SAMPLES
from . import build_review

random.seed(SEED)


def main():
    print(f"Generating {NUM_SAMPLES} synthetic Italian hotel reviews...")

    data = [build_review(i % 2) for i in range(NUM_SAMPLES)]
    random.shuffle(data)

    df = pd.DataFrame(data)

    # Validation
    print("\nDataset Statistics:")
    print(f"   Total samples: {len(df)}")
    print(f"   Unique reviews: {df['body'].nunique()} ({df['body'].nunique()/len(df):.1%})")
    print(f"\n   Sentiment distribution:")
    print(f"   {df['sentiment'].value_counts().to_dict()}")
    print(f"\n   Department distribution:")
    print(f"   {df['department'].value_counts().to_dict()}")
    print(f"\n   Strategy distribution:")
    print(f"   {df['strategy'].value_counts().to_dict()}")

    unique_pct = df['body'].nunique() / len(df)
    if unique_pct < 0.95:
        print("\nWARNING: Too many duplicates. Consider expanding vocabulary.")

    df.to_csv("dataset_recensioni.csv", index=False)
    print("\nDataset saved to 'dataset_recensioni.csv'")

    print("\nSample negation reviews (challenging for models):")
    print(df[df['strategy'] == 'negation'][['body', 'target']].head(3).to_string())

    print("\nSample mixed reviews (challenging for models):")
    print(df[df['strategy'] == 'mixed'][['body', 'target']].head(3).to_string())


if __name__ == "__main__":
    main()
