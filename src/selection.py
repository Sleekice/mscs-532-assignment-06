"""Find the kth smallest number without sorting the entire input."""

from __future__ import annotations
import random
from typing import Sequence


def _validate(values: Sequence[int], k: int) -> None:
    """Check that k describes a position in the given collection."""
    # We count positions from 1, so k=1 means the smallest element.
    if not 1 <= k <= len(values):
        raise ValueError(f"k must be in [1, {len(values)}], received {k}")


def _partition_three_way(a: list[int], lo: int, hi: int, pivot: int) -> tuple[int, int]:
    """Separate a[lo:hi] into values below, equal to, and above pivot."""
    # The active range is [lo, hi); hi itself is not included.
    # lt marks the end of the smaller values, and gt starts the larger values.
    lt, i, gt = lo, lo, hi
    while i < gt:
        if a[i] < pivot:
            # Move this small value to the left and examine the next one.
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            # The value moved from the right has not been checked yet.
            gt -= 1
            a[i], a[gt] = a[gt], a[i]
        else:
            # Equal values stay together in the middle section.
            i += 1
    # Every index from lt to gt-1 contains the pivot value.
    return lt, gt


def _median_of_medians(values: list[int]) -> int:
    """Choose a pivot by finding the median of small-group medians."""
    if len(values) <= 5:
        # Sorting five or fewer elements takes a fixed amount of work.
        ordered = sorted(values)
        return ordered[len(ordered) // 2]

    medians = []
    # Break the input into groups of up to five and collect each middle value.
    for start in range(0, len(values), 5):
        group = sorted(values[start:start + 5])
        medians.append(group[len(group) // 2])

    # Choose the middle of the medians, using a zero-based target index.
    # This keeps the pivot from being too close to either extreme.
    return _deterministic_select_list(medians, len(medians) // 2)


def _deterministic_select_list(a: list[int], target: int) -> int:
    """Find the value at a zero-based sorted position inside a working list."""
    lo, hi = 0, len(a)
    while True:
        if hi - lo <= 5:
            # For a tiny remaining range, direct sorting is simplest.
            return sorted(a[lo:hi])[target - lo]

        pivot = _median_of_medians(a[lo:hi])
        lt, gt = _partition_three_way(a, lo, hi, pivot)
        if target < lt:
            # The answer must be among values smaller than the pivot.
            hi = lt
        elif target >= gt:
            # The answer must be among values larger than the pivot.
            lo = gt
        else:
            # The requested position lies in the pivot's equal-value region.
            return pivot


def deterministic_select(values: Sequence[int], k: int) -> int:
    """Find the kth smallest value; worst-case O(n) time and O(n) extra space."""
    _validate(values, k)
    # Copy the input because partitioning rearranges elements in place.
    # Convert the public 1-based k to the internal zero-based index.
    return _deterministic_select_list(list(values), k - 1)


def randomized_select(values: Sequence[int], k: int, rng: random.Random | None = None) -> int:
    """Find the kth smallest value; expected O(n) time, worst-case O(n²)."""
    _validate(values, k)
    a = list(values)
    # Supplying rng makes benchmark and test runs reproducible.
    rng = rng if rng is not None else random.Random()
    target, lo, hi = k - 1, 0, len(a)

    while True:
        if hi - lo == 1:
            # With one candidate left, it must be the requested value.
            return a[lo]

        # Unlike Median of Medians, this pivot is selected at random.
        pivot = a[rng.randrange(lo, hi)]
        lt, gt = _partition_three_way(a, lo, hi, pivot)
        if target < lt:
            hi = lt
        elif target >= gt:
            lo = gt
        else:
            return pivot
