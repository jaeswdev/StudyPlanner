"""Monte Carlo simulation for Part J — total development cost risk.

Three uncertain variables, drawn independently each trial:
  hours  — triangular(low, high, mode), development hours (Part D used 300 as a point estimate)
  rate   — uniform($/hr), the fully-loaded rate (already includes overhead + person-time)
  rework — uniform(x), how much of the first version has to be redone

cost = hours * rate * rework, compared against the $30,000 budget from Part D.
"""

import random
import statistics

TRIALS = 10_000
BUDGET = 30_000

HOURS_LOW, HOURS_MODE, HOURS_HIGH = 250, 300, 380
RATE_LOW, RATE_HIGH = 70, 100
REWORK_LOW, REWORK_HIGH = 1.00, 1.30


def run(trials: int = TRIALS) -> list[float]:
    results = []
    for _ in range(trials):
        hours = random.triangular(HOURS_LOW, HOURS_HIGH, HOURS_MODE)
        rate = random.uniform(RATE_LOW, RATE_HIGH)
        rework = random.uniform(REWORK_LOW, REWORK_HIGH)
        results.append(hours * rate * rework)
    results.sort()
    return results


def report(results: list[float]) -> None:
    n = len(results)
    over = sum(1 for r in results if r > BUDGET) / n

    print(f"trials          {n:,}")
    print(f"mean cost       ${statistics.mean(results):,.0f}")
    print(f"P10 (best case) ${results[int(.10 * n)]:,.0f}")
    print(f"P90 (worst case)${results[int(.90 * n)]:,.0f}")
    print(f"P(over budget)  {over:.1%}   (budget = ${BUDGET:,})")


if __name__ == "__main__":
    random.seed(42)  # reproducible — same numbers every run, for grading
    results = run()
    report(results)

    import matplotlib.pyplot as plt

    plt.hist(results, bins=40, color="#4C72B0")
    plt.axvline(BUDGET, color="red", linestyle="--", label=f"budget (${BUDGET:,})")
    plt.xlabel("Total development cost ($)")
    plt.ylabel("Trials")
    plt.title("Monte Carlo: total development cost (10,000 trials)")
    plt.legend()
    plt.savefig("analysis/cost_distribution.png", dpi=150, bbox_inches="tight")
    print("\nChart saved to analysis/cost_distribution.png")
