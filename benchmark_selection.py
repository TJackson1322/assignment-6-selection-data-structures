"""Compare selection algorithms across input sizes and distributions.

Each algorithm receives the same data and selects the middle rank.
Results report the median runtime from seven trials.
"""

import csv
import random
import statistics
import time

from selection_algorithms import (
    deterministic_select,
    randomized_select,
)


def make_datasets(size):
    """Generate reproducible inputs outside the timed section."""
    # A fixed seed makes the generated input repeatable for this size.
    rng = random.Random(2026 + size)
    values = [rng.randrange(size * 10) for _ in range(size)]

    return {
        "random": values,
        "sorted": sorted(values),
        "reverse_sorted": sorted(values, reverse=True),
        "many_duplicates": [rng.randrange(10) for _ in range(size)],
        "all_equal": [7] * size,
    }


def main():
    sizes = [100, 1000, 10000]
    trials = 7
    results = []

    for size in sizes:
        for distribution, values in make_datasets(size).items():
            # For even sizes, this selects the lower middle value.
            k = (size + 1) // 2
            # Sorting supplies a correctness reference outside the timed section.
            expected = sorted(values)[k - 1]
            timings = {"deterministic": [], "randomized": []}

            for trial in range(trials):
                # Alternate order to reduce consistent timing-order bias.
                names = ["deterministic", "randomized"]
                if trial % 2:
                    names.reverse()

                for name in names:
                    rng = random.Random(size + trial)

                    # Time the selection call, including its internal input copy.
                    start = time.perf_counter_ns()

                    if name == "deterministic":
                        answer = deterministic_select(values, k)
                    else:
                        answer = randomized_select(values, k, rng)

                    elapsed_ms = (
                        time.perf_counter_ns() - start
                    ) / 1_000_000

                    if answer != expected:
                        raise AssertionError(
                            f"Incorrect result: {name}, "
                            f"{distribution}, size={size}"
                        )

                    timings[name].append(elapsed_ms)

            # The median limits the effect of an unusually slow individual trial.
            for name, measurements in timings.items():
                results.append({
                    "size": size,
                    "distribution": distribution,
                    "algorithm": name,
                    "median_ms": statistics.median(measurements),
                    "minimum_ms": min(measurements),
                    "maximum_ms": max(measurements),
                    "trials": trials,
                })

    # Rerunning this script replaces the CSV with measurements from that run.
    filename = "selection_results.csv"

    with open(filename, "w", newline="") as output:
        writer = csv.DictWriter(
            output, fieldnames=list(results[0].keys())
        )
        writer.writeheader()
        writer.writerows(results)

    print(
        f"{'Size':>7}  {'Distribution':<17}  "
        f"{'Algorithm':<14}  {'Median (ms)':>12}"
    )

    for row in results:
        print(
            f"{row['size']:>7}  "
            f"{row['distribution']:<17}  "
            f"{row['algorithm']:<14}  "
            f"{row['median_ms']:>12.4f}"
        )

    print(f"\nResults saved to {filename}")
    print("Every measured result matched the sorted reference.")


if __name__ == "__main__":
    main()
