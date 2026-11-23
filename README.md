# MSCS 532 — Assignment 6: Medians, Order Statistics & Elementary Data Structures

Python implementations, correctness tests, and an empirical benchmark for two selection algorithms and five basic data-structure implementations.

## Requirements

- Python 3.10 or newer
- Standard library only; no third-party packages

## Quick start

Run from the repository root:

```bash
python demo.py
python -m unittest discover -s tests -v
python benchmark.py
```

The last command regenerates `results/selection_benchmarks.csv` with median elapsed times in milliseconds. The benchmark uses 7 repetitions, a reproducible input seed, and `time.perf_counter_ns`. Exact timings depend on the computer and current system load.

## Project layout

```text
mscs-532-assignment-06/
├── src/
│   ├── __init__.py
│   ├── selection.py         # Median of Medians and Randomized Quickselect
│   └── structures.py        # DynamicArray, Matrix, ArrayStack, ArrayQueue, SinglyLinkedList
├── tests/
│   └── test_all.py          # Correctness tests and edge cases
├── results/
│   ├── selection_benchmarks.csv
│   └── benchmark_console.txt
├── benchmark.py             # Repeatable selection timing experiment
├── demo.py                  # Small examples of every implementation
├── report.md                # Design, complexity, results, real-world applications
├── .gitignore
└── README.md
```

## Selection API

```python
from src.selection import deterministic_select, randomized_select

numbers = [8, 3, 3, 10, 1]
print(deterministic_select(numbers, 2))  # 3
print(randomized_select(numbers, 2))     # 3
```

`k` is **1-based**, so `k=1` selects the minimum. Both functions raise `ValueError` for `k < 1`, `k > len(values)`, or empty inputs. Both copy the input and use a three-way partition to handle duplicates correctly.

## Elementary data-structure API

```python
from src.structures import DynamicArray, Matrix, ArrayStack, ArrayQueue, SinglyLinkedList

array = DynamicArray()
array.append(10)
array.insert(0, 5)
print(array.get(1), array.delete(0))

matrix = Matrix(2, 2)
matrix.set(0, 1, 9)
matrix.insert_row(2, [3, 4])
print(matrix.get(0, 1), matrix.delete_row(2))

stack = ArrayStack()
stack.push('first')
print(stack.peek(), stack.pop())

queue = ArrayQueue()
queue.enqueue('first')
print(queue.peek(), queue.dequeue())

linked = SinglyLinkedList()
linked.append(1)
linked.prepend(0)
linked.insert(1, 5)
linked.delete(5)
print(linked.to_list())
```

## Summary of findings

- Median of Medians guarantees linear time in the worst case through carefully selected pivots; it introduces extra grouping and pivot-selection overhead.
- Randomized Quickselect has linear **expected** time and quadratic worst-case time. It often benefits from selecting a pivot more cheaply.
- A dynamic array offers O(1) indexed access and amortized O(1) append but O(n) middle insertion/deletion.
- An array stack has amortized O(1) push and O(1) pop; a circular-buffer array queue has amortized O(1) enqueue and O(1) dequeue.
- A singly linked list supports O(1) prepend and tail append with a tail pointer, but O(n) arbitrary lookup or deletion by value.

See [`report.md`](report.md) for measured results, explanations, trade-offs, and applications.# mscs-532-assignment-06
