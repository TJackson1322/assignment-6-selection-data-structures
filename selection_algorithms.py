"""Selection algorithms for Assignment 6.

Both functions preserve the original input and support duplicate values.
Ranks start at 1.
"""

import random


def validate_rank(values, k):
    """Reject empty inputs and ranks outside the valid range."""
    if not values:
        raise ValueError("The input must contain at least one value.")
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an integer.")
    if not 1 <= k <= len(values):
        raise ValueError("k must be between 1 and the input length.")


def partition(values, pivot):
    """Separate values into three groups to handle duplicates."""
    # Keeping equal values together lets me handle duplicates in one step.
    smaller = []
    equal = []
    larger = []

    for value in values:
        if value < pivot:
            smaller.append(value)
        elif value > pivot:
            larger.append(value)
        else:
            equal.append(value)

    return smaller, equal, larger


def deterministic_select(values, k):
    """Find the kth smallest value using Median of Medians.

    Worst-case time is O(n). Auxiliary space is O(n).
    """
    validate_rank(values, k)
    # I copy the input so selecting a value leaves the original unchanged.
    return median_of_medians(list(values), k)


def median_of_medians(values, k):
    """Select using a pivot obtained from groups of five."""
    while len(values) > 5:
        medians = []

        # Sorting groups of at most five takes constant work per group.
        for start in range(0, len(values), 5):
            group = sorted(values[start:start + 5])
            medians.append(group[len(group) // 2])

        # Selecting the middle group median gives a pivot with a balance guarantee.
        pivot = median_of_medians(
            medians, (len(medians) + 1) // 2
        )
        smaller, equal, larger = partition(values, pivot)

        # Only the group containing the requested rank needs more work.
        if k <= len(smaller):
            values = smaller
        elif k <= len(smaller) + len(equal):
            return pivot
        else:
            # In the larger group, I subtract the ranks already skipped.
            k -= len(smaller) + len(equal)
            values = larger

    # k starts at 1, while Python list positions start at 0.
    return sorted(values)[k - 1]


def randomized_select(values, k, rng=None):
    """Find the kth smallest value using Randomized Quickselect.

    Expected time is O(n), with O(n²) worst-case time.
    Auxiliary space is O(n).
    An optional random generator supports reproducible experiments.
    """
    validate_rank(values, k)
    values = list(values)

    if rng is None:
        rng = random.Random()

    while True:
        # A random pivot avoids depending on the original input order.
        # Repeated poor pivots are still possible in the worst case.
        pivot = rng.choice(values)
        smaller, equal, larger = partition(values, pivot)

        # Only the group containing the requested rank needs more work.
        if k <= len(smaller):
            values = smaller
        elif k <= len(smaller) + len(equal):
            return pivot
        else:
            # In the larger group, I subtract the ranks already skipped.
            k -= len(smaller) + len(equal)
            values = larger


def main():
    """Demonstrate selection on an input containing duplicates."""
    values = [12, 3, 5, 7, 4, 19, 5]
    k = 4

    print("Original values:", values)
    print("Requested rank:", k)
    print("Median of Medians:", deterministic_select(values, k))
    print(
        "Randomized Quickselect:",
        randomized_select(values, k, random.Random(42)),
    )
    print("Expected result:", sorted(values)[k - 1])
    print("Original values after selection:", values)


if __name__ == "__main__":
    main()
