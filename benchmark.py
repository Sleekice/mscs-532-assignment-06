"""Reproducible median-selection benchmark; outputs CSV (times in milliseconds)."""
import csv
import random
import statistics
import time
from pathlib import Path
from src.selection import deterministic_select, randomized_select

# Test small and larger inputs to observe how runtime grows.
SIZES = (100, 500, 1000, 2000, 4000)
# Repeating measurements helps reduce the influence of temporary slowdowns.
REPEATS = 7
# Fixed seed makes generated input values reproducible across runs.
SEED = 53206


def run() -> None:
    """Time both algorithms and save median runtimes to a CSV file."""
    rng = random.Random(SEED)
    rows = []
    for n in SIZES:
        # Generate the same base values for all three ordered distributions.
        base = [rng.randrange(-10 * n, 10 * n) for _ in range(n)]
        cases = {
            'random': base,
            'sorted': sorted(base),
            'reverse': sorted(base, reverse=True),
            'duplicates': [rng.randrange(10) for _ in range(n)],
        }
        for distribution, values in cases.items():
            # Select the lower median for even input sizes.
            k = (n + 1) // 2
            expected = sorted(values)[k - 1]
            # Sorting here is only used to verify correctness, not timed.
            for method, select in [('deterministic', deterministic_select), ('randomized', randomized_select)]:
                samples = []
                for r in range(REPEATS):
                    # Only the selection call is included in the timing.
                    start = time.perf_counter_ns()
                    if method == 'randomized':
                        actual = select(values, k, random.Random(SEED + r))
                    else:
                        actual = select(values, k)
                    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
                    if actual != expected:
                        raise AssertionError(f'Incorrect result: {method} n={n} {distribution}')
                    samples.append(elapsed_ms)
                # The median is less sensitive to an unusually slow run.
                median_ms = statistics.median(samples)
                rows.append({'n': n, 'distribution': distribution, 'algorithm': method,
                             'repeats': REPEATS, 'median_ms': f'{median_ms:.6f}'})
                print(f'{n:5d} {distribution:10s} {method:13s} {median_ms:10.4f} ms')
    # Write results in a reusable format for spreadsheets or charts.
    output = Path('results/selection_benchmarks.csv')
    output.parent.mkdir(exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {output}')


# Only run benchmarks when this file is launched directly.
if __name__ == '__main__':
    run()
